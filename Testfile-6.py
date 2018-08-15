import platform
print platform.architecture()
print type(platform.architecture())
print platform.architecture()[0]
if platform.architecture()[0]=='64bit':
    print 1