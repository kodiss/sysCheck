import sys, os, commands
import psutil, platform
import json
import datetime
from colorama import init, Fore, Back, Style

'''
==================================================================================
                                 systemInfoPrint.py
==================================================================================
@ Explain
Print Current System infomation
 - Resource : Total and Used resource such as CPU, MEM, Disk and etc..
 - Information : Hardware Vendor, Model Name,
 - DBMS : DBMS NAME, Mode, Process Info
@ Description
# Script name : systemInfoPrint.py
# compile PyVersion : 2.7.12
# purpose : Read the json file for System information
            Get the System's current resource status.
            Print Every Information.
# Update History
   - 2017.03.23 : initial compile (th1227.kim@samsung.com, kodiss@naver.com)
'''
# Variable
JSON_FILE_NAME = 'envCheckSys.json'
CPU_WARNING_THRESHOLD = 80
CPU_CRITICAL_THRESHOLD = 90
MEM_WARNING_THRESHOLD = 80
MEM_CRITICAL_THRESHOLD = 90
CPU_AVG_THRESHOLD = (psutil.cpu_count() * 1.3)


def string_left_sort(str, totalSize, enterOrNot=1):
    if enterOrNot is 1:
        print str.ljust(totalSize)
    else:
        print str.ljust(totalSize),

def string_right_sort(str, totalSize, enterOrNot=1):
    if enterOrNot is 1:
        print str.rjust(totalSize)
    else:
        print str.rjust(totalSize),

def string_center_sort(str, totalSize, enterOrNot=1):
    if enterOrNot is 1:
        print str.center(totalSize)
    else:
        print str.center(totalSize),

def print_systemInfo():
    # load the json file
    SystemInfo = json.loads(open(JSON_FILE_NAME).read())

    # make the Current datetime data
    now = datetime.datetime.now()
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    Title = '  System Information  '

    # Title
    print Title.center(102,'-'),
    print now_time

    # System detailed Information
    print '|'.center(1),


    print "Hostname :".ljust(15),
    print SystemInfo['HOST_NAME'].center(20),
    print '|'.center(2),

    print "H/W :".ljust(10),
    print (SystemInfo['MACHINE_VENDOR'] + " / " + SystemInfo['MACHINE_NAME']).center(25),
    print '|'.center(2),

    print "Serial :".ljust(15),
    print SystemInfo['SERIAL_NUMBER'].center(20),
    print '|'.center(2)

    print '|'.center(1),

    print "CPU(Logi/Physi/Core) :".ljust(15),
    print (str(psutil.cpu_count()) + ' / ' + str(psutil.cpu_count(logical=False)) + ' / ' + cpuSpeed).center(53),
    print '|'.center(2),

    print "Physical MEM :".ljust(15),
    print (str(round(psutil.virtual_memory().total/1024/1024/1024)) +' GB').center(20),
    print '|'.center(2),
    print

    print '|'.center(1),

    print "OS VER :".ljust(15),
    print SystemInfo['OS_VERSION'].center(20),
    print '|'.center(2),

    print "Kernel :".ljust(15),
    print SystemInfo['KERNEL_VERSION'].center(20),
    print '|'.center(2),

    print "HA MODE :".ljust(15),
    print SystemInfo['HA_MODE'].center(20),
    print '|'.center(2)


    if SystemInfo['DBMS_NAME'] is not 'none':
        print "  DBMS Information  ".center(122,'-')

        print '|'.center(1),
        print "DBMS :".ljust(10),
        print SystemInfo['DBMS_NAME'].center(25),
        print '|'.center(2),

        print "DB SID :".ljust(10),
        print SystemInfo['DB_SID'].center(25),
        print '|'.center(2),

        print "DB Mode :".ljust(10),
        print SystemInfo['DB_MODE'].center(25),
        print '|'.center(2),
        print

    # First row
    print "  Resource Information  ".center(122, '-')
    print '|'.center(1),
    print " CPU ".center(27,'-'),
    print '|'.center(1),
    print " ",
    print " MEM ".center(27, '-'),
    print '|'.center(1),
    print " ",
    print " SWAP ".center(27, '-'),
    print '|'.center(1),
    print " ",
    print " ? ".center(22, '-'),
    print '|'.center(1),
    print " "

    # Third Row
    print '|'.center(1),
    if float(cpuAvg) > CPU_AVG_THRESHOLD:
        print (Back.RED + Fore.WHITE + "CPU Avg(/5Min)".ljust(15)),
        print (cpuAvg.rjust(10)),
        print(Back.RESET + Fore.RESET),
    else:
        print "CPU Avg(/5Min)".ljust(15),
        print cpuAvg.rjust(11),
    print '|'.center(2),

    print "Used (GB)".ljust(15),
    print Used_MEM.rjust(12),
    print '|'.center(2),

    print "Used/Total (GB)".ljust(15),
    print (Used_SWAP + ' / ' + Total_SWAP).rjust(12),
    print '|'.center(2)

    # Fourth Row

    print '|'.center(1),
    if UsedP_CPU > CPU_WARNING_THRESHOLD:
        print(Back.RED + Fore.WHITE  + "Usage (%)".ljust(15)),
        print((str(UsedP_CPU) + ' %').rjust(10)),
        print(Back.RESET + Fore.RESET),
    elif UsedP_CPU > CPU_WARNING_THRESHOLD:
        print(Back.YELLOW + Fore.WHITE + "Usage (%)".ljust(15)),
        print((str(UsedP_CPU) + ' %').rjust(11)),
        print(Back.RESET + Fore.RESET),
    else:
        print("Usage (%)".ljust(15)),
        print((str(UsedP_CPU) + ' %').rjust(11)),
    print '|'.center(2),


    if UsedP_MEM > MEM_CRITICAL_THRESHOLD:
        print(Back.RED + Fore.WHITE  + "Usage (%)".ljust(15)),
        print((str(UsedP_MEM) + ' %').rjust(12)),
        print(Back.RESET + Fore.RESET),
    elif UsedP_MEM > MEM_WARNING_THRESHOLD:
        print(Back.YELLOW + Fore.WHITE + "Usage (%)".ljust(15)),
        print((str(UsedP_MEM) + ' %').rjust(12)),
        print(Back.RESET + Fore.RESET),
    else:
        print("Usage (%)".ljust(15)),
        print((str(UsedP_MEM) + ' %').rjust(12)),
    print '|'.center(2),

    print "Usage (%)".ljust(15),
    print (str(Used_SWAP) + ' %').rjust(12),
    print '|'.center(2)

    print "  Process Information  ".center(122, '-')

if __name__ == "__main__":

    # get the System Current Information
    uptime = commands.getoutput('uptime')
    cpuAvg = uptime.split()[8][:-1]
    cpuSpeed = commands.getoutput('cat /proc/cpuinfo  | grep -i "model name" | tail -1').split(':')[1]
    Used_SWAP = str(round(float(psutil.swap_memory().used) / 1024 / 1024 / 1024,1))
    Total_SWAP = str(round(float(psutil.swap_memory().total)/1024/1024/1024,1))
    UsedP_CPU = round(psutil.cpu_percent())
    UsedP_MEM = round(psutil.virtual_memory().percent)
    Used_MEM = str(round(float(psutil.virtual_memory().used) / 1024 / 1024 / 1024))
    UsedP_SWAP = round(psutil.swap_memory().percent)


    print_systemInfo()
