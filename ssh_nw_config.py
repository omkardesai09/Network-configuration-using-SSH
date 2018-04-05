import paramiko
import time
import re
import subprocess
import os

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
        #print ip_octets
        if (len(ip_octets) == 4) and (1 <= int(ip_octets[0]) <= 223) and (int(ip_octets[0]) != 127) and (int(ip_octets[0]) != 169 or int(ip_octets[1]) != 254) and (0 <= int(ip_octets[1]) <= 255 and 0 <= int(ip_octets[2]) <= 255 and 0 <= int(ip_octets[3]) <= 255):
            continue

        else:
            print "Invaid IP address: %s \n Please correct." %str(".".join(ip_octets))
            continue

    # Check device's reachability using subprocess.call method

    print "\n Code is checking all device's reachability.\n Please wait...\n"

    flag = False
    for ip in list_of_ip:
        ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])

        if ping_reply == 0:
            flag = True
            continue

        elif ping_reply == 1 or ping_reply == 2:
            flag = False
            break

        else:
            flag = False
            break

    if flag == True:
        print "Awesome!!! All devices are reachable.\n"

    elif flag == False:
        print "Oh! Devices are not reachable. Please check IP addresses and connectivity again.\n"
        #valid_ip()

# Check for credential's file is available or not

def credential_file():
    global cred_file
    cred_file = raw_input("\n Enter filename where credentials are stored: ")
    while True:
        if os.path.isfile(cred_file) == True:
            break
        else:
            print "\n File does not exist. Please try again.\n"
            continue

valid_ip()
credential_file()