# Kumo Proposal Generator

Quick helper script to generate proposal drafts for **Kumo Solutions** from the standard lead-response template.

## Script

`scripts/kumo_proposal_generator.sh`

## Usage

```bash
./scripts/kumo_proposal_generator.sh "Client Name" [YYYY-MM-DD] [output_filename.md]
```

## Examples

```bash
# Uses today's UTC date and auto output path
./scripts/kumo_proposal_generator.sh "Acme Biotech"

# Explicit date
./scripts/kumo_proposal_generator.sh "Acme Biotech" "2026-03-01"

# Explicit output file
./scripts/kumo_proposal_generator.sh "Acme Biotech" "2026-03-01" "proposals/acme-proposal.md"
```

## Behavior

- Reads template: `docs/kumo-proposal-lead-response-accelerator-lr.md`
- Replaces placeholders:
  - `{{Client Name}}`
  - `{{Date}}`
- If no output file is provided, writes to:
  - `proposals/<date>-<client-slug>-proposal.md`
- Creates output directory automatically.
- Validates date format as `YYYY-MM-DD`.
