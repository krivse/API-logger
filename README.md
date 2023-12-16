# LogKeeper 

### Технологии
`FastApi` `SQLAlchemy` `Pydantic` `PostgresSQL (asyncpg)` `Alembic (async)`

## Описание
```
LogKeeper - это приложение, разработанное для обработки и сохранения лог-данных, сгенерированных клиентом и полученных от сервера, на котором работает сервис web api.

Приложение состоит из трёх сервисов:
    
    Сервис клиента:
    Генерирует текстовые данные;
    Отправляет данные в формате POST-запроса на сервер, сервису №2
    Сервер успешно записывает полученные данные в виде строки "{IP address} {HTTP method} {URI} {HTTP status code}":
    Сохраняет текст запросов в файлах: valid_text.txt и invalid_text.txt

    Сервис web api:
    Асинхронный сервис, который принимает данные от сервиса клиента в формате "{IP address} {HTTP method} {URI} {HTTP status code}";
    Проводит валидацию данных;
    Записывает полученные данные в локальное хранилище PostgresSQL;
    Предоставляет возможность получить данные в формате GET-запроса сервису № 3.

    Сервис фоновой обработки:
    Регулярно обращается к сервису web api при помощи GET-запросов;
    Получает данные от сервиса web api по признаку новых данных, которые ещё не были прочитаны;
    Сохраняет полученные данные в примонтированный файл log.json для последующего использования или анализа.

Приложение "LogKeeper" обеспечивает автоматизацию процесса записи и обработки лог-данных, что помогает повысить эффективность мониторинга и анализа системных событий.
```

##### Настройка файла .env выполняется при любом выборе запуска приложения.
```angular2html
Переименовать файл myenv.env -> .env. 
Обязательные поля для заполнения:
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=my_user
    DB_PASSWORD=my_password 
    DB_HOST==Хост БД / название контейнера

    HOST=Хост сервера / название контейнера, используется в сервисе client и worker 
    PORT=Порт сервера

    PROCESS_COUNT=Количество процессов для сервиса client
    DELAY_MS=Задержка для сервиса client

    REQUEST_DELAY_MS=Задержка для фоновой обработки сервиса worker
```

#### Запуск проекта в Docker:
```
Приложение имеет настроенный рабочий файл Docker-compose.yml и запускается в 3х контейнерах:
    - postgres: базаа данных 13.0-alpine
    - web:  python 3.11, веб-сервис: fastapi
    - client: python 3.11, изменение параметра "replicas" влияет на кол-во запущенных экземпляров приложения в докере
    - worker: python 3.11
    Проброс общей папки data, в которой собраны логи (данные) со всех 3 сервисов.
```
**_Установить на сервере Docker, Docker Compose_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose

```
**_Скопировать на сервер файлы docker-compose.yml, .env. Команды выполняются из корня проекта._**
```
scp docker-compose.yml .env username@IP:/home/username/
# username - имя пользователя на сервере
# IP - публичный IP сервера
```
#### Клонировать репозиторий удобным сопособом по https / ssh, если нет готового файла на docker_hub и перейти в него в командной строке:
#### *git clone "ссылка на репозиторий"*

**_Создать и запустить контейнеры Docker_**
```angular2html
sudo docker compose up -d
```
**_Для остановки контейнеров Docker:_**
```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```


### Как запустить проект вне Docker:

#### Клонировать репозиторий и перейти в него в командной строке:

#### *git clone "ссылка на репозиторий"*

#### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
# для OS Lunix и MacOS
source venv/bin/activate

# для OS Windows
source venv/Scripts/activate
```

#### Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Миграции:
```
Выполнить миграции в директории web:
    - Предварительно расскоментировать строчки:
        # Настройка импорта для локальной работы файла, вне контейнера
        * sys.path = ['', '..'] + sys.path[1:]
        * from web import models
    - Закоменитровать:
        import models  # Настройка импорта для работы файла внутри контейнере
    - Выполнить команды:
        - alembic revision --autogenerate
        - alembic upgrade head

Запустить файлы приложений:
    web:
        - python uvicorn api:app --reload
    client:
        - python client_simulator.py
    worker:
        - python background_processing.py
```


###### Ivan Krasnikov