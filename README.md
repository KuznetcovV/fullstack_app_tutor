# Tutor CRM Backend
Backend для CRM-системы репетиторов.

# Возможности
* JWT-аутентификация
* Управление учениками
* Управление расписанием
* Абонементы
* Журнал занятий
* Swagger/OpenAPI

# Стек
* Python 3.13
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Docker
* Docker Compose

# Запуск
## 1. Клонировать репозиторий
git clone https://github.com/KuznetcovV/fullstack_app_tutor.git

## 2. Создать .env
cp .env.example .env

## 3. Заполнить .env
Пример:  
POSTGRES_DB=fastapi_db  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=postgres  
  
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/fastapi_db  
  
SECRET_KEY=сюда_случайную_длинную_строку  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
REFRESH_TOKEN_EXPIRE_DAYS=30  

## 4. Сгенерировать SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"  
  
или  
  
import secrets  
  
print(secrets.token_hex(32))  

## 5. Запуск
docker compose up --build  
  
## Документация API  
### Swagger  
http://localhost:8000/docs  
### ReDoc  
http://localhost:8000/redoc  
  
## Seed-данные
* пользователи;
* ученики;
* расписание;
* абонементы;
* журналы занятий.

## Переменные окружения  
Название создаваемой базы данных: POSTGRES_DB  
Имя юзера при создании бд: POSTGRES_USER  
Пароль для подключения к бд: POSTGRES_PASSWORD  
Подключение к PostgreSQL: DATABASE_URL  
Ключ для подписи JWT: SECRET_KEY  
Время жизни Access Token в минутах: ACCESS_TOKEN_EXPIRE_MINUTES  
Время жизни Refresh Token в днях: REFRESH_TOKEN_EXPIRE_MINUTES  
  
## Документация
Полная документация находится в Confluence:  
