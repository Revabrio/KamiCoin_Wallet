import time
import json
import hashlib
import requests
import wallet_config

def get_work(user_iden):
    data = {"userIdentificator": user_iden, "minerName": wallet_config.MINER_NAME, "minerType": "PC"}
    req = requests.get(wallet_config.MINER_NODE_URL+'/getWork', json=data)
    return json.loads(req.text)

def work(work_data):
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
    data = {"userIdentificator": user_iden, "minerName": wallet_config.MINER_NAME, "minerType": "PC", "number": num,
            "hashrate": hashrate}
    req = requests.post(wallet_config.MINER_NODE_URL+'/checkWork', json=data)
    return json.loads(req.text)

def start_mining(user_iden):
    print('Start mining')
    num_succ_works = 0
    while True:
        print('Get work')
        work_data = get_work(user_iden)
        try:
            time_start = time.time()
            print(f'New work #{num_succ_works}')
            answer = work(work_data)
            print(f'Answer {answer} for work #{num_succ_works}')
            time_found = int((time.time()-time_start))
            hashrate = str((time_found * 1666) / 100)
            checked_work = check_work(answer, user_iden, hashrate)
            try:
                if int(checked_work['success']) == 1:
                    print(f'Work #{num_succ_works} was succesfully checked!')
                    print(f'speed - {hashrate} KH\s')
                    num_succ_works += 1
            except:
                print('Max coins was granted, wait another hour')
                time.sleep(60)
        except:
            print('Max coins was granted, wait another hour')
            time.sleep(60)