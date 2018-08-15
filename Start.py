#encoding=utf-8
import imp
import time
import platform
#########################################################################################################################################################################
file, path, desc = imp.find_module('main_test')
print file, path, desc
main_test_py = imp.load_module("main_test", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Read_license_configuration')
print file, path, desc
Read_license_configuration_py = imp.load_module("Read_license_configuration", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Get_version')
print file, path, desc
Get_version_py = imp.load_module("Get_version", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Restore_license')
print file, path, desc
Restore_license_py = imp.load_module("Restore_license", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Mixture_License_update_method')
print file, path, desc
Mixture_License_update_method_py = imp.load_module("Mixture_License_update_method", file, path, desc)
#########################################################################################################################################################################
file, path, desc = imp.find_module('Read_chassis_configuration')
print file, path, desc
Read_chassis_configuration_py = imp.load_module("Read_chassis_configuration", file, path, desc)
#########################################################################################################################################################################

#'SQA-SING82': '10.86.88.197'
#'SQA-SING90': '10.86.88.64'
#'SQA-SING63': '10.86.88.195'
##'SQA-SING61': '10.86.88.252'

#Chassis = {'SQA-SING82': '10.86.88.197',
#'SQA-SING63': '10.86.88.195',
#'SQA-SING61': '10.86.88.252',
#'SQA-SING90': '10.86.88.64'
#		   }
####################################################################################################
###Read chassis name from configuration sheet

Chassis={}
#Chassis=Read_chassis_configuration_py.Read_configuration(Chassis)
Read_chassis_configuration_py.Read_configuration(Chassis)
####################################################################################################


###control whether to run mixturetesting function,it is to random selete 2 license and one use new methold write into
#chassis -->Xgiglicense,one is write with old method -licenseagent
#'1" ,run the mixture _testing
#"Error = This is not a high-density 8-port narrow blade."---->SING61 can't use old methold to update license ,so sing61 will not test mixture_testing
#turn_on_mixture_testing=1


###########################################################################################################################################################################
for (key, value) in Chassis.items():
    chassis_name =key
    chassis_ip = value

    configuration = {}
    Appkitversion={}
    ####clearup logfile txt file

#    Appkitversion=Get_version_py.Get_App_version(chassis_name,Appkitversion)
    Get_version_py.Get_App_version(chassis_name, Appkitversion)
    #Record the time
    NOW = time.strftime('%Y-%m-%d_H%H_M%M_S%S', time.localtime(time.time()))


    Logfilename={
        'chassis_name':chassis_name,
        'APPKIT':Appkitversion['Appkit'],
        'StartTime':NOW,
        'IP':chassis_ip,
        "Reverse_Flag":0                                 ####design for don't need reverse testing case

    }

    if platform.architecture()[0]=='64bit':
        fname='C:\Program Files (x86)\Viavi\Xgig Analyzer\Xgig-TraceControl.exe'
    elif platform.architecture()[0]=='32bit':
        fname = 'C:\Program Files\Viavi\Xgig Analyzer\Xgig-TraceControl.exe'

    Logfile_py.Logfile("Analyzer App version= "+Appkitversion['Appkit'],Logfilename)
    Get_version_py.getFileProperties(fname, Logfilename)
    Logfile_py.Logfile("Start testing at "+NOW, Logfilename)
#    Logfile_py.Logfile(chassis_name,chassis_name)
 #   f = open(chassis_name+'_'+NOW+'_'+Appkitversion['Appkit']+'_logfile.txt', 'w+')
 #   f.truncate()
 #   f.close()
    ##################################################################
    Logfile_py.Logfile("***************************************************************************************************************************************",Logfilename)
    Logfile_py.Logfile('***********************************************************Start testing  '+chassis_name+' now***********************************************',Logfilename)
    Logfile_py.Logfile("***************************************************************************************************************************************",Logfilename)



    #######读取excel里面的配置
    Mixture_License_update_method = {'Run': 0}
    Logfile_py.Logfile('Start reading configuration from excel ',Logfilename)
    Read_license_configuration_py.Read_excel_configuration(configuration,Mixture_License_update_method,Logfilename)
    Logfile_py.Logfile('Finish reading configuration from excel ', Logfilename)

    #####开始测试
    Logfile_py.Logfile('Now start to test all the license from configuration excel and test TCAPI function under every license', Logfilename)
    main_test_py.main_function(configuration,Logfilename)
    Logfile_py.Logfile('Finish '+chassis_name+' testing',Logfilename)

    #####Test is finish and Try one pair Mixture license testing
    if (Mixture_License_update_method['Run']==1 and chassis_name!='SQA-SING61'and len(configuration)>=2):
        Logfile_py.Logfile('Now start to mixture license testing',Logfilename)

        Mixture_License_update_method_py.Mixturetesting(Logfilename, configuration)
        Logfile_py.Logfile('Finish mixture license testing', Logfilename)
    else:
        Logfile_py.Logfile(chassis_name+" will not test mixture license testing",Logfilename)

    ######恢复原来license
    result = {'False': 0}
    Logfile_py.Logfile('Restore chassis '+chassis_name+' old license',Logfilename)
    Restore_license_py.Restore(Logfilename,result)
    Logfile_py.Logfile('Restore finish and wait 180s for chassis up', Logfilename)
    Logfile_py.Logfile('Moved to next chassis', Logfilename)
    main_test_py.OutputResult("Restore license finished", result, Logfilename)




    Logfile_py.Logfile("***************************************************************************************************************************************",Logfilename)
    Logfile_py.Logfile('***********************************************************Finish testing  '+chassis_name+' now***********************************************',Logfilename)
    Logfile_py.Logfile("***************************************************************************************************************************************",Logfilename)