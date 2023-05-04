#!/usr/bin/env python3

import asyncio
import time
from bleak import BleakClient

class ComDoor:
    def __init__(self):
        self.TKO_DOOR_wanted_name = "TKO_DOOR"
        self.TKO_DOOR_device = "EE:11:65:68:71:64"
        self.TKO_DOOR_CTRL_UUID = "34860001-e699-4650-ae12-f1f3c8bf9ad9"

        # TKO_LIFT_DOOR
        self.TKO_LIFT_wanted_name = "TKO_LIFT_DOOR"
        self.TKO_LIFT_device = "F5:EC:6E:A0:BF:CD"
        self.TKO_LIFT_CTRL_UUID = "34860001-449d-4815-9141-c881fbbfd598"


    def door_task(self, msg):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.door_op(msg))

    def lift_task(self, msg):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.lift_op(msg))

    async def door_op(self, num):
        door_changed = False
        retry_cnt = 1
        while door_changed is False and retry_cnt > 0:
            try:                
                client = BleakClient(self.TKO_DOOR_device)                
                await asyncio.wait_for(client.connect(), timeout=10)
                write_value = bytearray([num])
                await client.write_gatt_char(self.TKO_DOOR_CTRL_UUID, write_value)
                door_changed = True
                print("door changed")
            except:
                print('door connection error')
                print("door not changed")
            finally:
                await client.disconnect()
            retry_cnt -= 1

    async def lift_op(self, num):
        lift_changed = False
        retry_cnt = 1
        while lift_changed is False and retry_cnt > 0:
            try:                
                client = BleakClient(self.TKO_LIFT_device)                
                await asyncio.wait_for(client.connect(), timeout=10)
                write_value = bytearray([num])
                await client.write_gatt_char(self.TKO_LIFT_CTRL_UUID, write_value)
                lift_changed = True
                print("lift changed")
            except:
                print('lift door connection error')
                print("lift not changed")
            finally:
                await client.disconnect()
            retry_cnt -= 1

    def door_operation(self, num):
        asyncio.get_event_loop().run_until_complete(self.door_op(num))

if __name__ == "__main__":
    # unit test 
    door = ComDoor()
    # open door
    door.door_operation(1)
    # close door
    # test.door_operation(0)
