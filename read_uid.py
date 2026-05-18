from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
import pyautogui
import time

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]


def to_hex(data):
    return "".join(f"{b:02X}" for b in data)


def main():
    r = readers()

    if not r:
        print("Aucun lecteur détecté")
        return

    reader = r[0]
    print(f"Lecteur : {reader}")
    print("Approche une carte NFC...")
    print("Quand une carte est scannée, son UID sera tapé au clavier puis Entrée.")

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
                    print(f"Carte détectée : {uid}")

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
            print("\nArrêt")
            break


if __name__ == "__main__":
    main()