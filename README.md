# TaskFlow

Канбан-менеджер задач (мини-аналог Trello) — пет-проект для резюме.

**Стек:** React 18 + TypeScript + Vite (фронт), FastAPI + SQLAlchemy + Pydantic (бэк), PostgreSQL.

## Что демонстрирует

- React + TypeScript: компонентная архитектура, типизация API-ответов, кастомные хуки.
- Drag-and-drop карточек между колонками с сохранением порядка.
- Python REST API + JWT-аутентификация.
- SQL: связи one-to-many и many-to-many (карточки ↔ метки).

## Структура

```
backend/   FastAPI-приложение
frontend/  React + TS + Vite
```

## Запуск

### 1. База данных

```bash
docker compose up -d   # PostgreSQL на localhost:5432
```

### 2. Бэкенд

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Swagger: http://localhost:8000/docs

### 3. Фронтенд

```bash
cd frontend
npm install
npm run dev
```

http://localhost:5173

## API (кратко)

| Метод | Путь | Описание |
| --- | --- | --- |
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Логин (JWT) |
| GET/POST | `/boards` | Список / создание досок |
| POST | `/boards/{id}/columns` | Создать колонку |
| POST | `/columns/{id}/cards` | Создать карточку |
| PATCH | `/cards/{id}/move` | Переместить карточку |

## Дальнейшее развитие

- [ ] Real-time через WebSocket
- [ ] Метки и фильтры на фронте
- [ ] Дедлайны и приоритеты
