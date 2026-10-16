# Data Testing Strategy — RSHB Data Platform

> Живой документ. В W01 достаточно прочитать. С W02 начинаешь заполнять и внедрять.

## Цель

Не пускать в **prod** данные, которые сломают отчёты аналитиков / DS.

## Когда что тестируем

| Стадия | Что проверяем | Где живёт тест | Блокирует релиз? |
|--------|---------------|----------------|------------------|
| Pre-load (raw) | файл есть, не пустой, колонки по контракту | `tests/dq/test_raw_contracts.py` | да (на test-прогоне) |
| Post-staging | типы, дубли PK, trim/normalize сделаны | `tests/dq/test_staging_*.py` | да |
| Post-mart | бизнес-правила, суммы сходятся | `tests/dq/` + позже dbt tests | да |
| Prod monitor | freshness, row count vs вчера | Ops Console + run_logs | алерт (M3+) |

## Виды проверок (словарь вакансии)

| Вид | Вопрос | Пример для clients |
|-----|--------|-------------------|
| **Schema conformity** | Совпадает ли схема с контрактом? | есть `client_id`, `segment`, ... |
| **Integrity** | Целостность связей/ключей? | `client_id` уникален в staging |
| **Freshness** | Данные свежие / за нужную дату? | партиция `dt=` = business_dt |
| **Quality** | Нет ли мусора? | email без пробелов, `client_type` из enum |
| **Accuracy** | Верно ли бизнес-правило? | KFH/OOO → segment начинается с `agro_` |

## Политика релиза (test → prod)

1. ETL успешно отработал на **test** (есть run_log `success`).  
2. `pytest tests/dq -q` зелёный.  
3. Глазами глянул Ops Console (строки, партиции).  
4. Только тогда: `python scripts/release_to_prod.py ...`  
5. На **prod** снова смотришь freshness/rowcount.

## CI/CD (целевое)

- На каждый PR: unit-тесты + DQ на фикстурах.  
- Перед merge в main: нельзя красным.  
- Файл: `.github/workflows/ci.yml` (каркас уже есть; расширяешь по спринтам).

## Что заполнишь ты (чеклист роста)

- [ ] W02: 3+ теста на clients staging  
- [ ] W04: accuracy-тест на первую витрину  
- [ ] W11: стратегия v1 «как в проде» (этот файл обновлён)  
- [ ] W16: dbt tests на marts  
- [ ] W21: freshness-мониторинг в консоли/логах  

## Заметки ученика

_(пиши сюда решения: почему дропаем дубли, какие пороги null-rate, и т.д.)_
