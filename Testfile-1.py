import xlrd
import imp
import sys
import time
import os

#

def Read_excel_configuration(configuration,Mixture_License_update_method,Logfilename):
    print os.getcwd()
    try:
        workbook = xlrd.open_workbook(r'configuration.xlsx')
    except Exception, e:
        print str(e)
        print "configuration can't be read"

    print workbook.sheet_names()
    print Logfilename['chassis_name']

    table = workbook.sheet_by_name(Logfilename['chassis_name'])
    #   print table
    nrows = table.nrows
    #  print nrows
    #   table_index = workbook.sheet_by_index(0)
    #  chassisip = table_index.cell(0, 3).value
    ###find the license number####
    for i in range(0,nrows):
        if table.cell(i, 1).value.find('Mixture')>=0:
            Mixture_License_update_method['Run'] =table.cell(i, 0).value
            break

    for i in range(0,nrows):
        if table.cell(i, 1).value.find('License_number')>=0:
           license_begin_rows_number=i+1
           print license_begin_rows_number
           break

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
            print list

    return configuration
if __name__ == '__main__':
    configuration={}
    Mixture_License_update_method={'Run':0}
    Logfilename={'chassis_name':'SQA-SING63'}
    Read_excel_configuration(configuration,Mixture_License_update_method,Logfilename)
    print configuration
    print Mixture_License_update_method
    print 1