# Personal Knowledge Base (RAG)

Implemented in:
- `scripts/knowledge_base_rag.py`
- config: `configs/knowledge_base.json`
- db: `data/knowledge_base.sqlite`

## Features implemented

- Ingest URL/file and auto-detect source type (`article`, `video`, `pdf`, `text`, `tweet`, `other`).
- Extraction fallback chains:
  - Tweets: FxTwitter API -> Twitter oEmbed -> scrape
  - YouTube: `youtube-transcript-api` -> `yt-dlp`
  - Other web: `trafilatura` -> Firecrawl (if API key) -> Playwright node fallback -> raw fetch + strip HTML
- Retry once for transient network errors with 2s delay.
- Content quality validation:
  - minimum 20 chars
  - non-tweets minimum 500 chars
  - non-tweets prose-line ratio >= 15%
  - error-page signal detection (2+ keywords)
  - max 200k chars truncation
- Dedup:
  - normalized URL unique check
  - content SHA-256 unique check
- Chunking:
  - size 800, overlap 200, min chunk 100
  - sentence-boundary split (`/(?<=[.!?])\s+/` equivalent)
- Embeddings:
  - provider preference from config (`gemini` default, `openai` fallback configurable)
  - max 8000 chars/chunk input
  - batches of 10, 200ms delay
  - retry x3 exponential backoff (1s, 2s, 4s)
  - LRU embedding cache (1000 entries)
- Storage:
  - SQLite WAL + foreign keys
  - `sources` + `chunks` tables with indexes + cascade FK
- Concurrency lock file:
  - `data/knowledge_base.lock`
  - stale logic: >15 min or dead PID
- Retrieval:
  - query embedding
  - cosine similarity across chunks
  - top-k (default 10)
  - dedupe best chunk per source
  - sanitize excerpt max 2500 chars
  - LLM synthesis prompt: answer only from context + cite sources

## Usage

Initialize:
```bash
cd /home/jpadmin/.openclaw/workspace
python3 scripts/knowledge_base_rag.py init
```

Ingest URL:
```bash
python3 scripts/knowledge_base_rag.py ingest "https://example.com/article" --tags "ai,cloud"
```

For trusted but transcript-like/noisy files that fail strict validators, use:
```bash
python3 scripts/knowledge_base_rag.py ingest "/path/to/file.md" --tags "telegram-upload" --force
```

Ingest file:
```bash
python3 scripts/knowledge_base_rag.py ingest "/path/to/file.pdf" --tags "paper"
```

Query:
```bash
python3 scripts/knowledge_base_rag.py query "What did I save about Terraform hiring trends?" --top-k 10
```

## Environment

For embeddings / extraction fallbacks:
- `GEMINI_API_KEY` (recommended)
- `OPENAI_API_KEY` (fallback)
- `FIRECRAWL_API_KEY` (optional fallback for hard sites)

For answer synthesis (query-time final response text):
- `synthesis_provider` in `configs/knowledge_base.json` supports: `auto|gemini|openai|none`
- `synthesis_model_gemini` default: `models/gemini-flash-latest`
- `synthesis_model_openai` default: `gpt-4o-mini`
- If synthesis fails, query output now returns provider-specific error details instead of a generic key-missing message.

Optional local tools:
- `yt-dlp`
- `pdftotext` (poppler)
- Node + `playwright`
- Python package `trafilatura`
