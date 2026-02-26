# AI Content Humanization Tool

Script: `scripts/ai_content_humanizer.py`

## What it does

1. Detects common AI-writing tells:
- stock phrases (`delve`, `landscape`, `leverage`, etc.)
- repetitive sentence starts
- hedging language
- uniform paragraph rhythm
- generated-feeling list structure

2. Rewrites text to sound more human:
- replaces vague/formal AI phrasing with direct wording
- trims filler
- varies sentence cadence
- applies natural contractions

3. Optional channel tuning:
- `twitter`: punchy + <= 280 chars
- `linkedin`: professional-conversational
- `blog`: allows voice/opinion
- `email`: brief, action-oriented opener

## Usage

```bash
cd /home/jpadmin/.openclaw/workspace
python3 scripts/ai_content_humanizer.py --text "Your draft text here" --channel linkedin --show-changes
```

Or from file:

```bash
python3 scripts/ai_content_humanizer.py --file /path/to/draft.txt --channel email --show-changes
```
