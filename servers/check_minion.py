# /bin/env python
#coding=utf8

import salt.config
import salt.key
import salt.client
import commands
import MySQLdb

# 全局变量，读取master的配置文件
__opts__ = salt.config.master_config('/etc/salt/master')

# 获取各minion的状态
def status():
    client = salt.client.LocalClient(__opts__['conf_file'])
    minions = client.cmd('*', 'test.ping', timeout=__opts__['timeout'])

    key = salt.key.Key(__opts__)
    keys = key.list_keys()
    ret = {}
    ret['up'] = sorted(minions)
    ret['down'] = sorted(set(keys['minions']) - set(minions))
    return ret

# 重启down的minion
if __name__ == '__main__':
    # connect database
    host="192.168.1.31"
    port=3759
    user="deploy"
    passwd="deploy"
    db="deploy"
    conn=MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cursor = conn.cursor()
    cursor.execute("TRUNCATE table servers_checkerror")
    conn.commit()

    ret = status()
    i=0
    for target in ret['down']:
        i+=1
        cmdstr = "salt-ssh '%s' -r  'sudo /etc/init.d/salt-minion restart' " % target
        (status, output) = commands.getstatusoutput(cmdstr)
        print "%d: %s %s"%(i, status, output)
        if output:
            retcode = int(output.split('\n')[3])
        else:
            retcode = 1
            output = "no response message"
        if retcode != 0:
            cursor.execute("INSERT INTO servers_checkerror(TIME, hostname, errormsg) VALUES(NOW(), %s, %s)", (target, output))
    conn.commit()
    cursor.close()
    conn.close()







