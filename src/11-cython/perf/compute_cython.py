import datetime
import math_core
from threading import Thread
import multiprocessing


def main():
    math_core.do_math(1)

    print("Doing math on {:,} processors.".format(multiprocessing.cpu_count()))

    processor_count = multiprocessing.cpu_count()
    threads = []
    for n in range(1, processor_count + 1):
        threads.append(Thread(target=math_core.do_math,
                              args=(3_000_000 * (n - 1) / processor_count,
                                    3_000_000 * n / processor_count),
                              daemon=True)
                       )

    t0 = datetime.datetime.now()
    [t.start() for t in threads]

    [t.join() for t in threads]
    # math_core.do_math(num=300_000)

    dt = datetime.datetime.now() - t0
    print("Done in {:,.2f} sec. (factor: {:,.2f}x)".format(
        dt.total_seconds(),
        0.80 / dt.total_seconds())
    )


# def do_math(start=0, num=10):
#     pos = start
#     k_sq = 1000 * 1000
#     while pos < num:
#         pos += 1
#         math.sqrt((pos - k_sq) * (pos - k_sq))


if __name__ == '__main__':
    main()
