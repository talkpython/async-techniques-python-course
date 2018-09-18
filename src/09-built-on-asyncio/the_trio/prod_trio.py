import datetime
import colorama
import random
import trio


async def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)

    data = trio.Queue(capacity=10)

    with trio.move_on_after(5):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(generate_data, 20, data, name='Prod 1')
            nursery.start_soon(generate_data, 20, data, name='Prod 2')
            nursery.start_soon(process_data, 40, data, name='Consumer')

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + "App exiting, total time: {:,.2f} sec.".format(
        dt.total_seconds()), flush=True)


async def generate_data(num: int, data: trio.Queue):
    for idx in range(1, num + 1):
        item = idx*idx
        await data.put((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f" -- generated item {idx}", flush=True)
        await trio.sleep(random.random() + .5)


async def process_data(num: int, data: trio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()

        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN +
              " +++ Processed value {} after {:,.2f} sec.".format(
                  value, dt.total_seconds()), flush=True)
        await trio.sleep(.5)


if __name__ == '__main__':
    trio.run(main)
