#!/usr/bin/python
#coding=utf-8
import os
import sys
import imp
import time
#hahaha
sys.path.append("C:\\Program Files (x86)\\Viavi\\Xgig Maestro\\SDK\\LoadTester\\lib")
import LoadTesterAPI_dll
from LoadTesterAPI_dll import *

sys.path.append("C:\\Program Files (x86)\\Viavi\\Xgig Maestro\\SDK\\Jammer\\bin")
from jammerapi_python import *

if sys.version_info <(2,7):
    # import _api_tracecontrol_python26 as _api_tracecontrol_python
    _api_tracecontrol_python = imp.load_dynamic("_api_tracecontrol_python" , "C:\Program Files (x86)\Viavi\Xgig Analyzer\SDK\TCAPI\Lib\_api_tracecontrol_python26.pyd")

else:
    # import _api_tracecontrol_python27 as _api_tracecontrol_python
    _api_tracecontrol_python = imp.load_dynamic("_api_tracecontrol_python" , "C:\Program Files (x86)\Viavi\Xgig Analyzer\SDK\TCAPI\Lib\_api_tracecontrol_python27.pyd")

######################################################################################################################################################################
#######import my telnet.py file ,you need to put it into same folder ,if not you need to write the path
#######This file is filed to update lidense to chassis ############
file, path, desc = imp.find_module('telnet')
print file, path, desc
Telnet_update_license_py = imp.load_module("telnet", file, path, desc)
#########################################################################################################################################################################
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################
#########################################################################################################################################################################
file, path, desc = imp.find_module('Reverse_testing')
print file, path, desc
Reverse_testing_py = imp.load_module("Reverse_testing", file, path, desc)
#########################################################################################################################################################################

#########################################################################################################################################################################
file, path, desc = imp.find_module('Read_protocol_speed_configuration_for_TCAPI')
print file, path, desc
Read_protocol_speed_configuration_for_TCAPI_py = imp.load_module("Read_protocol_speed_configuration_for_TCAPI", file, path, desc)
#########################################################################################################################################################################


DiscoverChassis = _api_tracecontrol_python.DiscoverChassis
UsePortEx = _api_tracecontrol_python.UsePortEx
LockPorts = _api_tracecontrol_python.LockPorts
UnlockPorts = _api_tracecontrol_python.UnlockPorts
CleanUp = _api_tracecontrol_python.CleanUp

getLastError = _api_tracecontrol_python.getLastError
CaptureFilter=_api_tracecontrol_python.CaptureFilter
RemoveCaptureFilter=_api_tracecontrol_python.RemoveCaptureFilter
TriggerOn=_api_tracecontrol_python.TriggerOn
RemoveTriggerOn=_api_tracecontrol_python.RemoveTriggerOn
SetCountForNextTransitionAPI=_api_tracecontrol_python.SetCountForNextTransitionAPI
LoadXml=_api_tracecontrol_python.LoadXml
SaveTrace=_api_tracecontrol_python.SaveTrace
StartCapture=_api_tracecontrol_python.StartCapture
StopCapture=_api_tracecontrol_python.StopCapture
GetStatus=_api_tracecontrol_python.GetStatus
Speed=_api_tracecontrol_python.Speed
ApplyConfiguration=_api_tracecontrol_python.ApplyConfiguration
CaptureMode=_api_tracecontrol_python.CaptureMode
LoadTccFileIntoCurrentPorts = _api_tracecontrol_python.LoadTccFileIntoCurrentPorts


###上面的都是引用，大家不用管#####
# All the licenses we need test for each type of X1K chassis - To be completed
####Read configuration ##############################
####################################################################################################################################################################################
##################################################################################################################################################################################################################
####################################################################################################################################################################################
######################################################################################################################################################

