# Papyrus [![Build Status](https://travis-ci.org/kyokley/papyrus.svg?branch=master)](https://travis-ci.org/kyokley/papyrus)
Generate offline cryptowallets

## Purpose
Papyrus is a script that can be used to generate offline cryptowallets. After generating the private keys for the wallet, they are immediately encrypted using AES-128 using a user provided passphrase.

## Usage:
### Basic Examples
```bash
$ papyrus generate bitcoin
Enter passphrase:
Confirm passphrase:

Encrypted Private Key:
NlLBC4w...

Address:
12P4Lrr...

$ papyrus recover -k 'NlLBC4w...' --stdout
Enter passphrase:

Private Key:
L3cfaMY...

$ papyrus -h
Usage:
    papyrus generate <ACCOUNT_TYPE> [--address=<FILE>] [--output=<FILE>] [--qrcode]
    papyrus recover (--key=<STRING> | [-] | <ENCRYPTED_KEY_FILE>)
                    ([--stdout --qrcode] | <DECRYPTED_KEY_FILE>)
    papyrus qrcode ([-] | <FILE>) (--output=<FILE> | --qrcode)
    papyrus --version
    papyrus --help

Arguments:
    <ACCOUNT_TYPE>        type of account (ethereum or bitcoin)
    <FILE>                specify the path to a file
                          (using a .png extension will treat the file as a qrcode, ascii otherwise)
    <STRING>              ascii string containing an encrypted key
    <ENCRYPTED_KEY_FILE>  path to file containing encrypted key
                          use a single '-' to accept data through stdin
    <DECRYPTED_KEY_FILE>  path to file for outputting decrypted key

Options:
    -a --address=<FILE>  file to be used for generated address
    -o --output=<FILE>   file to be used for outputted data
    -k --key=<STRING>    STRING containing encrypted private key
    -s --stdout          use stdout to display decrypted data
    -q --qrcode          display in-terminal qrcode of the data
    -h --help            display this help

Be extremely careful using the --stdout flag. Using this flag will display your decrypted data in the terminal.
```

## Installation
From inside a virtualenv, run the following:
```
$ pip install git+https://github.com/kyokley/papyrus/ --process-dependencies-links
```

Alternatively, it is possible to compile from source.
```
$ git clone https://github.com/kyokley/papyrus.git
$ cd papyrus
$ python setup.py install
$ pip install -r requirements.txt
```

## Disclaimer
I know nothing about cryptography. **Use this script at your own risk.** That being said, I've made a best effort attempt at being as secure as possible. If you notice anything in the code that looks suspect, please open an issue or PR with a fix.
