![image](https://github.com/user-attachments/assets/334f629a-88be-4780-9b12-7d230336ed10)


# Bitcoin-Address-Generator---BTC-Crumble-Gen
BTC Crumble Gen is a Bitcoin address generator tool that creates a Bitcoin wallet using a randomly generated mnemonic phrase. The tool allows you to view detailed wallet information including balance, transaction history, unspent outputs (UTXOs), and other wallet metadata by fetching data from multiple APIs.

This script continuously generates Bitcoin wallets and retrieves real-time information about each wallet from various public Bitcoin blockchain APIs.

## Features
- Generate Bitcoin Wallets: Create Bitcoin wallets with 12 or 24-word mnemonics.
- Fetch Bitcoin Data: Retrieve wallet balance, transaction history, and unspent transaction outputs (UTXOs).
- Multiple APIs Supported: Fetch wallet data from Blockstream, Blockchain, and BlockCypher APIs.
- Display Information: View detailed information about the generated Bitcoin wallet in a well-formatted terminal output.
- Real-Time Information: View real-time Bitcoin wallet data such as balance and transaction history.


## Installation
Python 3.6+ is required.
Install the required libraries
```
pip install mnemonic bitcoinlib requests pyfiglet colorama
```

> Wallet Generation: The script will continuously generate Bitcoin wallets using randomly chosen 12 or 24-word mnemonic phrases.
> Data Fetching: For each generated wallet, the script will fetch data (balance, transactions, and UTXOs) from three different public Bitcoin blockchain APIs: Blockstream, Blockchain, and BlockCypher.
> Display Information: After retrieving the data, the wallet information will be displayed in a clear, colored format in your terminal.
