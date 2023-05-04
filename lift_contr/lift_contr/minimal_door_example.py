import asyncio
from bleak import BleakClient

# DOOR
TKO_DOOR_wanted_name = "TKO_DOOR"
address = "E3:59:A8:08:10:F7" #"EE:11:65:68:71:64"
MODEL_NBR_UUID = "34860001-e699-4650-ae12-f1f3c8bf9ad9"

# LIFT_DOOR
address = "F5:EC:6E:A0:BF:CD"
MODEL_NBR_UUID = "34860001-E699-4650-ae12-f1f3c8bf9ad9"


async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))
        write_value = bytearray([1])
        await client.write_gatt_char(MODEL_NBR_UUID, write_value)
        print("success")
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(main(address))