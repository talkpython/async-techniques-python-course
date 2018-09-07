import datetime
import colorama
import asyncio


def main():
    lim = 250_000
    print("Running standard loop with {:,} actions.".format(lim*2))
    t0 = datetime.datetime.now()

    loop = asyncio.get_event_loop()
    data = asyncio.Queue()

    task1 = loop.create_task(generate_data(lim, data))
    task3 = loop.create_task(generate_data(lim, data))
    task2 = loop.create_task(process_data(2 * lim, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)


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
