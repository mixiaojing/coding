import xlrd
import imp

#########################################################################################################################################################################

def Read_configuration(chassis):
    try:
        workbook = xlrd.open_workbook(r'configuration.xlsx')
    except Exception, e:
        print str(e)
        print "configuration can't be read"
    table = workbook.sheet_by_name('chassis_configuration')
    #   print table
    nrows = table.nrows

    for i in range(0,nrows):
        if table.cell(i, 1).value.find('Chassis_name')>=0:
           chassis_name_begin=i+1
           break

    for i in range(0, nrows):
        if table.cell(i, 0).value=='':
            chassis_name_end = i
            break



    for i in range(chassis_name_begin, chassis_name_end):
        if table.cell(i, 0).value == 1:
            chassis[str(str(table.cell(i, 1).value))]=str(table.cell(i, 2).value)
            print 'Chassis ' + str(table.cell(i, 1).value) + ' is set to run'
        else:
             print   'Chassis ' + str(table.cell(i, 1).value) + ' is set to not run ,if want to run,please set run=1'
    return chassis

if __name__ == '__main__':
    chassis={}
    chassis=Read_configuration(chassis)
    print chassis