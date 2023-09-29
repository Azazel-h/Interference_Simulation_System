# Interference_Simulation_System

### Как развернуть приложение:
1. Поставить `docker` и `docker compose` по инструкции из официальной документации
2. Задать требуемые параметры в .env
```
# Debug/Production mode
DEBUG=True

# Deploy settings

## Port on which the Django application will run. In DEBUG mode application will be available on the given port.
DJANGO_PORT=8000

## Domain on which application will be deployed. Application will be available ONLY through given domain. WORKS ONLY IN PRODUCTION MODE!
WEB_DOMAIN=127.0.0.1
## Port on which application will be deployed. WORKS ONLY IN PRODUCTION MODE!
NGINX_PORT=8020
```
3. Запустить приложение через скрипт start.sh
```shell
$ ./start.sh
```
