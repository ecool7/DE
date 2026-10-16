"""Разрешение путей test/prod стендов."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def get_env_name() -> str:
    name = os.environ.get("RSHB_ENV", "test").strip().lower()
    if name not in {"test", "prod"}:
        raise ValueError(f"RSHB_ENV must be 'test' or 'prod', got: {name!r}")
    return name


def load_env_config(env_name: str | None = None) -> dict[str, Any]:
    env_name = env_name or get_env_name()
    path = ROOT / "configs" / "envs" / f"{env_name}.yml"
    with path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def resolve_path(key: str, env_name: str | None = None) -> Path:
    """key: raw | staging | curated | run_logs | root"""
    cfg = load_env_config(env_name)
    rel = cfg["paths"][key]
    return (ROOT / rel).resolve()


def assert_writable(env_name: str | None = None) -> None:
    cfg = load_env_config(env_name)
    if not cfg.get("allow_direct_write", False):
        raise PermissionError(
            f"Прямая запись в стенд '{cfg['name']}' запрещена. "
            "Работай в test или делай релиз: python scripts/release_to_prod.py ..."
        )
