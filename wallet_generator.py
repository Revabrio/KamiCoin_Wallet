import os
import ecdsa
import base64
import hashlib
import binascii

def generate_bits(len_bits=32):
    """Функция генерирует строку
    с заданым количеством битов

    :param len_bits:
    :return:
    """
    return os.urandom(len_bits)

def get_words_from_file():
    """Функция "парсит" слова
    из "словаря", которые используются
    для генерации seed фразы для кошелька

    :return:
    """
    with open('words_kamicoin.txt', 'r') as file:
        word_list = file.readlines()
        words_list = []
        for word in word_list:
            words_list.append(word.replace('\n', ''))
    return words_list

def get_hash_from_data(data):
    """Функция хеширует значение
    которое ей задают на вход

    :param data:
    :return:
    """
    return hashlib.sha256(data.encode()).hexdigest()

def get_bin_seed(seed):
    """Функция убирает лишние
    биты с начала строки

    :param seed:
    :return:
    """
    words_list = get_words_from_file()
    bin_seed = ''
    for word in seed:
        word_num = words_list.index(word)
        bin_num = bin(word_num)[2:]
        if len(bin_num) < 11:
            bin_num = ('0'*(11-len(bin_num)))+bin_num
        bin_seed += bin_num
    return bin_seed

def get_seed():
    """Функция генерирует seed фразу
    для кошелька

    :return:
    """
    words_list = get_words_from_file()
    seed = []
    check = 0
    while check == 0:
        seed = []
        data = generate_bits()
        if len(data) not in [16, 20, 24, 28, 32]:
            return 0
        h = hashlib.sha256(data).hexdigest()
        b = bin(int(binascii.hexlify(data), 16))[2:].zfill(len(data) * 8) + bin(int(h, 16))[2:].zfill(256)[
                                                                            : len(data) * 8 // 32]
        for i in range(len(b) // 11):
            indx = int(b[11 * i:11 * (i + 1)], 2)
            seed.append(words_list[indx])
        if 'kami' in seed:
            if 'love' in seed:
                check = 1
    return seed

def generate_ECDSA_keys(secret_data):
    """С помощью данной функции производится
    генерация публичного и приватного ключей
    для кошелька

    private_key: str
    public_ley: base64 (to make it shorter)
    """
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(secret_data), curve=ecdsa.SECP256k1)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    public_key = base64.b64encode(bytes.fromhex(public_key))
    return private_key, public_key.decode()