# /bin/env python
#coding=utf8

import salt.config
import salt.key
import salt.client
import os


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
    ret = status()
    for target in ret['down']:
        cmdstr = "salt-ssh '%s' -r  'sudo /etc/init.d/salt-minion restart'" % target
        os.system(cmdstr)


