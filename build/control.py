#!/usr/bin/env python

import asyncio
import websockets
import json
import numpy as np

from pid import PID

steering_pid = PID(0.154, 0.00012, 143.00)  


def getData(message):
    try:
        start = message.find("[")
        end = message.rfind("]")
        return message[start:end + 1]
    except:
        return ""


async def handleTelemetry(websocket, msgJson):
    cte = float(msgJson[1]["cte"])
    speed = float(msgJson[1]["speed"])
    angle = float(msgJson[1]["steering_angle"])

    steer_value = 0.0

    throttle_value = 0.05 + 0.5 * (1.0 - (abs(cte) / 2.0))  # * (float(speed) / 50)

    if throttle_value < 0.0:
        throttle_value = 0.05

  

    if cte > 1.8:  # 1.5:
        
        if speed > 10.0:
            throttle_value = -0.03 * (speed / 45)

  
    if cte < -1.8:  # -1.5:
       
        if speed > 10.0:
            throttle_value = -0.03 * (speed / 35)

    steer_value = steering_pid.PID

    response = {}

    steering_pid.Update(cte, speed, angle, steer_value, throttle_value)

    response["throttle"] = throttle_value
    response["steering_angle"] = steer_value

    msg = "42[\"steer\"," + json.dumps(response) + "]"

    await websocket.send(msg)


async def echo(websocket, path):
    async for message in websocket:
        if len(message) < 3 \
                or message[0] != '4' \
                or message[1] != '2':
            return

        s = getData(message)
        msgJson = json.loads(s)

        event = msgJson[0]
        if event == "telemetry":
            await handleTelemetry(websocket, msgJson)
        else:
            msg = "42[\"manual\",{}]"
            await websocket.send(msg)


def main():
    start_server = websockets.serve(echo, "localhost", 4567)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
