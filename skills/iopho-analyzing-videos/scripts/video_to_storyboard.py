#!/usr/bin/env python3
"""
video_to_storyboard.py — Analyze a video with Gemini and produce a .storyboard.md
Usage: python3 video_to_storyboard.py <video_path> [output_path] [--no-frames] [--model MODEL]
"""
import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import google.generativeai as genai

PROMPT = """Analyze this video in detail and produce a complete .storyboard.md document.

Output EXACTLY this structure — YAML frontmatter first, then scene-by-scene markdown:

---
title: "<detected title or filename>"
duration_seconds: <total seconds>
resolution: "1920x1080"
fps: 30
style:
  visual_style: "<describe overall visual style>"
  color_palette: ["#hex1", "#hex2", "#hex3"]
  typography: "<font style observed>"
  mood: "<emotional arc>"
audio:
  has_voiceover: <true/false>
  voiceover_language: "<en/zh/etc>"
  voiceover_tone: "<describe tone>"
  has_music: <true/false>
  music_style: "<describe music style>"
  music_mood: "<describe music mood>"
  has_sfx: <true/false>
content:
  type: "<product_demo/brand/explainer/etc>"
  framework: "<PAS/AIDA/etc>"
  key_message: "<one sentence>"
---

For EACH scene (detect natural cuts/transitions — aim for 10-20 scenes for an 80s video):

### Scene N: <Name> (<MM:SS> – <MM:SS>, <duration>s)

#### Visual
- **Shot Type**: <wide/medium/close-up/text-only/animation>
- **Camera Movement**: <static/pan/zoom/cut>
- **Subject**: <describe exactly what is shown on screen>
- **Text On Screen**: "<exact text visible>"
- **Graphics/Animation**: <describe any motion graphics, overlays, icons>

#### Audio
- **Voiceover**: "<exact transcript if any, else None>"
- **Music**: <describe music character at this moment>
- **SFX**: <describe any sound effects, or None>

#### Analysis
- **Narrative Purpose**: <why this scene exists in the story>
- **Emotional Beat**: <guilt/relief/wonder/confidence/etc>
- **Sales Element**: <problem/solution/benefit/CTA/social proof/None>
- **Transition Out**: <cut/fade/wipe/dissolve> to →

Be extremely detailed. Capture every text element, icon, animation, color change, and audio cue you can detect. This storyboard will be used to recreate the video."""


def upload_and_wait(path: str, model_name: str):
    print(f"[1/4] Uploading {path} to Gemini File API...")
    f = genai.upload_file(path)
    print(f"      Uploaded: {f.name}, state={f.state.name}")
    # Wait for processing
    while f.state.name == "PROCESSING":
        time.sleep(3)
        f = genai.get_file(f.name)
        print(f"      Processing... state={f.state.name}")
    if f.state.name != "ACTIVE":
        raise RuntimeError(f"File failed to process: {f.state.name}")
    print(f"      Ready: {f.uri}")
    return f


def analyze(file_obj, model_name: str) -> str:
    print(f"[2/4] Analyzing with {model_name}...")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        [file_obj, PROMPT],
        generation_config={"temperature": 0.2, "max_output_tokens": 8192},
        request_options={"timeout": 300},
    )
    print(f"      Done. ~{len(response.text)} chars")
    return response.text


def extract_frames(video_path: str, storyboard_text: str, frames_dir: Path) -> str:
    """Parse timestamps from storyboard, extract midpoint frames with ffmpeg."""
    print(f"[3/4] Extracting keyframes...")
    frames_dir.mkdir(exist_ok=True)

    # Find all scene time ranges like (0:05 – 0:12, 7s) or (0:05 – 0:12)
    pattern = re.compile(r"### Scene (\d+):[^\n]*\((\d+):(\d+)\s*[–-]\s*(\d+):(\d+)")
    scenes = pattern.findall(storyboard_text)

    inserted = storyboard_text
    for scene_num, m1, s1, m2, s2 in scenes:
        t1 = int(m1) * 60 + int(s1)
        t2 = int(m2) * 60 + int(s2)
        midpoint = (t1 + t2) / 2
        frame_file = frames_dir / f"scene-{int(scene_num):03d}.jpg"
        cmd = [
            "ffmpeg", "-ss", str(midpoint), "-i", video_path,
            "-frames:v", "1", "-q:v", "3", str(frame_file), "-y", "-loglevel", "error"
        ]
        subprocess.run(cmd, check=False)
        if frame_file.exists():
            print(f"      scene-{int(scene_num):03d}.jpg @ {midpoint:.1f}s")
            thumb_ref = f"\n**Thumbnail**: ![scene-{int(scene_num):03d}](./frames/scene-{int(scene_num):03d}.jpg)\n"
            # Insert after the scene header line
            header_pat = re.compile(
                rf"(### Scene {scene_num}:[^\n]*\n)", re.MULTILINE
            )
            inserted = header_pat.sub(r"\1" + thumb_ref, inserted, count=1)

    print(f"      {len(scenes)} frames extracted")
    return inserted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("output_path", nargs="?")
    parser.add_argument("--no-frames", action="store_true")
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"))
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)
    genai.configure(api_key=api_key)

    video_path = args.video_path
    if not Path(video_path).exists():
        print(f"ERROR: Video not found: {video_path}"); sys.exit(1)

    out_path = Path(args.output_path) if args.output_path else Path(video_path).with_suffix(".storyboard.md")
    frames_dir = out_path.parent / "frames"

    # Run pipeline
    file_obj = upload_and_wait(video_path, args.model)
    try:
        text = analyze(file_obj, args.model)
    finally:
        try:
            genai.delete_file(file_obj.name)
        except Exception:
            pass

    if not args.no_frames:
        text = extract_frames(video_path, text, frames_dir)

    print(f"[4/4] Writing {out_path}...")
    out_path.write_text(text, encoding="utf-8")
    print(f"\n✓ Done → {out_path}")
    scene_count = len(re.findall(r"^### Scene", text, re.MULTILINE))
    print(f"  Scenes detected: {scene_count}")
    print(f"  Output size: {len(text)} chars")


if __name__ == "__main__":
    main()