##########################clear logfile at the begining#########
###############################################################
'''
Protocol_Speed={
'FC':["4","8","16","Auto"],
'10GE':["10"],
'40GE':["40"],
'100GE':["100"],
'128':["128"],
'25GE':['25'],
'32FC':['32','16','8'],
'50GE':['50'],
'SAS':['12','6','3','Auto(SAS 6/3)','Auto(12/6)','Auto(12/6/3)'],
'PCIE':['Auto','8','5','2']
}

Protocol_Speed={
'SQA-SING63':
{
    'FC':["4","8","16","Auto"],
    '10GE':["10"],
    '40GE':["40"]
},

'SQA-SING82':
{
    'PCIE':['Auto','8','5','2'],
},

'SQA-SING90':
{
    '100GE':["100"],
    '128':["128"],
    '25GE':['25'],
    '32FC':['32','16','8'],
    '50GE':['50'],
},

'SQA-SING61':
{
'SAS':['12','6','3','Auto(SAS 6/3)','Auto(12/6)','Auto(12/6/3)'],
},

'Protocol_for_TCAPI':
{
    'FC': ['FC'],
    '10GE': ['GE'],
    '40GE': ["40GE"],
    'PCIEX4':['PCIE'],
    'PCIEX8': ['PCIE'],
    '100GE': ["100GE"],
    '128FC': ["128FC"],
    '25GE': ['GE'],
    '32FC': ['FC'],
    '50GE': ['50GE'],
    'SAS':['SAS']

}
}
'''


#######################################################################################################################
#################################################
# Check Analyzer Function worked if expected
def CheckAnalyzerFunction(Logfilename, Speeds_value_list,Protocol_TCAPI,port_list,result):

    index = 0
    ports_lock = ''
    while index < len(port_list)-1:
        ports_lock = ports_lock + Logfilename['chassis_name'] + ',1,'+ str(port_list[index]).strip(' ') + ' '
        index += 1
#    print ports_lock

    ports_lock = ports_lock + Logfilename['chassis_name'] + ',1,'+ str(port_list[len(port_list)-1]).strip(' ')
    Logfile_py.Logfile(ports_lock, Logfilename)
#    print ports_lock
# Check the allowed ports can be used
    print Logfilename['chassis_name']
    i = DiscoverChassis(Logfilename['chassis_name'])
    Logfile_py.Logfile(getLastError(), Logfilename)
    if i==0:
        Logfile_py.Logfile(str(i) + ' Successfully discovery chassis should return 0', Logfilename)
    else:
        Logfile_py.Logfile(getLastError(), Logfilename)
        Logfile_py.Logfile('Can not Discover chassis', Logfilename)

    i = UsePortEx(ports_lock,Protocol_TCAPI,1)
 #   print port_list
