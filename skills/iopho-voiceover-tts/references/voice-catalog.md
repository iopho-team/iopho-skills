# Voice Catalog — TTS Engines × Voices × Languages

> Reference for `/iopho-voiceover-tts`. Updated 2026-03.

## Engine Comparison

| Engine | Quality | Cost | Languages | Latency | API Key Required |
|--------|---------|------|-----------|---------|-----------------|
| **ElevenLabs** | ★★★★★ (EN), ★★★★ (ZH) | ~$0.30/1K chars | 29+ | 1-3s | Yes (`ELEVENLABS_API_KEY`) |
| **MiniMax** | ★★★ (EN), ★★★★★ (ZH) | ~$0.10/1K chars | 5 | 2-5s | Yes (`MINIMAX_API_KEY`) |
| **Edge TTS** | ★★★ (EN), ★★★½ (ZH) | **FREE** | 300+ | <1s | No |

## Recommended Routing

| Language | Primary Engine | Free Fallback | Notes |
|----------|---------------|---------------|-------|
| English | ElevenLabs | Edge TTS | ElevenLabs = industry-best EN quality |
| 中文 (Mandarin) | MiniMax | Edge TTS | MiniMax = best CN natural tone |
| Japanese / Korean | ElevenLabs | Edge TTS | ElevenLabs multilingual_v2 |
| Other languages | Edge TTS | — | 300+ voices, zero cost |

## Available Voices

### ElevenLabs

| Voice ID | Name | Gender | Tone | Best For |
|----------|------|--------|------|----------|
| `bIHbv24MWmeRgasZH58o` | Will | M | Deep, authoritative | SaaS demos, product launches |
| `pNInz6obpgDQGcFmaJgB` | Adam | M | Warm, conversational | Explainers, onboarding |
| `ErXwobaYiN019PkySvjV` | Antoni | M | Calm, professional | Corporate, enterprise |
| `9BWtsMINqrJLrRacOk9x` | Aria | F | Soft, neutral | Mandarin VO, gentle narration |

**Model**: `eleven_multilingual_v2`

**Proven Settings (from production)**:

| Setting | EN Value | ZH Value | Effect |
|---------|----------|----------|--------|
| stability | 0.50 | 0.55 | Lower = more expressive |
| similarity_boost | 0.75 | 0.75 | Higher = closer to original voice |
| style | 0.35 | 0.20 | Lower = more neutral |
| use_speaker_boost | true | true | Enhances clarity |

### MiniMax

| Voice | Language | Tone |
|-------|----------|------|
| `Chinese (Mandarin)_Gentleman` | zh-CN | Male, professional, clear |

**Model**: `speech-01-hd`
**Config**: sample_rate=32000, bitrate=128k, speed=1.0

### Edge TTS (Free)

| Voice ID | Language | Gender | Natural? |
|----------|----------|--------|----------|
| `zh-CN-XiaoxiaoNeural` | zh-CN | F | ★★★★ Warm, conversational |
| `zh-CN-YunxiNeural` | zh-CN | M | ★★★½ Professional |
| `zh-CN-XiaoyiNeural` | zh-CN | F | ★★★ Friendly, young |
| `en-US-JennyNeural` | en-US | F | ★★★★ Clear, neutral |
| `en-US-GuyNeural` | en-US | M | ★★★½ Authoritative |
| `en-GB-SoniaNeural` | en-GB | F | ★★★½ British, professional |

**SSML defaults**: rate="-5%", pitch="+0Hz"

## Cost Estimation

| Scenario | Words | Chars (~) | ElevenLabs | MiniMax | Edge TTS |
|----------|-------|-----------|------------|---------|----------|
| 30s teaser | ~50 | ~300 | $0.09 | $0.03 | FREE |
| 60s explainer | ~100 | ~600 | $0.18 | $0.06 | FREE |
| 90s launch | ~150 | ~900 | $0.27 | $0.09 | FREE |
| 3-voice audition | ~30×3 | ~540 | $0.16 | $0.05 | FREE |

## API Key Setup

### ElevenLabs
```bash
# Option 1: Environment variable
export ELEVENLABS_API_KEY="sk-..."

# Option 2: .env file (looked up at ~/path/to/papper-3rd/.env)
ELEVENLABS_API_KEY=sk-...
```
Get key: https://elevenlabs.io/app/settings/api-keys

### MiniMax
```bash
export MINIMAX_API_KEY="eyJ..."
```
Get key: https://platform.minimaxi.com/

### Edge TTS
No key needed. Install: `pip install edge-tts`
