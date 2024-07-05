class Version(object):

    def __init__(self, major,minor,update, rc=None):
        self.major = major
        self.minor = minor
        self.update = update
        self.rc =''
        if rc is not None:
            self.rc= rc
    
    def __str__(self):
        return self.get_value()
    
    def get_value(self):
        return 'v' + str(self.major) + '.' + str(self.minor) + '.' + self.rc + str(self.update)       
    