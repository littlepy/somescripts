#!/opt/python/bin/python
# -*- coding: utf-8 -*-

'''
商业银行服务端口扫描脚本
Songlihong in Sunyard
2016.03.23
'''


import socket
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

def netcat(localaddress, ip , port , timeout=2):
	try:
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cs.bind(localaddress)
		cs.settimeout(float(timeout))
		address=(str(ip),int(port))
		status = cs.connect_ex((address))
		if status == 0 :
			return True
	except Exception as e:
		print "error: {}".format(e)
	finally:
        cs.close()
	return False
    
    
def get_nods(inifile):
    NODES = []
    SECTION = 'ADDR LIST'
    cf = ConfigParser()
    cf.read(inifile)
    nodes = cf.options(SECTION)
    for n in nodes:
        value = cf.get(SECTION, n).split()[0].split(':')
        node, ip, port = n, value[0], value[1]
        NODES.append((node, ip, port))
    return NODES

    
    
if __name__ == '__main__':
    nodes = get_nods('/home/iccs/etc/tcp.ini')
    localaddress = ('172.31.101.100', 0)
    for node in nodes:
        if node[0] != '150':
            status = netcat(localaddress, node[1], node[2])
            if status:
                print("Node {}:\t\t OK！".format(node))
            else:
                print("Node {}:\t\t FAILED！".format(node))
        
    


