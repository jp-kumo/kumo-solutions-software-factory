# Architecture (Legacy-to-Modern Bridge)

```mermaid
flowchart LR
  A[Legacy COBOL Batch Export\n(Fixed-width file)] --> B[Parser/Normalizer\nPython ETL]
  B --> C[Processed JSON/CSV]
  C --> D[FastAPI Service]
  C --> E[Cloud Storage / Data Warehouse]
  D --> F[Consumer App / Dashboard]
```

## Pattern
- **Strangler bridge**: keep legacy producer unchanged, modernize downstream consumption.
- Low-risk, incremental, auditable.

## Key controls
- Fixed-width layout validation
- Date and numeric parsing checks
- Delinquency flag derivation for downstream analytics
