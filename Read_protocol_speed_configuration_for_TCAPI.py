import xlrd
import imp

#########################################################################################################################################################################

def Read_protocol_speed(Protocol_Speed,Logfilename):
    try:
        workbook = xlrd.open_workbook(r'configuration.xlsx')
    except Exception, e:
        print str(e)
        print "configuration can't be read"
    table = workbook.sheet_by_name('chassis_configuration')
    #   print table
    nrows = table.nrows
    print Logfilename['chassis_name']
 #   for i in range(0,nrows):
#      if table.cell(i, 0).value==Logfilename['chassis_name']:
#          protocol_speed_begin_rows=i
#           print i
#           for j in range(i+1,nrows):
#              if table.cell(j, 0).value != Logfilename['chassis_name']:
#                   protocol_speed_end_rows=j
#                   break
    #          break
    #   print i,j
    index = 1
    for i in range(0, nrows):
        if table.cell(i, 0).value == Logfilename['chassis_name']:
            list = {}
 #           list['Protocol'] = str(table.cell(i, 1).value)
            # personnality = table_index.cell(i, 1).value
#            list['Speed'] = str((table.cell(i, 2).value)).split(',')
            if type(table.cell(i, 2).value) is float:
                list['Speed'] = [str(int(table.cell(i, 2).value))]
            else:
                list['Speed'] = str((table.cell(i, 2).value)).split(',')
            # ports = table_index.cell(i, 2).value
            list['Convert_to_TCAPI_using'] = str(table.cell(i, 3).value)
            Protocol_Speed[str(table.cell(i, 1).value)]=list


    return Protocol_Speed


if __name__ == '__main__':
    Logfilename={
        'chassis_name':'SQA-SING63',
        'APPKIT':'11.1.1',
        'StartTime':'11111111',
        'IP':'10.86.88.195',
        "Reverse_Flag":0                                 ####design for don't need reverse testing case

    }
    Protocol_Speed={}

    Read_protocol_speed(Protocol_Speed,Logfilename)
    print Protocol_Speed

