#!/usr/bin/env python

from in_threads import customThread

def main():
    stack_worker = customThread(target='stack', args=(1,2,3,))
    stack_worker.setName('stack worker')
    stack_worker.start()

    queue_worker = customThread(name='queue worker', target='queue',args = (1,2,3,),)
    queue_worker.start()

if __name__ == '__main__':
    main()