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

ports=['1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8']
protocol = 'GE'
print 1
i = DiscoverChassis("SQA-SING63")
print 2
print i
i = UsePortEx("10.86.88.195,1,1",protocol, 1)
print i
print getLastError()

print 3
i = UsePortEx("10.86.88.195,1,1 10.86.88.195,1,2 10.86.88.195,1,3 10.86.88.195,1,4 10.86.88.195,1,5 10.86.88.195,1,6 10.86.88.195,1,7 10.86.88.195,1,8",protocol, 1)
print getLastError()
print i
i = LockPorts()
print i
if i != 0:
    print getLastError()
i = Speed("10")
print getLastError()
print i
print "\n"

i = CaptureMode('stop')

print i, "CaptureMode should return 0"
i = ApplyConfiguration()
print i
print getLastError()

if getLastError().find('X4') >= 1:
    print "need to change width in lancontrol to X4,use the configuration to do this ,I can't find the TCPAI CMD to change width"
    i = LoadTccFileIntoCurrentPorts(sys.path[0] + '\PCIE_LANEX4_CONFIGURATION.tcc')
    print getLastError()
    print i
    i = ApplyConfiguration()
    print getLastError()
print i, "ApplyConfiguration should return 0"
print getLastError()
i = StartCapture()
print i, "StartCapture should return 0"
time.sleep(2.5)
i = StopCapture()
print i, "StopCapture should return 0"
i = SaveTrace("16GStopTrace", 1, 1)
print i, "SaveTrace should return 0"
print "\n"
i = UnlockPorts()
print i
i = CleanUp()
print i

