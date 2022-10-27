#!/usr/bin/env python3

"""
Данная программа разработана для KamiCoin (Kami) - централизированного блокчейна

На данный момент данная программа исполняет функции:

1. Генератора кошельков.
2. Просмотр баланса кошелька.
3. Создание и отправка транзакций в блокчейн.
4. Майнинг монет.

Генерация кошельков, в KamiCoin выполнена с помощью seed-фраз для легкого восстановления кошелька
при утере его ключей.

Для "основы" был взят SimpleCoin:
https://github.com/Scotchmann/SimpleCoin
"""

import os
import time
import json
import aes_module
import wallet_config
import wallet_generator
import mining_module
import blockchain_module

def welcome_msg():
      print("""===================================\n
            KamiCoin Wallet - Кошелек для KamiCoin\n
            ============================================================================\n\n
            Репозиторий сервера для KamiCoin: https://github.com/Revabrio/KamiCoin\n
            Репозиторий кошелька KamiCoin: https://github.com/Revabrio/KamiCoin_Wallet\n
            Репозиторий explorer KamiCoin: https://github.com/Revabrio/KamiCoin_Explorer\n
            \n\n\n""")

def wallet(public_key, private_key):
    response = False
    while True:
        while response not in ["1","2","3","5"]:
            response = input("""Что вы хотите сделать?
            1. Показать данные кошелька
            2. Проверить баланс
            3. Отправить транзакцию
            4. Проверить транзакции (не работает)
            5. Начать майнинг\n""")

        if response == "1":

            print("""====================================================\n
                     ВАЖНО: НЕ ПЕРЕДАВАЙТЕ ПРИВАТНЫЙ КЛЮЧ ПОСТОРОННИМ!!!!\n
                     ====================================================\n""")
            print(f'Ваш публичный ключ / адресс кошелька: {public_key}')
            print(f'Ваш приватный ключ: {private_key}')
            response = False

        elif response == "2":

            wallet_address = str(input('Пожалуйста, введите адресс кошелька для проверки (или n для проверки вашего): '))
            if wallet_address == 'n':
                wallet_address = public_key
            blockchain_module.check_balance(wallet_address)
            response = False

        elif response == "3":

            addr_to = input("Введите адресс кошелька получателя: ")
            amount = str(input("Введите сумму (например 0.125): "))
            message = str(input("Введите комментарий к платежу (впишите n, если не хотите добавлять комментарий): \n"))
            if message == 'n' or len(message) > 128:
                print('Вы не добавляли комментарий, или он больше 128 символов')
                message = ''
            print("=========================================\n\n")
            print("Проверьте правильность данных:\n")
            print("Получатель: {0}\nСумма: {1}\nКомментарий: {2}".format(addr_to, amount, message))
            response = input("y/n\n")
            if response.lower() == "y":
                blockchain_module.send_transaction(str(time.time()), public_key,private_key,addr_to,amount, message)
            response = False

        elif response == "4":

            blockchain_module.check_transactions()

        elif response == "5":

            mining_module.start_mining(public_key)
            response = False

if __name__ == '__main__':
    while True:
        if os.path.exists('wallet_keys'):
            password = input('Пожалуйста введите ваш пароль (или введите n что бы удалить кошелек из программы): ')
            if password != 'n':
                with open('wallet_keys', 'r') as file:
                    data = file.readlines()
                    public_key = bytes.decode(aes_module.decrypt(json.loads(data[0].replace('\n', '')), password))
                    private_key = bytes.decode(aes_module.decrypt(json.loads(data[1]), password))
                welcome_msg()
                wallet(public_key, private_key)
                input("Нажмите любую кнопку для выхода...")
            else:
                os.remove('wallet_keys')
        else:
            type_keys = input("""Что вы хотите сделать?
1. Создать новый кошелек
2. Импортировать кошелек из seed фразы\n""")
            while type_keys not in ["1", "2"]:
                type_keys = input('')
            private_key = ''
            public_key = ''
            wallet_seed = ''
            if type_keys == '1':
                wallet_seed = wallet_generator.get_seed()
                bin_seed = wallet_generator.get_bin_seed(wallet_seed)
                seed_hash = wallet_generator.get_hash_from_data(bin_seed)
                private_key, public_key = wallet_generator.generate_ECDSA_keys(seed_hash)
            elif type_keys == '2':
                print('Пожалуйста введите seed фразу (например: kami coin polish new change)')
                seed = input('Она должна состоять из 18 слов: ')
                wallet_seed = seed.split(' ')
                try:
                    bin_seed = wallet_generator.get_bin_seed(wallet_seed)
                    seed_hash = wallet_generator.get_hash_from_data(bin_seed)
                    private_key, public_key = wallet_generator.generate_ECDSA_keys(seed_hash)
                except:
                    print('Попробуйте снова!')
            if public_key != '' and private_key != '':
                password = input('Пожалуйста, введите пароль для шифрования вашего кошелька: ')
                print('-' * 30)
                print('Обязательно запомните пароль!!!')
                print('Если вы его потеряете, кошелек можно будет восстановить только с помощью seed фразы!!!!')
                print('-' * 30)
                print('Обязательно запишите seed фразу кошелька и никому её не передавайте!!!!!')
                wallet_seed_show = ''
                for word in wallet_seed:
                    wallet_seed_show += word + ' '
                print('Seed фраза: ')
                print(wallet_seed_show)
                print('-' * 30)
                show_keys = input('Пожалуйста, введите y если хотите увидить адресс кошелька и приватный ключ от него: ')
                if show_keys == 'y':
                    print(f'Ваш публичный ключ / адресс кошелька: {public_key}')
                    print(f'Ваш приватный ключ: {private_key}')
                enc_private_key = aes_module.encrypt(private_key, password)
                enc_public_key = aes_module.encrypt(public_key, password)
                with open('wallet_keys', 'w') as file:
                    file.write(json.dumps(enc_public_key))
                    file.write('\n')
                    file.write(json.dumps(enc_private_key))
                welcome_msg()
                wallet(public_key, private_key)
                input("Нажмите любую кнопку для выхода...")