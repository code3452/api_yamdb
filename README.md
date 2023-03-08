# api_yamdb
api_yamdb
## Описание:
api_yamdb - это REST API для платформы YaMDb. Cобирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Ostashev/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

```
source venv/bin/activate 
```

Установить зависимости из файла requirements.txt:

```
python3.9 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в директорию api_yamdb:

```
cd api_yamdb
```

Выполнить миграции:

```
python3.9 manage.py migrate
```

Запустить проект:

```
python3.9 manage.py runserver
```
## Примеры запросов:
### Создание пользователя:
```
 [POST].../api/v1/users/
{

    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"

}
```
### Ответ:
```
{

    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"

}
```

### Регистрация пользователя:
```
 [POST].../api/v1/auth/signup/
{

    "email": "user@example.com",
    "username": "string"

}
```
### Ответ:
```
{

    "email": "string",
    "username": "string"

}
```

### Получение JWT-токена:
```
 [POST].../api/v1/auth/token/
{

    "username": "string",
    "confirmation_code": "string"

}
```
### Ответ:
```
{

    "token": "string"

}
```
### Получение списка всех категорий:
```
 [GET].../api/v1/categories/
```

### Ответ:
```
{

    "count": 0,
    "next": "string",
    "previous": "string",
    "results": 

[

        {}
    ]

}
```
### Добавление новой категории:
```
    [POST].../api/v1/categories/
{

    "name": "string",
    "slug": "string"

}
```
### Ответ:
```
{

    "name": "string",
    "slug": "string"

}
```


### Подробная документация в формате ReDoc доступна по адресу .../redoc/
