# Старт сегодня (Karen)

Сегодня пятница — можно сделать лёгкий онбординг. Полноценный Sprint 1 стартует в **понедельник 2026-10-19**.

## Прямо сейчас (30–60 мин)

1. Открой `tasks/CURRENT_SPRINT.md` — это твоя Jira.
2. Прочитай `tasks/HOW_TO_WORK.md` и `docs/ENVIRONMENTS.md` (test/prod + релиз).
3. Если ещё не ставил зависимости: `pip install -r requirements.txt`
4. `python scripts/bootstrap_stands.py`
5. `python scripts/generate_raw_data.py` — данные упадут на **test**
6. Запусти визуальную панель:

```powershell
streamlit run apps/ops_console/app.py
```

В браузере увидишь стенды test/prod, файлы и логи.

## С понедельника

Каждый понедельник в чат Cursor:

```text
Понедельник — выдай спринт
```

После задачи:

```text
Ревью моей работы
```

(перед этим заполни блок в `tasks/TASK_MANAGER.md`)

## Главное правило

Не учи «курс целиком». Бери тикет → гугли/спрашивай только то, что нужно для AC → сдавай на ревью.

Работаешь в **test** → проверяешь в Ops Console → **релизишь** в prod.
