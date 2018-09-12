import datetime
import random
import time
from threading import Thread, RLock
from typing import List


class Account:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = RLock()


def main():
    accounts = create_accounts()
    total = sum(a.balance for a in accounts)

    validate_bank(accounts, total)
    print("Starting transfers...")

    jobs = [
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
        Thread(target=do_bank_stuff, args=(accounts, total)),
    ]

    t0 = datetime.datetime.now()

    [j.start() for j in jobs]
    [j.join() for j in jobs]

    dt = datetime.datetime.now() - t0

    print("Transfers complete ({:,.2f}) sec".format(dt.total_seconds()))
    validate_bank(accounts, total)


def do_bank_stuff(accounts, total):
    for _ in range(1, 10_000):
        a1, a2 = get_two_accounts(accounts)
        amount = random.randint(1, 100)
        do_transfer(a1, a2, amount)
        validate_bank(accounts, total, quiet=True)


def create_accounts() -> List[Account]:
    return [
        Account(balance=5000),
        Account(balance=10000),
        Account(balance=7500),
        Account(balance=7000),
        Account(balance=6000),
        Account(balance=9000),
    ]


def do_transfer(from_account: Account, to_account: Account, amount: int):
    if from_account.balance < amount:
        return

    lock1, lock2 = (
        (from_account.lock, to_account.lock)
        if id(from_account) < id(to_account)
        else (to_account.lock, from_account.lock)
    )

    with lock1:
        with lock2:
            from_account.balance -= amount
            time.sleep(.000)
            to_account.balance += amount


transfer_lock = RLock()


def do_transfer_global_style(
        from_account: Account, to_account: Account, amount: int):
    if from_account.balance < amount:
        return

    with transfer_lock:
        from_account.balance -= amount
        time.sleep(.000)
        to_account.balance += amount


def validate_bank(accounts: List[Account], total: int, quiet=False):
    # with transfer_lock:
    #     current = sum(a.balance for a in accounts)

    [a.lock.acquire() for a in accounts]
    current = sum(a.balance for a in accounts)
    [a.lock.release() for a in accounts]

    if current != total:
        print("ERROR: Inconsistent account balance: ${:,} vs ${:,}".format(
            current, total
        ), flush=True)
    elif not quiet:
        print("All good: Consistent account balance: ${:,}".format(
            total), flush=True)


def get_two_accounts(accounts):
    a1 = random.choice(accounts)
    a2 = a1
    while a2 == a1:
        a2 = random.choice(accounts)

    return a1, a2


if __name__ == '__main__':
    main()
