import logging
import trio

from trio_bybit import AsyncClient
from trio_bybit.streams import BybitSocketManager


async def main():
    socket = BybitSocketManager(
        endpoint="private",
        api_key="GV0XaFwrE8Z7k0QHoy",
        api_secret="nmsmcyWGdvbxD7KDDBz4RttUjFeK7ijRNU1Q",
    )
    async with socket.connect():
        subscription = {
            "op": "subscribe",
            "args": ["order"],
        }
        await socket.subscribe(subscription)

        async for msg in socket.get_next_message():
            print(msg)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


    trio.run(main)
