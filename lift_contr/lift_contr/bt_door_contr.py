import asyncio
from bleak import BleakClient

OPEN_DOOR = 1
CLOSE_DOOR = 0

# DOOR
TKO_DOOR_wanted_name = "TKO_DOOR"
address_door = "E3:59:A8:08:10:F7" #"EE:11:65:68:71:64"
MODEL_NBR_UUID_door = "34860001-e699-4650-ae12-f1f3c8bf9ad9"

# LIFT_DOOR
address_lift = "F5:EC:6E:A0:BF:CD"
MODEL_NBR_UUID_lift = "34860001-E699-4650-ae12-f1f3c8bf9ad9"


async def door(cmd, address, uuid):
    client = BleakClient(address)
    try:
        await client.connect()
        write_value = bytearray([cmd])
        await client.write_gatt_char(uuid, write_value)
        print("success")
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(door(OPEN_DOOR,address_lift, MODEL_NBR_UUID_lift))
    print("finished")
    asyncio.run(door(CLOSE_DOOR,address_lift, MODEL_NBR_UUID_lift))
    print("finished")