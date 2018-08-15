#coding=utf-8
import telnetlib
import imp
import win32api
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################
# import  _api_cle_python
# Replaced with code snippet by post_swig_multiple_python_version_fixup.py
import sys
import imp
import time

# Add step 1 :need to judge the 32bit and 64bit os system ,then load differnt python api file
if sys.version_info < (2, 7):
    # import _api_tracecontrol_python26 as _api_tracecontrol_python
    _api_tracecontrol_python = imp.load_dynamic("_api_tracecontrol_python",
                                                "C:\Program Files (x86)\Viavi\Xgig Analyzer\SDK\TCAPI\Lib64\_api_tracecontrol_python26.pyd")

else:
    # import _api_tracecontrol_python27 as _api_tracecontrol_python
    _api_tracecontrol_python = imp.load_dynamic("_api_tracecontrol_python",
                                                "C:\Program Files (x86)\Viavi\Xgig Analyzer\SDK\TCAPI\Lib\_api_tracecontrol_python27.pyd")

DiscoverChassis = _api_tracecontrol_python.DiscoverChassis
UsePortEx = _api_tracecontrol_python.UsePortEx
getLastError = _api_tracecontrol_python.getLastError


def ports_with_protocol_reverse_testing(port_list,Protocol_TCAPI,Protocol_Speed,PF,Logfilename):
    Logfile_py.Logfile('#############################################################################################', Logfilename)
    Logfile_py.Logfile('########Reverse testing begin#######', Logfilename)

    Ports_all = ['1', '2', '3', '4', '5', '6', '7', '8']
    Protocol_all=[]
    for items in Protocol_Speed:
  #      print Protocol_Speed[items]
        Protocol_all.append(Protocol_Speed[items]['Convert_to_TCAPI_using'])

    ports_reverse = []
    protocol_reverse=[]

    ###获取反向Rever port list
    for i in Ports_all:
        if not i in port_list:
            ports_reverse.append(i)


    for i in Protocol_all:
      if not i in [Protocol_TCAPI]:
            protocol_reverse.append(i)
#    print Protocol_all
#    print ports_reverse
#    print protocol_reverse
    Logfile_py.Logfile('Protocol_all is '+str(Protocol_all), Logfilename)
    Logfile_py.Logfile('ports_reverse is '+str(ports_reverse), Logfilename)
    Logfile_py.Logfile('protocol_reverse is '+str(protocol_reverse), Logfilename)


    #####port will not support
    Logfile_py.Logfile('############Port reverse teting begin############', Logfilename)
    ports_no_list=['PCIE','40GE','100GE','128FC','50GE']

    if Protocol_TCAPI in ports_no_list:
        Logfile_py.Logfile('Protocl '+Protocol_TCAPI+' do not test port reverese ,because it only support 2 ports', Logfilename)
    elif ports_reverse==[]:
        Logfile_py.Logfile('ports_reverse is empyt ,so do not test port reverse',Logfilename)
    else:
        for i in range(0, len(ports_reverse)):
            ports_lock = Logfilename['IP'] + ',1,' + str(ports_reverse[i]).strip(' ')
            Logfile_py.Logfile('ports_lock on '+ports_lock+' with not supported port '+str(ports_reverse[i]+'with protocol '+Protocol_TCAPI), Logfilename)
            i = UsePortEx(ports_lock, Protocol_TCAPI, 1)
            Logfile_py.Logfile(str(i) + ' UsePortEx should return -1', Logfilename)
            if i==0:
                Logfile_py.Logfile("Reverse test on port with port  "+str(ports_reverse[i])+ ' with protocol '+Protocol_TCAPI+ ' Fail', Logfilename)
                PF['ports_reverse Fail']=1
                break

    Logfile_py.Logfile('############port reverse teting finish############', Logfilename)



    ####protocol 反转
    Logfile_py.Logfile('############Protocol reverse teting begin############', Logfilename)
    ports_no_list = ['PCIE', 'SAS']

    if Protocol_TCAPI in ports_no_list:
        Logfile_py.Logfile('Protocl '+Protocol_TCAPI+' chassis only support one protocol,so do not test protocl reverse ', Logfilename)
    elif protocol_reverse == []:
        Logfile_py.Logfile('Protocl reverse is empty ',Logfilename)
        #####get the all ports ports_lock argument####
    else:
        for j in range(0, len(protocol_reverse)):
            Logfile_py.Logfile('#############Now start protocol ' + protocol_reverse[j]+' reverse testing########',Logfilename)
            for a in range(1,9):
                #ports_lock = ports_lock+' '+Logfilename['IP'] + ',1,' +Ports_all[a]
                ports_lock = Logfilename['IP'] + ',1,' +str(a)
                Logfile_py.Logfile('Lock on port '+str(a) + ' with not supported protocol ' + protocol_reverse[j],Logfilename)
                i = UsePortEx(ports_lock, protocol_reverse[j], 1)
                Logfile_py.Logfile(str(i) + ' UsePortEx should return -1', Logfilename)
                if i == 0:
                  Logfile_py.Logfile("Reverse test on port with port  " + str(ports_reverse[j]) + ' Fail', Logfilename)
                  PF['ports_reverse Fail'] = 1
                  break

    Logfile_py.Logfile('############protocl reverse teting finish############', Logfilename)
    return PF

if __name__=='__main__':
    port_list=['1','2']
    protocol = 'SAS'

    Protocol_Speed = {
        'Analyzer_SAS': {'Convert_to_TCAPI_using': 'SAS', 'Speed': ['12','6','3','Auto(SAS 6/3)','Auto(12/6)','Auto(12/6/3)']},
    }

    PF = {'ports_reverse Fail': 0, 'protocol_reverse Fail': 0}

    Logfilename={
        'chassis_name':'SQA-SING61',
        'APPKIT':'11.1.1',
        'StartTime':'11111111',
        'IP':'10.86.88.252',
        "Reverse_Flag":0                                 ####design for don't need reverse testing case

    }

    ports_with_protocol_reverse_testing(port_list, protocol, Protocol_Speed, PF, Logfilename)