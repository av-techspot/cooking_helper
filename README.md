# Cooking helper

Проект доступен по ссылке https://kittyg.3utilities.com/

Cooking helper - сайт любителей вкусных блюд. Вы можете делиться своими любимыми рецептами, добавлять в избранное рецепты других пользователей, формировать список покупок, необходимый для выбранных вами рецептов.

#### Требования

- Python (версия ^3.9)
- Django (версия ^4.0)
- Node.js
- npm (устанавливается вместе с Node.js)
- Gunicorn
- Nginx

#### Установка и настройка Django Api

Клонируйте репозиторий проекта:
```
$ git clone git@github.com:av-techspot/cooking_helper.git
$ cd cooking_helper
```
Создайте и активируйте виртуальное окружение
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Установите зависимости
```
$ python -m pip install -r requirements.txt
```
Из директории с файлом manage.py: примените миграции и запустите сервер
```
$ python manage.py migrate
$ python manage.py runserver
```

### Установка и настройка React

Находясь в директории cooking_helper/frontend, установите зависимости
```
$ npm install
```
Разверните frontend
```
$ nmp start
```

Автор: Андрей Васильев
