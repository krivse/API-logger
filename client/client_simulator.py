from typing import AnyStr, List
from http.client import responses
import requests
import random
import time
import os
import logging
import multiprocessing
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname) 5s/%(asctime)s %(filename)s %(lineno)d] %(name)s: %(message)s]',
    )


def generate_ip_address() -> AnyStr:
    """Генерация случайного IP-адреса."""
    ip_address = []
    for _ in range(4):
        # Завышен диапазон для передачи некорректного запроса
        octet = random.randint(0, 270)
        ip_address.append(str(octet))

    return ".".join(ip_address)


def generate_http_method() -> AnyStr:
    """Генерация случайного HTTP метода."""
    # Добавлены несуществующие типы запросов для передачи некорректного запроса
    http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'HEAR', 'PAST']

    return random.choice(http_methods)


def generate_uri() -> AnyStr:
    """Генерация случайного URI."""
    # Создание Экземпляр класса Faker для создания случайных uri
    fake = Faker()

    return fake.uri()


def generate_http_status_code(http_statuses: List) -> AnyStr:
    """Генерация случайного HTTP статус кода."""
    if not http_statuses:
        # Запрос на получение списка http статусов
        for status in responses:
            http_statuses.append(str(status))
        # Добавлены несуществующие статусы запросов для передачи некорректного запроса
        incorrectly_status = ['600', '700', '800', '900', '1000']
        http_statuses.extend(incorrectly_status)

    return random.choice(http_statuses)


def generate_request(http_statuses) -> AnyStr:
    """
    Генерация случайного текста для запроса вида
    'ip-address http method uri http status code'.
    """
    ip_address = generate_ip_address()
    http_method = generate_http_method()
    uri = generate_uri()
    http_status_code = generate_http_status_code(http_statuses)

    text = f'{ip_address} {http_method} {uri} {http_status_code}'

    # Запись текста запроса в файл
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/logs/valid_text.txt', 'a') as file:
        file.write(text + '\n')

    return text


def send_request(request_text):
    """POST запрос на веб-сервис."""
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    try:
        with requests.post(f'http://{host}:{port}/api/data/', json={'log': request_text}) as response:
            # Проверка статуса ответа
            if response.status_code == 418:
                # Запись неправильного текста в файл
                with open(f'{os.path.dirname(os.path.abspath(__file__))}/logs/invalid_text.txt', 'a') as file:
                    file.write(request_text + '\n')
    except requests.exceptions.ConnectionError:
        logging.error(f'Не удалось установить соединение c cервером {host}:{port}')
        # Задержка для повторного подключения
        time.sleep(10)


def worker():
    logging.info(f'Process {multiprocessing.current_process().name}')
    m = int(os.getenv('DELAY_MS'))  # Задержка между запросами в миллисекундах
    http_statuses = []  # Создаём глобальную переменную для хранения HTTP-статусов
    while True:
        request_text = generate_request(http_statuses)
        send_request(request_text)
        delay = random.randint(0, m // 1000)  # Перевод задержки из миллисекунд в секунды
        time.sleep(delay)  # Задержка между запросами


def main():
    try:
        n = int(os.getenv('PROCESS_COUNT'))  # Количество процессов
        procs = []

        for _ in range(n):
            # Создание и запуск процессов
            process = multiprocessing.Process(target=worker, daemon=True)
            procs.append(process)
            process.start()
        [proc.join() for proc in procs]
    except ValueError as err:
        logging.error(err)


if __name__ == "__main__":
    try:
        logging.info('Программа запущена')
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error('Программа остановлена')
