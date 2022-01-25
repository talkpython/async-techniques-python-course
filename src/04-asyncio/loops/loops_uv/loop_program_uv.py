import datetime
import colorama
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main():
    lim = 250000
    print(f"Running standard loop with {lim * 2:,} actions.")
    t0 = datetime.datetime.now()

    # Changed this from the video due to changes in Python 3.10:
    # DeprecationWarning: There is no current event loop, loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    data = asyncio.Queue()

    task1 = loop.create_task(generate_data(lim, data))
    task3 = loop.create_task(generate_data(lim, data))
    task2 = loop.create_task(process_data(2 * lim, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + f"App exiting, total time: {dt.total_seconds():,.2f} sec.", flush=True)


async def generate_data(num: int, data: asyncio.Queue):
    for idx in range(1, num + 1):
        item = idx * idx
        await data.put((item, datetime.datetime.now()))
        await asyncio.sleep(0)


async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        await data.get()
        processed += 1
        await asyncio.sleep(0)


if __name__ == '__main__':
    main()
