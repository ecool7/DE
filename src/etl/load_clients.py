"""
RSHB-004: загрузка клиентов raw → staging.

Заготовка для ученика. Допиши очистку и запись по acceptance criteria спринта.

Запуск (после доработки) — всегда на TEST:
    $env:RSHB_ENV = "test"
    python -m src.etl.load_clients --business-dt 2026-10-16
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.common.env import assert_writable, resolve_path

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    # defaults из стенда (test по умолчанию)
    default_raw = resolve_path("raw")
    default_staging = resolve_path("staging")

    p = argparse.ArgumentParser(description="Load clients raw → staging")
    p.add_argument("--business-dt", required=True, help="YYYY-MM-DD")
    p.add_argument("--raw-root", type=Path, default=default_raw)
    p.add_argument("--staging-root", type=Path, default=default_staging)
    return p.parse_args()


def load_clients(business_dt: str, raw_root: Path, staging_root: Path) -> None:
    """
    TODO (RSHB-004):
    1. Прочитать raw CSV: raw_root / f"dt={business_dt}" / "clients.csv"
    2. Очистить: trim строк, нормализовать email, распарсить birth_date
    3. Обработать дубликаты client_id (реши и задокументируй правило)
    4. Записать в staging_root / "clients" / f"dt={business_dt}" /
    5. Залогировать counts: read / written / dropped
       (подсказка: from src.common.runlog import write_run_log)
    """
    assert_writable()  # на prod прямая запись запрещена
    raw_path = raw_root / f"dt={business_dt}" / "clients.csv"
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {raw_path}. "
            f"Run: python scripts/generate_raw_data.py --business-dt {business_dt}"
        )

    logger.info("env=%s", os.environ.get("RSHB_ENV", "test"))
    logger.info("Found raw file: %s", raw_path)
    # --- твой код ниже ---
    raise NotImplementedError("Implement RSHB-004: raw → staging for clients")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )
    args = parse_args()
    load_clients(args.business_dt, args.raw_root, args.staging_root)


if __name__ == "__main__":
    main()
