import asyncio
from bleak import BleakClient


# DOOR
TKO_DOOR_wanted_name = "TKO_DOOR"
address_door = "E3:59:A8:08:10:F7"
MODEL_NBR_UUID_door = "34860001-e699-4650-ae12-f1f3c8bf9ad9"

# LIFT_DOOR
address_lift = "F5:EC:6E:A0:BF:CD"
MODEL_NBR_UUID_lift = "34860001-E699-4650-ae12-f1f3c8bf9ad9"

class BtDoor():
    def __init__(self, adr, UUID):
        self.address = adr
        self.uuid = UUID
        self.OPEN = 1
        self.CLOSE = 0
        
        
    async def door(self, cmd):
        client = BleakClient(self.address)
        try:
            await client.connect()
            write_value = bytearray([cmd])
            await client.write_gatt_char(self.uuid, write_value)
            print("success")
        except Exception as e:
            print(e)
        finally:
            await client.disconnect()

    def control(self, cmd):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.door(cmd))

if __name__ == "__main__":
    lift = BtDoor(address_lift,MODEL_NBR_UUID_lift)
    lift.control(lift.OPEN)
    