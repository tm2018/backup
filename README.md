####note
```
The program can help you to backup config files or sql(mysql) and svn files,it is avaliabled in linux
```

####py file
```
hosts.py:it's your config file which record your server port sqluser sqlpasswd and so on
functions.py:functions to realize
main.py:call functions.py to backup
del_files.py:it will delete files from your backup server automatically
```
####use
```
1.exec "yum -y install rsync" in your src server
2.copy py files to your dest server
3.write your server,port,sqlinfo in hosts.py
4.set ssh-keyon in your src and dest server
5."python main.py" to test
6.set crontab rule as your need 
```

####others
```
please edit "~/.ssh/config" in your dest server and restart sshd:
#vi ~/.ssh/config
StrictHostKeyChecking no
UserKnownHostsFile /dev/null

```# backup
