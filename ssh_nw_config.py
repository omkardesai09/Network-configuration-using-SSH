import paramiko
import time
import re
import subprocess
import os.path
import sys
import threading

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

    while True:
        cred_file = raw_input("\n Enter filename where credentials are stored: ")
        if os.path.isfile(cred_file) == True:
            break
        else:
            print "\n File does not exist. Please try again.\n"
            continue


def command_file():
    global cmd_file

    while True:
        cmd_file = raw_input("\n Enter filename where commands are stored: ")
        if os.path.isfile(cmd_file) == True:
            break
        else:
            print "\n File does not exist. Please try again.\n"
            continue

valid_ip()
credential_file()
command_file()

# Function to setup SSH connection with all devices

def ssh_conn(ip):
    file2 = open(cred_file, 'r')
    file2.seek(0)
    username = file2.readlines()[0].split(",")[0]
    file2.seek(0)
    password = file2.readlines()[0].split(",")[1].rstrip('\n')

    # Logging into device
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to a device using username and password
    session.connect(ip, username = username, password = password)

    # Invoke shell inside device
    conn = session.invoke_shell()

    # Write following command on device's shell using send function
    conn.send('enable\n')
    time.sleep(1)
    conn.send(password + '\n')
    time.sleep(1)
    conn.send('terminal length 0\n')
    time.sleep(1)
    #conn.send('sh run | include int\n')
    #time.sleep(1)

    # Open Command file to configure devices
    file3 = open(cmd_file, 'r')
    file3.seek(0)
    for lines in file3.readlines():
        conn.send(lines + '\n')
        time.sleep(2)

    # Close credentials and command file
    file2.close()
    file3.close()

    # Checking shell output of device and print on local host
    output = conn.recv(65535)
    time.sleep(1)
    print output + '\n'
    session.close()

# Implement threading

def thread_func():
    thread = []
    for ip in list_of_ip:
        th = threading.Thread(target = ssh_conn, args = (ip,))
        th.start()
        thread.append(th)
    for th in thread:
        th.join()

thread_func()