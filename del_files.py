# -*- coding: UTF-8 -*-
__author__ = 'bobo'

'''
note:the scripts will delete dir which like "path/IP/2017-xx-xx",for example:/home/backup/10.1.1.148/2017-09-19
class：
    host_path:match path/ip from path which has set
    check_dir:check son dir and judge whether matching your rules
    del_dir:del dir

use：
1.set path your environment
2.set time for normal files and log file to del
3.set host list
'''
import os
import re
import shutil
from datetime import datetime


time_now = datetime.now()
path = '/home/backup'
#set time for delete
common_day = 30
log_day = 180
log_host = ['10.1.1.145','10.1.1.155']

class clean:
    def __init__(self,base_path):
        self.base_path = base_path

    def host_path(self):
        host_path = list(os.listdir(self.base_path))
        for i in range(len(host_path)):
            #re to match path:base_path/IP
            host_rep = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
            if host_rep.match(host_path[i]):
                host_dir = host_path[i]
                self.check_dir(host_dir)

    def check_dir(self,dir):
        host_dir = os.path.join(self.base_path,dir)
        back_dir = os.listdir(host_dir)
        for i in range(len(back_dir)):
            back_time = datetime.strptime(back_dir[i],"%Y-%m-%d")
            day_value = time_now - back_time
            day_sub = day_value.days
            if dir in log_host:   
                if day_sub > log_day:
                    del_dir = os.path.join(host_dir,back_dir[i])
                    self.del_dir(del_dir)
                else:
                    print "dir %s/%s backup at %s,it's under %s天，system will skip it" %(host_dir,back_dir[i],back_time,log_day)
            else:
                if day_sub > common_day:
                    del_dir = os.path.join(host_dir,back_dir[i])
                    self.del_dir(del_dir)
                else:
                    print "dir %s/%s backup at %s,it's under %s天，system will skip it" %(host_dir,back_dir[i],back_time,common_day)
    def del_dir(self,dir):
        shutil.rmtree(dir)
clean(path).host_path()
