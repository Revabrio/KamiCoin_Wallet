import time
import json
import hashlib
import requests
import wallet_config

def get_work(user_iden):
    """Функция, запрашивает задание у ноды блокчена
    Отправляет на ноду публичный ключ кошелька владельца майнинг-сервера.
    """
    data = {"userIdentificator": user_iden, "minerName": wallet_config.MINER_NAME, "minerType": "PC"}
    req = requests.get(wallet_config.MINER_NODE_URL+'/getWork', json=data)
    return json.loads(req.text)

def work(work_data):
    """Функция, ищущая решение задания, которое майнинг-сервер получил
    от ноды блокчейна. Перебирает числа от 0 до work_data['max'],
    добавляет к ним salt (id последнего добытого блока) и хеширует,
    проверяя сходится ли хеш, который сервер получил от ноды блокчейна.
    """
    answer = 0
    num_max = int(work_data['max'])
    hash_work = work_data['hash']
    salt_work = work_data['salt']
    for i in range(0, num_max):
        if hashlib.sha256((str(i)+salt_work).encode('utf-8')).hexdigest() == hash_work:
            answer = i
            break
    return answer

def check_work(num, user_iden, hashrate):
    """Функция, отправляет на проверку выполненное задание.
    """
    data = {"userIdentificator": user_iden, "minerName": wallet_config.MINER_NAME, "minerType": "PC", "number": num,
            "hashrate": hashrate}
    req = requests.post(wallet_config.MINER_NODE_URL+'/checkWork', json=data)
    return json.loads(req.text)

def start_mining(user_iden):
    """Главная функция майнинг-сервера. На вход принимает
    номер кошелька владельца майнинг-сервера, и далее контролирует
    работу майнинг-сервера.
    """
    print('Начинаем майнинг')
    num_succ_works = 0
    while True:
        work_data = get_work(user_iden)
        try:
            time_start = time.time()
            print(f'Новая работа #{num_succ_works}')
            answer = work(work_data)
            print(f'Нашли ответ {answer} на работу #{num_succ_works}')
            time_found = int((time.time()-time_start))
            hashrate = str((time_found * 1666) / 100)
            checked_work = check_work(answer, user_iden, hashrate)
            try:
                if int(checked_work['success']) == 1:
                    print(f'Работа #{num_succ_works} успешно проверена!')
                    print(f'скорость - {hashrate} KH\s')
                    num_succ_works += 1
            except:
                print('Максимальное количество монет было выдано, ожидаем следующий час')
                time.sleep(60)
        except:
            print('Максимальное количество монет было выдано, ожидаем следующий час')
            time.sleep(60)