from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
import time

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def to_hex(data):
    return " ".join(f"{b:02X}" for b in data)

def main():
    r = readers()

    if not r:
        print("Aucun lecteur détecté")
        return

    reader = r[0]
    print(f"Lecteur : {reader}")
    print("Approche une carte NFC...")

    last_uid = None

    while True:
        try:
            connection = reader.createConnection()
            connection.connect()

            data, sw1, sw2 = connection.transmit(GET_UID)
            uid = to_hex(data)

            if uid != last_uid:
                print("\nCarte détectée")
                print("UID :", uid)
                print(f"Status : {sw1:02X} {sw2:02X}")
                last_uid = uid

            connection.disconnect()
            time.sleep(0.5)

        except NoCardException:
            last_uid = None
            time.sleep(0.2)

        except CardConnectionException as e:
            print("Lecteur temporairement indisponible, nouvelle tentative...")
            time.sleep(1)

        except KeyboardInterrupt:
            print("\nArrêt")
            break

if __name__ == "__main__":
    main()