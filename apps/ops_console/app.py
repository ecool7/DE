"""
RSHB Ops Console — визуальная панель стендов test/prod.

Запуск:
    streamlit run apps/ops_console/app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.common.env import load_env_config, resolve_path  # noqa: E402
from src.common.runlog import list_run_logs  # noqa: E402

st.set_page_config(page_title="RSHB Ops Console", page_icon="🏦", layout="wide")


def count_rows_in_dir(path: Path) -> int | None:
    if not path.exists():
        return None
    files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in {".csv", ".parquet"}]
    if not files:
        return 0
    total = 0
    for f in files:
        try:
            if f.suffix.lower() == ".csv":
                total += max(sum(1 for _ in f.open(encoding="utf-8")) - 1, 0)
            else:
                total += len(pd.read_parquet(f))
        except Exception:
            continue
    return total


def list_partitions(layer_root: Path) -> pd.DataFrame:
    rows = []
    if not layer_root.exists():
        return pd.DataFrame(columns=["entity", "partition", "files", "approx_rows", "path"])
    for entity_dir in sorted([p for p in layer_root.iterdir() if p.is_dir()]):
        for part in sorted([p for p in entity_dir.iterdir() if p.is_dir()]):
            files = [f for f in part.rglob("*") if f.is_file()]
            rows.append(
                {
                    "entity": entity_dir.name,
                    "partition": part.name,
                    "files": len(files),
                    "approx_rows": count_rows_in_dir(part),
                    "path": str(part.relative_to(ROOT)),
                }
            )
    return pd.DataFrame(rows)


def load_releases() -> pd.DataFrame:
    rel_dir = ROOT / "stands" / "releases"
    if not rel_dir.exists():
        return pd.DataFrame()
    items = []
    for f in sorted(rel_dir.glob("REL-*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            items.append(
                {
                    "release_id": data.get("release_id"),
                    "status": data.get("status"),
                    "business_dt": data.get("business_dt"),
                    "entities": ", ".join(data.get("entities") or []),
                    "released_by": data.get("released_by"),
                    "notes": data.get("notes"),
                    "ts_utc": data.get("ts_utc"),
                }
            )
        except json.JSONDecodeError:
            continue
    return pd.DataFrame(items)


st.title("RSHB Data Platform — Ops Console")
st.caption("Учебные стенды test / prod. Работаешь в test → релизишь в prod.")

tab_overview, tab_data, tab_logs, tab_release = st.tabs(
    ["Обзор стендов", "Данные", "Логи запусков", "Релизы"]
)

with tab_overview:
    c1, c2 = st.columns(2)
    for col, env_name in ((c1, "test"), (c2, "prod")):
        cfg = load_env_config(env_name)
        with col:
            st.subheader(f"Стенд: {env_name.upper()}")
            st.write(cfg.get("description", ""))
            st.code(f"allow_direct_write = {cfg.get('allow_direct_write')}")
            staging = resolve_path("staging", env_name)
            curated = resolve_path("curated", env_name)
            raw = resolve_path("raw", env_name)
            st.metric("Raw partitions", len(list(raw.glob("dt=*"))) if raw.exists() else 0)
            st.metric(
                "Staging entities",
                len([p for p in staging.iterdir() if p.is_dir()]) if staging.exists() else 0,
            )
            st.metric(
                "Curated entities",
                len([p for p in curated.iterdir() if p.is_dir()]) if curated.exists() else 0,
            )

    st.info(
        "Как запустить пайплайн на test: `$env:RSHB_ENV='test'` затем "
        "`python -m src.etl.load_clients --business-dt ...` "
        "(после того как допишешь RSHB-004)."
    )

with tab_data:
    env = st.selectbox("Стенд", ["test", "prod"], key="data_env")
    layer = st.selectbox("Слой", ["raw", "staging", "curated"], key="data_layer")
    root = resolve_path(layer, env)
    st.write(f"Путь: `{root}`")

    if layer == "raw":
        # raw: dt=.../file.csv
        rows = []
        if root.exists():
            for part in sorted(root.glob("dt=*")):
                for f in sorted(part.glob("*.csv")):
                    try:
                        n = max(sum(1 for _ in f.open(encoding="utf-8")) - 1, 0)
                    except Exception:
                        n = None
                    rows.append(
                        {
                            "partition": part.name,
                            "file": f.name,
                            "approx_rows": n,
                            "path": str(f.relative_to(ROOT)),
                        }
                    )
        df = pd.DataFrame(rows)
    else:
        df = list_partitions(root)

    if df.empty:
        st.warning("Пока пусто. Сгенерируй raw или прогони ETL / релиз.")
    else:
        st.dataframe(df, use_container_width=True)

with tab_logs:
    env = st.selectbox("Стенд для логов", ["test", "prod"], key="log_env")
    logs = list_run_logs(env, limit=100)
    if not logs:
        st.warning("Логов нет. Они появятся после generate / ETL / release.")
    else:
        st.dataframe(pd.DataFrame(logs), use_container_width=True)

with tab_release:
    st.subheader("Как сделать релиз")
    st.markdown(
        """
1. Убедись, что в **test** есть `staging/<entity>/dt=...`
2. Проверь данные на вкладке **Данные** (стенд test)
3. В терминале:

```powershell
python scripts/release_to_prod.py --entities clients --business-dt 2026-10-16 --notes "first clients release"
```

4. Обнови эту страницу — релиз появится ниже, данные будут на **prod**
        """
    )
    rel_df = load_releases()
    if rel_df.empty:
        st.info("Релизов пока не было.")
    else:
        st.dataframe(rel_df, use_container_width=True)
