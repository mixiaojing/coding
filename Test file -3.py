#############################################################################
#########Port1,2 as Analyzer, sing64(10.86.88.243)port5,6 as Load tester


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
                                                "C:\Program Files (x86)\Viavi\Xgig Analyzer\SDK\TCAPI\Lib64\_api_tracecontrol_python27.pyd")

DiscoverChassis = _api_tracecontrol_python.DiscoverChassis
UsePortEx = _api_tracecontrol_python.UsePortEx
LockPorts = _api_tracecontrol_python.LockPorts
UnlockPorts = _api_tracecontrol_python.UnlockPorts
CleanUp = _api_tracecontrol_python.CleanUp

getLastError = _api_tracecontrol_python.getLastError
CaptureFilter = _api_tracecontrol_python.CaptureFilter
RemoveCaptureFilter = _api_tracecontrol_python.RemoveCaptureFilter
TriggerOn = _api_tracecontrol_python.TriggerOn
RemoveTriggerOn = _api_tracecontrol_python.RemoveTriggerOn
SetCountForNextTransitionAPI = _api_tracecontrol_python.SetCountForNextTransitionAPI
LoadXml = _api_tracecontrol_python.LoadXml
SaveTrace = _api_tracecontrol_python.SaveTrace
StartCapture = _api_tracecontrol_python.StartCapture
StopCapture = _api_tracecontrol_python.StopCapture
GetStatus = _api_tracecontrol_python.GetStatus
Speed = _api_tracecontrol_python.Speed
ApplyConfiguration = _api_tracecontrol_python.ApplyConfiguration
CaptureMode = _api_tracecontrol_python.CaptureMode
LoadTccFileIntoCurrentPorts = _api_tracecontrol_python.LoadTccFileIntoCurrentPorts
chassis_name='10.86.88.195'
port_list=['1','2','3','4']
index = 0
ports_lock = ''
while index < len(port_list)-1:
    ports_lock = ports_lock + chassis_name + ',1,'+ str(port_list[index]).strip(' ') + ' '
    index += 1
    print ports_lock

ports_lock = ports_lock + chassis_name + ',1,'+ str(port_list[len(port_list)-1]).strip(' ')
print ports_lock



ports_all = ['1', '2', '3', '4', '5', '6', '7', '8']
protocol_all=['GE','FC','10GE','SAS','PCIE']
ports_reverse = []
protocol_reverse=[]

protocol='GE'
for i in ports_all:
    if not i in port_list:
        ports_reverse.append(i)
print ports_reverse
print 1
for i in protocol_all:
    if not i in protocol:
        protocol_reverse.append(i)
print protocol_reverse
print 2

i = DiscoverChassis('SQA-SING63')
    #####port will not support
for i in range(0, len(ports_reverse)):
    ports_lock = '10.86.88.195' + ',1,' + str(ports_reverse[i]).strip(' ')
    print ports_lock
    i = UsePortEx(ports_lock, protocol, 1)
    print i
    if i==0:
        print 'fail'



print 3
from random import choice
protocol_reverse_random = choice(protocol_reverse)
print protocol_reverse_random
for i in range(0, len(port_list)):
    ports_lock = '10.86.88.195' + ',1,' + str(port_list[i]).strip(' ')
    print ports_lock
    i = UsePortEx(ports_lock, protocol_reverse_random, 1)
    print i
    if i==0:
       print 'fail'