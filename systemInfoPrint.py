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

'''
"%s-70s\n" "System Information
"%70s\n" "-"*30
%-17s%=30s\n
'''

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


now = datetime.datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

Title = '  System Information  '


print Title.center(90,'-'),
print now_time


# First row
print " CPU ".center(25,'-')

# Second Row
string_left_sort("Logical Count",20,0)
string_right_sort(str(psutil.cpu_count()),5,1)


# Third Row
string_left_sort("Physical Count",20,0)
string_right_sort(str(psutil.cpu_count(logical=False)),5,1)

# Fourth Row
print '%22s' % ( "CPU Usage : " + str(psutil.cpu_percent()))

print ("CPU Usage : " + str(psutil.cpu_percent())).center(25,' ')



psutil.cpu_count()

psutil.cpu_count(logical=False)

psutil.swap_memory().total/1024/1024
psutil.virtual_memory().total/1024/1024

MEM_INFO = psutil.swap_memory()
#print MEM_INFO
#print psutil.virtual_memory()

