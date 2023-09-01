# Проект Foodgram
Сайт с возможностью публикации рецептов, доступен по адресу [awesome-foodgram.ru](https://awesome-foodgram.ru).

## Технологии
- Python
- Django
- Django REST framework
- JavaScript

## Запуск проекта

### Запуск из образа Docker Hub
Для запуска необходимо скачать в папку проекта файл docker-compose.production.yml и запустить его:
```
sudo docker compose -f docker-compose.production.yml up
```
Произойдет скачивание образов, создание и включение контейнеров, создание томов и сети.

### Запуск проекта из исходников GitHub
Клонируем к себе репозиторий:
```
git clone git@github.com:mogubudu/foodgram-project-react.git
```
Запускаем:
```
sudo docker compose -f docker-compose.yml up
```

### Миграции и сбор статики
```
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py migrate

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py collectstatic

sudo docker compose -f [имя-файла-docker-compose.yml] exec backend cp -r /app/collected_static/. /static/static/
```

Проект будет доступен локально по адресу [http://localhost:8080/](http://localhost:8080/)

### Наполнение сайта
1. Для того, чтобы загрузить ингредиенты в базу данных можно использовать менеджмент-команду Джанго:
```
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py load_data
```
2. Далее необходимо создать администратора:
```
sudo docker compose -f [имя-файла-docker-compose.yml] exec backend python manage.py createsuperuser
```
3. Далее переходите в админку, добавляете нужные вам теги для рецептов.

## Документация API
Документация доступна как локально, так и на опубликованом сайте по пути `api/docs/`
