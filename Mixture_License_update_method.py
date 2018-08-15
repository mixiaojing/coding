# encoding=utf-8
#####However, we want to test chassis that has old licenses programmed on the EEPROM and we add new license scheme.
# You don’t need old app kit to program the license to the EEPROM.
# Use the licenseagent application to program it then continue with your test for the new licensing scheme.
# The test cases are to add license on blade/chassis which already had license(s) programmed in the EEPROM -> the mixtures of old and new licenses.
# 1 for new methold ,2 for old method

import sys
import imp
import time
import os
import random

### 获取 上一层目录 并且加入到sys。path中，这样就能找到下面的文件了
#sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
#os.chdir(os.path.abspath(os.path.dirname(os.getcwd())))

#########################################################################################################################################################################
file, path, desc = imp.find_module('main_test')
print file, path, desc
main_test_py = imp.load_module("main_test", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################
#######This file is filed to update lidense to chassis ############
file, path, desc = imp.find_module('telnet')
print file, path, desc
Telnet_update_license_py = imp.load_module("telnet", file, path, desc)
#########################################################################################################################################################################
#########################################################################################################################################################################
file, path, desc = imp.find_module('Read_protocol_speed_configuration_for_TCAPI')
print file, path, desc
Read_protocol_speed_configuration_for_TCAPI_py = imp.load_module("Read_protocol_speed_configuration_for_TCAPI", file, path, desc)
#########################################################################################################################################################################

#########################################################################################################################################################################

def Mixturetesting(Logfilename, configuration):
    #######################################################
    f = open(Logfilename['chassis_name']+'_'+ Logfilename['APPKIT']+'_'+ Logfilename['StartTime']+'_TestResult.txt','a')
    f.write('#############below two license is for mixture license testing ##########' + '\n')
    f.close()
    #######################################################################################
    ###### random to selete 2 from configuration for test
    Number = random.sample(configuration, 2)

    Logfile_py.Logfile("##########################################################################################################",Logfilename)
    Logfile_py.Logfile(configuration[Number[0]]['number'] + ' is test for old method ,use Agenlicencemanagement to write license',Logfilename)
    Logfile_py.Logfile(configuration[Number[1]]['number'] + ' is test for new method:use C:\Xgigliense.txt to write license',Logfilename)
    Logfile_py.Logfile("##########################################################################################################",Logfilename)


    # Update license into chassis new method with Xgiglicense
    result = {'False': 0}
    Logfile_py.Logfile("##########################################################################################################", Logfilename)
    Logfile_py.Logfile(' Update license with new method with ' + configuration[Number[1]]['number'] + ' is start',Logfilename)
    Update = Telnet_update_license_py.telnetdo(Logfilename, configuration[Number[1]]['number'], result)
    result = Update.telnetdo_newmethod_add()
    Logfile_py.Logfile('Finish to write license ' + configuration[Number[1]]['number'] + "into Xgiglicense file with new method",Logfilename)
    if result['False'] != 0:
        Logfile_py.Logfile('Fail to update license' + configuration[Number[1]]['number']+' with new method', Logfilename)
    Logfile_py.Logfile("##########################################################################################################",Logfilename)

    # Update license into chassis with licenseagent

    Logfile_py.Logfile("##########################################################################################################",Logfilename)
    Logfile_py.Logfile(' Update license with old methold with ' + configuration[Number[0]]['number'] + ' is start',Logfilename)
    Update = Telnet_update_license_py.telnetdo(Logfilename, configuration[Number[0]]['number'], result)
    result = Update.telnetdo_oldmethod_add()
    if result['False'] != 0:
        Logfile_py.Logfile('Fail to update license' + configuration[Number[1]]['number'], Logfilename)
    Logfile_py.Logfile("##########################################################################################################",Logfilename)


    ####Reboot the chassis
    Logfile_py.Logfile("Reboot chassis "+Logfilename['chassis_name']+"now", Logfilename)
    Telnet_update_license_py.Reboot_chassis(Logfilename)

    ####TCAPI Testing
    Protocol_Speed = {}
    Read_protocol_speed_configuration_for_TCAPI_py.Read_protocol_speed(Protocol_Speed, Logfilename)
    Logfilename['Reverse_Flag']=1
    #####configuration[Number[0]]['number'] TCAPI Testing
    license_number = configuration[Number[0]]['number']
    Logfile_py.Logfile( "Test " + license_number + " TCAPI starts:" ,Logfilename)
    personalities = configuration[Number[0]]['personalities']
    port_list = configuration[Number[0]]['ports']


    result = main_test_py.SingleLicenseCheck(Logfilename, personalities, Protocol_Speed,port_list, result)
    main_test_py.OutputResult("Test on " + license_number, result, Logfilename)

    ####TCAPI Testing
    #####configuration[Number[1]]['number'] TCAPI Testing
    license_number = configuration[Number[1]]['number']
    Logfile_py.Logfile("Test " + license_number + " TCAPI starts:", Logfilename)
    personalities = configuration[Number[1]]['personalities']
    port_list = configuration[Number[1]]['ports']

    result = main_test_py.SingleLicenseCheck(Logfilename, personalities, Protocol_Speed,port_list, result)
    main_test_py.OutputResult("Test on " + license_number, result, Logfilename)

    #######Erace new methold license
    Logfile_py.Logfile("##########################################################################################################",Logfilename)
    Logfile_py.Logfile(' Delete license with old methold with ' + configuration[Number[0]]['number'] + ' is start',Logfilename)
    Update = Telnet_update_license_py.telnetdo(Logfilename, configuration[Number[0]]['number'], result)
    result = Update.telnetdo_oldmethod_del()
    if result['False'] != 0:
        Logfile_py.Logfile('Fail to delete license' + configuration[Number[1]]['number'], Logfilename)
    Logfile_py.Logfile(' Finish delete license with old methold' ,Logfilename)
    Logfile_py.Logfile("##########################################################################################################",Logfilename)
    Logfilename['Reverse_Flag']=0















