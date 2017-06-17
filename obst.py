#!/usr/bin/python

import socket,os,time,commands

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(("",8888))

while True:

	#data will recieve drive name
	data=s.recvfrom(20)
	dn=data[0]
	#data1 will recieve drive size in M
	data1=s.recvfrom(20)
	ds=data1[0]
	#data2 will recieve drive format
	data2=s.recvfrom(5)
	df=data2[0]
	#Address of client
	cliaddr=data1[1][0]
	#Creating LVM 
	os.system("lvcreate --name "+dn+" --size "+ds+"M vg1")
	#Formating LVM
	os.system("mkfs."+df+" -f /dev/vg1/"+dn)
	#Creating mounting point
	os.system('mkdir /mnt/'+dn)
	#Mounting the drive locally
	os.system('mount /dev/vg1/'+dn+' /mnt/'+dn)
	#Installing nfs-utils
	os.system('yum install nfs-utils -y')
	#Entry in nfs export file
	entry="/mnt/"+dn+' '+cliaddr+'(rw,no_root_squash)\n'
	#Append the entry into etc/exports file
	f=open('/etc/exports','a')
	f.write(entry)
	f.close()
	#Nfs service & persistant (first time)
	"""
	os.system('systemctl restart nfs-server')
	os.system('systemctl enabled nfs-server')
	"""
	#Checking the export file
	check=os.system('exportfs -r')
	if check==0:
		s.sendto("done",data1[1])
	else :
		print "ERROR !!!"
