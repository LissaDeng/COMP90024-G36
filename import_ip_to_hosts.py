#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import json

ip_file = open("/home/ubuntu/ansible/ip_address", "r") 
hosts = open("/home/ubuntu/ansible/hosts", "w")

line = ip_file.readline()
ip_list = json.loads(line)

webserver = ip_list[0]
harvester1 = ip_list[1]
harvester2 = ip_list[2]
harvester3 = ip_list[3]

#single node
hosts.write("[webserver]\n")
hosts.write(webserver+"\n\n")
hosts.write("[harvester1]\n")
hosts.write(harvester1+"\n\n")
hosts.write("[harvester2]\n")
hosts.write(harvester2+"\n\n")
hosts.write("[harvester3]\n")
hosts.write(harvester3+"\n\n")

#group info
hosts.write("[harvester]\n")
hosts.write(harvester1+"\n")
hosts.write(harvester2+"\n")
hosts.write(harvester3+"\n\n")

hosts.write("[db_master]\n")
hosts.write(webserver+"\n\n")

hosts.write("[db_slave]\n")
hosts.write(harvester1+"\n")
hosts.write(harvester2+"\n")
hosts.write(harvester3+"\n\n")



hosts.write("[all:vars]\nansible_ssh_user=ubuntu\nansible_ssh_private_key_file=/home/ubuntu/ansible/second.pem")

ip_file.close()
hosts.close()

print("import hosts success\n")
