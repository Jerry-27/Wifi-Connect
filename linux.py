class BSSID():
    def __init__(self,pc_type):
        if pc_type == 'windows':
            self.windows()
        elif pc_type == 'linux':
            self.linux()
        else:
            return 'OS type not recognized'
    
    def windows(self):
        self.signal = None
        self.radio = None
        self.channel = None
        self.basic_rate = None
        self.other_rate = None
    def linux(self):
        pass
    
#Object class for netowrks  
class network():  
    def __init__(self,pc_type):
        if pc_type == 'windows':
            self.windows()
        elif pc_type == 'linux':
            self.linux()
        else:
            return 'OS type not recognized'
    def windows(self):
        self.ssid = None
        self.type = None
        self.authentication = None
        self.encryption = None
        self.bssids = []
          
    def linux(self):
        pass