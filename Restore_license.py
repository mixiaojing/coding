import imp
import telnetlib
import time

#######This file is filed to update lidense to chassis ############
file, path, desc = imp.find_module('telnet')
print file, path, desc
Telnet_update_license_py = imp.load_module("telnet", file, path, desc)
#####################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################

def Restore(Logfilename,result):
    USER='Administrator'
    PASS='jdsu'

    license={
        'SQA-SING90':['ATBSZFGANQEDPZ8XT3CNYEBHWZFQRVPS'],
        'SQA-SING61':['AQGM7NGBJ08DPZ8HT3CNYHJRHK6ZCH01','AQGM7NGB229DPZ8HT3CNYK48873MHZ99'],
        'SQA-SING63':['AXGXHG0CJB4DPZ8HT3CNZAS3KZZ8DZ09','ASGXHG0CJQMFPZ8HT3CNYDVHSK6Q8A8Z','ASGXHG0CNFMFYZ8HT3CNYPMK44HW9FM1','A9GXHG0CJB4DPZ8HT3CNZAHJGPSHV4B1','ASGXHG0CMF4FPZ8HT3CNYH599JBZHKE0',
                 'ASGXHG0CNQMFPZ8HT3CNZCZNRJC2YMJT','AXGXHG0CMV4DPZ8HT3CNZX8ZGZKSK807'],
        'SQA-SING82':['ASYXGR0DJZ4DPF8HT3CNZQCB394AS3NF']
    }

    tn = telnetlib.Telnet(Logfilename['IP'])
    tn.open(Logfilename['IP'])
    tn.write('\r\n')
    tn.read_until("login:")
    tn.write(USER + '\r\n')
    tn.write(PASS + '\r\n')
    tn.read_until("password")
    tn.write('del C:\\xgiglicenses.txt'+ '\r\n')
    print tn.read_until(">")
    tn.write('echo JDSU > C:\\xgiglicenses.txt' + '\r\n')
    print tn.read_until(">")

    for i in range(0,len(license[Logfilename['chassis_name']])):
        tn.write('echo \r\n >> C:\\xgiglicenses.txt' + '\r\n')
        time.sleep(1)
        tn.write('echo ' + license[Logfilename['chassis_name']][i] + '>> C:\\xgiglicenses.txt' + '\r\n')
        time.sleep(1)
        tn.write('type C:\\xgiglicenses.txt' + '\r\n')
        tn.write('dir' + '\r\n')
        tmp = tn.read_until('free', 5)
        if tmp.find(license[Logfilename['chassis_name']][i]) >= 1:
            Logfile_py.Logfile('Successfully restore license  ' + license[Logfilename['chassis_name']][i] + ' into chassis license txt',Logfilename)
        else:
            Logfile_py.Logfile('Fail to restore license txt ' + license[Logfilename['chassis_name']][i]+ ' into chassis license txt',Logfilename)
            result['False']=result['False']+1

    tn.close()
    Telnet_update_license_py.Reboot_chassis(Logfilename)
