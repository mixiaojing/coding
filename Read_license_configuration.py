import xlrd
import imp
import sys
import time
import os


#########################################################################################################################################################################
file, path, desc = imp.find_module('Logfile')
print file, path, desc
Logfile_py = imp.load_module("Logfile", file, path, desc)
#########################################################################################################################################################################

def Read_excel_configuration(configuration,Mixture_License_update_method,Logfilename):
#    print os.getcwd()
    try:
        workbook = xlrd.open_workbook(r'configuration.xlsx')
    except Exception, e:
        print str(e)
        Logfile_py.Logfile(str(e), Logfilename)
#        print "configuration can't be read"
        Logfile_py.Logfile('configuration can not be read', Logfilename)
#    print workbook.sheet_names()
#    print Logfilename['chassis_name']

    table = workbook.sheet_by_name(Logfilename['chassis_name'])
    #   print table
    nrows = table.nrows
    ####Get Mixture_License_update_method Value####
    for i in range(0,nrows):
        if table.cell(i, 1).value.find('Mixture')>=0:
            Mixture_License_update_method['Run'] = table.cell(i, 0).value
            break

    for i in range(0,nrows):
        if table.cell(i, 1).value.find('License_number')>=0:
           license_begin_rows_number=i+1
           break

#    Mixture_License_update_method['Run']=table.cell(3, 0).value
#    print Mixture_License_update_method['Run']
    #  print nrows
    #   table_index = workbook.sheet_by_index(0)
    #  chassisip = table_index.cell(0, 3).value
    index = 1
    for i in range(license_begin_rows_number, nrows):
        if table.cell(i, 0).value == 1:
            list = {}
            list['number'] = str(table.cell(i, 1).value)
            # personnality = table_index.cell(i, 1).value
            list['personalities'] = str(table.cell(i, 2).value).split(',')
            # ports = table_index.cell(i, 2).value
            list['ports'] = str(table.cell(i, 3).value).split(',')
            configuration[str(index)] = list
            index=index+1
            Logfile_py.Logfile('Licence ' + str(table.cell(i, 1).value) + ' is set to run',Logfilename)
        else:
            Logfile_py.Logfile('Licence ' + str(table.cell(i, 1).value) + ' is set to not run ,if want to run,please set run=1',Logfilename)
    Logfile_py.Logfile(configuration, Logfilename)
    return configuration,Mixture_License_update_method


