#!/usr/bin/python

import os,sys,time,socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_ip="192.168.122.124"
s_port=8888

#Name of the drive
d_name=raw_input("Enter the name of Drive : ")
#Size of the drive
d_size=raw_input("Enter the size in M : ")
#Format for drive
d_format=raw_input("Enter the format of Drive (xfs,ext4,ext3,ext2,vfat) : ")

s.sendto(d_name,(s_ip,s_port))
s.sendto(d_size,(s_ip,s_port))
s.sendto(d_format,(s_ip,s_port))

res=s.recvfrom(4)
if res[0]=='done':
	os.system('mkdir /media/'+d_name)
	os.system('mount '+s_ip+':/mnt/'+d_name+' /media/'+d_name)
else :
	print 'No response from storage cloud'

