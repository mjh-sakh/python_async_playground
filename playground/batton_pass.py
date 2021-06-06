import asyncio
import random
from time import sleep, monotonic


async def batton_pass():
    await asyncio.sleep(0)


async def process(id: str):
    my_id = f'id={id:2}:'
    print(f"Start process id = {id}")
    await batton_pass()
    for i in range(5):
        print(f'{my_id} here my step number {i}')
        sleep(.1)
        await batton_pass()
    print(f'{my_id} finished')


def blocking_io():
    time_to_exectue = random.uniform(0, 1)
    sleep(time_to_exectue)
    print(f"Blocking IO finished operation, it took {time_to_exectue:.2f} sec.")


def execute():
    start_time = monotonic()
    loop = asyncio.get_event_loop()
    blocking_task = loop.run_in_executor(None, blocking_io)
    group = asyncio.gather(process("1"), process("2"), blocking_task)
    loop.run_until_complete(group)
    loop.close()
    finish_time = monotonic()
    print(f'Totally it took {finish_time - start_time} sec.')


if __name__ == "__main__":
    execute()
