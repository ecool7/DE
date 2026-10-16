# Архитектура RSHB Data Platform (целевая)

## Бизнес-контекст

Россельхозбанк обслуживает:

- физлиц (карты, вклады, потребительские кредиты);
- агробизнес (КФХ, ООО АПК) — **кредиты на сезон, технику, оборотный капитал**;
- отделения по регионам РФ.

Data Platform кормит отчётность по портфелю АПК, операционные дашборды, риск-витрины.

## Стенды (test → prod)

```
[разработка ETL] → stands/test → [release_to_prod.py] → stands/prod
                                      │
                                      ▼
                              stands/releases/*.json
```

Ops Console (`apps/ops_console`) — визуальный просмотр обоих стендов.  
Детали: `docs/ENVIRONMENTS.md`.

## Слои данных

```
[АБС / Card System / CRM / File Exchange]
              │
              ▼
   stands/{env}/data/raw/     ← as-is, append-only, партиции по dt
              │
              ▼
   stands/{env}/data/staging  ← очистка типов, rename, дедуп
              │
              ▼
         core (core)          ← dims + facts, SCD2 где нужно (месяц 2+)
              │
              ▼
   stands/{env}/data/curated  ← витрины / marts
```

## Домены (bounded contexts)

| Домен | Сущности | Примеры витрин |
|-------|----------|----------------|
| Customer | client, segment, address | 360 клиента |
| Accounts | account, balance_snapshot | остатки на день |
| Payments | transaction | обороты, MCC |
| Lending / АПК | loan, schedule, overdue | портфель, NPL |
| Org | branch, region, employee | сеть отделений |
| Ref | currency, product, calendar | справочники |

## Пайплайн дня (целевой daily)

1. Ingest raw файлов за `business_dt`  
2. Validate file contract (колонки, rowcount > 0)  
3. Load staging  
4. Build/merge core dims & facts  
5. Run DQ checks  
6. Publish marts  
7. Write run_log (успех/ошибка, метрики)

## Технологии по этапам обучения

| Этап | Storage | Compute | Orchestration | Transform |
|------|---------|---------|---------------|-----------|
| M1 | файлы | Python | вручную / скрипт | pandas + SQL файлы |
| M2 | PostgreSQL | Python + SQL | скрипты | SQL |
| M3–4 | PostgreSQL + Parquet | Python | Airflow | dbt |
| M5–6 | PG + lake files | Spark + Python | Airflow | dbt + Spark |

## Принципы (как в банке)

1. **Raw не меняем** — только дописываем.  
2. **Идемпотентность** — повторный прогон за дату не портит данные.  
3. **ПДн** — в marts маскируем / хешируем где возможно.  
4. **Зернистость** — у каждого fact явно написан grain.  
5. **Контракт источника** — схема файла версионируется в `configs/`.
