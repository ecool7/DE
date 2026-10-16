"""
Релиз test → prod: копирует выбранные сущности из staging (и опционально curated).

Как в банке: не правим прод руками — промоутим проверенный артефакт.

Запуск:
    python scripts/release_to_prod.py --entities clients --business-dt 2026-10-16
    python scripts/release_to_prod.py --entities clients,accounts --business-dt 2026-10-16 --layers staging
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.common.env import resolve_path  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Promote data from test stand to prod")
    p.add_argument("--entities", required=True, help="Comma-separated: clients,accounts,...")
    p.add_argument("--business-dt", required=True, help="YYYY-MM-DD")
    p.add_argument(
        "--layers",
        default="staging",
        help="Comma-separated layers: staging,curated,raw (default: staging)",
    )
    p.add_argument("--released-by", default="karen", help="Who releases (for audit)")
    p.add_argument("--notes", default="", help="Release notes")
    return p.parse_args()


def promote_entity(layer: str, entity: str, business_dt: str) -> dict:
    src = resolve_path(layer, "test") / entity / f"dt={business_dt}"
    dst = resolve_path(layer, "prod") / entity / f"dt={business_dt}"

    if not src.exists():
        return {
            "layer": layer,
            "entity": entity,
            "status": "failed",
            "reason": f"source missing: {src}",
        }

    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)

    files = list(dst.rglob("*"))
    file_count = sum(1 for f in files if f.is_file())
    return {
        "layer": layer,
        "entity": entity,
        "status": "ok",
        "src": str(src),
        "dst": str(dst),
        "files": file_count,
    }


def main() -> None:
    args = parse_args()
    entities = [e.strip() for e in args.entities.split(",") if e.strip()]
    layers = [l.strip() for l in args.layers.split(",") if l.strip()]

    results = []
    for layer in layers:
        if layer not in {"raw", "staging", "curated"}:
            raise SystemExit(f"Unknown layer: {layer}")
        for entity in entities:
            results.append(promote_entity(layer, entity, args.business_dt))

    failed = [r for r in results if r["status"] != "ok"]
    status = "failed" if failed else "success"
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    release_id = f"REL-{ts}"

    manifest = {
        "release_id": release_id,
        "status": status,
        "business_dt": args.business_dt,
        "entities": entities,
        "layers": layers,
        "released_by": args.released_by,
        "notes": args.notes,
        "ts_utc": ts,
        "results": results,
    }

    releases_dir = ROOT / "stands" / "releases"
    releases_dir.mkdir(parents=True, exist_ok=True)
    out = releases_dir / f"{release_id}.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # run log на prod
    prod_logs = resolve_path("run_logs", "prod")
    prod_logs.mkdir(parents=True, exist_ok=True)
    (prod_logs / f"{ts}_release_{status}.json").write_text(
        json.dumps(
            {
                "job": "release_to_prod",
                "status": status,
                "business_dt": args.business_dt,
                "message": args.notes or release_id,
                "metrics": {"entities": len(entities), "ok": len(results) - len(failed)},
                "ts_utc": ts,
                "env": "prod",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Release {release_id}: {status}")
    for r in results:
        print(f"  [{r['status']}] {r['layer']}/{r['entity']} — {r.get('reason') or r.get('dst')}")
    print(f"Manifest: {out}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
