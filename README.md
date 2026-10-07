# Tutor CRM Backend

Backend для CRM-системы репетиторов: ученики, расписание, абонементы и журнал занятий.

## Возможности

- JWT-аутентификация (access + refresh токены)
- Управление учениками
- Постоянное расписание занятий
- Абонементы
- Журнал занятий
- Автогенерируемая документация API (Swagger / ReDoc)

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (async, asyncpg)
- PostgreSQL
- Alembic
- Pytest, GitHub Actions (CI)
- Docker, Docker Compose

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/KuznetcovV/fullstack_app_tutor.git
cd fullstack_app_tutor
```

### 2. Создать `.env`

```bash
cp .env.example .env
```

### 3. Заполнить `.env`

Пример:

```env
POSTGRES_DB=fastapi_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/fastapi_db

SECRET_KEY=сюда_случайную_длинную_строку
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

DEBUG=True
FRONTEND_URL=http://localhost:5173
TIMEZONE=Europe/Moscow
```

`SECRET_KEY` можно сгенерировать так:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Запустить

```bash
docker compose up --build
```

После запуска доступны:

- Swagger: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Переменные окружения

| Переменная | Обязательна | Описание |
|---|---|---|
| `POSTGRES_DB` | да (Docker) | Имя создаваемой базы данных |
| `POSTGRES_USER` | да (Docker) | Пользователь БД |
| `POSTGRES_PASSWORD` | да (Docker) | Пароль пользователя БД |
| `DATABASE_URL` | да | Строка подключения к PostgreSQL |
| `SECRET_KEY` | да | Ключ для подписи JWT |
| `FRONTEND_URL` | да | URL фронтенда, которому разрешён доступ к API (CORS) |
| `ALGORITHM` | нет (`HS256`) | Алгоритм подписи JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | нет (`30`) | Время жизни access-токена, минуты |
| `REFRESH_TOKEN_EXPIRE_DAYS` | нет (`30`) | Время жизни refresh-токена, дни |
| `DEBUG` | нет (`false`) | Режим отладки. В продакшене должен быть `False` |
| `TIMEZONE` | нет (`Europe/Moscow`) | Часовой пояс для работы с датой и временем |
| `TEST_DATABASE_URL` | только для тестов | Подключение к **отдельной** тестовой БД, см. ниже |

## Тесты

Тесты запускаются на отдельной базе данных. Её адрес задаётся в `TEST_DATABASE_URL`
и **обязан отличаться** от `DATABASE_URL`: при совпадении тесты откажутся запускаться,
чтобы случайно не затронуть рабочие данные. Для запуска самого приложения эта переменная не нужна.

1. Поднять тестовую БД (например, в Docker):

   ```bash
   docker run --name tutor-test-db \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=fastapi_test_db \
     -p 5433:5432 -d postgres:16
   ```

2. Добавить в `.env`:

   ```env
   TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/fastapi_test_db?ssl=disable
   ```

3. Запустить:

   ```bash
   pytest
   ```

Тесты также автоматически запускаются в GitHub Actions при каждом pull request
и при пуше в `main`.

## Seed-данные

При старте контейнера в базу добавляются тестовые данные: пользователи, ученики,
расписание, абонементы и журналы занятий (см. `app/scripts/seeds/`).

> Seed создаёт пользователей с заранее известными паролями. Это удобно для разработки,
> но в продакшене сид нужно отключить или сменить учётные данные.