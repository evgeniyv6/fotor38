#!/usr/bin/env python

import sys
import asyncio
import itertools
import random

from mystack import Stack as myS
from myqueue import Queue as myQ

SPINNER_SLEEP = .05

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
            write('spinner stopped\n')
            flush()
            break
    return 'spinner stopped'

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

def task_canceller(t):
    t.cancel()

async def main(loop):
    spinner_run = loop.create_task(spinner())
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
    el = asyncio.get_event_loop()
    try:
        res = el.run_until_complete(main(el))
        print(res)
    finally:
        el.close()

