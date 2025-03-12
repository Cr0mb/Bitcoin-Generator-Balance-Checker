import os
import ecdsa
import hashlib
import base58
from mnemonic import Mnemonic
import bech32
import requests
from colorama import Fore, Style, init
import time
import json

init(autoreset=True)

API_URLS = {
    "blockstream": "https://blockstream.info/api/address/",
    "blockchain": "https://blockchain.info/rawaddr/",
    "blockcypher": "https://api.blockcypher.com/v1/btc/main/addrs/"
}

def generate_private_key():
    return os.urandom(32)

def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    return sk.get_verifying_key().to_string()

def private_key_to_mnemonic(private_key):
    seed = hashlib.sha256(private_key).digest()
    return Mnemonic("english").to_mnemonic(seed)

def public_key_to_addresses(public_key):
    ripemd160 = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    legacy_address = base58.b58encode_check(b'\x00' + ripemd160)
    segwit_address = bech32.encode('bc', 0, ripemd160)
    return legacy_address, segwit_address

def get_wallet_info(address):
    for name, url in API_URLS.items():
        response = requests.get(f"{url}{address}")
        if response.status_code == 200:
            return response.json(), name
    return None, "None"

def display_wallet_info(wallet_type, address, info):
    print(Fore.CYAN + f"\n{wallet_type} Address Info:")
    print(Fore.GREEN + f"TX History: {info.get('txs', [])}")
    print(Fore.RED + f"Unspent Transactions: {info.get('unspent', [])}")
    print(Fore.YELLOW + f"Balance: {info.get('final_balance', 0) / 1e8} BTC")

def save_wallet_to_file(wallet_info):
    if os.path.exists('wallets.json'):
        with open('wallets.json', 'r') as file:
            wallets_data = json.load(file)
    else:
        wallets_data = []

    wallets_data.append(wallet_info)
    with open('wallets.json', 'w') as file:
        json.dump(wallets_data, file, indent=4)

def generate_wallet():
    private_key = generate_private_key()
    public_key = private_key_to_public_key(private_key)
    mnemonic_phrase = private_key_to_mnemonic(private_key)
    legacy_address, segwit_address = public_key_to_addresses(public_key)
    print("\n\nBitcoin Generator & Balance checker\n\n")
    
    print(Fore.YELLOW + "Made by Cr0mb\n\n")
    print(Fore.CYAN + "Mnemonic Phrase: ", Style.BRIGHT + mnemonic_phrase)
    print(Fore.GREEN + "Private Key (Hex): ", Style.BRIGHT + private_key.hex())
    print(Fore.YELLOW + "Public Key (Hex): ", Style.BRIGHT + public_key.hex())
    print(Fore.MAGENTA + "Legacy Address (P2PKH): ", Style.BRIGHT + legacy_address.decode('utf-8'))
    print(Fore.MAGENTA + "SegWit Address (P2WPKH/P2SH): ", Style.BRIGHT + segwit_address)

    for address, addr_type in [(legacy_address.decode('utf-8'), "Legacy"), (segwit_address, "SegWit")]:
        info, api_name = get_wallet_info(address)
        if info:
            display_wallet_info(f"{addr_type} Address Info from {api_name.capitalize()} API", address, info)
            
            if ('txs' in info and len(info['txs']) > 0) or info.get('final_balance', 0) > 0:
                wallet_info = {
                    'address': address,
                    'type': addr_type,
                    'transaction_history': info.get('txs', []),
                    'balance': info.get('final_balance', 0) / 1e8
                }
                save_wallet_to_file(wallet_info)
                
        else:
            print(Fore.RED + f"\nError fetching {addr_type} Address info from all APIs, blacklisted.")
            print(Fore.YELLOW + "\nWaiting for 20 minutes before trying again...")
            time.sleep(1200)

def run_continuously():
    while True:
        clear_screen()
        generate_wallet()
        print(Fore.YELLOW + "\nWaiting 1 second before generating the next wallet...\n")
        time.sleep(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    run_continuously()
