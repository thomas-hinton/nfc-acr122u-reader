from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
import pyautogui
import time

# APDU command used to retrieve card UID
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]


def to_hex(data):
    """Convert byte array to uppercase hexadecimal string."""
    return "".join(f"{b:02X}" for b in data)


def main():
    available_readers = readers()

    if not available_readers:
        print("No NFC reader detected.")
        return

    reader = available_readers[0]
    
    print(f"Reader detected: {reader}")
    print("Waiting for an NFC card...")
    print("Scanned card UIDs will be typed automatically followed by Enter.")

    last_uid = None
    card_present = False

    while True:
        try:
            connection = reader.createConnection()
            connection.connect()

            data, sw1, sw2 = connection.transmit(GET_UID)
            uid = to_hex(data)

            if sw1 == 0x90 and sw2 == 0x00:
                if not card_present or uid != last_uid:
                    print(f"Card detected: {uid}")

                    pyautogui.write(uid)
                    pyautogui.press("enter")

                    last_uid = uid
                    card_present = True

            connection.disconnect()
            time.sleep(0.3)

        except NoCardException:
            card_present = False
            last_uid = None
            time.sleep(0.2)

        except CardConnectionException:
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nProgram terminated.")
            break


if __name__ == "__main__":
    main()