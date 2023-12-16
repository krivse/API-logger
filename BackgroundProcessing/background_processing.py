import json
import os
import random
import time
import logging
import requests
from dotenv import load_dotenv
import fcntl

load_dotenv()


logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname) 5s/%(asctime)s %(filename)s %(lineno)d] %(name)s: %(message)s]',
    )


def save_data(data):
    """Запись данных в файл."""
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/logs/log.json"

    # Открываем файл в режиме блокировки
    # file_lock = open(file_path, 'a')
    # fcntl.flock(file_lock, fcntl.LOCK_EX)
    # Проверяем, существует ли файл
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Открываем существующий файл и считываем данные
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    else:
        # Создаем пустой список для данных, если файл не существует
        json_data = []
    # Добавляем новую запись в список с данными
    json_data.append(data[0])
    # Записываем данные в файл
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
        # Снимаем блокировку с файла и закрываем его
        # fcntl.flock(file_lock, fcntl.LOCK_UN)
        # file_lock.close()


def data_request():
    """Получение данных с WebApi сервиса."""
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    try:
        with requests.get(f'http://{host}:{port}/api/data/') as response:
            # Проверка статуса ответа
            if response.status_code == 200:
                data = response.json()
                if data:
                    save_data(data)
    except requests.exceptions.ConnectionError:
        logging.error(f'Не удалось установить соединение c cервером {host}:{port}')
        # Задержка для повторного подключения
        time.sleep(10)


def main():
    m = int(os.getenv('REQUEST_DELAY_MS'))
    while True:
        data_request()
        delay = random.randint(0, m // 1000)  # Перевод задержки из миллисекунд в секунды
        time.sleep(delay)  # Задержка между запросами


if __name__ == '__main__':
    try:
        logging.info('Программа запущена')
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error('Программа остановлена')
