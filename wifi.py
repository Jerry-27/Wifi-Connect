import subprocess
import platform
import errno
import os
from config import config

import win

class net():
    
    def __init__(self,card='wlan'):
        self.card = card
        self.pc_type = self._get_platform()
        self.current = self._settings_dir()
        self.config = config()

        arg = {'card': self.card,'pc_type':self.pc_type,
                'direc': self.current,'config':self.config}
        
        systems = {'windows':win.windows(arg)}
        self.system = systems[self.pc_type]
            
    def _get_platform(self):
        try:
            plat = platform.system().lower()
        except Exception as e:
            plat = 0
            print(e)
        return plat
    
    def _settings_dir(self):
        direc = os.path.join(os.getcwd(),"config","profiles")
        try:
            os.makedirs(direc)   
        except OSError as e:
            if e.errno != errno.EEXIST:
                direc = "."
        
        return direc
    
    def sys(self):
        return self.system

 
def test_scan():
    work = net().sys()
    items = work.scan()
    
    for i in items:
        print('%s:%s------\n'%(i.ssid,i.authentication))
        #if len(i.bssids) >=1:
           # print(i.bssids[0].id)
def test_disconnect():
    work = net().sys().disconnect()
#test_scan()
    
#test export
setting= {'name':'RGGCN','password':'123456'}
print(net().sys()._create_profile_xml(setting))

#print([item.authentication for item in net().sys().scan()])

input("Press any key to exit.")

# connect(SSID,password)


