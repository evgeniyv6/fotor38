#!/usr/bin/env python

import sys
import asyncio
import itertools
import random

from mystack import Stack as myS
from myqueue import Queue as myQ

SPINNER_SLEEP = .1

async def spinner():
    write, flush = sys.stdout.write, sys.stdout.flush
    for ch in itertools.cycle('|/-\\'):
        write(ch)
        flush()
        write('\x08' * len(ch))
        try:
            await asyncio.sleep(SPINNER_SLEEP)
        except asyncio.CancelledError:
            write(' ' * len(ch) + '\x08' * len(ch))
            write('cancelled\n')
            flush()
            break
    return 'spinner stops'

async def stack_task(*args):
    st = myS()
    for e in args:
        st.push(e)
    st.pop()
    await asyncio.sleep(random.randrange(1,3))
    return st

async def queue_task(*args):
    q = myQ()
    for e in args:
        q.enqueue(e)
    await asyncio.sleep(random.randrange(1,3))
    q.dequeue()
    return q


async def main():
    spinner_run = asyncio.ensure_future(spinner())
    stack_run = asyncio.ensure_future(stack_task(1,2,3,))
    queue_run = asyncio.ensure_future(queue_task(1,2,3,))
    c, p = await asyncio.wait([spinner_run, stack_run], timeout=5)

# never stops spinner
async def main3(loop):
    stack_run = loop.create_task(stack_task(1,2,3,))
    queue_run = loop.create_task(queue_task(1,2,3,))
    spinner_run = loop.create_task(spinner())
    res_st = await stack_run; res_q = await queue_run; await spinner_run
    print(res_st, res_q)

def task_canceller(t):
    t.cancel()

async def main4(loop):
    spinner_run = loop.create_task(spinner())
    # await spinner_run
    results = []
    for next_done in asyncio.as_completed([stack_task(1,2,3,), queue_task(1,2,3,)]):
        res = await next_done
        results.append(res)
    loop.call_soon(task_canceller, spinner_run)
    try:
        await spinner_run
    except asyncio.CancelledError:
        pass
    return results

if __name__ == '__main__':
    # asyncio.run(main())
    el = asyncio.get_event_loop()
    try:
        res = el.run_until_complete(main4(el))
        print(res)
    finally:
        el.close()

