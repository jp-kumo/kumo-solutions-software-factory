# COBOL Modernization Bridge (Starter)

A portfolio-friendly starter project that simulates a legacy COBOL batch feed and modernizes it into API-ready JSON.

## Why this project exists
Many enterprises still run critical workloads on COBOL/mainframes. Instead of “big-bang rewrite,” this project demonstrates a low-risk bridge pattern:

1. Ingest fixed-width legacy records
2. Parse to structured data
3. Normalize values (including implied-decimal money)
4. Export clean JSON/CSV for modern APIs/data platforms

---

## Project structure

```text
projects/cobol-modernization-bridge/
├── data/
│   ├── raw/
│   │   ├── customer_master.fwf
│   │   └── record_layout.md
│   └── processed/
├── docs/
│   ├── architecture.md
│   └── interview-story-pack.md
├── src/
│   ├── parse_fixed_width.py
│   └── app.py
├── requirements.txt
└── README.md
```

---

## Legacy record layout (simulated)

Each line in `customer_master.fwf` is fixed-width:

| Field | Start | End | Length | Notes |
|---|---:|---:|---:|---|
| customer_id | 1 | 10 | 10 | Numeric, zero-padded |
| account_type | 11 | 12 | 2 | CH=Checking, SV=Savings, LN=Loan |
| full_name | 13 | 42 | 30 | Left-justified |
| status | 43 | 43 | 1 | A=Active, C=Closed, D=Delinquent |
| balance_cents | 44 | 53 | 10 | Implied 2 decimals |
| open_date | 54 | 61 | 8 | YYYYMMDD |
| risk_code | 62 | 63 | 2 | 01 low, 05 high |

---

## Quick start

### 1) Fast path with Makefile

```bash
cd /home/jpadmin/.openclaw/workspace/projects/cobol-modernization-bridge
make parse
```

### 2) Run tests

```bash
make test
```

### 3) Optional API preview

```bash
make api
```

### Manual path (if preferred)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/parse_fixed_width.py \
  --input data/raw/customer_master.fwf \
  --out-json data/processed/customers.json \
  --out-csv data/processed/customers.csv
uvicorn src.app:app --reload --port 8088
```

Then open:
- `http://127.0.0.1:8088/healthz`
- `http://127.0.0.1:8088/customers`

---

## What this demonstrates in interviews
- Understanding of legacy fixed-width/COPYBOOK-style data
- Safe modernization pattern (extract/transform/serve)
- Data quality validation and anomaly surfacing
- Cloud-ready handoff format (JSON/CSV/API)

---

## Next upgrades
- Add unit tests for parser
- Add schema validation (Pydantic)
- Add db sink (SQLite/Postgres)
- Add drift checks + daily summary report
