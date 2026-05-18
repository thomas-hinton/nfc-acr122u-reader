# NFC ACR122U Reader

Minimal Python project for interacting with an ACS ACR122U NFC/RFID USB reader.
https://www.amazon.fr/dp/B086HTYWR4?ref=ppx_yo2ov_dt_b_fed_asin_title

## Hardware

* Reader: ACS ACR122U
* Interface: USB
* Protocols: NFC / RFID
* Communication: PC/SC

## Features

* Detect NFC cards/tags
* Read card UID
* Display raw reader responses
* Simple testing environment for NFC experiments

## Requirements

* Python 3.10+
* `pyscard`
* PC/SC compatible system

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python read_uid.py
```

Then place a NFC card on the reader.

## Example Output

```txt
Lecteur : ACS ACR122 0

Carte détectée
UID : BB 0F AD A7
Status : 90 00
```

## Repository Goal

This repository is intended as a playground for experimenting with NFC communication, APDU commands, and card interactions using the ACR122U reader.

## Repository Goal

This repository is intended as a playground for experimenting with NFC communication, APDU commands, and card interactions using the ACR122U reader.
