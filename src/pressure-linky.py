import asyncio
from datetime import datetime
from datetime import timedelta

import aiohttp
from dateutil import parser
import matplotlib
import matplotlib.pyplot as plt


async def main():
    matplotlib.use("TkAgg")
    plt.style.use("ggplot")

    plt.figure(figsize=(10, 8))

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        dts = []
        values = []

        start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
        url = f"http://lully:8085/pressure?start={start_datetime}"
        skip_first = True
        async with session.get(url) as r:
            async for line in r.content:
                if skip_first:
                    skip_first = False
                    continue
                dt, value = line.decode().strip().split(',')
                dts.append(parser.parse(dt))
                values.append(float(value))

    plt.subplot(2, 1, 1)
    plt.title("Pression")
    plt.ylabel("hPa")
    plt.plot(dts, values)

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        dts = []
        values = []

        start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
        url = f"http://lully:8085/linky?start={start_datetime}"
        skip_first = True
        async with session.get(url) as r:
            async for line in r.content:
                if skip_first:
                    skip_first = False
                    continue
                dt, _, sinst = line.decode().strip().split(',')
                sinst = int(sinst)
                dts.append(parser.parse(dt))
                values.append(sinst)

    plt.subplot(2, 1, 2)
    plt.title("Linky")
    plt.ylabel("VA")
    plt.plot(dts, values)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    asyncio.run(main())
