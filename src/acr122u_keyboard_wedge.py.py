#!/usr/bin/env python3
import logging
import signal
import time

from evdev import UInput, ecodes as e
from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException

# APDU command used to retrieve card UID
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
READER_NAME_HINT = "ACR122"
POLL_WHEN_READY = 0.08
POLL_WHEN_CARD_PRESENT = 0.20
READER_RETRY_SECONDS = 2.0
READER_CLEAR_THRESHOLD = 3
KEY_DELAY_SECONDS = 0.01


STOP = False


KEY_MAP = {
    "0": e.KEY_0,
    "1": e.KEY_1,
    "2": e.KEY_2,
    "3": e.KEY_3,
    "4": e.KEY_4,
    "5": e.KEY_5,
    "6": e.KEY_6,
    "7": e.KEY_7,
    "8": e.KEY_8,
    "9": e.KEY_9,
    "A": e.KEY_A,
    "B": e.KEY_B,
    "C": e.KEY_C,
    "D": e.KEY_D,
    "E": e.KEY_E,
    "F": e.KEY_F,
}


def handle_stop(signum, frame):
    del signum, frame
    global STOP
    STOP = True


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def to_hex(data):
    """Convert byte array to uppercase hexadecimal string."""
    return "".join(f"{byte:02X}" for byte in data)


def choose_reader():
    available = readers()
    if not available:
        return None

    for reader in available:
        if READER_NAME_HINT.lower() in str(reader).lower():
            return reader

    return available[0]


def create_virtual_keyboard():
    capabilities = {
        e.EV_KEY: sorted({*KEY_MAP.values(), e.KEY_ENTER}),
    }
    ui = UInput(capabilities, name="ACR122U RFID Keyboard")
    logging.info("Virtual keyboard ready")
    return ui


def tap_key(ui, key_code):
    ui.write(e.EV_KEY, key_code, 1)
    ui.write(e.EV_KEY, key_code, 0)
    ui.syn()
    time.sleep(KEY_DELAY_SECONDS)


def emit_uid(ui, uid):
    for char in uid:
        key_code = KEY_MAP.get(char)
        if key_code is None:
            raise ValueError(f"Unsupported UID character: {char!r}")
        tap_key(ui, key_code)

    tap_key(ui, e.KEY_ENTER)


def read_uid_once(reader):
    connection = reader.createConnection()
    connection.connect()
    try:
        data, sw1, sw2 = connection.transmit(GET_UID)
        if sw1 == 0x90 and sw2 == 0x00 and data:
            return to_hex(data)
        return None
    finally:
        try:
            connection.disconnect()
        except Exception:
            pass


def main():
    setup_logging()
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    ui = create_virtual_keyboard()

    locked_until_removed = False
    last_uid = None
    no_card_streak = 0
    last_reader_name = None
    missing_reader_logged = False

    try:
        while not STOP:
            reader = choose_reader()
            if reader is None:
                if not missing_reader_logged:
                    logging.warning("No PC/SC reader detected")
                    missing_reader_logged = True
                time.sleep(READER_RETRY_SECONDS)
                continue

            missing_reader_logged = False

            reader_name = str(reader)
            if reader_name != last_reader_name:
                logging.info("Using reader: %s", reader_name)
                last_reader_name = reader_name

            try:
                uid = read_uid_once(reader)
                no_card_streak = 0

                if uid is None:
                    time.sleep(POLL_WHEN_CARD_PRESENT)
                    continue

                if not locked_until_removed:
                    logging.info("Card detected: %s", uid)
                    emit_uid(ui, uid)
                    locked_until_removed = True
                    last_uid = uid
                else:
                    if uid != last_uid:
                        logging.info(
                            "Card change ignored while waiting for removal: previous=%s new=%s",
                            last_uid,
                            uid,
                        )

                time.sleep(POLL_WHEN_CARD_PRESENT)

            except (NoCardException, CardConnectionException):
                no_card_streak += 1
                if locked_until_removed and no_card_streak >= READER_CLEAR_THRESHOLD:
                    locked_until_removed = False
                    last_uid = None
                    logging.info("Reader clear, re-armed")

                time.sleep(POLL_WHEN_READY)

            except Exception:
                logging.exception("Unexpected RFID error")
                time.sleep(1.0)

    finally:
        ui.close()
        logging.info("RFID service stopped")


if __name__ == "__main__":
    main()