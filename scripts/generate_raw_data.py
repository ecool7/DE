"""
Генератор синтетических raw-выгрузок «как из систем Россельхозбанка».

Запуск:
    python scripts/generate_raw_data.py
    python scripts/generate_raw_data.py --business-dt 2026-10-16 --clients 500
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# По умолчанию пишем на TEST-стенд (не в prod)
RAW_ROOT = ROOT / "stands" / "test" / "data" / "raw"
RUN_LOGS = ROOT / "stands" / "test" / "run_logs"

REGIONS = [
    ("23", "Краснодарский край"),
    ("61", "Ростовская область"),
    ("26", "Ставропольский край"),
    ("64", "Саратовская область"),
    ("02", "Республика Башкортостан"),
    ("16", "Республика Татарстан"),
    ("54", "Новосибирская область"),
    ("52", "Нижегородская область"),
    ("36", "Воронежская область"),
    ("48", "Липецкая область"),
]

BRANCHES = [
    ("BR-001", "23", "Краснодар — Центральный"),
    ("BR-002", "23", "Краснодар — АПК"),
    ("BR-003", "61", "Ростов-на-Дону"),
    ("BR-004", "26", "Ставрополь"),
    ("BR-005", "64", "Саратов"),
    ("BR-006", "02", "Уфа"),
    ("BR-007", "16", "Казань"),
    ("BR-008", "54", "Новосибирск"),
    ("BR-009", "52", "Нижний Новгород"),
    ("BR-010", "36", "Воронеж"),
]

FIRST_NAMES = ["Иван", "Пётр", "Сергей", "Алексей", "Дмитрий", "Анна", "Мария", "Елена", "Ольга", "Наталья"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Козлов", "Новиков", "Морозова", "Волкова", "Соколова"]
PATRONYMICS = ["Иванович", "Петрович", "Сергеевич", "Алексеевич", "Дмитриевич", "Ивановна", "Петровна", "Сергеевна"]

AGRO_NAMES = [
    "КФХ Урожай",
    "КФХ Золотой Колос",
    "ООО Агро-Юг",
    "ООО Донские Поля",
    "ООО КубаньАгро",
    "КФХ Степное",
    "ООО СибирьЗерно",
    "ООО ВолгаАгроТрейд",
]


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate synthetic RSHB raw data")
    p.add_argument("--business-dt", default="2026-10-16", help="Business date YYYY-MM-DD")
    p.add_argument("--clients", type=int, default=400)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def _rng_phone(rng: random.Random) -> str:
    return f"+7{rng.randint(900, 999)}{rng.randint(1000000, 9999999)}"


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_clients(rng: random.Random, n: int, business_dt: date) -> list[dict]:
    rows: list[dict] = []
    for i in range(1, n + 1):
        branch_id, region_code, _ = rng.choice(BRANCHES)
        region_name = dict(REGIONS)[region_code]
        roll = rng.random()
        if roll < 0.55:
            client_type = "FL"
            segment = "retail"
            full_name = f"{rng.choice(LAST_NAMES)} {rng.choice(FIRST_NAMES)} {rng.choice(PATRONYMICS)}"
            inn = ""
            birth = business_dt - timedelta(days=rng.randint(18 * 365, 70 * 365))
            birth_date = birth.isoformat()
        elif roll < 0.80:
            client_type = "KFH"
            segment = rng.choice(["agro_small", "agro_mid"])
            full_name = f"{rng.choice(AGRO_NAMES)}-{rng.randint(1, 99)}"
            inn = str(rng.randint(10**11, 10**12 - 1))
            birth_date = ""
        else:
            client_type = "OOO"
            segment = rng.choice(["agro_mid", "agro_large"])
            full_name = rng.choice([n for n in AGRO_NAMES if n.startswith("ООО")]) + f" {rng.randint(1, 50)}"
            inn = str(rng.randint(10**9, 10**10 - 1))
            birth_date = ""

        # Намеренные «грязные» данные для практики очистки (~5%)
        email = f"user{i}@mail.example"
        if rng.random() < 0.05:
            email = f"  {email.upper()}  "
        if rng.random() < 0.03:
            full_name = f" {full_name} "

        registered = datetime(2018, 1, 1) + timedelta(days=rng.randint(0, 2800))
        updated = datetime.combine(business_dt, datetime.min.time()) + timedelta(hours=rng.randint(0, 20))

        rows.append(
            {
                "client_id": f"C{i:06d}",
                "client_type": client_type,
                "full_name": full_name,
                "inn": inn,
                "birth_date": birth_date,
                "region_code": region_code,
                "region_name": region_name,
                "branch_id": branch_id,
                "segment": segment,
                "email": email,
                "phone": _rng_phone(rng),
                "registered_at": registered.strftime("%Y-%m-%d %H:%M:%S"),
                "is_active": "true" if rng.random() > 0.08 else "false",
                "updated_at": updated.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    # Дубликат client_id для DQ-практики
    if rows:
        dup = dict(rows[0])
        dup["email"] = "duplicate@mail.example"
        rows.append(dup)

    return rows


def generate_accounts(rng: random.Random, clients: list[dict], business_dt: date) -> list[dict]:
    rows: list[dict] = []
    aid = 1
    for c in clients:
        if c["client_id"] != clients[0]["client_id"] and c.get("_dup"):
            continue
        n_acc = 1 if c["client_type"] == "FL" else rng.randint(1, 3)
        for _ in range(n_acc):
            open_date = business_dt - timedelta(days=rng.randint(30, 2000))
            rows.append(
                {
                    "account_id": f"A{aid:08d}",
                    "client_id": c["client_id"],
                    "account_type": rng.choice(["current", "deposit", "loan_tech"]),
                    "currency": "RUB",
                    "open_date": open_date.isoformat(),
                    "close_date": "",
                    "status": "open" if c["is_active"] == "true" else "blocked",
                    "balance_amount": f"{rng.uniform(0, 5_000_000):.2f}",
                    "updated_at": f"{business_dt.isoformat()} 18:00:00",
                }
            )
            aid += 1
    return rows


def generate_transactions(
    rng: random.Random, accounts: list[dict], business_dt: date, per_account: int = 3
) -> list[dict]:
    rows: list[dict] = []
    tid = 1
    mccs = ["5411", "5812", "5541", "4111", "5999", ""]
    for acc in accounts:
        if acc["status"] != "open":
            continue
        for _ in range(rng.randint(0, per_account)):
            ts = datetime.combine(business_dt, datetime.min.time()) + timedelta(
                minutes=rng.randint(0, 24 * 60 - 1)
            )
            direction = rng.choice(["debit", "credit"])
            amount = rng.uniform(100, 250_000)
            rows.append(
                {
                    "txn_id": f"T{tid:010d}",
                    "account_id": acc["account_id"],
                    "client_id": acc["client_id"],
                    "txn_ts": ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "amount": f"{amount:.2f}",
                    "currency": "RUB",
                    "direction": direction,
                    "mcc": rng.choice(mccs),
                    "description": rng.choice(
                        ["POS purchase", "ATM cash", "Agro supplier payment", "Salary", "Transfer"]
                    ),
                    "branch_id": rng.choice(BRANCHES)[0],
                }
            )
            tid += 1
    return rows


def generate_loans(rng: random.Random, clients: list[dict], business_dt: date) -> list[dict]:
    """Кредиты АПК — пригодятся с месяца 2–4."""
    rows: list[dict] = []
    lid = 1
    agro = [c for c in clients if c["client_type"] in {"KFH", "OOO"}]
    for c in agro:
        if rng.random() > 0.45:
            continue
        start = business_dt - timedelta(days=rng.randint(60, 1200))
        amount = rng.choice([1_000_000, 3_000_000, 7_500_000, 15_000_000, 40_000_000])
        overdue_days = rng.choice([0, 0, 0, 0, 15, 45, 90])
        rows.append(
            {
                "loan_id": f"L{lid:07d}",
                "client_id": c["client_id"],
                "product_code": rng.choice(["AGRO_SEASON", "AGRO_TECH", "AGRO_WC", "AGRO_INVEST"]),
                "purpose": rng.choice(["seeds", "fuel", "machinery", "livestock", "working_capital"]),
                "principal_amount": f"{amount:.2f}",
                "currency": "RUB",
                "rate_pct": f"{rng.uniform(8.5, 18.0):.2f}",
                "start_date": start.isoformat(),
                "end_date": (start + timedelta(days=rng.randint(180, 1800))).isoformat(),
                "status": "overdue" if overdue_days >= 30 else "active",
                "overdue_days": overdue_days,
                "region_code": c["region_code"],
                "updated_at": f"{business_dt.isoformat()} 19:00:00",
            }
        )
        lid += 1
    return rows


def generate_branches() -> list[dict]:
    return [
        {
            "branch_id": b[0],
            "region_code": b[1],
            "branch_name": b[2],
            "is_agro_center": "true" if "АПК" in b[2] or b[0] in {"BR-002", "BR-003", "BR-004"} else "false",
        }
        for b in BRANCHES
    ]


def main() -> None:
    args = _parse_args()
    rng = random.Random(args.seed)
    business_dt = date.fromisoformat(args.business_dt)
    out_dir = RAW_ROOT / f"dt={business_dt.isoformat()}"

    clients = generate_clients(rng, args.clients, business_dt)
    accounts = generate_accounts(rng, clients, business_dt)
    transactions = generate_transactions(rng, accounts, business_dt)
    loans = generate_loans(rng, clients, business_dt)
    branches = generate_branches()

    _write_csv(
        out_dir / "clients.csv",
        list(clients[0].keys()),
        clients,
    )
    _write_csv(out_dir / "accounts.csv", list(accounts[0].keys()), accounts)
    _write_csv(out_dir / "transactions.csv", list(transactions[0].keys()), transactions)
    _write_csv(out_dir / "loans_agro.csv", list(loans[0].keys()) if loans else ["loan_id"], loans)
    _write_csv(out_dir / "branches.csv", list(branches[0].keys()), branches)

    print(f"OK: raw data written to {out_dir} [stand=test]")
    print(f"  clients:      {len(clients)} (включая 1 дубликат)")
    print(f"  accounts:     {len(accounts)}")
    print(f"  transactions: {len(transactions)}")
    print(f"  loans_agro:   {len(loans)}")
    print(f"  branches:     {len(branches)}")

    RUN_LOGS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = RUN_LOGS / f"{ts}_generate_raw_success.json"
    log_path.write_text(
        json.dumps(
            {
                "job": "generate_raw",
                "status": "success",
                "business_dt": business_dt.isoformat(),
                "message": "synthetic raw files generated",
                "metrics": {
                    "clients": len(clients),
                    "accounts": len(accounts),
                    "transactions": len(transactions),
                    "loans_agro": len(loans),
                },
                "ts_utc": ts,
                "env": "test",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  run_log:      {log_path}")


if __name__ == "__main__":
    main()
