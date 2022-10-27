import json
import time
import ecdsa
import base64
import requests
import wallet_config

def check_transactions():
    """В скором времени функция будет удалена
    """
    res = requests.get(wallet_config.MINER_NODE_URL+'/blocks')
    print(res.text)

def check_balance(wallet_to_check):
    """Функция используется для получения баланса кошелька
    с помощью explorer блокчейна
    """
    data = {"wallet": wallet_to_check}
    req = requests.get(wallet_config.EXPLORER_URL + '/wallet_balance', json=data)
    print(f'Баланс кошелька {wallet_to_check}: ' + str(json.loads(req.text)[wallet_to_check]))

def sign_ECDSA_msg(private_key, addr_from, addr_to, amount, message_send, timestamp):
    """Функция, подписывающая транзакции для блокчейна
    """
    #get timestamp, round it, make it string and encode it to bytes
    message=str(timestamp)+'|||'+str(addr_from)+'|||'+str(addr_to)+'|||'+str(amount)+'|||'+str(message_send)
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature,message

def send_transaction(timestamp, addr_from,private_key,addr_to,amount, message):
    """Функция, формирующая запрос к блокчейну для добавления новой транзакции
    Так же отправляет эту транзакцию на сервер
    """

    if len(private_key) == 64:
        signature,sig_message = sign_ECDSA_msg(private_key, addr_from, addr_to, amount, message, timestamp)
        url     = wallet_config.MINER_NODE_URL+'/txion'
        payload = {"source": "wallet","option":"newtx", "datetime": timestamp, "from_address": addr_from, "to_address": addr_to, "amount": amount, "signature": signature.decode(), "msig_essage": sig_message, "message": message}
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print("Не верный адресс или ключ, перепроверьте данные!!!")