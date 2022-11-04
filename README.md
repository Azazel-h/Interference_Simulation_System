# Fabry-Perot_Interferometer

Как запустить приложение:
1. Поставить docker
2. Установить образ python командой *docker pull python*
3. Запустить run_container.sh из папки docker
Примечание: при запуске run_container.sh можно передать порт, на котором будет доступно приложение, следующим образом:
```
./run_container.sh 8080
```

Ручной запуск (из корня проекта):
```
docker build . --tag interferometer
docker run --rm -it -p 8000:8000 -v /путь/от/корня/Fabry-Perot_Interferometer:/project interferometer
```
