
"""
MINER_NAME - Используется для обозначения майнинговой машины для пользователя

MINER_IP - Используется для хранения ip главного сервера блокчена

MINER_PORT - Используется для хранения ip главного сервера блокчейна

MINER_NODE_URL - Используется для создания ссылки на гланвый сервер блокчейна

EXPLORER_IP - Используется для хранения ip explorer блокчена

EXPLORER_PORT - Используется для хранения ip explorer блокчейна

EXPLORER_URL - Используется для создания ссылки на explorer блокчейна
"""

MINER_NAME = "PC#1"

MINER_IP = "localhost"
MINER_PORT = 5000
MINER_NODE_URL = "http://"+MINER_IP+":"+str(MINER_PORT)

EXPLORER_IP = 'localhost'
EXPLORER_PORT = 5001
EXPLORER_URL = "http://"+EXPLORER_IP+":"+str(EXPLORER_PORT)