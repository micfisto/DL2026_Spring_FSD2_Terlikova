# GeoQuiz — географическая викторина

Веб-приложение для проверки знаний географии. Игроку предлагается отмечать на карте столицы государств, страны или достопримечательности и получать баллы за точность.

## Возможности

- **Три режима игры:** столицы, страны, достопримечательности
- **Три уровня сложности:** лёгкий, средний, сложный
- **Интерактивная карта:** выбор ответа кликом по карте (Leaflet)
- **Система очков:** начисление баллов зависит от точности ответа
- **Таблица рейтинга:** сохранение и отображение лучших результатов
- **Админ-панель:** управление вопросами (добавление, редактирование, удаление)
- **Docker-контейнеризация:** запуск всего проекта одной командой

## Технологический стек

| Компонент | Технологии |
|----------|------------|
| Frontend | React, Vite, Leaflet (react-leaflet), CSS Modules |
| Backend | Python, FastAPI, SQLAlchemy |
| База данных | PostgreSQL (локально через Docker или Supabase) |
| Контейнеризация | Docker, Docker Compose |
| Миграции | Alembic |

## Требования

- [Docker](https://www.docker.com/) и Docker Compose
- [Node.js](https://nodejs.org/) (опционально, для локальной разработки frontend)
- [Python 3.11+](https://www.python.org/) (опционально, для локальной разработки backend)

## Быстрый старт

### Запуск через Docker Compose

```bash
# Клонирование репозитория
git clone <repository-url>
cd TraineeShip_12devs

# Запуск всех сервисов
docker-compose up --build
```

После запуска:
- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **Документация API:** http://localhost:8000/docs

### Локальная разработка

#### Backend

```bash
cd backend

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev
```

## Структура проекта

```
TraineeShip_12devs/
├── backend/                # Python backend (FastAPI)
│   ├── app/
│   │   ├── models/         # Модели SQLAlchemy
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   └── utils/          # Утилиты
│   ├── alembic/            # Миграции БД
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # React приложение
│   ├── src/
│   │   ├── api/           # API клиент
│   │   ├── components/    # React компоненты
│   │   ├── hooks/        # Кастомные хуки
│   │   ├── pages/        # Страницы
│   │   ├── store/        # Zustand хранилище
│   │   └── styles/       # Глобальные стили
│   ├── Dockerfile
│   └── package.json
│
├── docs/                   # Документация
│   └── design.md          # Технический дизайн
│
├── docker-compose.yml      # Конфигурация Docker Compose
└── README.md              # Этот файл
```

## Конфигурация

### Переменные окружения (Backend)

Создайте файл `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/geoquiz
```

### Переменные окружения (Frontend)

Создайте файл `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Админ-панель

Для доступа к админ-панели используйте учётные данные:

- **URL:** `/admin`
- **Логин:** `admin`
- **Пароль:** `admin123`

> **Внимание:** Рекомендуется изменить пароль в продакшене.

## API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/game/start` | Начало новой игры |
| GET | `/api/game/{sessionId}/question` | Получение текущего вопроса |
| POST | `/api/game/{sessionId}/answer` | Отправка ответа |
| GET | `/api/game/{sessionId}/next` | Следующий вопрос |
| POST | `/api/game/{sessionId}/finish` | Завершение игры |
| GET | `/api/game/{sessionId}/result` | Получение итогов |
| POST | `/api/leaderboard` | Сохранение результата |
| GET | `/api/leaderboard` | Получение таблицы рейтинга |

Полная документация API доступна по адресу `/docs` после запуска backend.

## Миграции базы данных

```bash
# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## Лицензия

MIT License