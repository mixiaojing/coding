#encoding=utf-8
import telnetlib, sys
from time import sleep
import threading
import sys
import time
import os
import imp

USER= 'Administrator'
PASS = 'jdsu'
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
########################################################################################################################################################################
#####################################################################
#for ping the chassis to sure the chassis is up
def Ping(Logfilename):
    Pingtong=0
    command = 'ping '+Logfilename['chassis_name']  # 可以直接在命令行中执行的命令
    r = os.popen(command)  # 执行该命令
    info = r.readlines()  # 读取命令行的输出到一个list
    if info[3].find("TTL=")>=1:
       Logfile_py.Logfile('Chassis can be ping succeffully', Logfilename)
       Pingtong=1
    else:
       Logfile_py.Logfile('Chasis can not be ping', Logfilename)
       Pingtong=0
    return Pingtong

#####wreite license into xigilicense.txt and check the license####
####################################################################
######reboot the chassis ####

def Reboot_chassis(Logfilename):
    tn = telnetlib.Telnet()
    try:
        tn.open(Logfilename['IP'])
        print 'connect Host successfully'
    except:
        print "Cannot open host"
    tn.write('\r\n')
    tn.read_until("login:")
    tn.write(USER + '\r\n')

    tn.read_until("password")
    tn.write(PASS + '\r\n')
    tn.read_until('>',5)
    tn.write('reboot'+'\r\n')
    tn.read_until('>',5)
    print tn.read_until('reboot',5)
    print "reboot command have been delivered ,now waiting for reboot"
    Logfile_py.Logfile('reboot command have been delivered ,now waiting for reboot', Logfilename)
    tn.close()

    ####wait for chassis to up######
    Logfile_py.Logfile('Chassis is rebooting and waiting for the chassis up', Logfilename)
    Logfile_py.Logfile('Wait 180s', Logfilename)
    time.sleep(180)

