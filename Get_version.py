import telnetlib
import imp
import win32api
import platform
#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################

# NOW Only supply the Analyzer appp version ,Other app version if need ,can add

def Get_App_version(chassis_name,Appkitversion):
    USER='Administrator'
    PASS='jdsu'

    tn = telnetlib.Telnet()
    try:
        tn.open(chassis_name)
        print 'connect Host successfully'
    except:
        print "Cannot open host"
    tn.write('\r\n')
    tn.read_until("login:")
    tn.write(USER + '\r\n')
    tn.write(PASS + '\r\n')
    tn.read_until("password")
    tn.read_until('>',5)
    tn.write('type F:\\Finisar\\FrameWork\\version.txt' +'\r\n')
    Version=tn.read_until('>').split('\r\n')
    Version=Version[1].split('=')
    Appkitversion['Appkit']=Version[1]
    tn.close()
    return Appkitversion


def getFileProperties(fname,Logfilename):

    propNames = ('Comments', 'InternalName', 'ProductName',
                 'CompanyName', 'LegalCopyright', 'ProductVersion',
                 'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                 'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                                                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)
        Logfile_py.Logfile("Analyzer Client version= " + str(strInfo['ProductVersion']), Logfilename)
        props['StringFileInfo'] = strInfo
        print strInfo['ProductVersion']

    except:
        pass
    return props

if '__name__'=='__main__':
    Logfilename = {
        'chassis_name': 'SQA-SING63',
        'APPKIT': '11.1.1',
        'StartTime': '11111111',
        'IP': '10.86.88.195',
        "Reverse_Flag": 0  ####design for don't need reverse testing case

    }
    if platform.architecture()[0]=='64bit':
        fname='C:\Program Files (x86)\Viavi\Xgig Analyzer\Xgig-TraceControl.exe'
    elif platform.architecture()[0]=='32bit':
        fname = 'C:\Program Files\Viavi\Xgig Analyzer\Xgig-TraceControl.exe'

    print getFileProperties(fname, Logfilename)