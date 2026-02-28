from pathlib import Path
import json

from src.parse_fixed_width import parse_line, parse_file


def test_parse_line_basic():
    line = "0000001001CHJACQUES PAYNE                 A00001234562023010101"
    rec = parse_line(line)
    assert rec["customer_id"] == "0000001001"
    assert rec["account_type"] == "CH"
    assert rec["full_name"] == "JACQUES PAYNE"
    assert rec["status"] == "A"
    assert rec["balance"] == 1234.56
    assert rec["open_date"] == "2023-01-01"
    assert rec["risk_code"] == "01"
    assert rec["is_delinquent"] is False


def test_parse_file_count():
    p = Path(__file__).resolve().parents[1] / "data" / "raw" / "customer_master.fwf"
    rows = parse_file(p)
    assert len(rows) == 5
    assert rows[2]["is_delinquent"] is True
