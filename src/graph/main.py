import argparse
import asyncio
from datetime import datetime
from datetime import timedelta

import aiohttp
from dateutil import parser as dateparser
import matplotlib
import matplotlib.pyplot as plt

import graph.config as config


async def plot():
    config.read("config.toml")

    matplotlib.use("TkAgg")
    plt.style.use("ggplot")

    # pressure and linky
    plt.figure(figsize=(10, 8))

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        dts = []
        values = []

        start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
        url = (
            f"http://{config.server.hostname}:{config.server.port}/"
            f"pressure?start={start_datetime}"
        )
        skip_first = True
        async with session.get(url) as r:
            async for line in r.content:
                if skip_first:
                    skip_first = False
                    continue
                dt, value = line.decode().strip().split(',')
                dts.append(dateparser.parse(dt))
                values.append(float(value))

    plt.subplot(2, 1, 1)
    plt.title("Pression")
    plt.ylabel("hPa")
    plt.plot(dts, values)

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        dts = []
        values = []

        start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
        url = (
            f"http://{config.server.hostname}:{config.server.port}/"
            f"linky?start={start_datetime}"
        )
        skip_first = True
        async with session.get(url) as r:
            async for line in r.content:
                if skip_first:
                    skip_first = False
                    continue
                dt, _, sinst = line.decode().strip().split(',')
                sinst = int(sinst)
                dts.append(dateparser.parse(dt))
                values.append(sinst)

    plt.subplot(2, 1, 2)
    plt.title("Linky")
    plt.ylabel("VA")
    plt.plot(dts, values)

    # sonoff snzb-02p
    for n, device in enumerate(config.device.snzb02p):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            dts = []
            hmds = []
            tmps = []

            start_datetime = int((datetime.now() - timedelta(days=2)).timestamp())
            url = (
                f"http://{config.server.hostname}:{config.server.port}/"
                f"snzb02p?device={device}&start={start_datetime}"
            )
            skip_first = True
            async with session.get(url) as r:
                async for line in r.content:
                    if skip_first:
                        skip_first = False
                        continue
                    dt, humidity, temperature = line.decode().strip().split(',')
                    dts.append(dateparser.parse(dt))
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


async def close():
    pass


async def run(config_filename: str):
    config.read("config.toml")

    await plot()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="config.toml")
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run(args.config))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(close())
        loop.stop()
