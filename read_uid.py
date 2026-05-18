from smartcard.System import readers
from smartcard.Exceptions import NoCardException
import time

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

def to_hex(data):
    return " ".join(f"{b:02X}" for b in data)

r = readers()

if not r:
    print("Aucun lecteur détecté")
    exit()

reader = r[0]

print(f"Lecteur : {reader}")
print("Approche une carte NFC...")

while True:
    try:
        connection = reader.createConnection()
        connection.connect()

        data, sw1, sw2 = connection.transmit(GET_UID)

        print("\nCarte détectée")
        print("UID :", to_hex(data))
        print(f"Status : {sw1:02X} {sw2:02X}")

        time.sleep(1)

    except NoCardException:
        time.sleep(0.2)

    except KeyboardInterrupt:
        print("Arrêt")
        break