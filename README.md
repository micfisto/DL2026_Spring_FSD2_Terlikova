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
|-----------|------------|
| Frontend | React, Vite, Leaflet (react-leaflet), Zustand, CSS Modules |
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| База данных | PostgreSQL |
| Контейнеризация | Docker, Docker Compose |

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
│   │   ├── hooks/         # Кастомные хуки
│   │   ├── pages/         # Страницы
│   │   ├── store/         # Zustand хранилище
│   │   └── styles/        # Глобальные стили
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

### Переменные окружения

Для локальной разработки создайте файл `.env` в корне проекта на основе `.env.example`:

```env
# База данных
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/geoquiz

# JWT секрет для админ-панели
JWT_SECRET_KEY=your-secret-key-here

# API URL для frontend
VITE_API_URL=http://localhost:8000
```

Для запуска через Docker Compose переменные окружения задаются в `docker-compose.yml` и `.env` файле в корне проекта.

## Админ-панель

Для доступа к админ-панели используйте учётные данные:

- **URL:** `/admin`
- **Логин:** `admin`
- **Пароль:** `admin123`

> **Внимание:** Рекомендуется изменить пароль в продакшене.

## API Endpoints

### Game API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/game/start` | Начало новой игры |
| GET | `/api/game/{session_id}/question` | Получение текущего вопроса |
| POST | `/api/game/{session_id}/answer` | Отправка ответа |
| GET | `/api/game/{session_id}/next` | Следующий вопрос |
| POST | `/api/game/{session_id}/finish` | Завершение игры |
| GET | `/api/game/{session_id}/result` | Получение итогов |

### Leaderboard API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/leaderboard/save` | Сохранение результата |
| GET | `/api/leaderboard?mode={mode}` | Получение таблицы рейтинга |
| GET | `/api/leaderboard/with-user?mode={mode}&user_entry_id={id}` | Рейтинг с позицией пользователя |

### Admin API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/admin/login` | Авторизация администратора |
| GET | `/api/admin/questions` | Получение всех вопросов |
| POST | `/api/admin/questions` | Создание нового вопроса |
| PUT | `/api/admin/questions/{question_id}` | Обновление вопроса |
| DELETE | `/api/admin/questions/{question_id}` | Удаление вопроса |

Полная документация API доступна по адресу http://localhost:8000/docs после запуска backend.

## Миграции базы данных

```bash
# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## 🌐 Deployment

| Платформа         | URL                                               | Описание         |
| ----------------- | ------------------------------------------------- | ---------------- |
| Frontend (Vercel) | https://dl-2026-spring-fsd-2-terlikova.vercel.app | React приложение |
| Backend (Render)  | https://dl2026-spring-fsd2-terlikova.onrender.com | FastAPI сервер   |

### Настройка переменных окружения для продакшена

Для корректной работы фронтенд должен знать URL бэкенда:

```env
VITE_API_URL=https://your-backend.onrender.com
```

## Лицензия

MIT License
