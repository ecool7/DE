"""
Создаёт папки стендов test/prod и переносит старые data/raw → stands/test (если есть).

Запуск:
    python scripts/bootstrap_stands.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LAYERS = ("raw", "staging", "curated")


def ensure_stand(name: str) -> None:
    base = ROOT / "stands" / name
    for layer in LAYERS:
        (base / "data" / layer).mkdir(parents=True, exist_ok=True)
    (base / "run_logs").mkdir(parents=True, exist_ok=True)
    (ROOT / "stands" / "releases").mkdir(parents=True, exist_ok=True)
    print(f"OK: stand '{name}' -> {base}")


def migrate_legacy_raw() -> None:
    legacy = ROOT / "data" / "raw"
    target = ROOT / "stands" / "test" / "data" / "raw"
    if not legacy.exists():
        return
    partitions = [p for p in legacy.iterdir() if p.is_dir() and p.name.startswith("dt=")]
    if not partitions:
        return
    for part in partitions:
        dest = target / part.name
        if dest.exists():
            print(f"skip migrate (already exists): {dest}")
            continue
        shutil.copytree(part, dest)
        print(f"migrated: {part} → {dest}")


def main() -> None:
    ensure_stand("test")
    ensure_stand("prod")
    migrate_legacy_raw()
    print("Done. Default env is test (RSHB_ENV=test).")


if __name__ == "__main__":
    main()
