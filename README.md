# LR4

Лабораторная работа №4: бэкенд на FastAPI с хранением данных в MongoDB через асинхронный драйвер Motor.

## Стек

- Python 3.12
- FastAPI
- MongoDB 7.0
- Motor (асинхронный драйвер MongoDB)
- Pydantic v2
- Docker / Docker Compose

## Структура проекта
```
lr4-noSQL/
├── app/
│ ├── init.py
│ ├── main.py # эндпоинты FastAPI (async def)
│ ├── schemas.py # Pydantic-модели
│ └── database.py # подключение к MongoDB, get_collection()
├── requirements.txt
├── Dockerfile
├── docker-compose.yml # api + mongodb
├── .gitignore
└── README.md
```

## Эндпоинты

| Метод | Путь | Описание | Коды ответа |
|---|---|---|---|
| POST | `/students` | Создать студента | 201, 400, 422 |
| GET | `/students` | Список всех студентов | 200 |
| GET | `/students/{id}` | Студент по id (ObjectId-строка) | 200, 400, 404 |
| PUT | `/students/{id}` | Изменить имя студента | 200, 400, 404, 422 |
| DELETE | `/students/{id}` | Удалить студента | 204, 400, 404 |

Swagger UI: `http://localhost:8000/docs`

## Модель данных

База `students_db`, коллекция `students`. Документ создаётся автоматически при первой вставке.

| Поле | Тип BSON | Ограничения | Описание |
|---|---|---|---|
| `_id` | ObjectId | PRIMARY KEY, генерируется автоматически | Идентификатор документа |
| `name` | String | 1–100 символов (Pydantic) | ФИО студента |
| `email` | String | валидный email, уникальный (проверка в коде) | Электронная почта |

Пример запроса POST:

```json
{ "name": "Ivan", "email": "ivan@example.com" }
```
Пример ответа (201):

```json
{ "id": "674a1f2e3b4c5d6e7f8a9b0c", "name": "Ivan", "email": "ivan@example.com" }
```
В API поле _id сериализуется как id — 24-символьная hex-строка ObjectId.

Переменные окружения
Переменная	По умолчанию	Описание
MONGO_URL	mongodb://localhost:27017	Строка подключения к MongoDB
Запуск локально
Нужна запущенная MongoDB на localhost:27017 (например, docker run -d -p 27017:27017 --name mongo mongo:7.0).

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\Activate.ps1       # Windows PowerShell
```
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Запуск в Docker (рекомендуется)
bash
docker compose up --build
Compose поднимет два контейнера: mongodb (порт 27017, volume mongo_data) и api (порт 8000, MONGO_URL=mongodb://mongodb:27017).

Открыть: http://localhost:8000/docs