####################################################################
class telnetdo(object):
    def __init__(self, Logfilename,license_number,result):
        self.chassis_name=Logfilename['chassis_name']
        self.Logfilename=Logfilename
        self.result=result
        self.license_number = license_number

    def telnetdo_oldmethod_add(self):
        time.sleep(3)
        Ping(self.Logfilename)
        tn = telnetlib.Telnet()
        try:
            tn.open(self.chassis_name)
     #       print 'connect Host successfully'
            Logfile_py.Logfile('connect Host successfully ', self.Logfilename)
        except:
     #       print "Cannot open host"
            Logfile_py.Logfile('Can not open host ,exit ', self.Logfilename)

            return
        tn.write('\r\n')
        tn.read_until("login:")
        tn.write(USER + '\r\n')
        tn.read_until("password")
        tn.write(PASS + '\r\n')
        tn.read_until(">")
        tn.write('F:\Finisar\GTX-A\LicenseAgent.exe -w 1 '+self.license_number + '\r\n')
        tn.read_until(">")
        tn.write('F:\Finisar\GTX-A\LicenseAgent.exe -q 1' + '\r\n')
        tmp=tn.read_until(">")
 #       print tmp
        #Check the license have been writen into the Xgiglicense.txt#
        License_update = 0
        if tmp.find(self.license_number)>=0:
            Logfile_py.Logfile('Successfully replace license txt ' + self.license_number + ' into chassis license txt',self.Logfilename)

        else:
            Logfile_py.Logfile('fail to replace license txt ' + self.license_number + ' into chassis license txt',self.Logfilename)
            self.result['False'] = self.result['False'] + 1
    #   Logfile_py.Logfile(tn.write('type F:\\Finisar\\FrameWork\\version.txt'+ '\r\n'),chassis_name)
        tn.close()
        return self.result

    def telnetdo_newmethod_add(self):
        time.sleep(3)
        Ping(self.Logfilename)
        tn = telnetlib.Telnet()
        try:
            tn.open(self.chassis_name)
            #       print 'connect Host successfully'
            Logfile_py.Logfile('connect Host successfully ', self.Logfilename)
        except:
            #       print "Cannot open host"
            Logfile_py.Logfile('Can not open host ,exit ', self.Logfilename)
            exit()
            return
        tn.write('\r\n')
        tn.read_until("login:")
        tn.write(USER + '\r\n')

        tn.read_until("password")
        tn.write(PASS + '\r\n')

        tn.write('del C:\\xgiglicenses.txt' + '\r\n')
        print tn.read_until(">")

        tn.write('echo JDSU > C:\\xgiglicenses.txt' + '\r\n')
        print tn.read_until(">")

        tn.write('echo \r\n >> C:\\xgiglicenses.txt' + '\r\n')
        print tn.read_until(">")

        tn.write('echo ' + self.license_number + '>> C:\\xgiglicenses.txt' + '\r\n')
        tn.read_until('>', 5)

        tn.write('type C:\\xgiglicenses.txt' + '\r\n')
        tmp = tn.read_until(self.license_number)
        print tmp
        # Check the license have been writen into the Xgiglicense.txt#
        License_update = 0
        if tmp.find(self.license_number) >= 0:
            Logfile_py.Logfile('Successfully replace license txt ' + self.license_number + ' into chassis license txt',
                               self.Logfilename)

        else:
            Logfile_py.Logfile('Fail to replace license txt ' + self.license_number + ' into chassis license txt',
                               self.Logfilename)
            self.result['False'] = self.result['False'] + 1

            #   Logfile_py.Logfile(tn.write('type F:\\Finisar\\FrameWork\\version.txt'+ '\r\n'),chassis_name)
        tn.close()
        return self.result

    def telnetdo_oldmethod_del(self):
        time.sleep(3)
        Ping(self.Logfilename)
        tn = telnetlib.Telnet()
        try:
            tn.open(self.chassis_name)
            #       print 'connect Host successfully'
            Logfile_py.Logfile('connect Host successfully ', self.Logfilename)
        except:
            #       print "Cannot open host"
            Logfile_py.Logfile('Can not open host ,exit ', self.Logfilename)
            exit()
            return
        tn.write('\r\n')
        tn.read_until("login:")
        tn.write(USER + '\r\n')
        tn.read_until("password")
        tn.write(PASS + '\r\n')
        tn.read_until(">")
        tn.write('F:\Finisar\GTX-A\LicenseAgent.exe -e 1 4*1' + '\r\n')
        tn.read_until(">")
        tn.write('F:\Finisar\GTX-A\LicenseAgent.exe -q 1' + '\r\n')
        tmp = tn.read_until(">")
        #       print tmp
        # Check the license have been writen into the Xgiglicense.txt#
        License_update = 0
        if tmp.find(self.license_number) >=0:
            Logfile_py.Logfile('fail to delete license txt' + self.license_number,self.Logfilename)
            self.result['False'] = self.result['False'] + 1

        else:
            Logfile_py.Logfile('Successful to delete license ' + self.license_number,self.Logfilename)
            #   Logfile_py.Logfile(tn.write('type F:\\Finisar\\FrameWork\\version.txt'+ '\r\n'),chassis_name)
        tn.close()
        return self.result


###the main function ,provide more action to control the telnet ######
	###The thread is used to control the time for forcing closing the telnet ,because the telnet number is limited####
def telnet_main(Logfilename,license_number,result):

    Logfile_py.Logfile('1.start to update license ' + license_number, Logfilename)

    ###Chassis remote accournt and passowrd#
    update=telnetdo(Logfilename,license_number,result)
    result=update.telnetdo_newmethod_add()
  #  t1=threading.Thread(target=A)
 #   t1.start()
 #   t1.join(30)

    #####reboot the chasssis####
    if result['False']==0:
        Logfile_py.Logfile('2.reboot the chassis to make license effect', Logfilename)
        Reboot_chassis(Logfilename)
    ###for different chassis ,need to update waiting time to make sure chassis is up dan TCAPI CAN WORK
        Logfile_py.Logfile('finish update license', Logfilename)
    return result
    #############################################################################################

