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


async def fry_bacon(slices: int):
    print(f'putting {slices} slices of bacon in the pan')
    print('cooking first side of bacon...')
    await asyncio.sleep(3)
    for _ in range(slices):
        print('flipping a slice of bacon')
    print('cooking the second side of bacon...')
    await asyncio.sleep(3)
    print('Put bacon on plate')


class Bread:
    def __init__(self, slices: int):
        self.slices = slices

    async def toast(self):
        for _ in range(self.slices):
            print('Putting a slice of bread in the toaster')
        print('Start toasting...')
        await asyncio.sleep(3)
        print('Remove toast from toaster')

    def apply_butter(self):
        print('Putting butter on the toast')

    def apply_jam(self):
        print('Putting jam on the toast')


def pour_juice():
    print('Pouring orange juice')


async def breakfast():
    pour_coffee()
    print("coffee is ready")

    egg_task = fry_eggs(2)
    await egg_task
    print('eggs are ready')

    bacon_task =  fry_bacon(3)
    await bacon_task
    print('bacon is ready')

    toast = Bread(2)
    toast_task = toast.toast()
    await toast_task
    toast.apply_butter()
    toast.apply_jam()
    print('toast is ready')

    pour_juice()
    print('juice is ready')

    print('Breakfast is ready')


if __name__ == "__main__":
    print("Coocking started.")
    start_time = monotonic()
    # two_breakfasts = asyncio.gather(breakfast(), breakfast())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(breakfast())
    loop.close()
    print(f'It took {monotonic() - start_time} mins.')
