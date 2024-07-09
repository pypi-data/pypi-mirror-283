import asyncio
import time
from datetime import datetime

from sensoterra.customerapi import CustomerApi, InvalidAuth, Timeout


async def main():
    if True:
        api = CustomerApi("mark.ruys@sensoterra.com", "Kubus1966!")
        print(api.get_version())
    else:
        api = CustomerApi("cus577@sensoterra.com", "jcmFE6Gfpn7KxTs2aHk6")
        api.api_base_url = "http://localhost:8001/api"
    api.set_language("nl")

    if True:
        token = await api.get_token(
            "Home Assistant", "READONLY", datetime(2038, 1, 1, 0, 0)
        )
        api = CustomerApi()
        api.set_language("nl")
        api.set_token(token)

    while True:
        try:
            probes = await api.poll()

            for probe in probes:
                if probe.serial != "24000092104":
                    continue
                print(probe)
                for sensor in probe.sensors():
                    print(sensor)
                print()
        except Timeout as exp:
            print("Timeout")
        except InvalidAuth as exp:
            print(exp)

        time.sleep(10)
        print("-" * 70)


asyncio.run(main())
