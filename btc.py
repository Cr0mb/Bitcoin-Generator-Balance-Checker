import sys
import random
import time
import os
from mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet
from bitcoinlib.keys import Key
import requests
import pyfiglet
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# API URLs
BLOCKSTREAM_API_URL = "https://blockstream.info/api/address/"
BLOCKCHAIN_API_URL = "https://blockchain.info/rawaddr/"
BLOCKCYPHER_API_URL = "https://api.blockcypher.com/v1/btc/main/addrs/"

# Function to generate Bitcoin address and wallet using mnemonic
def generate_bitcoin_address(mnemonic_words):
    wallet_name = f"Bitcoin_Wallet_{mnemonic_words[:4]}"
    try:
        wallet = Wallet.create(wallet_name, keys=mnemonic_words, network='bitcoin')
    except Exception as e:
        print(f"Wallet creation error (may already exist): {e}")
        time.sleep(2)
        wallet = Wallet(wallet_name)  # Open the existing wallet without error
    key = wallet.get_key()
    address = key.address
    private_key = key.wif
    public_key = key.public()
    return address, private_key, public_key, key, wallet

# Function to generate a mnemonic
def generate_mnemonic(word_count):
    mnemo = Mnemonic("english")
    if word_count == 12:
        return mnemo.generate(strength=128)
    elif word_count == 24:
        return mnemo.generate(strength=256)
    else:
        print("Invalid choice. Please choose either 12 or 24 words.")
        sys.exit(1)

# Function to fetch data from an API
def fetch_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        time.sleep(1)
        return None

# Function to get Bitcoin balance
def get_bitcoin_balance(address, api_type="blockstream"):
    if api_type == "blockstream":
        url = f"{BLOCKSTREAM_API_URL}{address}"
        data = fetch_from_api(url)
        if data:
            balance = data['chain_stats']['funded_txo_sum'] - data['chain_stats']['spent_txo_sum']
            return balance / 1e8  # Convert from satoshis to BTC
    elif api_type == "blockchain":
        url = f"{BLOCKCHAIN_API_URL}{address}"
        data = fetch_from_api(url)
        if data:
            return data['final_balance'] / 1e8  # Convert from satoshis to BTC
    elif api_type == "blockcypher":
        url = f"{BLOCKCYPHER_API_URL}{address}/balance"
        data = fetch_from_api(url)
        if data:
            return data.get('final_balance', 0) / 1e8
    return 0

# Function to get transaction history
def get_transaction_history(address, api_type="blockstream"):
    if api_type == "blockstream":
        url = f"{BLOCKSTREAM_API_URL}{address}/txs"
        return fetch_from_api(url)
    elif api_type == "blockchain":
        url = f"{BLOCKCHAIN_API_URL}{address}"
        data = fetch_from_api(url)
        if data:
            return data.get('txs', [])
    elif api_type == "blockcypher":
        url = f"{BLOCKCYPHER_API_URL}{address}/full"
        return fetch_from_api(url).get('txs', [])
    return []

# Function to get unspent outputs
def get_unspent_outputs(address, api_type="blockstream"):
    if api_type == "blockstream":
        url = f"{BLOCKSTREAM_API_URL}{address}/utxo"
        return fetch_from_api(url)
    elif api_type == "blockchain":
        url = f"{BLOCKCHAIN_API_URL}{address}"
        data = fetch_from_api(url)
        if data:
            return data.get('unspent_outputs', [])
    elif api_type == "blockcypher":
        url = f"{BLOCKCYPHER_API_URL}{address}/full"
        return fetch_from_api(url).get('unspent_outputs', [])
    return []

# Function to display wallet information
def display_information(mnemonic_words, address, private_key, public_key, balance, key, wallet, transactions, unspent_outputs):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

    # Display title with pyfiglet
    ascii_title = pyfiglet.figlet_format("BTC Crumble Gen")
    print(Fore.GREEN + ascii_title)
    print(Fore.YELLOW + "Made by github.com/Cr0mb/\n")
    
    print(Fore.CYAN + "Welcome to the Bitcoin Address Generator")
    print(Fore.CYAN + "Generating Bitcoin wallet...\n")
    
    print(Fore.CYAN + "\n" + "-"*40)
    print(Fore.GREEN + "   --- Generated Information ---")
    print(Fore.CYAN + "-"*40)
    print(Fore.GREEN + f"Mnemonic: {mnemonic_words}")
    print(Fore.YELLOW + f"Bitcoin Address: {address}")
    print(Fore.MAGENTA + f"Balance: {balance} BTC")
    print(Fore.RED + f"Private Key (WIF): {private_key}")
    print(Fore.BLUE + f"Public Key: {public_key}")
    try:
        print(f"Derivation Path: {key.path}")
    except Exception as e:
        print(f"Error fetching derivation path: {e}")
    print(Fore.CYAN + "\n" + "-"*40)
    print(Fore.CYAN + "   --- Transaction History ---")
    print(Fore.CYAN + "-"*40)
    if transactions:
        for tx in transactions:
            print(f"TX Hash: {tx.get('txid', 'N/A')}, Received: {tx.get('value', 'N/A') / 1e8} BTC")
    else:
        print("No transactions found.")
    print(Fore.CYAN + "\n" + "-"*40)
    print(Fore.CYAN + "   --- Unspent Outputs (UTXOs) ---")
    print(Fore.CYAN + "-"*40)
    print(f"Unspent Transactions: {len(unspent_outputs)}")
    print(Fore.CYAN + "\n" + "-"*40)
    print(Fore.CYAN + "   --- Additional Wallet Info ---")
    print(Fore.CYAN + "-"*40)
    print(f"Wallet Name: {wallet.name}")
    print(f"Network: {wallet.network}")

# Function to generate wallets continuously
def generate_wallets(rate_limit_delay=1):
    apis = ["blockstream", "blockchain", "blockcypher"]
    
    while True:
        word_count = random.choice([12, 24])  # Randomly choose 12 or 24-word mnemonic
        mnemonic_words = generate_mnemonic(word_count)
        print(Fore.GREEN + f"\nGenerating wallet with {word_count}-word mnemonic...\n")

        address, private_key, public_key, key, wallet = generate_bitcoin_address(mnemonic_words)

        # Try fetching data from APIs
        for api_type in apis:
            print(Fore.CYAN + f"\nFetching data from {api_type.capitalize()} API...\n")
            time.sleep(1)
            balance = get_bitcoin_balance(address, api_type)
            transactions = get_transaction_history(address, api_type)
            unspent_outputs = get_unspent_outputs(address, api_type)

            if balance is not None and transactions is not None and unspent_outputs is not None:
                display_information(mnemonic_words, address, private_key, public_key, balance, key, wallet, transactions, unspent_outputs)
                break  # If data is successfully fetched, stop trying other APIs
            else:
                print(Fore.RED + f"Rate limit hit or failed to fetch data from {api_type.capitalize()}, switching to another API...\n")
                time.sleep(rate_limit_delay)  # Wait before switching to another API

        # Wait for the specified delay before generating another address
        time.sleep(rate_limit_delay)

def main():
    # Start generating wallets continuously
    generate_wallets()

if __name__ == "__main__":
    main()
