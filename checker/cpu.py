#!/usr/bin/env python
# -*- coding:utf8 -*-
#abc
__author__='haibo.zhang'

from . import CheckerBase
import pickle
import time
import os
import json
from optparse import OptionParser 

class Checker(CheckerBase):
    def __init__(self,filepath="/proc/stat"):
        super(Checker,self).__init__()
        self.stat_path=filepath
        self.pickle_path="/var/run/cpu.pickle"
        self.cpucount=0
        if os.path.exists(self.pickle_path):
            self.old_data=pickle.load(open(self.pickle_path, "r"))
        else:
            self.old_data={}
    def _get_raw_data(self):
        kvps={}
        fh=open(self.stat_path,"r")
        keylines=fh.readlines()
        fh.close()
        for line in keylines:
            kv_list=line.split()
            kvps.update({kv_list[0]:kv_list[1:]})
        return kvps
    def get_cpucount(self):
        kvps={}
        fh=open(self.stat_path,"r")
        keylines=fh.readlines()
        fh.close()
        for line in keylines:
            kv_list=line.split()
            if kv_list[0][0:3] == "cpu":
                self.cpucount+=1
        return self.cpucount-1
    def _get_current_value(self,key):
        stat_data=self._get_raw_data()
        return stat_data[key]
    def get_values(self,key):
        if len(self.old_data.keys()) != 0:
            old_data=self.old_data
        else:
            old_data={}
        current_raw_data=self._get_raw_data()
        idle = current_raw_data["cpu"][3]
        cputime=0
        for i in current_raw_data["cpu"]:
            cputime +=long(i)
        cputime_idle={}
        cputime_idle.update({"cputime":cputime})
        cputime_idle.update({"idle":idle})
        current_data={}
        current_data.update({"time":time.time()})
        current_data.update({"cputime":cputime})
        current_data.update({"cputime_idle":cputime_idle})
        current_data.update({"idle":current_raw_data["cpu"][3]})
        current_data.update({"iowait":current_raw_data["cpu"][4]})
        current_data.update({"irq":current_raw_data["cpu"][5]})
        current_data.update({"softirq":current_raw_data["cpu"][6]})
        if len(old_data.keys()) == 0:
            pickle.dump(current_data, open(self.pickle_path, "w"))
            return 0
        if key == "useage":
            #interval = long(current_data["time"] - old_data["time"])
            value = ((((long(cputime)- long(idle))) - (long(old_data["cputime_idle"]["cputime"]) - long(old_data["cputime_idle"]["idle"]))) / float(long(cputime) - long(old_data["cputime_idle"]["cputime"])))*100
            value = str("%.2f"%value)
            #print current_data
            #print old_data
            #print "enter usage"
        else:
            value = (long(current_data[key]) - long(old_data[key]))/100
            value = int (value)
            #print "enter other"
        if (current_data["time"] - old_data["time"]) > 30:
            pickle.dump(current_data, open(self.pickle_path, "w"))
        return value

    def do_check_cputime(self):
        current_raw_data = self._get_raw_data()
        cputime = 0
        for i in current_raw_data["cpu"]:
            cputime +=long(i)
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path,"r"))
            if "cputime" in o_data.keys():
                o_cputime = o_data["cputime"]
                o_data["cputime"] = cputime
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return int((long(cputime) - long(o_cputime))/100)
            else:
                o_data.update({"cputime":cputime})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            o_data.update({"cputime":cputime})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0
    
    def do_check_idle(self):
        current_raw_data = self._get_raw_data()
        idle = current_raw_data["cpu"][3]
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path,"r"))
            if "idle" in o_data.keys():
                o_idle = o_data["idle"]
                o_data["idle"] = idle
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return int((long(idle) - long(o_idle))/100)
            else:
                o_data.update({"idle":idle})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            o_data.update({"idle":idle})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0
    
    def do_check_iowait(self):
        current_raw_data = self._get_raw_data()
        iowait = current_raw_data["cpu"][4]
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path,"r"))
            if "iowait" in o_data.keys():
                o_iowait = o_data["iowait"]
                o_data["iowait"] = iowait
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return int((long(iowait) - long(o_iowait))/100)
            else:
                o_data.update({"iowait":iowait})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            o_data.update({"iowait":iowait})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0

    def do_check_hard_interrupt(self):
        current_raw_data = self._get_raw_data()
        irq = current_raw_data["cpu"][5]
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path,"r"))
            if "irq" in o_data.keys():
                o_irq = o_data["irq"]
                o_data["irq"] = irq
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return int((long(irq) - long(o_irq))/100)
            else:
                o_data.update({"irq":irq})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            o_data.update({"irq":irq})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0

    def do_check_soft_interrupt(self):
        current_raw_data = self._get_raw_data()
        softirq = current_raw_data["cpu"][6]
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path,"r"))
            if "softirq" in o_data.keys():
                o_softirq = o_data["softirq"]
                o_data["softirq"] = softirq
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return int((long(softirq) - long(o_softirq))/100)
            else:
                o_data.update({"softirq":softirq})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            o_data.update({"softirq":softirq})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0

    def do_check_cpu_usage(self):
        current_raw_data = self._get_raw_data()
        cputime = 0
        for time in current_raw_data["cpu"]:
            cputime += long(time)
        idle = current_raw_data["cpu"][3]
        if os.path.exists(self.pickle_path):
            o_data = pickle.load(open(self.pickle_path, "r"))
            if "cputime_idle" in o_data.keys():
                o_cputime = o_data["cputime_idle"]["cputime"]
                o_idle = o_data["cputime_idle"]["idle"]
                o_data["cputime_idle"]["cputime"]= cputime
                o_data["cputime_idle"]["idle"] = idle
                pickle.dump(o_data, open(self.pickle_path, "w"))
                value = ((((long(cputime) - long(idle))) - (long(o_cputime) - long(o_idle)))/float(long(cputime) - long(o_cputime)))*100
                value = str("%.2f"%value)
                return value
            else:
                cputime_idle={}
                cputime_idle.update({"cputime":cputime})
                cputime_idle.update({"idle":idle})
                o_data.update({"cputime_idle":cputime_idle})
                pickle.dump(o_data, open(self.pickle_path, "w"))
                return 0
        else:
            o_data={}
            cputime_idle={}
            cputime_idle.update({"cputime":cputime})
            cputime_idle.update({"idle":idle})
            o_data.update({"cputime_idle":cputime_idle})
            pickle.dump(o_data, open(self.pickle_path, "w"))
            return 0

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a","--argument",dest="arg")
    options,agrs = parser.parse_args()
    cpu=CPU("/proc/stat")
    print cpu.do_check_iowait()
        
    
