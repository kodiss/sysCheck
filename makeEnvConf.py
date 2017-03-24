import sys, os, commands
import psutil, platform
import json
from datetime import datetime

'''
==================================================================================
                                 makeEnvConf.py
==================================================================================
@ Explain
Get the System default information.
This information also save to json file.
Using this information, check the system status when run thee sysCheckMain.py

@ Description
# Script name : makeEnvConf.py
# compile PyVersion : 2.7.12
# purpose : make the json file from system information
# Update History
   - 2017.03.23 : initial compile (th1227.kim@samsung.com, kodiss@naver.com)
'''
# Variable
NETWORK_FS_TYPE = ('nfs', 'cifs', 'smb', 'samba')
JSON_FILE_NAME = 'envCheckSys.json'

'''
    "DBMS_NAME": "kind of DBMS like oracle, ppas, mysql, sap hana and etc",
    "DB_MODE": "DB Cluster mode like rac, single",
    "DB_SID": "IF it is DB, Database ID",
    "FS_TOTAL_COUNT": total mounted filesystem count,
    "HA_MODE": "Cluster S/W such as serviceguard, powerha",
    "HOST_NAME": "hostname",
    "KERNEL_VERSION": "OS Current Kernel Version",
    "LSNR_COUNT": If is is oracle, the Listener process count,
    "MACHINE_NAME": "Hardware Model Name",
    "MACHINE_VENDOR": "Hardware Vendor",
    "NETWORK_FS_COUNT": 'totla mounted filesystem like nfs, samba',
    "ORACLE_HOME": "Oracle HOME PATH or none",
    "ORACLE_LOG": "Oracle LOG PATH or none",
    "OS_ARCHITECTURE": "Hardware Architecture such as x86_64 or x86",
    "OS_VERSION": "OS Detailed version such as Redhat, Suse, Ubuntu",
    "SCRIPT_PATH": "this script's path",
    "SERIAL_NUMBER": "Hardware Serial Number"
'''

# System Basic Information
Total_Info = platform.uname()
# Total_Info
# ('Linux', 'kodiss-VirtualBox', '4.8.0-41-generic', '#44~16.04.1-Ubuntu SMP Fri Mar 3 17:11:16 UTC 2017', 'x86_64', 'x86_64')

SystemInfo={}
SystemInfo['HOST_NAME'] = Total_Info[1]
SystemInfo['KERNEL_VERSION'] = Total_Info[2]
SystemInfo['OS_ARCHITECTURE'] = Total_Info[5]
SystemInfo['OS_VERSION'] = commands.getoutput('lsb_release -a | grep -i description').split(':')[1].strip()


# Filesystem information
SystemInfo['FS_TOTAL_COUNT'] = len(commands.getoutput('df -hP').split('\n')[1:])

# from 'mount' command, get and search the network filesystem type

MountInfo = commands.getoutput('mount').split('\n')
for line in MountInfo:
    NetworkFSCount = 0
    FsType = line.split()[4]
    if FsType in NETWORK_FS_TYPE:
        NetworkFSCount = NetworkFSCount + 1

SystemInfo['NETWORK_FS_COUNT'] = NetworkFSCount

SystemInfo['HA_MODE'] = 'Need to Update(serviceguard, powerha, steeleye, etc, none)'

# DBMS Information
DBInfo = commands.getstatusoutput('ps -ef | grep -i -e pmon -e hdbindexserver -e postgre -e mysql -e mssql| grep -v grep')

if DBInfo[0] is 256:
    SystemInfo['DBMS_NAME'] = 'none'
    SystemInfo['DB_MODE'] = 'none'
    SystemInfo['DB_SID'] = 'none'
else:
    DB_Process = DBInfo[1].split('\n')
    DBCount = 0
    SystemInfo['DB_MODE'] = 'Need to Update(rac, single, none)'
    for line in DB_Process:
        if line[8].find('oracle'):
            SystemInfo['DBMS_NAME'] = 'oracle'
            DBCount = DBCount + 1
        elif line[8].find('hdbindexserver'):
            SystemInfo['DBMS_NAME'] = 'sap hana'
            DBCount = DBCount + 1
        elif line[8].find('ppas'):
            SystemInfo['DBMS_NAME'] = 'postgres'
            DBCount = DBCount + 1
        elif line[8].find('mysql'):
            SystemInfo['DBMS_NAME'] = 'mysql'
            DBCount = DBCount + 1
        elif line[8].find('mariadb'):
            SystemInfo['DBMS_NAME'] = 'mariadb'
            DBCount = DBCount + 1
        SystemInfo['DB_SID'] = 'Need to Update DB SID'
        SystemInfo['DB_HOME'] = 'Need to update(Path or none)'
        SystemInfo['DB_LOG'] = 'Need to update(Path or none)'

if SystemInfo['DBMS_NAME'] is 'oracle':
    ListenerInfo = commands.getoutput('ps -ef | grep -i tns | grep -v grep')
    SystemInfo['LSNR_COUNT'] = len(ListenerInfo.split('\n'))

SerialNumber = commands.getoutput('dmidecode -s system-serial-number')
if SerialNumber is 0:
    SystemInfo['SERIAL_NUMBER'] = 'virtualmachine'
else:
    SystemInfo['SERIAL_NUMBER'] = SerialNumber

SystemInfo['MACHINE_VENDOR'] = commands.getoutput('dmidecode -s bios-vendor | tail -1')
SystemInfo['MACHINE_NAME'] = commands.getoutput('dmidecode -s system-product-name | tail -1')

pathname = os.path.dirname(sys.argv[0])
SystemInfo['SCRIPT_PATH'] = os.path.abspath(pathname)

fileTime = datetime.now().strftime('%Y%m%d_%H%M%S')
if (os.path.isfile(JSON_FILE_NAME)):
    os.rename(JSON_FILE_NAME, JSON_FILE_NAME +'.' + fileTime)

with open(JSON_FILE_NAME,'w') as outfile:
    json.dump(SystemInfo, outfile, sort_keys=True, indent=4)
outfile.close()



