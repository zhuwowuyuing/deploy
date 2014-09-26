# /bin/env python

import salt.client
import MySQLdb
import types


conn=MySQLdb.connect(host="192.168.1.92", port=3316, user="deploy",passwd="deploy",db="deploy")
cursor = conn.cursor()

cursor.execute("TRUNCATE table servers_diskinfo")
cursor.execute("TRUNCATE table servers_networkinfo")
cursor.execute("TRUNCATE table servers_errorinfo")
# cursor.execute("SET FOREIGN_KEY_CHECKS=0")
# cursor.execute("TRUNCATE table servers_baseinfo")
# cursor.execute("SET FOREIGN_KEY_CHECKS=1")
cursor.execute("ALTER TABLE servers_diskinfo AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE servers_networkinfo AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE servers_errorinfo AUTO_INCREMENT = 1")
conn.commit()

cli = salt.client.LocalClient()

machineInfo = cli.cmd('*', 'grains.item', ['cpu_model', 'osfullname', 'osrelease', 'osarch', 'kernelrelease', 'num_cpus', 'manufacturer', 'mem_total', 'productname'])
diskInfo = cli.cmd('*', 'status.diskusage', ['ext?'])
networkInfo = cli.cmd('*', 'network.interfaces')
activeInfo = cli.cmd('*', 'test.ping')

for (hostname, Info) in machineInfo.items():
	if type(Info) is not types.DictType:
		cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get grains items"))
		continue
	status 		    = str(activeInfo.get(hostname, False))
	cpu_model	    = Info.get('cpu_model', '')
	num_cpus	    = Info.get('num_cpus', '')
	mem_total	    = Info.get('mem_total', '')
	os		        = Info.get('osfullname', '') + ' ' + Info.get('osrelease', '') + ' ' + Info.get('osarch', '') + ' '+ Info.get('kernelrelease', '')
	manufacturer    = Info.get('manufacturer', '')
	productname     = Info.get('productname', '')
    lines           = cursor.execute("select hostname from servers_baseinfo where hostname=%s", (hostname,))

	if lines == 0:
        	cursor.execute("INSERT into servers_baseinfo(hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os) \
                       VALUES(%s, %s, %s,%s, %s, %s, %s, %s)",\
                       (hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os))
	elif lines == 1 :
        	cursor.execute("update servers_baseinfo set status=%s, cpu_model=%s, num_cpus=%s, mem_total=%s, manufacturer=%s, productname=%s, os=%s where hostname=%s",(status, cpu_model, num_cpus, mem_total, manufacturer, productname, os,hostname))

conn.commit()

for (hostname, diskusage) in diskInfo.items():
#	print hostname
	if not machineInfo.has_key(hostname):
		cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can get disks info,but baseinfo no this Machine"))
		continue
	if type(diskusage) is not types.DictType:
		cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get disk data"))
		continue

	for (mount, info) in diskusage.items():
		available	= info.get('available', 0)
		total		= info.get('total', 0)

		cursor.execute("INSERT into servers_diskinfo(hostname_id, mount, available, total) VALUES(%s,%s,%s,%s)", (hostname, mount, available, total))

conn.commit()

for (hostname, interface) in networkInfo.items():
	if not machineInfo.has_key(hostname):
		cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can get network interface data, but baseinfo no this Machine"))
		continue
	if type(interface) is not types.DictType:
		cursor.execute("INSERT INTO servers_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get network interface data"))
                continue
	for (device, info) in interface.items():
		if not info.has_key('inet') or not cmp(device, 'lo'):
			continue
		hwaddr =	info.get('hwaddr', '')
		ipaddr =	((info['inet'])[0])['address']

		cursor.execute("INSERT into servers_networkinfo(hostname_id, interface, hwaddr, ipaddr) VALUES(%s,%s,%s,%s)", (hostname,device, hwaddr, ipaddr))
        conn.commit()

conn.commit()
cursor.close()
conn.close()
