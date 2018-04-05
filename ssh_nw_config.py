import paramiko
import time
import re

# To check IP addresses mentioned in file are valid or not
def valid_ip():
    check = False
    global list_of_ip

    file_ip = raw_input("Enter file name containing list of IP addresses: ")

    try:
        file1 = open(file_ip,'r')
        file1.seek(0)
        list_of_ip = file1.readlines()
        file1.close()

        for ip in list_of_ip:
            print ip

    except IOError:
        print "File %s does not exist" %file_ip

        # Check IP address is valid or not

    for ip in list_of_ip:
        ip_octets = ip.split('.')
        ip_octets[3] = ip_octets[3].strip('\n')
        print ip_octets
        if (len(ip_octets) == 4) and (1 <= int(ip_octets[0]) <= 223) and (int(ip_octets[0]) != 127) and (int(ip_octets[0]) != 169 or int(ip_octets[1]) != 254) and (0 <= int(ip_octets[1]) <= 255 and 0 <= int(ip_octets[2]) <= 255 and 0 <= int(ip_octets[3]) <= 255):
            continue

        else:
            print "Invaid IP address: %s \n Please correct." %str(".".join(ip_octets))
            continue

valid_ip()