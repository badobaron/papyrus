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
11ktHb6...

Address:
13K8TSg...

$ papyrus recover --key '11ktHb6...' --stdout
Enter passphrase:

Private Key:
xprv...

$ papyrus -h
Usage:
    papyrus generate <account_type> [--address_file=<FILE>] [--address_qrcode=<FILE>]
                                    [--key_file=<FILE>] [--key_qrcode=<FILE>] [--stdout_qrcode]
    papyrus recover ((<encrypted_key_file> | --key_file=<FILE>) | --key_qrcode=<FILE> | --key=<STRING> | [-])
                    (<decrypted_key_file> | --decrypted_key_qrcode=<FILE> | [--stdout --stdout_qrcode])
    papyrus --version
    papyrus --help

Arguments:
    <account_type>        type of account (ethereum or bitcoin)
    <encrypted_key_file>  path to file containing encrypted key
                          use a single '-' to accept data through stdin
    <decrypted_key_file>  path to file for outputting decrypted key

Options:
    --address_file=<FILE>          file to be used for generated address
    --address_qrcode=<FILE>        file to be used to save a QR code of the generated address
    --key=<STRING>                 STRING containing encrypted private key
    --key_file=<FILE>              file to be used for encrypted private key data
    --key_qrcode=<FILE>            file to be used for encrypted private key data in QR code form
    --decrypted_key_qrcode=<FILE>  file to be used for decrypted private key data in QR code form
    --stdout                       use stdout to display decrypted data
    --stdout_qrcode                display in-terminal qrcode of the data
    -h --help                      display this help

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
