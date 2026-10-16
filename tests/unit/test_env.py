"""Unit-тесты инфраструктуры стендов (как в вакансии: тесты как код)."""

from __future__ import annotations

import os

from src.common.env import assert_writable, get_env_name, load_env_config


def test_default_env_is_test(monkeypatch):
    monkeypatch.delenv("RSHB_ENV", raising=False)
    assert get_env_name() == "test"


def test_test_stand_is_writable(monkeypatch):
    monkeypatch.setenv("RSHB_ENV", "test")
    assert_writable("test")  # не должно кидать


def test_prod_stand_blocks_direct_write(monkeypatch):
    monkeypatch.setenv("RSHB_ENV", "prod")
    cfg = load_env_config("prod")
    assert cfg["allow_direct_write"] is False
    try:
        assert_writable("prod")
        raise AssertionError("prod must block direct write")
    except PermissionError:
        pass
