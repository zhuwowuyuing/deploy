# /bin/env python

import salt.config
import salt.client
import MySQLdb
import types

# connect database
host="192.168.0.118"
port=3306
user="deploy"
password="deploy"
db="deploy"

# get grains.item, status.diskusage, network.interfaces, test.ping value
def get_info():
    opts = salt.config.master_config('/etc/salt/master')
    client = salt.client.LocalClient(opts['conf_file'])
    grains_items_args = ['cpu_model', 'osfullname', 'osrelease', 'osarch', 'kernelrelease', \
                         'num_cpus', 'manufacturer', 'mem_total', 'productname', 'idc', 'ingw']
    disk_args = ['ext?']

    result = client.cmd('*', ['grains.item', 'status.diskusage', 'network.interfaces', 'test.ping'], [grains_items_args, disk_args, [], []],\
                        timeout=opts['timeout'])

    return result

# is  table server_baseinfo  have hostname record ?
def is_exist(cursor, hostname):
    sql = "select hostname from servers_baseinfo where hostname=%s"
    if 1 == cursor.execute(sql, (hostname,)):
        return 1
    else:
        return 0

def update_info(manchine_info, cursor):
    for (hostname, info) in manchine_info.items():
        grains = info.get('grains.item', '')
        network = info.get('network.interfaces', '')
        disk = info.get('status.diskusage', '')
        status = info.get('test.ping', False)

        if grains:
            update_baseinfo(hostname, grains, status, cursor)

        machine_exist = is_exist(cursor, hostname)

        if disk:
            update_disk(hostname, disk, cursor, machine_exist)

        if network:
            update_network(hostname, network, cursor, machine_exist)

# update baseinfo data
def update_baseinfo(hostname, items, status, cursor):
    if type(items) is not types.DictType:
        sql = "INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)"
        err_msg = "Can not get grains items"
        cursor.execute(sql, (hostname, err_msg))
        return

    status	        = str(status)
    cpu_model	    = items.get('cpu_model', '')
    num_cpus	    = items.get('num_cpus', '')
    mem_total	    = items.get('mem_total', '')
    os		        = items.get('osfullname', '') + ' ' + items.get('osrelease', '') + ' ' + \
                        items.get('osarch', '') + ' '+ items.get('kernelrelease', '')
    manufacturer    = items.get('manufacturer', '')
    productname     = items.get('productname', '')
    idc             = items.get('idc', '')
    ingw            = items.get('ingw', '')

    lines           = cursor.execute("select hostname from servers_baseinfo where hostname=%s", (hostname,))

    if lines == 0:
        sql = "INSERT into servers_baseinfo(hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os, idc,ingw) \
                  VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os, idc, ingw))
    elif lines == 1 :
        sql = "update servers_baseinfo set status=%s, cpu_model=%s, num_cpus=%s, mem_total=%s, manufacturer=%s, productname=%s, \
                  os=%s, idc=%s, ingw=%s where hostname=%s"
        cursor.execute(sql,(status, cpu_model, num_cpus, mem_total, manufacturer, productname, os,idc, ingw, hostname))

# update disk data
def update_disk(hostname, items, cursor, machine_exist):
    if not machine_exist:
        sql = "INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)"
        errmsg = "Can get disks info,but baseinfo no this Machine"
        cursor.execute(sql, (hostname, errmsg))

    if type(items) is not types.DictType:
        cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get disk data"))
        return

    for (mount, info) in items.items():
        available	= info.get('available', 0)
        total		= info.get('total', 0)
        lines       = cursor.execute("select hostname_id, mount from servers_diskinfo where hostname_id=%s and mount=%s", \
                                 (hostname,mount,))

        lines       = cursor.execute("select hostname_id, mount from servers_diskinfo where hostname_id=%s and mount=%s", \
                                     (hostname,mount,))
        if lines == 0:
            sql = "INSERT into servers_diskinfo(hostname_id, mount, available, total) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (hostname, mount, available, total))
        elif lines == 1:
            sql = "update servers_diskinfo set available=%s,  total=%s where hostname_id=%s and mount=%s"
            cursor.execute(sql, (available, total,hostname,mount))

# update network data
def update_network(hostname, items, cursor, machine_exist):
    if not machine_exist:
        sql = "INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)"
        errmsg = "Can get network data, but baseinfo no this Machine"
        cursor.execute(sql, (hostname, errmsg))

    if type(items) is not types.DictType:
        sql = "INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)"
        errmsg = "Can not get network interface data"
        cursor.execute(sql, (hostname, errmsg))
        return

    for (interface, info) in items.items():
        if not info.has_key('inet') or not cmp(interface, 'lo'):
            continue

        hwaddr =	info.get('hwaddr', '')
        ipaddr =	((info['inet'])[0])['address']

        lines       = cursor.execute("select hostname_id, interface from servers_networkinfo where hostname_id=%s and interface=%s", \
                                 (hostname, interface,))
        if lines == 0:
            sql = "INSERT into servers_networkinfo(hostname_id, interface, hwaddr, ipaddr) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (hostname, interface, hwaddr, ipaddr))
        elif lines == 1:
            sql = "update servers_networkinfo set hwaddr=%s,  ipaddr=%s where hostname_id=%s and interface=%s"
            cursor.execute(sql, (hwaddr, ipaddr, hostname,interface))

if __name__ == '__main__':
    conn=MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db)
    conn.autocommit(1)
    cursor = conn.cursor()
    machine_info = get_info()
    update_info(machine_info, cursor)
    conn.commit()
    cursor.close()
    conn.close()
