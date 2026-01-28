Movie Search API

REST API для поиска информации о фильмах с использованием OMDb API и локального кэширования в PostgreSQL.

Содержание

- [Архитектура проекта](#архитектура-проекта)
- [Технологический стек](#технологический-стек)
- [Структура проекта](#структура-проекта)
- [Установка и запуск](#установка-и-запуск)
- [API Endpoints](#api-endpoints)
- [Примеры запросов](#примеры-запросов)

Архитектура проекта

Проект построен на основе Clean Architecture и разделен на несколько слоев:

1. Domain Layer** (Доменный слой)
Расположение: `src/domain/`

Содержит бизнес-сущности (entities) - чистые Python классы без зависимостей от фреймворков или БД. Это ядро бизнес-логики приложения.

- `entities/movie_entity.py` - сущность фильма
- `entities/request_log_entity.py` - сущность лога запроса

Принцип: Domain layer не зависит ни от каких других слоев.

2. App Layer (Слой приложения)
Расположение:** `src/app_layer/`

Содержит бизнес-логику приложения и определяет интерфейсы для взаимодействия с внешними системами.

Компоненты:
- Use Cases (`use_cases/`) - бизнес-логика приложения
  - `movie_service.py` - сервис для работы с фильмами
  - `request_logs_service.py` - сервис для работы с логами запросов

- DTOs (`dto/`) - Data Transfer Objects для передачи данных между слоями
  - `movie_dto.py` - DTO для фильмов
  - `request_logs_dto.py` - DTO для логов

- Interfaces** (`interfaces/`) - абстрактные интерфейсы (ABC)
  - `muvie_repository.py` - интерфейс репозитория фильмов
  - `clients.py` - интерфейс внешнего клиента (OMDb)
  - `request_logs_repository.py` - интерфейс репозитория логов

Принцип: App layer зависит только от Domain layer и определяет контракты для Infrastructure layer.

3. infrastructure Layer (Инфраструктурный слой)
Расположение: `src/infra/`

Содержит реализации интерфейсов из App layer и работу с внешними системами.

Компоненты:
- Repositories (`repositories/`) - реализация репозиториев для работы с БД
  - `movie_repository.py` - реализация репозитория фильмов
  - `request_log_repository.py` - реализация репозитория логов

- Clients (`clients/`) - клиенты для внешних API
  - `omdb_client.py` - клиент для OMDb API

- Database (`db/`) - модели БД и настройка сессий
  - `models/` - SQLAlchemy модели
  - `session.py` - настройка асинхронной сессии БД

Принцип: Infrastructure layer реализует интерфейсы из App layer и зависит от Domain layer.

4. API Layer (Слой API)
Расположение: `src/api/`

Содержит HTTP endpoints, схемы валидации и middleware.

Компоненты:
- Routers (`routers/`) - FastAPI роутеры
  - `movie.py` - эндпоинты для работы с фильмами

- Schemas (`schemas/`) - Pydantic схемы для валидации запросов/ответов
  - `movie_schemas.py` - схемы для фильмов
  - `request_logs_shemas.py` - схемы для логов

- Middlewares (`middlewares/`) - промежуточное ПО
  - `log_middleware.py` - middleware для логирования запросов

Принцип: API layer зависит от App layer и использует Dependency Injection для получения сервисов.

Dependency Injection

Проект использует dependency-injector для управления зависимостями. Конфигурация находится в `src/depends.py`:

- `DBContainer` - управление сессиями БД
- `RepositoryContainer` - создание репозиториев
- `GatewayContainer` - создание внешних клиентов
- `UseCaseContainer` - создание бизнес-сервисов
- `Container` - главный контейнер, объединяющий все остальные

Технологический стек

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **PostgreSQL** - база данных
- **Alembic** - миграции БД
- **Pydantic** - валидация данных и настройки
- **dependency-injector** - dependency injection
- **aiohttp** - асинхронные HTTP запросы
- **Poetry** - управление зависимостями
- **Docker** - контейнеризация

Структура проекта

```
PythonProject5/
├── src/
│   ├── api/                    # API Layer
│   │   ├── middlewares/        # Middleware
│   │   ├── routers/            # API роутеры
│   │   └── schemas/            # Pydantic схемы
│   ├── app_layer/              # App Layer
│   │   ├── dto/                # Data Transfer Objects
│   │   ├── interfaces/         # Абстрактные интерфейсы
│   │   └── use_cases/          # Бизнес-логика
│   ├── domain/                 # Domain Layer
│   │   └── entities/           # Доменные сущности
│   ├── infra/                  # Infrastructure Layer
│   │   ├── clients/            # Внешние API клиенты
│   │   ├── db/                 # Модели БД и сессии
│   │   └── repositories/       # Реализация репозиториев
│   ├── config.py               # Конфигурация приложения
│   ├── depends.py              # Dependency Injection
│   └── main.py                 # Точка входа
├── migrations/                 # Alembic миграции
├── docker-compose.yaml         # Docker Compose конфигурация
├── Dockerfile                  # Docker образ
├── entrypoint.sh              # Скрипт запуска
├── pyproject.toml             # Poetry конфигурация
└── README.md                   # Этот файл
```

## Установка и запуск

Предварительные требования

- Python 3.13+
- Poetry
- Docker и Docker Compose (для запуска через Docker)
- PostgreSQL (если запускаете локально без Docker)

Вариант 1: Запуск через Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd PythonProject5
```

2. **Создайте файл `.env` в корне проекта:**
```env
PostgreSQL настройки
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=movies_db

OMDb API ключ (получите на https://www.omdbapi.com/apikey.aspx)
OMDB_API_KEY=your_api_key_here

# Настройки приложения
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false
```

3. **Запустите проект:**
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Вариант 2: Локальный запуск

1. **Установите зависимости:**
```bash
poetry install
```

2. **Создайте файл `.env`** (см. пример выше, но измените `POSTGRES_HOST` на `localhost`)

3. **Настройте PostgreSQL** и создайте базу данных

4. **Примените миграции:**
```bash
poetry run alembic upgrade head
```

5. **Запустите приложение:**
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

API Endpoints

Health Check
```
GET /ht/
```
Проверка работоспособности сервиса.

Поиск фильма по названию
```
GET /api/v1/movies/search?title={название}
```
Ищет фильм сначала в локальной БД, если не найден - запрашивает OMDb API и сохраняет результат.

**Параметры:**
- `title` (обязательный) - название фильма (1-250 символов)

### Получить список фильмов
```
GET /api/v1/movies/?skip={skip}&limit={limit}
```
Возвращает список фильмов из локальной БД с пагинацией.

**Параметры:**
- `skip` (опционально, по умолчанию 0) - количество пропущенных записей
- `limit` (опционально, по умолчанию 10) - количество записей на странице

### Получить фильм по IMDB ID
```
GET /api/v1/movies/{imdb_id}
```
Возвращает фильм по его IMDB ID из локальной БД.

**Параметры:**
- `imdb_id` (обязательный) - IMDB ID фильма (например, "tt0133093")

## Примеры запросов

### Пример 1: Поиск фильма
```bash
curl "http://localhost:8000/api/v1/movies/search?title=The%20Matrix"
```

**Ответ:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "The Matrix",
  "imdb_id": "tt0133093",
  "type": "movie",
  "year": "1999",
  "poster": "https://example.com/poster.jpg",
  "created_at": "2024-01-01T12:00:00"
}
```

### Пример 2: Получить список фильмов
```bash
curl "http://localhost:8000/api/v1/movies/?skip=0&limit=5"
```

**Ответ:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "The Matrix",
    "imdb_id": "tt0133093",
    "type": "movie",
    "year": "1999",
    "poster": "https://example.com/poster.jpg",
    "created_at": "2024-01-01T12:00:00"
  },
  "..."
]
```

### Пример 3: Получить фильм по IMDB ID
```bash
curl "http://localhost:8000/api/v1/movies/tt0133093"
```

**Ответ:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "The Matrix",
  "imdb_id": "tt0133093",
  "type": "movie",
  "year": "1999",
  "poster": "https://example.com/poster.jpg",
  "created_at": "2024-01-01T12:00:00"
}
```

### Пример 4: Health Check
```bash
curl "http://localhost:8000/ht/"
```

**Ответ:**
```json
{
  "status": "OK"
}
```

### Примеры с использованием Python (requests)
```python
import requests

BASE_URL = "http://localhost:8000"

# Поиск фильма
response = requests.get(f"{BASE_URL}/api/v1/movies/search", params={"title": "Inception"})
movie = response.json()
print(movie)

# Список фильмов
response = requests.get(f"{BASE_URL}/api/v1/movies/", params={"skip": 0, "limit": 10})
movies = response.json()
print(movies)

# Фильм по IMDB ID
response = requests.get(f"{BASE_URL}/api/v1/movies/tt1375666")
movie = response.json()
print(movie)
```
## Поток данных

1. **Запрос приходит** в API Layer (роутер)
2. **Роутер** использует Dependency Injection для получения сервиса из App Layer
3. **Сервис** (Use Case) выполняет бизнес-логику:
   - Проверяет наличие фильма в БД через Repository
   - Если не найден - запрашивает через External Client (OMDb)
   - Сохраняет результат в БД через Repository
4. **Repository** конвертирует Entity в Model и работает с БД
5. **Сервис** конвертирует Entity в DTO
6. **Роутер** конвертирует DTO в Schema и возвращает ответ

## Миграции БД

Для создания новой миграции:
```bash
poetry run alembic revision --autogenerate -m "описание изменений"
```

Для применения миграций:
```bash
poetry run alembic upgrade head
```

Для отката миграции:
```bash
poetry run alembic downgrade -1
```

## Переменные окружения

Все настройки приложения управляются через переменные окружения:

- `POSTGRES_HOST` - хост PostgreSQL
- `POSTGRES_PORT` - порт PostgreSQL
- `POSTGRES_USER` - пользователь PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `POSTGRES_DB` - название базы данных
- `OMDB_API_KEY` - API ключ для OMDb
- `APP_HOST` - хост приложения
- `APP_PORT` - порт приложения
- `APP_DEBUG` - режим отладки (true/false)

## Дополнительная информация

- API документация доступна по адресу: `http://localhost:8000/docs` (Swagger UI)
- Альтернативная документация: `http://localhost:8000/redoc` (ReDoc)
- Все запросы логируются через `RequestLogMiddleware`


