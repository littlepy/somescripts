import paramiko
import time



class SSH:
	def __init__(self, ip, port, username, password):
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password

	def sshClient(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.ip, port=self.port,
					username=self.username, password=self.password)
		return ssh

	def sftpClient(self):
		ts = paramiko.Transport((self.ip, self.port))
		ts.connect(username=self.username, password=self.password)
		sftp = paramiko.SFTPClient.from_transport(ts)
		return sftp

	def generateLocalFile(self):
		local_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
		filename = str(int(time.time()))+'.req'
		with open(filename, 'w') as file:
			file.write("This file is sended by '9.112.36.149'\n")
			file.write("Sender is Songlihong.\n")
			file.write("My server time is:\n")
			file.write(f"{local_time}\n\n")
			file.write("--------------------------\n\n")
			file.write("Your server time and ip address:\n")
		return filename

	def execComand(self):
		cmd = "ifconfig | grep inet| grep -v inet6 | awk '{print $2}'|awk -F: '{print $2}'"
		_, stdout, stderr = self.ssh.exec_command(cmd)
		result = stdout.read()
		if not result:
			result = stderr.read()
		return result


	def runForever(self):
		while True:
			try:
				self.ssh = self.sshClient()
				self.sftp = self.sftpClient()
				if all((self.ssh, self.sftp)):
					break
			except (paramiko.SSHException, TimeoutError, Exception) as e:
				print(e)
				continue
		while True:
			file = self.generateLocalFile()
			self.sftp.put(file, f'/root/upfile/{file}')
			self.ssh.exec_command(f"date +'%Y-%m-%d %H:%M:%S' >> /root/upfile/{file}")
			self.ssh.exec_command(f"echo '{self.execComand().decode('utf8')}' >> /root/upfile/{file}")
			self.ssh.exec_command(f"dos2unix /root/upfile/{file}")
			print(self.ssh)
			print(self.sftp)
			time.sleep(30)



if __name__ == '__main__':
	# host = ('9.112.45.248', 8388)
	host = ('192.168.100.100', 22)
	ssh = SSH(host[0], host[1], 'root', 'song')
	ssh.runForever()





