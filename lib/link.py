#!/usr/bin/env python
#-*- coding:utf8 -*-

from gevent.queue import Queue

class Chanels(object):
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Chanels, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance
    def __init__(self):
        self._queue_list={}
    def append(self,queuename):
        #setattr(self, queuename, Queue())
        if not self._queue_list.has_key(queuename):
            self._queue_list[queuename]=Queue()
        return True
    
    def __getitem__(self,key):
        return self._queue_list.get(key,None)
    
    def __contains__(self,key):
        if key in self._queue_list.keys():
            return True
        else:
            return False