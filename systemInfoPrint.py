import sys, os, commands
import psutil, platform
import json
import datetime

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
    string_center_sort('|', 1, 0)

    string_left_sort("Hostname :",15,0)
    string_center_sort(SystemInfo['HOST_NAME'],20,0)
    string_center_sort('|',1,0)
    print " ",

    string_left_sort("H/W :",10,0)
    string_center_sort(SystemInfo['MACHINE_VENDOR'] + " / " + SystemInfo['MACHINE_NAME'],25,0)
    string_center_sort('|', 1, 0)
    print " ",

    string_left_sort("Serial :",15,0)
    string_center_sort(SystemInfo['SERIAL_NUMBER'],20,0)
    string_center_sort('|', 1, 0)
    print " ",
    print

    string_center_sort('|', 1, 0)

    string_left_sort("CPU(Logi/Physi/Core):",20,0)
    string_center_sort(str(psutil.cpu_count())+' / '+str(psutil.cpu_count(logical=False)) + ' / ' + cpuSpeed,55,0)
    string_center_sort('|',1,0)
    print " ",

    string_left_sort("Physical MEM :",15,0)
    string_center_sort(str(round(psutil.virtual_memory().total/1024/1024/1024)) +' GB',20,0)
    string_center_sort('|', 1, 0)
    print " ",
    print

    string_center_sort('|', 1, 0)


    string_left_sort("OS VER :",15,0)
    string_center_sort(SystemInfo['OS_VERSION'],20,0)
    string_center_sort('|', 1, 0)
    print " ",

    string_left_sort("Kernel :",15,0)
    string_center_sort(SystemInfo['KERNEL_VERSION'],20,0)
    string_center_sort('|', 1, 0)
    print " ",

    string_left_sort("HA MODE :",15,0)
    string_center_sort(SystemInfo['HA_MODE'],20,0)
    string_center_sort('|', 1, 0)
    print " ",
    print


    if SystemInfo['DBMS_NAME'] is not 'none':
        print "  DBMS Information  ".center(122,'-')
        string_center_sort('|', 1, 0)

        string_left_sort("DBMS :", 10, 0)
        string_center_sort(SystemInfo['DBMS_NAME'], 25, 0)
        string_center_sort('|', 1, 0)
        print " ",

        string_left_sort("DB SID :", 10, 0)
        string_center_sort(SystemInfo['DB_SID'], 25, 0)
        string_center_sort('|', 1, 0)
        print " ",

        string_left_sort("DB Mode :", 10, 0)
        string_center_sort(SystemInfo['DB_MODE'], 25, 0)
        string_center_sort('|', 1, 0)
        print " ",
        print

    # First row
    print "  Resource Information  ".center(122, '-')
    string_center_sort('|', 1, 0)
    print " CPU ".center(27,'-'),
    string_center_sort('|', 1, 0)
    print " ",
    print " MEM ".center(27, '-'),
    string_center_sort('|', 1, 0)
    print " ",
    print " SWAP ".center(27, '-'),
    string_center_sort('|', 1, 0)
    print " ",
    print " ? ".center(22, '-'),
    string_center_sort('|', 1, 0)
    print " ",
    print

    # Third Row
    string_center_sort('|', 1, 0)
    string_left_sort("CPU Avg(/5Min)",15,0)
    string_right_sort(cpuAvg,10,0)
    string_center_sort('|', 4, 0)

    string_left_sort("Used (GB)",15,0)
    Used_MEM = str(round(psutil.virtual_memory().used/1024/1024/1024))
    string_right_sort(Used_MEM,10,0)
    string_center_sort('|', 4, 0)

    string_left_sort("Used/Total (GB)",15,0)
    Used_SWAP = str(round(psutil.swap_memory().used/1024/1024/1024))
    Total_SWAP = str(round(psutil.swap_memory().total / 1024 / 1024 / 1024))
    string_right_sort(Used_SWAP + ' / ' + Total_SWAP,10,0)
    string_center_sort('|', 4, 0)

    print

    # Fourth Row
    string_center_sort('|', 1, 0)
    string_left_sort("Usage (%)", 15, 0)
    UsedP_CPU = str(round(psutil.cpu_percent()))
    string_right_sort( UsedP_CPU + '%', 10, 0)
    string_center_sort('|', 4, 0)

    string_left_sort("Usage (%)",15,0)
    UsedP_MEM = str(round(psutil.virtual_memory().percent)) + '%'
    string_right_sort(UsedP_MEM,10,0)
    string_center_sort('|', 4, 0)

    string_left_sort("Usage (%)",15,0)
    UsedP_SWAP = str(round(psutil.swap_memory().percent)) + '%'
    string_right_sort(UsedP_SWAP,10,0)
    string_center_sort('|', 4, 0)

    print

if __name__ == "__main__":
    uptime = commands.getoutput('uptime')
    cpuAvg = uptime.split()[8][:-1]
    cpuSpeed = commands.getoutput('cat /proc/cpuinfo  | grep -i "model name" | tail -1').split(':')[1]

    print_systemInfo()
