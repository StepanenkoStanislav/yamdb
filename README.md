
# Проект YAMDB

## Описание проекта
Проект YaMDb собирает отзывы пользователей на произведения. 

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или 
послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Например, в категории «Книги» могут быть произведения «Винни-Пух и 
все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» 
группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен 
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, 
«Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые 
отзывы и ставят произведению оценку в диапазоне от одного до десяти 
(целое число); из пользовательских оценок формируется усреднённая оценка 
произведения — рейтинг (целое число). На одно произведение пользователь может 
оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только 
аутентифицированные пользователи.

## Установка
В директории yamdb/infra необходимо создать файл .env (пример находится в yamdb/infra/example.env), где необходимо указать:
```python
DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql
DB_NAME=postgres - имя базы данных
POSTGRES_USER=postgres - логин для подключения к базе данных
POSTGRES_PASSWORD=postgres - пароль для подключения к БД
DB_HOST=db - название сервиса (контейнера)
DB_PORT=5432 - порт для подключения к БД 
SECRET_KEY=secret_key - SECRET_KEY из settings.py
```

Запуск проекта
```python
# В директории yamdb/infra
docker-compose up --build
docker-compose exec web python manage.py migrate
```

Создание суперпользователя
```python
docker-compose exec web python manage.py createsuperuser
```

Загрузка тестовых данных
```python
docker-compose exec web python manage.py loaddata fixtures.json
```

Собрать статические файлы
```python
docker-compose exec web python manage.py collectstatic
```

Описание [ендпоинтов API](http://158.160.100.47/redoc/)

## Технологии

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="python" alt="python" width="40" height="40"/>&nbsp
  <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg" title="django" alt="django" width="40" height="40"/>&nbsp
  <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="docker" alt="docker" width="40" height="40"/>&nbsp
  <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg" title="postgresql" alt="postgresql" width="40" height="40"/>&nbsp
</div>

В проекте используются следующие технологии:
- python 3.7
- Django 3.2
- DjangoRestFramework 3.12.4
- PyJWT 2.1.0
- Postgresql 13.0-alpine
- Docker 20.10.24


## Авторы
- [Александров Роман](https://t.me/gnome_black) - Тимлидер, работа с отзывами, комментариями
- [Степаненко Станислав](https://t.me/tme_zoom) - Работа с произведениями, жанрами, категориями
- [Гнётов Захар](https://t.me/sp1edh4ck) - Работа с пользователями, аутентификация
