#!/usr/bin/env python3

"""

"""

import os
import time
import json
import aes_module
import mining_module
import blockchain_module

def welcome_msg():
    print("""=========================================\n
        KamiCoin v0.1.1 - BLOCKCHAIN SYSTEM\n
        =========================================\n\n
        You can find more help for blockchain at: https://github.com/Revabrio/KamiCoin\n
        You can find more help for wallet at: https://github.com/Revabrio/KamiCoin_Wallet\n
        \n\n\n""")

def wallet(public_key, private_key):
    response = False
    while True:
        while response not in ["1","2","3","5"]:
            response = input("""What do you want to do?
            1. Show your wallet data
            2  Check balance
            3. Send coins to another wallet
            4. Check transactions
            5. Start mining\n""")

        if response == "1":

            print("""====================================================\n
                    IMPORTANT: DONT give this data to another peoples!!!!\n
                  =======================================================\n""")
            print(f'Your public key / wallet address: {public_key}')
            print(f'Your private key: {private_key}')
            response = False

        elif response == "2":

            blockchain_module.check_balance(public_key)
            response = False

        elif response == "3":

            addr_to = input("To: introduce destination wallet address\n")
            amount = str(input("Amount: number stating how much do you want to send\n"))
            message = str(input("You can send message with transaction, enter this message or print n\n"))
            if message == 'n' or len(message) > 128:
                print('You refuse to send message, or message too long')
                message = ''
            print("=========================================\n\n")
            print("Is everything correct?\n")
            print("From: {0}\nPrivate Key: {1}\nTo: {2}\nAmount: {3}\n".format(public_key,private_key,addr_to,amount))
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
    if os.path.exists('wallet_keys'):
        password = input('Please, enter your password: ')
        with open('wallet_keys', 'r') as file:
            data = file.readlines()
            public_key = bytes.decode(aes_module.decrypt(json.loads(data[0].replace('\n', '')), password))
            private_key = bytes.decode(aes_module.decrypt(json.loads(data[1]), password))
        welcome_msg()
        wallet(public_key, private_key)
        input("Press any key to exit...")
    else:
        private_key, public_key = blockchain_module.generate_ECDSA_keys()
        password = input('Please, enter password for encrypting you wallet data: ')
        print('-'*30)
        print('Please, remember your password!!!')
        print('If you will lose it, you can not restore your wallet!!!!')
        print('-' * 30)
        show_keys = input('Please, enter y if you want to see your wallet keys: ')
        if show_keys == 'y':
            print(f'Your public key / wallet address: {public_key}')
            print(f'Your private key: {private_key}')
        enc_private_key = aes_module.encrypt(private_key, password)
        enc_public_key = aes_module.encrypt(public_key, password)
        print(enc_public_key)
        with open('wallet_keys', 'w') as file:
            file.write(json.dumps(enc_public_key))
            file.write('\n')
            file.write(json.dumps(enc_private_key))
        welcome_msg()
        wallet(public_key, private_key)
        input("Press any key to exit...")