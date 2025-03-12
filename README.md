![image](https://github.com/user-attachments/assets/83fbf13e-6b4d-4248-a83d-6ffbc68847aa)

## Updates

| Issue | Solution |
|--------|------------|
| **Multiple API calls even after success** | Stop checking APIs after the first successful response. |
| **Potential JSON corruption in `wallets.json`** | Use a temporary file for atomic writes. |
| **Incorrect SegWit address generation** | Corrected Bech32 encoding of hashed public key. |
| **Improper Mnemonic derivation** | Used proper entropy source for BIP-39 compliance. |
| **Unsafe script termination** | Handle `KeyboardInterrupt` to exit cleanly. |
| **Long API failure wait (20 min delay)** | Removed `time.sleep(1200)` and continued execution. |
| **Lack of logging/debugging tools** | Added logging to track wallet generation and issues. |


# Bitcoin Generator & Balance Checker

This Python script generates Bitcoin wallets, displays relevant wallet information, and checks the balance for both Legacy and SegWit addresses using multiple public APIs.

## Features
- Generates a random Bitcoin private key and corresponding public key.
- Derives Bitcoin Legacy (P2PKH) and SegWit (P2WPKH/P2SH) addresses from the public key.
- Displays the mnemonic phrase for wallet recovery.
- Fetches and displays transaction history and unspent transactions from multiple public APIs.
- Includes a delay to handle rate limits and API blacklisting (waits for 20 minutes if blacklisted).

## Prerequisites
- Python 3.7 or higher
```
pip install ecdsa hashlib base58 mnemonic bech32 requests colorama
```

The script will start generating wallets continuously and display the following information:

> Mnemonic Phrase (for wallet recovery)

> Private Key (in hexadecimal format)

> Public Key (in hexadecimal format)

> Legacy Address (P2PKH)

> SegWit Address (P2WPKH/P2SH)
