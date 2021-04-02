# Foodgram

Онлайн сервис где люди могут делиться рецептами, подписываться на других пользователей, добавлять рецепты в список избранного и список покупок.

Это выпускной проект программы Яндекс.Практикума Python-разработчик.
### Installing

Проект использует:
- django - https://www.djangoproject.com
- django REST framework - https://www.django-rest-framework.org
- Docker - https://www.docker.com/products/docker-desktop
- docker-compose - https://docs.docker.com/compose/
- PostgreSQL - https://www.postgresql.org
- nginx - https://nginx.org/ru/

### Чтобы запустить проект необходимо:

Запустить docker-compose:

    'sudo docker-compose up -d'

Далее нужно найти id контейнера:

    'sudo docker container ls'

Затем заходим в контейнер:

    'docker-compose exec -it <id> bash'

Миграции:

    'python manage.py migrate'
    
Загруказ тестовых данных:

    'python manage.py loaddata fixtures.json'
    
Создаем супер пользователя:    
    
    'python manage.py createsuperuser'

И собираем статику:

    'python manage.py collectstatic'




