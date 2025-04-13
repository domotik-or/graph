import asyncio
from datetime import datetime
from datetime import timedelta

import aiohttp
from dateutil import parser
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


async def main():
    matplotlib.use("TkAgg")
    plt.style.use("ggplot")

    for n, device in enumerate(["sejour", "chambre_haut"]):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            dts = []
            hmds = []
            tmps = []

            start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
            url = f"http://lully:8085/snzb02p?device={device}&start={start_datetime}"
            skip_first = True
            async with session.get(url) as r:
                async for line in r.content:
                    if skip_first:
                        skip_first = False
                        continue
                    dt, humidity, temperature = line.decode().strip().split(',')
                    dts.append(parser.parse(dt))
                    hmds.append(float(humidity))
                    tmps.append(float(temperature))

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
        fig.suptitle(device, fontsize=16)

        ax1.plot(dts, hmds)
        ax1.set_title("Humidity")
        ax1.set_ylabel("%RH")

        ax2.plot(dts, tmps)
        ax2.set_title("Temperature")
        ax2.set_ylabel("°C")

    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
