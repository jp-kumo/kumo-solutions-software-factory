# Personal CRM Intelligence (Phase 1)

This implements your requested personal CRM intelligence pipeline with filtering, scoring, dedupe, and summaries.

## Files
- `scripts/personal_crm_intelligence.py`
- `configs/personal_crm_learning.json`
- SQLite DB: `data/personal_crm.sqlite`
- Run reports: `data/reports/personal_crm_run_*.json`

## What is implemented

### Data sources (ready now)
- JSON exports for email and calendar (configured via `email_json_path`, `calendar_json_path`)
- Optional live command adapters (`email_command`, `calendar_command`) for direct API/CLI ingestion

### Contact extraction
- Email parsing from sender/recipient fields
- Exchange estimate:
  - `min(floor(total_messages/2), thread_count)`
- Calendar attendee extraction with constraints:
  - attendees between 1 and `max_attendees`
  - event duration >= `min_duration_minutes`

### Two-stage filtering
1. **Hard filters**:
   - own emails
   - excluded contacts
   - previously rejected/already present
   - role inboxes (`info@`, `team@`, `noreply@`, etc.)
   - marketing-like prefixes
2. **AI classification**:
   - heuristic classifier always available
   - optional Gemini Flash call when `GEMINI_API_KEY` is set

### Contact scoring
- Base 50
- +5/exchange (max +20)
- +3/meeting (max +15)
- +15 preferred title match
- +10 if calendar meetings exist (small-meeting signal)
- +10 if last touch <=7d; +5 if <=30d
- +25 if appears in both email and calendar
- +10 recognizable role, +5 company

### Learning system
- `configs/personal_crm_learning.json`
- Updates `skip_domains` from rejected candidates only after threshold (`domain_rejection_threshold`, default 3 distinct rejected senders)
- Supports guardrails:
  - `allow_emails`
  - `allow_domains`

### Deduplication
- email match first
- fallback name+company
- merges records (no duplicate contact rows)

### Storage
- SQLite + WAL + foreign keys
- tables: `contacts`, `interactions`, `rejections`, `contact_embeddings`, `runs`

### Notifications
- per-run summary emitted to stdout
- optional `notify_command` hook for external summary delivery

### First-run safety controls
- `shadow_mode` (default `true`) approves candidates but does not write contacts
- `max_new_contacts_per_run` anomaly threshold
- `max_rejections_per_run` anomaly threshold
- on anomaly, learning updates are not persisted for that run

### Query helpers (SQL views)
- `v_stale_contacts_30d`
- `v_cross_signal_contacts`
- `v_recent_high_score`

---

## Run

Initialize:
```bash
python3 scripts/personal_crm_intelligence.py --init
```

Ingest:
```bash
python3 scripts/personal_crm_intelligence.py --run
```

---

## Daily cron example

```bash
0 13 * * * cd /home/jpadmin/.openclaw/workspace && /usr/bin/python3 scripts/personal_crm_intelligence.py --run >> /home/jpadmin/.openclaw/workspace/data/reports/personal_crm_cron.log 2>&1
```

---

## Live ingestion wiring (implemented)
Configured commands in `configs/personal_crm_learning.json`:
- `email_command`: `python3 /home/jpadmin/.openclaw/workspace/scripts/crm_fetch_gmail.py`
- `calendar_command`: `python3 /home/jpadmin/.openclaw/workspace/scripts/crm_fetch_calendar.py`

Helper scripts added:
- `scripts/crm_fetch_gmail.py`
- `scripts/crm_fetch_calendar.py`

### Required env for gog keyring backend
If gog keyring password is required in non-interactive runs, set:
- `GOG_KEYRING_PASSWORD`

You can place this in the cron command line or a sourced env file.