#    Logfile_py.Logfile(getLastError(), chassis_name)
    if i == 0:
        i = LockPorts()
        if i == 0:
            for speed in Speeds_value_list:
                i=Speed(speed)
                Logfile_py.Logfile(getLastError(), Logfilename)
                Logfile_py.Logfile(str(i) + ' set speed should return 0', Logfilename)
      #          Logfile_py.Logfile(getLastError(), chassis_name)
                if i == 0:
                    mode = ['stop', 'full', 'trigger', 'arm', 'rollback']
                    from random import choice
                    i=CaptureMode(choice(mode))
                    Logfile_py.Logfile(getLastError(), Logfilename)
                    Logfile_py.Logfile(str(i) + ' CaptureMode should return 0', Logfilename)
 #                   print i,"CaptureMode should return 0"
                    if i == 0:
                        i=ApplyConfiguration()
 #                       Logfile_py.Logfile(getLastError(), Logfilename)
                        ########only for PCIEX4 license,can't apply configuration if not change lane width to 4 ,there is no TCAPI to change it ,so load a auto configuration to this########
                        if getLastError().find('X4')>=0:
                            Logfile_py.Logfile( "need to change width in lancontrol to X4,use the configuration to do this ,I can't find the TCPAI CMD to change width",Logfilename)
                            i = LoadTccFileIntoCurrentPorts(sys.path[0]+'\PCIE_LANEX4_CONFIGURATION.tcc')
                            print getLastError()
                            Logfile_py.Logfile(str(i) + ' LoadTccFileIntoCurrentPorts should return 0', Logfilename)
                            i = ApplyConfiguration()
                            print getLastError()
                        #print i, "ApplyConfiguration should return 0"
                        Logfile_py.Logfile(str(i) + ' ApplyConfiguration should return 0', Logfilename)
                        if i == 0:
                            i = StartCapture()
                            #print i,"StartCapture should return 0"
                            Logfile_py.Logfile(getLastError(), Logfilename)
                            Logfile_py.Logfile(str(i) + ' StartCapture should return 0', Logfilename)
                            time.sleep(15)
                            if(i == 0):
                                i = StopCapture()
                                Logfile_py.Logfile(getLastError(), Logfilename)
      #                          print i,"StopCapture should return 0"
                                Logfile_py.Logfile(str(i) + ' StopCapture should return 0', Logfilename)
                                if (i==0):
                                    #print "Analyzer Function Check on Ports" + str(port_list) + " as " + protocol + " at " + speed + "G : PASS"
                                    Logfile_py.Logfile("Analyzer Function Check on Ports" + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : PASS", Logfilename)
                                    #result = True
                                else:
                                    #print "StopCapture on Ports " + str(port_list) + " as " + protocol + " at " + speed + "G : FAIL"
                                    Logfile_py.Logfile("StopCapture on Ports " + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : FAIL", Logfilename)
                                    result['False']=result['False']+1
                                    break
                            else:
                                #print "StartCapture on Ports " + str(port_list) + " as " + protocol + " at " + speed + "G : FAIL"
                                Logfile_py.Logfile("StartCapture on Ports " + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : FAIL", Logfilename)
                                result['False'] = result['False'] + 1
                                break
                        else:
                            #print "ApplyConfiguration on Ports " + str(port_list) + " as " + protocol + " at " + speed + "G : FAIL"
                            Logfile_py.Logfile("ApplyConfiguration on Ports " + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : FAIL", Logfilename)
                            result['False'] = result['False'] + 1
                            break
                    else:
                        #print "CaptureMode on Ports " + str(port_list) + " as " + protocol + " at " + speed + "G : FAIL"
                        Logfile_py.Logfile("CaptureMode on Ports " + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : FAIL", Logfilename)
                        result['False'] = result['False'] + 1
                        break
                else:
                    #print "Set Speed on Ports " + str(port_list) + " as " + protocol + " at " + speed + "G : FAIL"
                    Logfile_py.Logfile("Set Speed on Ports " + str(port_list) + " as " + Protocol_TCAPI + " at " + speed + "G : FAIL", Logfilename)
                    result['False'] = result['False'] + 1
 #                   print getLastError()
 #                   Logfile_py.Logfile(getLastError(), chassis_name)
                    break
            i = UnlockPorts()
            #print i,"UnlockPorts should return 0"
            Logfile_py.Logfile(str(i)+" UnlockPorts should return 0", Logfilename)
        else:
            #print "Lock Ports" + str(port_list) + " as " + protocol + " : FAIL"
            Logfile_py.Logfile("Lock Ports" + str(port_list) + " as " + Protocol_TCAPI + " : FAIL", Logfilename)
            result['False'] = result['False'] + 1
    else:
        #print "Use Ports" + str(port_list) + " as " + protocol + " : FAIL"
        Logfile_py.Logfile("Use Ports" + str(port_list) + " as " + Protocol_TCAPI + " : FAIL", Logfilename)
        result['False'] = result['False'] + 1

    i = CleanUp()
    print i,"CleanUp should return 0"
    Logfile_py.Logfile(str(i)+" CleanUp should return 0", Logfilename)

    Logfile_py.Logfile( "########################################################################################################################################", Logfilename)
    return result

def CheckLoadTesterFunction(Logfilename,protocol,port_list,speeds,result,revert):

    port_all = ['1','2','3','4','5','6','7','8']
    if (revert == 1):
        port_all = port_list
        Logfile_py.Logfile('invert test Loadtester_'+protocol+ 'start!', Logfilename)
    rtn = lt_SetProtocolForNextOpen(protocol)
    if (rtn != 0):
        #print "Set Protocol failed"
        Logfile_py.Logfile(str(rtn) + 'Set Protocol failed', Logfilename)
        result['False'] = result['False'] + 1
        lt_Close()
        return result
    #print "the current protocol is %s \n" %protocol
    Logfile_py.Logfile('the current protocol is ' + protocol + '\n', Logfilename)
    i = 0
    portIndex = []
    for port in port_all:

        print "start locking port%s" %port
        rtn = lt_OpenAndLockPort(Logfilename['chassis_name'], 1, int(port))
        if (rtn != 0):
            if (port in port_list and revert != 1):
                #print "Lock Port %s failed" %port
                Logfile_py.Logfile(str(rtn) + ' Lock Port '+port+' failed', Logfilename)
                lt_Close()
                result['False'] = result['False'] + 1
                lt_Close()
                return result
            elif (revert == 1 or port not in port_list):
                #print "This port can not be locked without license support. This step passed\n"
                Logfile_py.Logfile('This port can not be locked without license support. This step passed\n', Logfilename)
                continue
        else:
            if (revert == 1 or port not in port_list):
                #print"This port can be locked without license support. This step failed\n"
                Logfile_py.Logfile('This port can be locked without license support. This step failed\n',Logfilename)
                result['False'] = result['False'] + 1
                continue
        portIndex.append("{0} (1,1,{1})".format(Logfilename['chassis_name'], port))
        i = i + 1

    if (revert == 1):
        #print "invert test finished!\n"
        Logfile_py.Logfile('revert test Loadtester_'+protocol+ ' finished!\n', Logfilename)
        lt_Close()
        return result
    #print "\n port%s have been locked \n" %port_list
    Logfile_py.Logfile('\n port ' + str(portIndex) + '  have been locked \n', Logfilename)

    for speed in speeds:
        if (speed == "Auto"):
            continue
        #print "\n Test speed %s started!\n" %speed
        Logfile_py.Logfile('\n Test speed ' + speed + ' started!\n', Logfilename)
        for port in portIndex:
            #print "  start setting speed for %s\n" % port
            rtn = LoadTesterAPI_dll.Speed(port, int(speed))
            if (rtn != 0):
                #print "Set speed for Port %s failed" %port
                Logfile_py.Logfile(str(rtn) + 'Set speed for Port ' + port + ' failed\n', Logfilename)
                result['False'] = result['False'] + 1

            else:
                #print "Set speed for Port %s passed" %port
                Logfile_py.Logfile(str(rtn) + 'Set speed for Port ' + port + ' passed', Logfilename)
            time.sleep(2)

    lt_Close()
    time.sleep(1)
    return result

def CheckJammerFunction(Logfilename, protocol, port_list, speeds, result,revert):
    InitJammerAPI()
    port_all = ["1", "2", "3", "4", "5", "6", "7", "8"]
    if (revert == 1):
        #print "revert test Jammer_%s start!" % protocol
        Logfile_py.Logfile('invert test Jammer_' + protocol + 'start!', Logfilename)
        port_all = port_list

    if protocol == "FC":
        lockType = pt16GFC
    # FeatureSetID = fsBasic16GFC
    elif protocol == "GE":
        lockType = pt10GE
    elif protocol == "SAS":
        lockType = ptSASSATA
    elif "PCIE" in protocol:
        lockType = ptPCIe
        port_all = ["1", "2"]
    elif protocol == "25GE":
        lockType = pt25GE

    #print "the current protocol is %s \n" % protocol
    Logfile_py.Logfile('the current protocol is ' + protocol + '\n', Logfilename)
    portIndex = []
    for port in port_all:

        if int(port) % 2 == 0:
            continue
        if int(port) % 2 != 0:
            # print "start locking port pair%d"%(i+1)
            result_i = LockPort(Logfilename['chassis_name'], 1, 1, int(port), lockType, None)

            if (result_i == -1):
                if (port in port_list and revert != 1):
                    #print "Lock port pair%d failure! Test will exit\n" % ((int(port) + 1) / 2)
                    Logfile_py.Logfile(str(result_i) + ' Lock Port pair ' + str((int(port) + 1) / 2) + ' failure! Test will exit\n', Logfilename)
                    result['False'] = result['False'] + 1
                    UninitJammerAPI()
                    return result

                elif (revert == 1 or port not in port_list):
                    #print "This port can not be locked without license support. This step passed\n"
                    Logfile_py.Logfile('This port can not be locked without license support. This step passed\n',Logfilename)
                    continue
            else:
                if (revert == 1 or port not in port_list):
                    #print"This port can be locked without license support. This step failed\n"
                    Logfile_py.Logfile('This port can be locked without license support. This step failed\n',Logfilename)
                    continue

            portIndex.append(result_i)

    if (revert == 1):
        #print "revert test Jammer_%s finished!\n" % protocol
        Logfile_py.Logfile('revert test Jammer_' + protocol + ' finished!\n', Logfilename)
        time.sleep(1)
        UninitJammerAPI()
        return result

    #print "port pair%s have been locked \n" % str(portIndex)
    Logfile_py.Logfile('port pair ' + str(portIndex) + '  have been locked \n', Logfilename)

    suiteID_i = CreateTestSuite(lockType)
    if (suiteID_i == -1):
        #print "Test suite create failed\n"
        Logfile_py.Logfile('Test suite create failed\n', Logfilename)
        result['False'] = result['False'] + 1
        UninitJammerAPI()
        return result
    else:
        #print "Test suite has been created\n"
        Logfile_py.Logfile('Test suite has been created\n', Logfilename)

    SetTestTimeOut(suiteID_i, 1, 3)
    # print "start set test mode \n"
    result_i = SetTestMode(suiteID_i, 1, tmTriggerJamA)
    if (result_i != 1):
        #print "SetTestMode failure! Test will exit\n"
        Logfile_py.Logfile('SetTestMode failure! Test will exit\n', Logfilename)
        result['False'] = result['False'] + 1
    else:
        #print "SetTestMode successfully\n"
        Logfile_py.Logfile('SetTestMode successfully\n', Logfilename)
    # print "start set trigger name\n"
    if (SetTriggerName(suiteID_i, 1, "Any Frame") == 1):
        #print "trigger name set successfully \n"
        Logfile_py.Logfile('trigger name set successfully\n', Logfilename)
    else:
        #print "trigger name set failed\n"
        Logfile_py.Logfile('trigger name set failed\n', Logfilename)
        result['False'] = result['False'] + 1

    if ("PCIE" in protocol):
        lane_no = protocol.split('-')[1]
        for i in range(1, int(lane_no) + 1):
            result_i = SelectOSLanes(suiteID_i, 1, tsTrigger, "0-" + str(i))
            if (result_i != API_Success):
                #print "select lanes failure!\n"
                Logfile_py.Logfile(str(result_i) + 'select lanes failure!\n', Logfilename)
                result['False'] = result['False'] + 1
            else:
                print "set lane to 0-%s\n" % str(i)
                Logfile_py.Logfile(str(result_i) + ' set lane to 0-' + str(i) + '\n',Logfilename)
            for port in portIndex:
                # print "start attach test suite to port pair%d\n" %port
                Logfile_py.Logfile(' start attach test suite to port pair' + str(port) + '\n', Logfilename)
                result_i = AttachTestSuite(port, suiteID_i)
                # print "result is %d\n" % result_i
                if (result_i != 1):
                    # print "AttachTestSuite for port pair%d failure! Test will exit\n" %port
                    Logfile_py.Logfile(str(result_i) + ' AttachTestSuite for port pair' + str(port) + ' failure! Test will exit\n',Logfilename)
                    result['False'] = result['False'] + 1
                    UninitJammerAPI()
                    return result
                else:

                    # print "AttachTestSuite for port pair%d passed!\n" % port
                    Logfile_py.Logfile(str(result_i) + ' AttachTestSuite for port pair' + str(port) + ' passed!\n',Logfilename)

                # print "  start jammer for port pair%s\n" % port
                if (Start(port) == 1):
                    # print "  test started running...\n"
                    Logfile_py.Logfile('  test started running...\n', Logfilename)
                else:
                    # print "start jammer for port pair%s failure!\n" % port
                    Logfile_py.Logfile('start jammer for port pair' + str(port) + ' failure!\n', Logfilename)
                    result['False'] = result['False'] + 1
                time.sleep(2)
                result_i = GetJamStatus(port)
                if (result_i == jstWaitForTrigger):
                    # print ("  jam test has started\n")
                    Logfile_py.Logfile('  jam test has started\n', Logfilename)
                else:
                    # print ("  jam test failed to be started\n")
                    Logfile_py.Logfile('  jam test failed to be started\n', Logfilename)
                    result['False'] = result['False'] + 1
                time.sleep(3)
                result_i = GetJamStatus(port)
                if (result_i == jstTimedOut):
                    # print ("  jam test stopped\n\n\n")
                    Logfile_py.Logfile('  jam test stopped\n\n\n', Logfilename)
                else:
                    # print ("  jam test failed to stopped\n")
                    Logfile_py.Logfile('  jam test failed to stopped\n', Logfilename)
                    result['False'] = result['False'] + 1

    else:
        for speed in speeds:
            #print "Test speed %s started!\n" % speed
            Logfile_py.Logfile('Test speed ' + speed + ' started!\n', Logfilename)
            if (speed == "Auto"):
                continue
            elif speed == "3":
                clockType = snwNonOobForce30
            elif speed == "4":
                clockType = cr4_2500Gbps
            elif speed == "6":
                clockType = snwNonOobForce60
            elif speed == "8":
                clockType = cr8_5000Gbps
            elif speed == "12":
                clockType = snwNonOobForce12
            elif speed == "16":
                clockType = cr14_0250Gbps
            elif speed == "10":
                clockType = cr10_3125Gbps
            elif speed == "25":
                clockType = cr25_78125Gbps
            elif speed == "Auto(SAS 6/3)":
                clockType = AutoNegRangeIn_3G
            elif speed == "Auto(12/6)":
                clockType = AutoNegRangeIn_6_3G
            elif speed == "Auto(12/6/3)":
                clockType = AutoNegRangeIn_12_6_3G

            for port in portIndex:
                #print "start attach test suite to port pair%d\n" % port
                Logfile_py.Logfile('start attach test suite to port pair' + str(port) + '\n', Logfilename)
                result_i = AttachTestSuite(port, suiteID_i)
                # print "result is %d\n" % result_i
                if (result_i != 1):
                    #print "AttachTestSuite for port pair%d failure! Test will exit\n" % port
                    Logfile_py.Logfile(str(result_i) + 'AttachTestSuite for port pair' + str(port) + ' failure! Test will exit\n',Logfilename)
                    result['False'] = result['False'] + 1
                    ReleaseTestSuite(suiteID_i)
                    UninitJammerAPI()
                    return result
                else:
                    #print "AttachTestSuite for port pair%d passed!\n" % port
                    Logfile_py.Logfile(str(result_i) + 'AttachTestSuite for port pair' + str(port) + ' passed!\n', Logfilename)
                # print "  start setting clock rate for port pair%d\n"%port
                time.sleep(1)
                if (protocol == "SAS"):
                    if ("Auto" in speed):
                        result_i = SetSpeedAutoNegRange(port, clockType)
                        if (result_i == -1):
                            #print " SetSpeedAutoNegRange for port pair%d failure!\n" % port
                            Logfile_py.Logfile(str(result_i) + ' SetSpeedAutoNegRange for port pair' + str(port) + ' failure!\n', Logfilename)
                            result['False'] = result['False'] + 1
                        else:
                            Logfile_py.Logfile(str(result_i) + 'SetSpeedAutoNegRange for port pair' + str(port) + ' passed!\n',Logfilename)
                    else:
                        result_i = SetNonOOBSpeedNegotiation(port, clockType)
                        if (result_i == -1):
                            #print " SetNonOOBSpeedNegotiation for port pair%d failure!\n" % port
                            Logfile_py.Logfile(str(result_i) + ' SetNonOOBSpeedNegotiation for port pair' + str(port) + ' failure!\n',Logfilename)
                            result['False'] = result['False'] + 1
                        else:
                            Logfile_py.Logfile(str(result_i) + 'SetNonOOBSpeedNegotiation for port pair' + str(port) + ' passed!\n',Logfilename)

                else:
                    result_i = SetClockRate(port, clockType)
                    if (result_i == -1):
                        #print " SetClockRate for port pair%d failure! Test will exit\n" % port
                        Logfile_py.Logfile(str(result_i) + ' SetClockRate for port pair' + str(port) + ' failure!\n',Logfilename)
                        result['False'] = result['False'] + 1

                    time.sleep(4)
                    currentClock = GetClockRate(port)
                    # print "current clock is %s\n"%currentClock
                    # print "clockType is %s\n"%clockType

                    if (currentClock != clockType):
                        #print "SetClockRate for port pair%d failure!\n" % port
                        Logfile_py.Logfile(str(result_i) + 'SetClockRate for port pair' + str(port) + ' failure!\n',Logfilename)
                        result['False'] = result['False'] + 1
                    else:
                        #print "SetClockRate for port pair%d successfully!\n" % port
                        Logfile_py.Logfile(str(result_i) + 'SetClockRate for port pair' + str(port) + ' successfully!\n',Logfilename)
                time.sleep(1)
                #print "  start jammer for port pair%d\n" % port
                Logfile_py.Logfile('  start jammer for port pair' + str(port) + '\n', Logfilename)
                if (Start(port) != 1):
                    #print "  start jammer for port pair%d failure!\n" % port
                    Logfile_py.Logfile('  start jammer for port pair' + str(port) + ' failure!\n',Logfilename)
                    result['False'] = result['False'] + 1
                time.sleep(2)
                result_i = GetJamStatus(port)
                if (result_i == jstWaitForTrigger):
                    #print ("  jam test has started\n")
                    Logfile_py.Logfile('  jam test has started\n', Logfilename)
                else:
                    #print ("  jam test failed to be started\n")
                    Logfile_py.Logfile('  jam test failed to be started\n', Logfilename)
                    result['False'] = result['False'] + 1
                time.sleep(3)
                result_i = GetJamStatus(port)
                if (result_i == jstTimedOut):
                    #print ("  jam test stopped\n\n\n")
                    Logfile_py.Logfile('  jam test stopped\n\n\n', Logfilename)
                else:
                    #print ("  jam test failed to stopped\n")
                    Logfile_py.Logfile('  jam test failed to stopped\n', Logfilename)
                    result['False'] = result['False'] + 1

    for port in portIndex:
        # print "start unlock port pair%d\n"%port

        res = UnlockPort(port)
        if (res != 1):
            #print "Unlock Port pair%d failure!\n" % port
            Logfile_py.Logfile(str(res) + 'Unlock Port pair' + str(port) + ' failure!\n', Logfilename)
            result['False'] = result['False'] + 1
        else:
            #print "Port pair%d has been unlocked\n" % port
            Logfile_py.Logfile(str(res) + 'Port pair' + str(port) + ' has been unlocked\n', Logfilename)
    ReleaseTestSuite(suiteID_i)
    time.sleep(1)
    UninitJammerAPI()
    return result

def GetFunction(personality):
    return personality.split('_')[0]


def GetProtocol(personality):
    return personality.split('_')[1]


# License is already applied, to check if the function in this license work as expected
def SingleLicenseCheck(Logfilename, personalities,Protocol_Speed,port_list,result):
#  result = True
  for item in personalities:
    function = GetFunction(item)
    protocol = GetProtocol(item)

 #   print protocol
#  print function
    Speeds_value_list = Protocol_Speed[item]['Speed']
    Protocol_TCAPI = Protocol_Speed[item]['Convert_to_TCAPI_using']
    Logfile_py.Logfile(function + ' ' + function + ' on ports ' + str(port_list) + ' at speed ' + str(Speeds_value_list), Logfilename)
 #   print function + ' ' + protocol + ' on ports ' + str(port_list) + ' at speed ' + str(speeds)
    # Analyzer Function
    if function == 'Analyzer':
      #check allowed part if worked as expected
      result = CheckAnalyzerFunction(Logfilename,Speeds_value_list,Protocol_TCAPI,port_list,result)
      if result['False']!=0 :
        break
      #check un-allowed part if not worked as expected, to be completed...
    ###Analyzer function test
    if Logfilename['Reverse_Flag'] == 0:
        Logfile_py.Logfile("Start Reverse testing", Logfilename)
        PF = {'ports_reverse Fail': 0, 'protocol_reverse Fail': 0}
        Reverse_testing_py.ports_with_protocol_reverse_testing(port_list,Protocol_TCAPI, Protocol_Speed, PF, Logfilename)
        if (PF['ports_reverse Fail'] != 0 or PF['protocol_reverse Fail'] != 0):
            result['False'] = result['False'] + 1
    # Jammer Function - To be completed
    if function == 'JAMMER':
        # check allowed part if worked as expected
        result = CheckJammerFunction(Logfilename, Protocol_TCAPI, port_list, Speeds_value_list, result, 0)
        if result['False'] != 0:
          break

    # LoadTestor Function - To be completed
    if function == 'LOADTESTER':
        # check allowed part if worked as expected
        result = CheckLoadTesterFunction(Logfilename, Protocol_TCAPI, port_list, Speeds_value_list, result, 0)
        if result['False'] != 0:
          break

    # Generator Function - To be completed
  return result

#Write the test result to file
def OutputResult(license,result,Logfilename):

    if result['False']==0:
        PF = 'PASS'
    else:
        PF = 'FAIL'
    f=open(Logfilename['chassis_name']+'_'+ Logfilename['APPKIT']+'_'+ Logfilename['StartTime']+'_TestResult.txt','a')
    words = license + ' is ' + PF + '\n'
    f.write(words)
    f.close()



# clean the test result at the beginning of every testing
def main_function(configuration,Logfilename):

    #clear previous record txt
 #   f = open(chassis_name+'_TestResult.txt', 'w+')
 #   f.truncate()
#    f.close()
    # Apply one license at one time
    Protocol_Speed = {}
    Read_protocol_speed_configuration_for_TCAPI_py.Read_protocol_speed(Protocol_Speed, Logfilename)


    index = 1
    while index <= len(configuration):
        license_number = configuration[str(index)]['number']
        Logfile_py.Logfile("Test No." + str(index) + ":" + license_number + " starts:",Logfilename)
        personalities = configuration[str(index)]['personalities']
        port_list = configuration[str(index)]['ports']
        print port_list

        result = {'False': 0}
        # 1.Clear all licenses - To be completed  # 2.Add license - To be completed  # 3.Apply license - To be completed
        Logfile_py.Logfile('Start update license', Logfilename)
        result=Telnet_update_license_py.telnet_main(Logfilename,license_number,result)
        Logfile_py.Logfile('Finish update license', Logfilename)

        if result['False']==0:
#          print 'Check the license if worked as expected'
          result = SingleLicenseCheck(Logfilename, personalities,Protocol_Speed, port_list,result)
        else:
            Logfile_py.Logfile('Fail to update license',Logfilename)
        # write result to TestResult file
        OutputResult("Test No." + str(index) + ":" + license_number, result,Logfilename)
        index += 1
        # Apply one license at one time End