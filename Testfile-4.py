import telnetlib
import time



def telnetdo_newmethod_add(ip):
    time.sleep(3)
    USER='Administrator'
    PASS='jdsu'
    tn = telnetlib.Telnet()
    try:
        tn.open(ip)
        print 1

    except:
        print 2
    tn.write('\r\n')
    tn.read_until("login:")
    tn.write(USER + '\r\n')
    tn.read_until("password")
    tn.write(PASS + '\r\n')
    time.sleep(3)
    print tn.read_until(">")
    tn.write('type C:\\xgiglicenses.txt' + '\r\n')
    tmp=tn.read_until(">")
    print tmp
    # Check the license have been writen into the Xgiglicense.txt#
    License_update = 0
    if tmp.find('ATBSZFGANQEDPZ8XT3CNYEBHWZFQRVPS') >=0:
        print 3

    else:
        print 4

if __name__=='__main__':
    ip='10.86.88.64'
    telnetdo_newmethod_add(ip)
