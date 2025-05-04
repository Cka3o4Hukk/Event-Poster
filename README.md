# Events App 🎉

<div align="center" style="display: flex; gap: 10px; justify-content: center; align-items: center;"><a href="https://www.python.org" style="text-decoration: none; border: none;"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" style="display: block;"/></a><a href="https://www.djangoproject.com" style="text-decoration: none; border: none;"><img src="https://cdn.worldvectorlogo.com/logos/django.svg" width="40" height="40" style="display: block;"/></a><a href="https://www.postgresql.org" style="text-decoration: none; border: none;"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40" style="display: block;"/></a><a href="https://www.docker.com" style="text-decoration: none; border: none;"><img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" width="40" height="40" style="display: block;"/></a><a href="https://redis.io" style="text-decoration: none; border: none;"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" width="40" height="40" style="display: block;"/></a><a href="https://docs.celeryq.dev" style="text-decoration: none; border: none;"><img src="https://docs.celeryq.dev/en/stable/_static/celery_512.png" width="40" height="40" style="display: block;"/></a><a href="https://pytest.org" style="text-decoration: none; border: none;"><img src="https://raw.githubusercontent.com/pytest-dev/pytest/main/doc/en/img/pytest_logo_curves.svg" width="40" height="40" style="display: block;"/></a></div>

<br/>

REST API приложение "Афиша мероприятий" для просмотра и бронирования событий с системой уведомлений.

## 🚀 Функциональность

- Просмотр и фильтрация событий
- Бронирование участия и отмена брони
- Система уведомлений (бронирование, отмена, напоминания)
- Оценка прошедших событий
- Теги для мероприятий
- Автоматическое обновление статусов событий

## 🛠 Технологии

- **Python 3.10+**: Основной язык программирования
- **Django 4.2+**: Web-фреймворк
- **Django REST Framework 3.14+**: REST API фреймворк
- **PostgreSQL 13+**: База данных
- **Celery 5.3+**: Асинхронные задачи
- **Redis 7.0+**: Брокер сообщений
- **Docker & Docker Compose**: Контейнеризация
- **Poetry**: Управление зависимостями

## 📋 Требования

- Docker и Docker Compose
- Make (опционально)

## 🚀 Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Cka3o4Hukk/Test-task-Event-Poster.git
cd Test-task-Event-Poster
```

2. Создайте файл .env в корневой директории:

```env
# Django
SECRET_KEY=ваш-секретный-ключ
DEBUG=True

# Database
DB_NAME=events
DB_USER=user
DB_PASSWORD=test123
DB_HOST=db
DB_PORT=5432

```

3. Запустите проект через Docker Compose:

```bash
docker-compose up --build
```

Приложение автоматически выполнит:

- Применение миграций
- Создание суперпользователя (если не существует)
- Сбор статических файлов

Данные для входа по умолчанию:

- Username: admin
- Password: admin123

## 📚 API Endpoints

### События

- `GET /api/events/` - Список всех событий
- `POST /api/events/` - Создание нового события
- `GET /api/events/{id}/` - Детали события
- `PUT/PATCH /api/events/{id}/` - Обновление события
- `DELETE /api/events/{id}/` - Удаление события
- `PATCH /api/events/{id}/update_status/` - Обновление статуса события

### Бронирования

- `GET /api/bookings/` - Список бронирований пользователя
- `POST /api/bookings/` - Создание бронирования
- `DELETE /api/bookings/{id}/cancel_booking/` - Отмена бронирования

### Оценки

- `GET /api/ratings/` - Список оценок пользователя
- `POST /api/ratings/` - Создание оценки
- `GET /api/ratings/{id}/` - Детали оценки

### Уведомления

- `GET /api/notifications/` - Список уведомлений пользователя

## 🔍 Фильтрация событий

События можно фильтровать по следующим параметрам:

- `location` - Город проведения
- `status` - Статус события
- `start_time` - Дата и время начала
- `seats` - Количество мест
- `available` - Наличие свободных мест
- `avg_rating` - Средняя оценка
- `tags` - Теги события

Пример:

```
GET /api/events/?location=Moscow&status=planned&available=true
```

## 🔄 Периодические задачи

- Отправка уведомлений о предстоящих событиях (за час до начала)
- Автоматическое обновление статусов завершенных событий (каждые 3 часа)

## 🧪 Тестирование

Запуск тестов:

```bash
docker-compose exec web pytest
```

## 📝 Структура проекта

```
events_app/
├── events_app/                  # Django-конфигурация
│   ├── __init__.py
│   ├── apps.py                  # Главный AppConfig
│   ├── asgi.py                  # ASGI-конфиг
│   ├── celery.py                # Celery-конфиг
│   ├── settings.py              # Настройки проекта
│   ├── urls.py                  # Корневые URLs проекта
│   └── wsgi.py                  # WSGI-конфиг
│
├── events/                      # Ядро приложения
│   ├── api/                     # API слой
│   │   ├── filters/             # Фильтры запросов
│   │   ├── mixins/              # DRF-миксины
│   │   ├── serializers/         # Сериализаторы
│   │   └── views/               # Представления
│   │
│   ├── domain/                  # Бизнес-логика
│   │   ├── models/              # Модели БД
│   │   ├── repositories/        # Паттерн Repository
│   │   ├── services/            # Бизнес-сервисы
│   │   └── tasks/               # Фоновые задачи
│   │
│   ├── middleware/              # Прослойки обработки запросов
│   ├── migrations/              # Миграции БД
│   ├── tests/                   # Тестирование
│   │   ├── integration/         # Интеграционные тесты
│   │   └── unit/                # Изолированные тесты
│   │
│   ├── admin.py                 # Регистрация моделей
│   ├── apps.py                  # AppConfig для приложения events
│   └── urls.py                  # Локальные URLs
│
├── static/                      # Статические файлы
│
├── .env                         # Переменные окружения
├── .gitignore                   # Игнорируемые файлы
├── Dockerfile                   # Конфигурация Docker
├── docker-compose.yml           # Оркестрация контейнеров
├── manage.py                    # Управление Django
├── pyproject.toml               # Зависимости
└── README.md                    # Документация

```

## 👥 Автор

[Alex](https://github.com/Cka3o4Hukk)
