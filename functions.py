# -*- coding:utf-8 -*-
__author__ = 'bobo'

import subprocess,os
import time
import re
import paramiko
import logging

time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#####################################################################################################################
#split to get your server's info for connection for your config file
def hp(server):
    servers = re.split(':',server)
    server = servers[0]
    try:
        port = servers[1]
    except:
        port = '22'
    try:
        user = servers[2]
    except:
        user = 'root'
    try:
        passwd = servers[3]
    except:
        passwd = 0
    return server,port,user,passwd

#check dest dir , if not exist,it will create
def dir(base,server,time_now):
    path = '%s%s/%s' %(base,server,time_now)
    if os.path.isdir(path):
        pass
    else:
        os.makedirs(path)
    return path

#connect ssh
def ssh(server,port,cmd):
    try:
        #set ssh-keygen to connect remote server
        pkeyfile = '/root/.ssh/id_rsa'
        key = paramiko.RSAKey.from_private_key_file(pkeyfile)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(server,port,timeout=5,pkey=key)
        cmd_status = 1
        stdin,stdout,stderr = ssh.exec_command(cmd)
        print '%s: %scmd has sent sucessfuly\n' %(server,cmd)
        err = stderr.readlines()
        for msg in err:
            #tak out blanks and line break
            msg = msg.strip()
            log(msg,server)
            cmd_status = 0
        ssh.close()
    except BaseException,e:
        print '%s\tssh login failed!! error:%s\n' %(server,e)
        log(e,server)
        cmd_status = 0
    return cmd_status   
#write error log
def log(msg,host=0):
    logging.basicConfig(level=logging.WARNING,
                format = '%(asctime)s %(filename)s[line %(lineno)d]: %(message)s',
                datefmt = '%b %d %Y %H:%M:%S',
                filename = '/home/backup/logs/backup_error.log',
                filemode = 'a')
    message = '%s %s %s' %(msg,'targethost:',host)
    logging.error(message)

#####################################################################################################################
#get file from remote server cycles
def get_file(servers,items,base_path):
    for i in range(len(servers)):
        servers_port = hp(servers[i])
        servers[i] = servers_port[0]
        port = servers_port[1]
        for j in range(len(items)):
             dir_dest = dir(base_path,servers[i],time_now)
             back_files(servers[i], items[j],port,dir_dest)
             time.sleep(0.5)

#function for get_file
def back_files(server,item,port,dest):
    if item[-2:]=='gz':
        print ".gz file ,it will be remove after geting "
        cmd = '%s%s:%s %s %s' % ('/usr/bin/rsync -aucvvLzP --remove-source-files --progress root@', server, item, dest,'-e \'ssh -p '+port+'\'')
    else:
        cmd = '%s%s:%s %s %s' % ('/usr/bin/rsync -aucvvLzP --progress root@', server, item, dest,'-e \'ssh -p '+port+'\'')
    try:
        result = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE)
        stderr = result.stderr.readlines()
        for msg in stderr:
            msg = msg.strip()
            log(msg,server)
        result.wait()
    except Exception,e:
        print '%s:%s' %('backup failed',e)
        log(e,server)
#########################################################
#get sql from remote server cycles
def get_sql(servers,items,base_path,user=0,passwd=0):
    for i in range(len(servers)):
        host = hp(servers[i])
        servers[i] = host[0]
        port = host[1]
        user = host[2]
        passwd = host[3]
        #get server and database from dict
        items1 = items[servers[i]]
        #get database from databases
        item_server = re.split(':',items1)
        for j in range(len(item_server)):
             dir_dest = dir(base_path,servers[i],time_now)
             sql_sucess = backup_sqls(servers[i],port,item_server[j],user,passwd)
             #not sucess to backup,it will skip this database
             if sql_sucess == 0:
                print '%s:%s backup failed,system will skip it' %(servers[i],item_server[j])
                continue
             #get dir of remote server
             sql_src = '%s%s' %(sql_path,item_server[j])
             #get sql file from remote server
             get_back_files(servers[i], sql_src,port,dir_dest)
             time.sleep(0.5)
#exec remote sql cmd
#you must insure /usr/bin/mysqldump exists and it's avaliable
def backup_sqls(server,port,database,user_sql,passwd_sql=0):
    port = int(port)
    #passwd_sql==0 if sql passwd is null
    mysqldump = '/usr/bin/mysqldump -u'
    global sql_path
    sql_path = '/home/'
    if passwd_sql == 0:
        cmd = '%s %s %s %s %s%s' %(mysqldump,user_sql,database,'>',sql_path,database)
    else:
        cmd = '%s %s %s%s %s %s %s%s' %(mysqldump,user_sql, '-p',passwd_sql,database,'>',sql_path,database)
    sql_sucess = ssh(server,port,cmd)
    return sql_sucess
#########################################################
##get svn file from remote server cycles
def get_svn(servers,items,base_path):
    for server in servers:
        host = hp(server)
        server = host[0]
        port = host[1]
        #get file you want to backup from dict
        items1 = items[server]
        items = re.split(':',items1)
        for item in items:
             dir_dest = dir(base_path,server,time_now)
             svn_sucess,svn_path = backup_svn(server,item,port,base_path)
             #if not sucess to backup,system will skip it
             if svn_sucess == 0:
                print '%s:%s backup failed,system will skip it' %(servers,svn_path)
                continue
             #get svn dir from remote server
             svn_src = '%s%s' %(svn_path,'.svn')
             print svn_src
             #get svn_file
             get_back_files(servers,svn_src,port,dir_dest)
             time.sleep(0.5)

#function to backup svn file
def backup_svn(server,item,port,base_path):
    port = int(port)
    #get son dir
    p = re.compile(r'^/[A-Za-z0-9]*/')
    path = p.sub(r'',item)
    svn_path = "%s%s" %(base_path,path)
    mkdir = "mkdir -p %s" %(svn_path)
    ssh(server,port,mkdir)
    #exec remote cmd to backup svn
    cmd = "/usr/bin/svnadmin dump %s > %s.svn" %(item,svn_path)
    svn_sucess = ssh(server,port,cmd)
    svn_sucess = 1
    return svn_sucess,svn_path
#########################################################
#####################################################################################################################