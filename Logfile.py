
def Logfile(info,Logfilename):
        print info
        if isinstance(info,int) or isinstance(info,str):
           f = open(Logfilename['chassis_name']+'_'+ Logfilename['APPKIT']+'_'+ Logfilename['StartTime']+'_detail_logfile.txt', 'a+')
           f.write(info + '\r\n')
        elif isinstance(info,dict):
           f = open(Logfilename['chassis_name']+'_'+ Logfilename['APPKIT']+'_'+ Logfilename['StartTime']+'_detail_logfile.txt', 'a+')
           key=info.keys()
           value=info.values()
           for key,value in info.items():
               print key,"=", value
               f.write(str(key))
               f.write("=")
               f.write(str(value)+'\r\n')

        f.close()

# ############################################################################