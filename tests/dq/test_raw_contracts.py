"""
Каркас DQ: schema conformity для raw clients.

W01: просто убедись, что тест находится и проходит на сгенерированных данных.
W02+: расширишь integrity / quality / accuracy.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CLIENTS_CONTRACT = ROOT / "configs" / "sources" / "clients.yml"
RAW_CLIENTS = ROOT / "stands" / "test" / "data" / "raw"


def _latest_clients_csv() -> Path:
    parts = sorted(RAW_CLIENTS.glob("dt=*/clients.csv"))
    if not parts:
        pytest.skip("No raw clients yet. Run: python scripts/generate_raw_data.py")
    return parts[-1]


def test_clients_raw_file_not_empty():
    path = _latest_clients_csv()
    df = pd.read_csv(path)
    assert len(df) > 0, f"Empty file: {path}"


def test_clients_raw_schema_conformity():
    """Колонки raw соответствуют контракту configs/sources/clients.yml."""
    with CLIENTS_CONTRACT.open(encoding="utf-8") as f:
        contract = yaml.safe_load(f)
    expected = [c["name"] for c in contract["columns"]]

    df = pd.read_csv(_latest_clients_csv())
    missing = set(expected) - set(df.columns)
    extra = set(df.columns) - set(expected)

    assert not missing, f"Missing columns vs contract: {missing}"
    # extra не всегда ошибка — но в учебном контракте лишних быть не должно
    assert not extra, f"Unexpected columns: {extra}"
