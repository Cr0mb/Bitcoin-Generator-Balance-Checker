import os
import ecdsa
import hashlib
import base58
import json
import time
import requests
import bech32
import logging
import tempfile
from mnemonic import Mnemonic
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Logging setup
logging.basicConfig(filename="wallet_generator.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    print(Fore.YELLOW + message)  # Console output
    logging.info(message)  # Log file output

API_URLS = {
    "blockstream": "https://blockstream.info/api/address/",
    "blockchain": "https://blockchain.info/rawaddr/",
    "blockcypher": "https://api.blockcypher.com/v1/btc/main/addrs/",
    "blockchair": "https://api.blockchair.com/bitcoin/dashboards/address/"
}

def generate_private_key():
    return os.urandom(32)

def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    return sk.get_verifying_key().to_string()

def private_key_to_mnemonic(private_key):
    return Mnemonic("english").to_mnemonic(private_key)

def public_key_to_addresses(public_key):
    sha256_pk = hashlib.sha256(public_key).digest()
    ripemd160_pk = hashlib.new('ripemd160', sha256_pk).digest()
    
    legacy_address = base58.b58encode_check(b'\x00' + ripemd160_pk).decode('utf-8')
    nested_segwit_address = base58.b58encode_check(b'\x05' + ripemd160_pk).decode('utf-8')
    segwit_address = bech32.encode('bc', 0, list(ripemd160_pk))
    
    return legacy_address, nested_segwit_address, segwit_address

def get_wallet_info(address):
    for name, url in API_URLS.items():
        try:
            response = requests.get(f"{url}{address}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if name == "blockchair":
                    data = data.get('data', {}).get(address, {})
                    if 'address' in data:
                        return {
                            'final_balance': data['address'].get('balance', 0),
                            'txs': data.get('transactions', []),
                        }, name
                else:
                    return data, name
        except requests.exceptions.RequestException:
            pass  # Skip to the next API if request fails
    return None, "None"

def display_wallet_info(wallet_type, address, info):
    print(Fore.CYAN + f"\n{wallet_type} Address Info:")
    print(Fore.GREEN + f"TX History: {info.get('txs', [])}")
    print(Fore.RED + f"Balance: {info.get('final_balance', 0) / 1e8} BTC")

def save_wallet_to_file(wallet_info):
    wallets_data = []
    if os.path.exists('wallets.json'):
        try:
            with open('wallets.json', 'r') as file:
                wallets_data = json.load(file)
        except (json.JSONDecodeError, IOError):
            log_event("Warning: Corrupted wallets.json, resetting file.")
    wallets_data.append(wallet_info)
    temp_filename = tempfile.mktemp()
    with open(temp_filename, 'w') as temp_file:
        json.dump(wallets_data, temp_file, indent=4)
    os.replace(temp_filename, 'wallets.json')

def generate_wallet():
    private_key = generate_private_key()
    public_key = private_key_to_public_key(private_key)
    mnemonic_phrase = private_key_to_mnemonic(private_key)
    legacy_address, nested_segwit_address, segwit_address = public_key_to_addresses(public_key)
    
    print("\nBitcoin Wallet Generator & Balance Checker\n")
    print(Fore.YELLOW + "Made by Cr0mb\n")
    print(Fore.CYAN + "Mnemonic Phrase: " + Style.BRIGHT + mnemonic_phrase)
    print(Fore.GREEN + "Private Key (Hex): " + Style.BRIGHT + private_key.hex())
    print(Fore.YELLOW + "Public Key (Hex): " + Style.BRIGHT + public_key.hex())
    print(Fore.MAGENTA + "Legacy Address (P2PKH): " + Style.BRIGHT + legacy_address)
    print(Fore.MAGENTA + "Nested SegWit Address (P2SH-P2WPKH): " + Style.BRIGHT + nested_segwit_address)
    print(Fore.MAGENTA + "SegWit Address (P2WPKH): " + Style.BRIGHT + segwit_address)

    all_failed = True

    for address, addr_type in [
        (legacy_address, "Legacy"),
        (nested_segwit_address, "Nested SegWit"),
        (segwit_address, "SegWit"),
    ]:
        info, api_name = get_wallet_info(address)
        if info:
            all_failed = False
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
            log_event(f"Error fetching {addr_type} Address info from all APIs.")

    if all_failed:
        log_event("All APIs failed! Pausing for 20 minutes before retrying...")
        time.sleep(1200)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_continuously():
    try:
        while True:
            clear_screen()
            generate_wallet()
            log_event("Waiting 1 second before generating the next wallet...")
            # time.sleep(1)  # Uncomment if needed
    except KeyboardInterrupt:
        log_event("Process interrupted. Exiting gracefully...")

if __name__ == "__main__":
    run_continuously()
