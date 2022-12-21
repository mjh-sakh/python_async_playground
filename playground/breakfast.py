import asyncio
from time import monotonic


def pour_coffee():
    print('Pouring coffee')


async def fry_eggs(how_many: int):
    print('Warming the egg pan...')
    await asyncio.sleep(3)
    print(f'cracking {how_many} eggs')
    print('cooking the eggs ...')
    await asyncio.sleep(3)
    print('Put eggs on plate')
    return 'eggs'


async def fry_bacon(slices: int):
    print(f'putting {slices} slices of bacon in the pan')
    print('cooking first side of bacon...')
    await asyncio.sleep(3)
    for _ in range(slices):
        print('flipping a slice of bacon')
    print('cooking the second side of bacon...')
    await asyncio.sleep(4)
    print('Put bacon on plate')
    return 'bacon'


class Bread:
    def __init__(self, slices: int):
        self.slices = slices

    async def toast(self):
        for _ in range(self.slices):
            print('Putting a slice of bread in the toaster')
        print('Start toasting...')
        await asyncio.sleep(3)
        # print('Fire! Toast is ruined')
        # raise Exception('The toaster is on fire')
        print('Remove toast from toaster')

    def apply_butter(self):
        print('Putting butter on the toast')

    def apply_jam(self):
        print('Putting jam on the toast')

    async def make_toast(self):
        await self.toast()
        self.apply_butter()
        self.apply_jam()
        return 'toast'


def pour_juice():
    print('Pouring orange juice')


async def ponder(minutes: int):
    await asyncio.sleep(minutes)
    print('Yawing...')


async def breakfast():
    pour_coffee()
    print("coffee is ready")

    egg_task = asyncio.create_task(fry_eggs(2))

    bacon_task = asyncio.create_task(fry_bacon(3))

    await ponder(0)  # a way to start some tasks, see https://github.com/python/asyncio/issues/284

    toast = Bread(2)
    toast_task = asyncio.create_task(toast.make_toast())

    pour_juice()
    print('juice is ready')

    all_tasks = [egg_task, bacon_task, toast_task]
    for task in asyncio.tasks.as_completed(all_tasks):
        earliest_result = await task
        if earliest_result == "eggs":
            print('eggs are ready')
        elif earliest_result == "bacon":
            print('bacon is ready')
        elif earliest_result == "toast":
            print('toast is ready')

    print('Breakfast is ready')


if __name__ == "__main__":
    print("Cooking started.")
    start_time = monotonic()
    # two_breakfasts = asyncio.gather(breakfast(), breakfast())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(breakfast())
    print(f'It took {monotonic() - start_time} mins.')
