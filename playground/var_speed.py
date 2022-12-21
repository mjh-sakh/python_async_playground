import asyncio


class Actor:
    def __init__(self, speed: float) -> None:
        self.speed = max(0, min(1, speed))  # limiting b/w 0 and 1 seconds
        self.name = 'slow' if self.speed > 0.5 else 'fast'
        self.state = 0

    async def act(self) -> int:
        await asyncio.sleep(self.speed)
        self.state += 1
        return self


def as_completed(fs, *, timeout=None):
    """
    Adoption of asyncio.as_completed to run forever or until timeout.
    """
    done = asyncio.Queue()
    loop = asyncio.get_event_loop()
    todo = set(fs)
    timeout_handle = None

    def _on_timeout():
        for f in todo:
            f.cancel()
            done.put_nowait(None)  # Queue a dummy value for _wait_for_one().
        todo.clear()  # Can't do todo.remove(f) in the loop.

    def _on_completion(f):
        if not todo:
            return  # _on_timeout() was here first.
        todo.remove(f)
        done.put_nowait(f)
        actor = f.result()
        repeated_f = asyncio.create_task(actor.act())
        todo.add(repeated_f)
        repeated_f.add_done_callback(_on_completion)
        if not todo and timeout_handle is not None:
            timeout_handle.cancel()

    async def _wait_for_one():
        f = await done.get()
        if f is None:
            # Dummy value from _on_timeout().
            return
        return f.result()  # May raise f.exception().

    for f in todo:
        f.add_done_callback(_on_completion)
    if todo and timeout is not None:
        timeout_handle = loop.call_later(timeout, _on_timeout)
    while True:
        yield _wait_for_one()
        if len(todo) == 0:
            return


async def main():
    slow = Actor(0.8)
    fast = Actor(0.3)

    print("S\tF")
    tasks = [asyncio.create_task(slow.act()), asyncio.create_task(fast.act())]
    for task in as_completed(tasks, timeout=5):
        actor = await task
        if isinstance(actor, Actor):
            offset = '\t' if actor.name == 'fast' else ''
            print(f'{offset}{actor.state}', end='\n')


if __name__ == "__main__":
    print("Started.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
    print("Finished.")
