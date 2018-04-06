
# Network configuration using SSH

The main objective of this project is to connect multiple devices in the topology via Virtualbox VM host and configure network commands on it.

Python script will create multiple threads to work on multiple devices at the same time.  

### Prerequisites

Build the topology as shown in screenshot.png in GSN3 to check output. Virtualbox VM (Debian 7) is used as a host in GNS topology.

Create following text files:
ssh_ip_list.txt ==> Which contains a list of IP addresses of devices present in the topology
ssh_cmd.txt     ==> Which contains commands to configure on devices
credentials.txt ==> Which contains username and password separated by comma

### Initial Configurations on router(R1)

Refer Initial_config_R1.txt and Initial_config_R2.txt files and do similar steps on router R1 and R2.

### Final Steps

Run ssh_nw_config.py script on host (Debian 7 VM) 