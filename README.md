# NFC ACR122U Reader Keyboard Emulator

Minimal Python project for interacting with an ACS ACR122U NFC/RFID USB reader.
Python project that turns an ACS ACR122U NFC/RFID USB reader into a keyboard-like input device.

When a RFID/NFC card is scanned, the program reads the card UID, types it automatically as keyboard input, and presses Enter.

## Hardware

* Reader: ACS ACR122U
* Interface: USB
* Protocols: NFC / RFID
* Communication: PC/SC
* Reference: https://www.amazon.fr/dp/B086HTYWR4

## Features

* Detect NFC cards/tags
* Read card UID
* Display raw reader responses
* Keyboard emulation mode
* Automatically type scanned UID followed by Enter
* Simple testing environment for NFC experiments

## Requirements

* Python 3.10+
* Windows recommended
* PC/SC compatible system

Python dependencies:

```txt
pyscard
pyautogui
```

## Installation

Create virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment:

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python read_uid.py
```

Then place a NFC card on the reader.

## Keyboard Emulation

When a card is scanned:

1. The UID is read
2. The UID is automatically typed as keyboard input
3. The Enter key is pressed automatically

Example:

```txt
BB0FADA7
```

This allows the NFC reader to behave like a barcode scanner or keyboard wedge device.

## Example Console Output

```txt
Lecteur : ACS ACR122 0

Carte détectée : BB0FADA7
```

## Repository Goal

This repository is intended as a playground for experimenting with:

* NFC communication
* APDU commands
* Keyboard emulation
* Card interactions using the ACS ACR122U reader
