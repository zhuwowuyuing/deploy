# /bin/env python

import salt.client
import MySQLdb
import types


conn=MySQLdb.connect(host="192.168.1.92", port=3316, user="deploy",passwd="deploy",db="deploy")
cursor = conn.cursor()

cursor.execute("TRUNCATE table salt_MachineInfo_diskinfo")
cursor.execute("TRUNCATE table salt_MachineInfo_interfaceinfo")
cursor.execute("TRUNCATE table salt_MachineInfo_errorinfo")
cursor.execute("SET FOREIGN_KEY_CHECKS=0")
cursor.execute("TRUNCATE table salt_MachineInfo_baseinfo")
cursor.execute("SET FOREIGN_KEY_CHECKS=1")
cursor.execute("ALTER TABLE salt_MachineInfo_diskinfo AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE salt_MachineInfo_interfaceinfo AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE salt_MachineInfo_errorinfo AUTO_INCREMENT = 1")
conn.commit()

cli = salt.client.LocalClient()

machineInfo = cli.cmd('*', 'grains.item', ['cpu_model', 'osfullname', 'osrelease', 'osarch', 'kernelrelease', 'num_cpus', 'manufacturer', 'mem_total', 'productname'])
diskInfo = cli.cmd('*', 'status.diskusage', ['ext?'])
networkInfo = cli.cmd('*', 'network.interfaces')
activeInfo = cli.cmd('*', 'test.ping')

for (hostname, Info) in machineInfo.items():
	if type(Info) is not types.DictType:
		cursor.execute("INSERT INTO salt_MachineInfo_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get disk data"))
		continue
	status 		= str(activeInfo.get(hostname, False))
	cpu_model	= Info.get('cpu_model', '')
	num_cpus	= Info.get('num_cpus', '')
	mem_total	= Info.get('mem_total', '')
	os		= Info.get('osfullname', '') + ' ' + Info.get('osrelease', '') + ' ' + Info.get('osarch', '') + ' '+ Info.get('kernelrelease', '')
	manufacturer    = Info.get('manufacturer', '')
	productname     = Info.get('productname', '')
#	print "%s, %s, %s, %d, %d, %s, %s, %s" % (hostname, status, cpu_model, num_cpus, mem_total, productname, manufacturer, os)
	cursor.execute("INSERT into salt_MachineInfo_baseinfo(hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os) VALUES(%s, %s, %s,%s, %s, %s, %s, %s)", (hostname, status, cpu_model, num_cpus, mem_total, manufacturer, productname, os))
	conn.commit()

for (hostname, diskusage) in diskInfo.items():
#	print hostname
	if not machineInfo.has_key(hostname):
		cursor.execute("INSERT INTO salt_MachineInfo_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Baseinfo no this Machine"))
		continue
	if type(diskusage) is not types.DictType:
		cursor.execute("INSERT INTO salt_MachineInfo_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get disk data"))
		continue
	for (mount, info) in diskusage.items():
#		print "%s, %s" % (hostname, mount)
		available	= info.get('available', 0)
		total		= info.get('total', 0)
		print hostname
		cursor.execute("INSERT into salt_MachineInfo_diskinfo(hostname_id, mount, available, total) VALUES(%s,%s,%s,%s)", (hostname, mount, available, total))
		conn.commit()

for (hostname, interface) in networkInfo.items():
	if not machineInfo.has_key(hostname):
		cursor.execute("INSERT INTO salt_MachineInfo_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Baseinfo no this Machine"))
		continue
	if type(interface) is not types.DictType:
		cursor.execute("INSERT INTO salt_MachineInfo_errorinfo(hostname, info) VALUE(%s, %s)", (hostname, "Can not get network interface data"))
                continue
	for (device, info) in interface.items():
		if not info.has_key('inet') or not cmp(device, 'lo'):
			continue
		hwaddr =	info.get('hwaddr', '')
		ipaddr =	((info['inet'])[0])['address']

		cursor.execute("INSERT into salt_MachineInfo_interfaceinfo(hostname_id, interface, hwaddr, ipaddr) VALUES(%s,%s,%s,%s)", (hostname,device, hwaddr, ipaddr))
		conn.commit()

conn.commit()
cursor.close()
conn.close()

