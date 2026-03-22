# iopho-skills

[English](README.md) | [简体中文](README.zh-CN.md)

适用于 [iopho](https://github.com/iopho-team) 产品的 AI Agent 技能包。支持 Claude Code、Cursor、Windsurf 及 [40+ 其他 Agent](https://skills.sh/)。

## 可用技能

### iopho 产品应用

iopho 自有产品的配套技能——阅读、笔记与知识管理。

| 技能 | 说明 |
|------|------|
| [reedle](skills/reedle/) | 智能阅读库 CLI——保存/阅读文章、YouTube 与 Bilibili 字幕提取、语义搜索、划线高亮、闪卡复习<br>`npx skills add iopho-team/iopho-skills --skill reedle` · _更新于 2026-03-22_ |
| [pnote](skills/pnote/) | [PromptNote](https://promptnoteapp.com/) CLI——管理提示词、笔记与代码片段<br>`npx skills add iopho-team/iopho-skills --skill pnote` · _更新于 2026-03-22_ |

### 视频制作 — 主编导技能

从这里开始。主编导技能将引导你完成完整的制作流程，并自动调用其他所有技能。

| 技能 | 说明 |
|------|------|
| [iopho-video-director](skills/iopho-video-director/) | 主编导：四阶段完整流程（背景调研 → 分镜脚本 → 制作生产 → 视觉审核）<br>`npx skills add iopho-team/iopho-skills --skill iopho-video-director` · _更新于 2026-03-19_ |

### 视频制作 — 专项技能

流程中各阶段的独立技能，可单独使用，也可由主编导技能自动调用。

| 技能 | 说明 |
|------|------|
| [iopho-product-context](skills/iopho-product-context/) | 交互式产品信息收集问卷 → 生成 context.md（产品定位/受众/品牌规范）<br>`npx skills add iopho-team/iopho-skills --skill iopho-product-context` · _更新于 2026-03-19_ |
| [iopho-searching-videos](skills/iopho-searching-videos/) | 在 YouTube、Bilibili 等平台搜索视频（不下载）<br>`npx skills add iopho-team/iopho-skills --skill iopho-searching-videos` · _更新于 2026-02-27_ |
| [iopho-getting-videos](skills/iopho-getting-videos/) | 从 1800+ 平台下载视频、音频、字幕及元数据<br>`npx skills add iopho-team/iopho-skills --skill iopho-getting-videos` · _更新于 2026-02-27_ |
| [iopho-analyzing-videos](skills/iopho-analyzing-videos/) | 逆向解析视频，生成 .storyboard.md 分镜文档（可用于 AI 重新生成）<br>`npx skills add iopho-team/iopho-skills --skill iopho-analyzing-videos` · _更新于 2026-03-13_ |
| [iopho-recording-checklist](skills/iopho-recording-checklist/) | 根据分镜脚本生成逐镜头录屏拍摄清单<br>`npx skills add iopho-team/iopho-skills --skill iopho-recording-checklist` · _更新于 2026-03-19_ |
| [iopho-seedance-prompts](skills/iopho-seedance-prompts/) | 即梦 Seedance 2.0 提示词工程——中文优先，覆盖 10 种能力模式<br>`npx skills add iopho-team/iopho-skills --skill iopho-seedance-prompts` · _更新于 2026-02-28_ |
| [iopho-voiceover-tts](skills/iopho-voiceover-tts/) | 使用 ElevenLabs / MiniMax / Edge TTS 生成配音，支持多语言、声音试听与多段拼接<br>`npx skills add iopho-team/iopho-skills --skill iopho-voiceover-tts` · _更新于 2026-03-19_ |
| [iopho-audio-director](skills/iopho-audio-director/) | BGM + 配音 + 音效混音，含 Suno 提示词模板与 FFmpeg 音量闪避导出<br>`npx skills add iopho-team/iopho-skills --skill iopho-audio-director` · _更新于 2026-03-19_ |

## 快速安装

```bash
# 安装指定技能
npx skills add iopho-team/iopho-skills --skill iopho-video-director

# 安装全部技能
npx skills add iopho-team/iopho-skills --all

# 全局安装（在所有项目中可用）
npx skills add iopho-team/iopho-skills --skill iopho-video-director -g -y
```

## 手动安装

每个技能是 `skills/` 目录下的一个文件夹，包含 `SKILL.md` 文件。将技能目录复制到你的 Agent 技能文件夹中：

- **Claude Code**：`.claude/skills/`
- **Cursor / Windsurf / 其他**：`.agents/skills/`

## 许可证

MIT
