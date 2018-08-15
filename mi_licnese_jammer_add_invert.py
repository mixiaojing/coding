import sys
import time
# customize the path where your libraries are located
sys.path.append("C:\\Program Files (x86)\\Viavi\\Xgig Maestro\\SDK\\Jammer\\bin")
from jammerapi_python import *

chassis_name = "SQA-SING61"
bladeNum = 1
#port_list = ["5","6","7","8"]
#port_list = ["1","2"]
#port_list = ["1","2","3","4"]
port_list = ["1","2","3","4","5","6","7","8"]
#speeds = ["4","8","16"]
#speeds = ["25"]
#speeds = ["10"]
speeds = ['12','6','3','Auto(SAS 6/3)','Auto(12/6)','Auto(12/6/3)']
#speeds = ['Auto','8','5','2']
#protocol = "25GE"
#protocol = "GE"
#protocol = "PCIE-4"
#protocol = "FC"
protocol = "SAS"
revert = 0
NULL = ""

                

def basic_check (chassis_name, protocol, port_list, speeds,revert):
		port_all = ["1","2","3","4","5","6","7","8"]
		if (revert == 1):
			print "revert test Jammer_%s start!"%protocol
			port_all = port_list

		if protocol == "FC":
			lockType = pt16GFC
			#FeatureSetID = fsBasic16GFC
		elif protocol == "GE":
			lockType = pt10GE
		elif protocol == "SAS":
			lockType = ptSASSATA
		elif "PCIE" in protocol:
			lockType = ptPCIe
			port_all = ["1","2"]
		elif protocol == "25GE":
			lockType = pt25GE

		print "the current protocol is %s \n"%protocol


		portIndex = []
		for port in port_all:
			
			if int(port)%2 == 0:
				continue
			if int(port)%2 != 0:
				#print "start locking port pair%d"%(i+1)
				result_i = LockPort(chassis_name,1,1,int(port),lockType, None)
				
				if (result_i == -1) :
					if (port in port_list and revert != 1):
						print "Lock port pair%d failure! Test will exit\n" %((int(port)+1)/2)
						return

					elif (revert == 1 or port not in port_list):
						print "This port can not be locked without license support. This step passed\n"
						continue
				else:
					if (revert == 1 or port not in port_list):
						print"This port can be locked without license support. This step failed\n"
						continue


				portIndex.append(result_i)

		if (revert == 1):
			print "revert test Jammer_%s finished!\n"%protocol
			return

		print "port pair%s have been locked \n"%str(portIndex)

		suiteID_i = CreateTestSuite(lockType)
		if (suiteID_i == -1) :
			print "Test suite create failed"
			return
		else:
			print "Test suite has been created\n"
		SetTestTimeOut( suiteID_i, 1, 2 )
		#print "start set test mode \n"
		result_i = SetTestMode(suiteID_i,1,tmTriggerJamA)
		if (result_i != 1) :
			print "SetTestMode failure! Test will exit\n"
			return
		else:
			print "SetTestMode successfully\n"
		#print "start set trigger name\n"
		if(SetTriggerName(suiteID_i,1,"Any Frame") == 1):
			print "trigger name set successfully \n"
		else:
			print "trigger name set failed\n"
			return


		if ("PCIE" in protocol) :
			lane_no = protocol.split('-')[1]
			for i in range(1, int(lane_no) + 1):
				result_i = SelectOSLanes(suiteID_i, 1, tsTrigger, "0-" + str(i))
				if (result_i != API_Success):
					print "select lanes failure!\n"
				else:
					print "set lane to 0-%s\n" % str(i)

				for port in portIndex:
					print "start attach test suite to port pair%d\n" % port
					result_i = AttachTestSuite(port, suiteID_i)
					# print "result is %d\n" % result_i
					if (result_i != 1):
						print "AttachTestSuite for port pair%d failure! Test will exit\n" % port
						return
					else:

						print "AttachTestSuite for port pair%d passed!\n" % port
					print "  start jammer for port pair%s\n" % port
					if (Start(port) == 1):
						print "  test started running...\n"
					else:
						print "start jammer for port pair%s failure! Test will exit\n" % port
						return
					time.sleep(1)
					result_i = GetJamStatus(port)
					if (result_i == jstWaitForTrigger):
						print ("  jam test has started\n")
					else:
						print ("  jam test failed to be started\n")
						return
					time.sleep(3)
					result_i = GetJamStatus(port)
					if (result_i == jstTimedOut):
						print ("  jam test stopped\n\n\n")
					else:
						print ("  jam test failed to stopped\n")
						return
				

		else:
			for	speed in speeds:
				print "Test speed %s started!\n"%speed
				if speed == "3":
					clockType = snwNonOobForce30
				if speed == "4":
					clockType = cr4_2500Gbps
				if speed == "6":
					clockType = snwNonOobForce60
				if speed == "8":
					clockType = cr8_5000Gbps
				if speed == "12":
					clockType = snwNonOobForce12
				if speed == "16":
					clockType = cr14_0250Gbps	
				if speed == "10":
					clockType = cr10_3125Gbps
				if speed == "25":
					clockType = cr25_78125Gbps
				if speed == "Auto(SAS 6/3)":
					clockType = AutoNegRangeIn_3G
				if speed == "Auto(12/6)":
					clockType = AutoNegRangeIn_6_3G
				if speed == "Auto(12/6/3)":
					clockType = AutoNegRangeIn_12_6_3G

				for port in portIndex:
					print "start attach test suite to port pair%d\n"%port
					result_i = AttachTestSuite(port, suiteID_i)
					#print "result is %d\n" % result_i
					if (result_i != 1):
						print "AttachTestSuite for port pair%d failure! Test will exit\n"%port
						return
					else:

						print "AttachTestSuite for port pair%d passed!\n" %port
					#print "  start setting clock rate for port pair%d\n"%port
					if(protocol == "SAS"):
						if("Auto" in speed):
							result_i = SetSpeedAutoNegRange(port,clockType)
							if (result_i == -1):
								print " SetSpeedAutoNegRange for port pair%d failure! Test will exit\n" % port
								return
						else:
							result_i = SetNonOOBSpeedNegotiation(port, clockType)
							if (result_i == -1):
								print " SetNonOOBSpeedNegotiation for port pair%d failure! Test will exit\n" % port
								return
					else:
						result_i = SetClockRate(port, clockType)
						if (result_i == -1):
							print " SetClockRate for port pair%d failure! Test will exit\n" %port
							return

					time.sleep(1)
					if (protocol != "SAS"):
						currentClock = GetClockRate(port)
						#print "current clock is %s\n"%currentClock
						#print "clockType is %s\n"%clockType
						time.sleep(4)
						if (currentClock != clockType):
							print "SetClockRate for port pair%d failure! Test will exit\n"%port
							return
						else:
							print "SetClockRate for port pair%d successfully!\n"%port

					print "  start jammer for port pair%d\n"%port
					if (Start(port) != 1):
						print "  start jammer for port pair%d failure! Test will exit\n"%port
						return
					time.sleep(1)
					result_i = GetJamStatus(port)
					if (result_i == jstWaitForTrigger):
						print ( "  jam test has started\n" )
					else:
						print ( "  jam test failed to be started\n" )
						return
					time.sleep(3)
					result_i = GetJamStatus(port)
					if (result_i == jstTimedOut):
						print ( "  jam test stopped\n\n\n" )
					else:
						print ( "  jam test failed to stopped\n" )
						return
						
		for port in portIndex:
			#print "start unlock port pair%d\n"%port

			res = UnlockPort(port)
			if (res != 1) :
				print "Unlock Port pair%d failure! Test will exit\n"%port
				return
			else:
				print "Port pair%d has been unlocked\n"%port
		ReleaseTestSuite(suiteID_i)
		time.sleep(1)



##################################        
# Main Test Area
##################################

InitJammerAPI()

basic_check(chassis_name,protocol,port_list,speeds,revert)

UninitJammerAPI()

print 'haha'