# Backlog

Идеи и долги вне текущего спринта. AI забирает отсюда в понедельник.  
Приоритет — линия вакансии DE + Data QA (`docs/TARGET_VACANCY.md`).

## Ready (можно в спринт)

- [ ] W02: `tests/dq/test_staging_clients.py` — integrity (unique client_id) + quality (email trim)
- [ ] Pre-release gate: скрипт `scripts/pre_release_check.py` (pytest + наличие staging)
- [ ] Единый CLI `python -m src.cli ingest --entity clients --dt ...`
- [ ] Runbook: `docs/runbooks/job_failed.md` — как разбирать упавший job по run_logs

## Icebox (потом)

- [ ] Docker Compose: Postgres + Airflow
- [ ] Great Expectations / elemental DQ framework
- [ ] dbt docs publish + dbt test в CI
- [ ] Маскирование ФИО/телефона в marts
- [ ] Mock API курсов валют ЦБ
- [ ] Slack/email алерт-заглушка при fail job

## Tech debt

- [ ] (появится после первых ревью)
