"""Простые JSON-логи прогонов пайплайна (видны в Ops Console)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.common.env import resolve_path


def write_run_log(
    job: str,
    status: str,
    *,
    business_dt: str | None = None,
    metrics: dict[str, Any] | None = None,
    message: str = "",
    env_name: str | None = None,
) -> Path:
    log_dir = resolve_path("run_logs", env_name)
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = log_dir / f"{ts}_{job}_{status}.json"
    payload = {
        "job": job,
        "status": status,
        "business_dt": business_dt,
        "message": message,
        "metrics": metrics or {},
        "ts_utc": ts,
        "env": env_name or "test",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def list_run_logs(env_name: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    log_dir = resolve_path("run_logs", env_name)
    if not log_dir.exists():
        return []
    files = sorted(log_dir.glob("*.json"), reverse=True)[:limit]
    rows: list[dict[str, Any]] = []
    for f in files:
        try:
            rows.append(json.loads(f.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return rows
