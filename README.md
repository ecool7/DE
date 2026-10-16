# RSHB Data Platform (учебный проект)

Учебная data-платформа **как будто внутри Россельхозбанка**: кредиты АПК, клиенты (физлица / агробизнес), счета, транзакции, отделения, витрины для отчётности.

Цель: за 6 месяцев вырасти с слабого junior Data Engineer до уверенного middle **через практику на одном сквозном проекте**, а не через теорию ради теории.

## Как учиться

| День | Что делать |
|------|------------|
| Пн–Пт | 2–3 часа по задачам из `tasks/CURRENT_SPRINT.md` |
| Пн (утро) | Напиши в чат: **«Понедельник — выдай спринт»** |
| После задачи | Заполни `tasks/TASK_MANAGER.md` → попроси ревью |
| Сб–Вс | Отдых или лёгкий рефактор (по желанию) |

Подробный план: [`docs/ROADMAP_6_MONTHS.md`](docs/ROADMAP_6_MONTHS.md)  
Целевая вакансия (DE + Data QA): [`docs/TARGET_VACANCY.md`](docs/TARGET_VACANCY.md)  
Как работать с задачами: [`tasks/HOW_TO_WORK.md`](tasks/HOW_TO_WORK.md)

## Стек (растёт вместе с тобой)

1. **Мес 1–2:** Python, SQL, CSV/Parquet, PostgreSQL, pandas  
2. **Мес 3–4:** Airflow, dbt, data quality, SCD, инкременты  
3. **Мес 5–6:** Spark (batch), API-источники, мониторинг, документация, портфолио

## Стенды test / prod

Как в банке: сначала тест, потом релиз в прод.

| Стенд | Папка | Что делаешь |
|-------|--------|-------------|
| **test** | `stands/test/` | Разработка, отладка ETL |
| **prod** | `stands/prod/` | Только через релиз |

Подробно: [`docs/ENVIRONMENTS.md`](docs/ENVIRONMENTS.md)

```powershell
# Работа всегда на test (по умолчанию)
$env:RSHB_ENV = "test"
python scripts/generate_raw_data.py

# Релиз в prod
python scripts/release_to_prod.py --entities clients --business-dt 2026-10-16
```

## Визуально смотреть сервис

Да. Есть **Ops Console** (веб-панель в браузере):

```powershell
.venv\Scripts\activate
streamlit run apps/ops_console/app.py
```

Откроется http://localhost:8501 — там test/prod, файлы, логи, релизы.

## Структура репозитория

```
rshb-data-platform/
├── README.md
├── apps/ops_console/      # визуальная панель стендов
├── docs/                  # архитектура, roadmap, стенды
├── tasks/                 # «Jira» + task-manager + ревью
├── stands/
│   ├── test/              # тестовый стенд (data + run_logs)
│   ├── prod/              # прод-стенд
│   └── releases/          # манифесты релизов
├── sql/
├── src/
├── dags/                  # Airflow (позже)
├── dbt/                   # dbt (позже)
├── configs/envs/          # test.yml / prod.yml
└── scripts/               # generate, bootstrap, release
```

## Быстрый старт (неделя 1)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python scripts/bootstrap_stands.py
python scripts/generate_raw_data.py

# Открыть визуальную панель
streamlit run apps/ops_console/app.py

# Затем: tasks/CURRENT_SPRINT.md
```

## Роли в симуляции

- **Ты** — Junior → Middle Data Engineer команды DWH  
- **AI в Cursor** — тимлид / ментор / code reviewer  
- **«Бизнес»** — кредитный департамент АПК, риск, отчётность

## Важно

Это **учебный** проект. Названия и процессы вдохновлены банком, но данные синтетические. Не используй реальные ПДн клиентов.
