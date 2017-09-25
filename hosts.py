# -*- coding:utf-8 -*-
__author__ = 'bobo'

#the file is config file


#base_path in your dest server
base_path = '/home/backup/'

#it can be null if your server's ssh port is 22
#################################################################################################################
#nginx
nginx_servers = ['10.1.1.184:9022','10.1.1.185:9022']
nginx_items = ['/etc/nginx/conf.d','/etc/nginx/nginx.conf','/home/config','/var/log/nginx/*.gz']

#jenkins
jenkins_servers = ['172.16.20.18']
jenkins_items = ['/home/jenkins']

#phpredis
phpredis_servers = ['172.16.20.49']
phpredis_items = ['/etc/nginx/nginx.conf','/etc/nginx/nginx.d','/var/www']

#keepalived
keepalived_servers = ['10.1.1.186:9022','10.1.1.176:9022']
keepalived_items = ['/etc/keepalived/keepalived.conf']

#nexus
nexus_servers = ['10.1.1.40:22']
nexus_items = ['/home/nexus-2.14.0-01','/home/sonatype-work']

#################################################################################################################
###sqlinfo,sql_databases must be dict
#sql_servers = ['host:ssh_port:mysql_user:mysql_passwd']
#sql_databases = {'host':'database1:database2:databasen'}

sql_servers = ['192.168.110.4:22:root','192.168.110.5:22:root:123456']
sql_databases = {'192.168.110.4':'zentao:test1:test2','192.168.110.5':'mysql:test1:test2'}
#################################################################################################################
#svn,items must be dict
svn_servers = ['10.1.1.231']
svn_items = {'10.1.1.231':'/home/Repositories/abcd;/home/Repositories/main:/home/Repositories/manager'}
#################################################################################################################
