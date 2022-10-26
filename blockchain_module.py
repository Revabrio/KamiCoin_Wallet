import time
import ecdsa
import base64
import requests
import wallet_config

def check_transactions():
    """Retrieve the entire blockchain. With this you can check your
    wallets balance. If the blockchain is to long, it may take some time to load.
    """
    res = requests.get(wallet_config.MINER_NODE_URL+'/blocks')
    print(res.text)

def check_balance(wallet_to_check):
    url     = wallet_config.MINER_NODE_URL+'/txion'
    payload = {"source": "wallet", "option":"balance", "wallet": wallet_to_check}
    headers = {"Content-Type": "application/json"}

    res = requests.post(url, json=payload, headers=headers)
    print('Your balance is: ' + str(float(res.text)))

def generate_ECDSA_keys():
    """This function takes care of creating your private and public (your address) keys.
    It's very important you don't lose any of them or those wallets will be lost
    forever. If someone else get access to your private key, you risk losing your coins.

    private_key: str
    public_ley: base64 (to make it shorter)
    """
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
    private_key = sk.to_string().hex() #convert your private key to hex
    vk = sk.get_verifying_key() #this is your verification key (public key)
    public_key = vk.to_string().hex()
    #print("Private key: {0}".format(private_key))
    #we are going to encode the public key to make it shorter
    public_key = base64.b64encode(bytes.fromhex(public_key))
    #using decode() to remove the b'' from the printed string
    #print("Wallet address / Public key: {0}".format(public_key.decode()))
    return private_key, public_key.decode()

def sign_ECDSA_msg(private_key, addr_from, addr_to, amount, message_send, timestamp):
    """Sign the message to be sent
    private_key: must be hex

    return
    signature: base64 (to make it shorter)
    message: str
    """
    #get timestamp, round it, make it string and encode it to bytes
    message=str(timestamp)+'|||'+str(addr_from)+'|||'+str(addr_to)+'|||'+str(amount)+'|||'+str(message_send)
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature,message

def send_transaction(timestamp, addr_from,private_key,addr_to,amount, message):
    """Sends your transaction to different nodes. Once any of the nodes manage
    to mine a block, your transaction will be added to the blockchain. Dispite
    that, there is a low chance your transaction gets canceled due to other nodes
    having a longer chain. So make sure your transaction is deep into the chain
    before claiming it as approved!
    """
    #for fast debuging REMOVE LATER
    #private_key="d9319751ce59ff9450f4c8b469738227bb34c26a9e94283e123c0be6fa494466"
    #amount="5"
    #addr_from="i7YqTe+slTO9f+MpPYTOrh8p52T21jxpZBf/RiVAS1QRnCel31hpzEfa1T29UWvWlEbzeReIzHG43TxkAnlw5w=="
    #addr_to="i7YqTe+slTO9f+MpPYTOrh8p52T21jxpZBf/RiVAS1QRnCel31hpzEfa1T29UWvWlNEWADRESS"

    if len(private_key) == 64:
        signature,sig_message = sign_ECDSA_msg(private_key, addr_from, addr_to, amount, message, timestamp)
        url     = wallet_config.MINER_NODE_URL+'/txion'
        payload = {"source": "wallet","option":"newtx", "datetime": timestamp, "from_address": addr_from, "to_address": addr_to, "amount": amount, "signature": signature.decode(), "msig_essage": sig_message, "message": message}
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print("Wrong address or key length! Verify and try again.")