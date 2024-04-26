# Docker

## Stop and delete all containers/images
sudo docker stop `sudo docker ps -a -q` && sudo docker rm `sudo docker ps -a -q` && sudo docker rmi `sudo docker images -q`

## Run container
sudo docker compose run bizint_web

## Delete all volumes with name <name>
sudo docker volume ls | cut -d' ' -f6 | grep <name> | xargs sudo docker volume rm {}

## Run containers from other compose file
sudo docker compose -f docker-compose.prod.yml up 

# Setup

## DB
### Run migrate
sudo docker exec bizint_web python manage.py migrate --noinput

### Load static files in prod
sudo docker exec bizint_web python manage.py collectstatic

### Flush DB
sudo docker exec bizint_web python manage.py flush --no-input

# Django

### Create superuser
sudo docker exec -it bizint_web python manage.py createsuperuser

