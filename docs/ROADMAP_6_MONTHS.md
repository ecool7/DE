# Roadmap: Junior → Middle Data Engineer (6 месяцев)

**Режим:** пн–пт, 2–3 часа/день ≈ **10–15 ч/неделя** ≈ **240–360 ч за 6 месяцев**  
**Старт:** базовый Python + базовый SQL  
**Финиш:** middle DE **с мышлением Data QA** — ETL + витрины + стратегия тестирования данных + CI + релиз test→prod  
**Компас вакансии:** [`docs/TARGET_VACANCY.md`](TARGET_VACANCY.md)

Теория только **в контексте задачи**. Не читаешь «курс SQL» целиком — учишь `WINDOW` / `JOIN` / `CTE`, когда они нужны в витрине.

**Сквозная линия (каждую неделю чуть-чуть):** Data Testing (schema / integrity / freshness / quality / accuracy) + документация + code review.

---

## Месяц 1 — «Файлы банка → staging» + первый DQ

**Цель:** ETL raw→staging на **test**, базовые проверки качества, понимание релиза в **prod**.

| Неделя | Фокус | Что получишь в портфолио |
|--------|--------|---------------------------|
| W01 | Онбординг, стенды, Ops Console, raw→staging clients | `load_clients.py`, первый `pytest` |
| W02 | Валидация, дубли, Data Testing Strategy v0 | `tests/dq/` integrity/quality |
| W03 | Транзакции: chunking, логирование, разбор ошибок в run_logs | пайплайн + мониторинг |
| W04 | Витрина оборотов + accuracy-тест + релиз в prod | mart + green tests |

**Навыки:** pathlib, pandas/csv, logging, SQL, pytest, test→prod, чтение ТЗ.

---

## Месяц 2 — «DWH в PostgreSQL» (модель данных банка)

**Цель:** понимаешь слои raw → staging → core → marts; строишь star schema под кредиты АПК.

| Неделя | Фокус | Артефакт |
|--------|--------|----------|
| W05 | PostgreSQL локально, DDL, схема `stg` / `core` / `mart` | `sql/ddl/` |
| W06 | Dimensions: client, branch, product, calendar | `dim_*` |
| W07 | Facts: transactions, loan_applications | `fct_*` |
| W08 | SCD Type 2 для адреса/сегмента клиента | история изменений |

**Навыки:** нормализация vs star schema, PK/FK, индексы, миграции (простые), psycopg2/SQLAlchemy.

---

## Месяц 3 — «Оркестрация и качество» (как в проде)

**Цель:** пайплайны запускаются по расписанию, падения видны, данные проверяются.

| Неделя | Фокус | Артефакт |
|--------|--------|----------|
| W09 | Apache Airflow: первый DAG загрузки raw | `dags/rshb_daily_ingest.py` |
| W10 | Зависимости задач, retries, SLA (учебно) | DAG с ветвлением |
| W11 | Data Testing Strategy v1 + freshness/quality гейты перед publish | обновлённый `DATA_TESTING_STRATEGY.md` |
| W12 | Инкремент + CI: DQ в GitHub Actions на каждый PR | зелёный `.github/workflows/ci.yml` |

**Навыки:** идемпотентность, backfill, алерты, контракты, **тесты данных как код**, разбор упавших джобов.

---

## Месяц 4 — «dbt + бизнес-витрины АПК»

**Цель:** трансформации как код; витрины для кредитного комитета и риска.

| Неделя | Фокус | Артефакт |
|--------|--------|----------|
| W13 | dbt init, models staging/intermediate/marts | `dbt/` |
| W14 | Витрина портфеля кредитов АПК | `mart_agro_loan_portfolio` |
| W15 | Витрина просрочки / NPL (упрощённо) | `mart_npl_overview` |
| W16 | dbt docs + тесты schema/unique/not_null/relationships + accuracy | dbt test suite |

**Навыки:** Jinja в dbt, ref/source, **dbt test**, зернистость, бизнес-метрики (accuracy).

---

## Месяц 5 — «Масштаб и интеграции»

**Цель:** не только CSV: API, batch на Spark, партиции, производительность.

| Неделя | Фокус | Артефакт |
|--------|--------|----------|
| W17 | REST API ЦБ/курсы/справочники (мок) → DWH | `src/connectors/` |
| W18 | PySpark: обработка транзакций в batch | `src/spark/` |
| W19 | Партиционирование Parquet, prune, explain | оптимизация |
| W20 | CDC-имитация (файлы delta / soft-delete) | near-realtime учебный контур |

**Навыки:** FastAPI-мок или httpx, Spark DataFrame API, партиции, стоимость скана.

---

## Месяц 6 — «Прод-готовность и middle-профиль»

**Цель:** мониторинг, безопасность ПДн (учебно), портфолио, mock-interview.

| Неделя | Фокус | Артефакт |
|--------|--------|----------|
| W21 | Метрики пайплайна: row counts, lag, freshness | dashboard/лог-отчёт |
| W22 | Маскирование ПДн, роли доступа (описать + частично внедрить) | `docs/security.md` |
| W23 | End-to-end прогон «день банка», рефакторинг | стабильный daily run |
| W24 | Портфолио README, архитектура, 10 вопросов с собеса | готово к найму |

**Навыки middle:** ownership пайплайна, trade-offs, capacity to debug prod-like issues, коммуникация с бизнесом.

---

## Критерии «я middle» (чеклист к концу = готов к этой вакансии)

- [ ] Сам проектируешь слойную модель DWH под задачу банка  
- [ ] Пишешь идемпотентный ETL с инкрементом  
- [ ] Поднимаешь оркестрацию (Airflow) и понимаешь retries/backfill  
- [ ] Есть **Data Testing Strategy** и DQ-гейты до релиза в prod  
- [ ] Пишешь автотесты: schema / integrity / freshness / quality / accuracy  
- [ ] Тесты крутятся в **CI** (pytest и/или dbt test)  
- [ ] Умеешь объяснить grain, SCD2, late-arriving data  
- [ ] Документируешь источники, витрины, runbook «упал job»  
- [ ] Можешь оценить объём данных и узкое место пайплайна  
- [ ] Спокойно ревьюишь чужой SQL/Python и принимаешь ревью на свой

---

## Связь с таск-менеджером

Каждый понедельник AI выдаёт задачи недели в `tasks/CURRENT_SPRINT.md`  
по этому roadmap + твоему факту прогресса из `tasks/TASK_MANAGER.md`.

Если отстаёшь — спринт ужимаем. Если прёшь — даём hardening / spike на неделю вперёд.
