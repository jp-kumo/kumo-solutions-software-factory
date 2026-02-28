# Fixed-Width Record Layout (COBOL-style simulation)

- customer_id: cols 1-10
- account_type: cols 11-12
- full_name: cols 13-42
- status: col 43
- balance_cents: cols 44-53 (implied decimal, divide by 100)
- open_date: cols 54-61 (YYYYMMDD)
- risk_code: cols 62-63

Example line length: 63 chars
