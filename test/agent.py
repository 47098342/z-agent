#!/usr/bin/env python2.7
# -*- coding:utf8 -*-

from gevent import monkey
monkey.patch_all()

import os
import time
import click

import gevent
from gevent.threadpool import ThreadPool
from gevent.queue import Queue,Empty
from gevent.event import AsyncResult
from gevent.lock import BoundedSemaphore
from gevent.pool import Pool

from gevent.baseserver import StreamServer


def main(args):
    pass

def daemon(func,args=None):
    __doc__ = '''
    name: daemon
    description: daemonize main process
    input:
          None
    output:
          None
    '''
    pid=os.fork();
    if pid > 0:
        sys.exit(0);
    elif pid == 0:
        os.chdir("/");
        os.umask(0);
        os.setsid();
        pid2=os.fork();
        if pid2 > 0:
            logger.info("daemon start with pid: {0}".format(pid2))
            open("/var/run/compress_logfile.pid","w").write("%s"%pid2);
        elif pid2 == 0:
            for f in sys.stdout, sys.stderr: f.flush();
            si = file("/dev/null", 'r');
            so = open("/var/log/agent.log",'a');
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(so.fileno(), sys.stderr.fileno())
            if args:
                func(args);
            else:
                func();
        else:
            print("2 fork failed");
    else:
        print("fork failed!");

class MainProcess(gevent.Greenlet):
    def __init__(self, run=None,*args, **kwargs):
        super(MainProcess,self).__init__(run=run,*args,**kwargs)
    def _run(self):
        gevent.sleep(10)
        print("haha")

#evt=AsyncResult()
evt=Queue()
b = BoundedSemaphore(1)
def t1():
    global evt,b
    while True:
        try:
            with b:
                data=evt.get(timeout=2)
            if data:
                print("1 recv data: %s"%data)
        except Empty:
            gevent.sleep(1)

def t2():
    global evt
    for i in xrange(20000):
        evt.put(i)
        print("put: %d"%i)
    return "over"

def t3():
    global evt,b
    while True:
        try:
            with b:
                data=evt.get(timeout=2)
            if data:
                print("2 recv data: %s"%data)
        except Empty:
            gevent.sleep(1)

def cb(result):
    print(result)


class Agent(object):
    def __init__(self):
        import os
        if not os.path.exists("/var/lib/z-agent"):
            os.mkdir("/var/lib/z-agent")
    @classmethod
    def main(cls,*args,**kwarg):
        pool =ThreadPool(4)
        #启动命令接口器
        #启动
        #pool.spawn(t1)
        #pool.spawn(t3)
        #pool.spawn(t2)

if __name__ == "__main__":
    Agent.main()
