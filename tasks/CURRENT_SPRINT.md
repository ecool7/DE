# Sprint 1 — Онбординг и первая загрузка (W01)

**Период:** 2026-10-19 → 2026-10-23 (пн–пт)  
**Цель спринта:** понять проект под целевую вакансию (DE + Data QA), поднять test/prod, Ops Console и первый ETL clients.  
**Тема roadmap:** Месяц 1 / Неделя 1  
**Story points (условно):** 13  
**Owner:** Karen (Junior DE)  
**Компас:** `docs/TARGET_VACANCY.md`

---

## Sprint Goal

> «Я понимаю test→prod и Data QA-линию вакансии, вижу стенды в Ops Console и гружу clients в staging на test.»

---

## Board

### RSHB-001 · Task · 2–3 ч · To Do
**Title:** Онбординг: прочитать доки и нарисовать поток данных  
**Acceptance criteria:**
- [ ] Прочитаны `README.md`, `docs/ARCHITECTURE.md`, `docs/GLOSSARY.md`, `docs/ENVIRONMENTS.md`, `tasks/HOW_TO_WORK.md`
- [ ] Прочитаны `docs/TARGET_VACANCY.md` и `docs/DATA_TESTING_STRATEGY.md` (пока обзорно)
- [ ] В `docs/notes/w01_data_flow.md` есть твоя схема: raw → staging → (пока пусто) и 5–10 предложений «что делает платформа»
- [ ] В заметке 3–5 строк: «какие обязанности вакансии закрываю уже в W01»
- [ ] В `TASK_MANAGER.md` отмечено, что онбординг пройден

**Навыки:** чтение ТЗ, системное мышление, карта навыков под вакансию  
**Подсказка:** не зубрить — своими словами.

---

### RSHB-002 · Task · 1–2 ч · To Do
**Title:** Поднять окружение + стенды test/prod + Ops Console  
**Acceptance criteria:**
- [ ] Создан `.venv`, установлены зависимости из `requirements.txt`
- [ ] Выполнены `python scripts/bootstrap_stands.py` и `python scripts/generate_raw_data.py`
- [ ] Файлы появились в `stands/test/data/raw/dt=.../` (не в prod)
- [ ] Запущен `streamlit run apps/ops_console/app.py` — в браузере виден стенд test с данными
- [ ] Прочитан `docs/ENVIRONMENTS.md` (понимаешь: test → release → prod)
- [ ] Команда `pytest tests -q` проходит (после generate)

**Навыки:** venv, pip, стенды, мониторинг, первый CI-локальный прогон  
**Подсказка:** если ошибка — целиком traceback в TASK_MANAGER.

---

### RSHB-003 · Task · 2–3 ч · To Do
**Title:** Изучить контракт сырых файлов клиентов  
**Acceptance criteria:**
- [ ] Открыт `stands/test/data/raw/.../clients.csv` (путь после генерации)
- [ ] В `docs/notes/w01_clients_profile.md` описано: колонки, типы «как кажется», странности (пустые, дубли?), 3 примера строк
- [ ] Заполнен/уточнён `configs/sources/clients.yml` (комментарии своими словами ок)

**Навыки:** data profiling руками, YAML-контракты  
**Подсказка:** считай строки, смотри уникальность `client_id`.

---

### RSHB-004 · Story · 4–6 ч (можно пн+вт) · To Do
**Title:** ETL: загрузка клиентов raw → staging (Parquet/CSV)  
**Acceptance criteria:**
- [ ] Есть `src/etl/load_clients.py` (можно доработать заготовку)
- [ ] Скрипт читает raw clients за `business_dt`
- [ ] Пишет результат в `stands/test/data/staging/clients/dt=YYYY-MM-DD/`
- [ ] Базовая очистка: trim строк, парсинг дат рождения, нижний регистр email если есть
- [ ] Лог в консоль: сколько прочитано / записано / отброшено
- [ ] Запуск через CLI: `python -m src.etl.load_clients --business-dt 2026-10-16` (или дата из генератора)
- [ ] (бонус) Релиз в prod: `python scripts/release_to_prod.py --entities clients --business-dt ...` и проверка в Ops Console на вкладке prod

**Навыки:** argparse/typer, pathlib, pandas или csv, logging, релиз  
**Definition of Done:** повторный запуск за ту же дату не плодит мусор (перезапись папки/файла ок).

---

### RSHB-005 · Task · 1–2 ч · To Do
**Title:** SQL-разведка по staging-клиентам  
**Acceptance criteria:**
- [ ] Файл `sql/adhoc/w01_clients_checks.sql` с запросами (можно через DuckDB или загрузку в SQLite/PG — на твой выбор, опиши как запускал)
- [ ] Ответы на вопросы:
  1. Сколько клиентов?
  2. Сколько в сегментах (физлицо / КФХ / ООО)?
  3. Топ-5 регионов по числу клиентов?
- [ ] Результаты коротко в `docs/notes/w01_sql_answers.md`

**Навыки:** GROUP BY, COUNT, базовый JOIN если понадобится справочник  
**Подсказка:** если PG ещё нет — DuckDB отлично читает Parquet/CSV.

---

### RSHB-006 · Chore · 1 ч · To Do
**Title:** Сдать спринт: ревью + weekly summary  
**Acceptance criteria:**
- [ ] Все Done/переносы отражены в `CURRENT_SPRINT.md`
- [ ] В `TASK_MANAGER.md` заполнены ревью-запросы и weekly summary
- [ ] Написано в чат: **«Ревью моей работы»** хотя бы 1 раз за спринт (лучше после RSHB-004)

---

## Не в этом спринте (осознанно)

- PostgreSQL DWH  
- Airflow  
- Кредиты АПК витрины  

Сначала — дисциплина слоёв и один честный ETL.

---

## Daily notes (опционально)

| День | План на 2–3 ч | Факт |
|------|----------------|------|
| Пн | RSHB-001, RSHB-002 | |
| Вт | RSHB-003 | |
| Ср | RSHB-004 (часть 1) | |
| Чт | RSHB-004 (часть 2) | |
| Пт | RSHB-005, RSHB-006 | |
