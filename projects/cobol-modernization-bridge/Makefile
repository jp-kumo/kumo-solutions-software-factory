PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
UVICORN := $(VENV)/bin/uvicorn

INPUT := data/raw/customer_master.fwf
OUT_JSON := data/processed/customers.json
OUT_CSV := data/processed/customers.csv

.PHONY: help venv install parse api test clean

help:
	@echo "Targets:"
	@echo "  venv     - create virtualenv"
	@echo "  install  - install dependencies"
	@echo "  parse    - parse fixed-width sample into JSON/CSV"
	@echo "  api      - run FastAPI on :8088"
	@echo "  test     - run pytest"
	@echo "  clean    - remove generated processed files"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

parse: install
	$(PY) src/parse_fixed_width.py --input $(INPUT) --out-json $(OUT_JSON) --out-csv $(OUT_CSV)

api: install
	$(UVICORN) src.app:app --reload --port 8088

test: install
	PYTHONPATH=. $(PY) -m pytest -q

clean:
	rm -f data/processed/customers.json data/processed/customers.csv
