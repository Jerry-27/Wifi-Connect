import subprocess
import platform
import errno
import os
from config import config

#To do:
# implement scan,create,connect,disconnect,delete(maybe)
# linux iwlist netsh

# Object class for BSSIDs
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
      
# Windows - run a command line program to get
    #           a list of available networks. Parse
    #           the text response to retrieve individual
    #           network information       
class win_wifi():

    def __init__(self,kwargs):
        self.card = kwargs['card']
        self.pc_type = kwargs['pc_type']
        self.current = kwargs['direc']
        self.config = kwargs['config']
        
    def scan(self):
        return self._networks()
    
    def connect(self):
        return self._connect()
    
    def disconnect(self):
        return self._disconnect()
    
    def export(self,crypt=False):
        return self._export_profiles(encrypt=crypt)
    
    def _networks(self):
        pc_type=self.pc_type
        results = subprocess.check_output(["netsh",self.card,"show","networks","mode=bssid"],shell=True)
        results = results.decode("ascii").replace("\r","")
        ls = results.split("\n")
        
        count = 0
        network_list = []
        cell = network(pc_type)
        prev =""
        for item in ls:
            items = item.split(":")
            if(len(items)) >= 2:
                if items[0][0:4] == "SSID":
                    cell = network(pc_type)
                    cell.ssid = items[1].strip()
                    count+=1
                else:
                    setting = items[0].strip()
                    value = items[1].strip()
                    
                    if  setting == 'Network type':
                        cell.type = value
                    elif setting == 'Authentication':
                       cell.authentication = value
                    elif setting == 'Encryption':
                       cell.encryption = value
                    elif 'BSSID' in setting:
                       new_bssid = BSSID(pc_type)
                       new_bssid.id = items[1:len(items)-1]
                    elif setting == 'Signal':
                       new_bssid.signal = value
                    elif setting == 'Radio type':
                       new_bssid.radio = value
                    elif setting == 'Channel':
                       new_bssid.channel = value
                    elif setting == 'Basic rates (Mbps)':
                       new_bssid.basic_rate = value
                    elif setting == 'Other rates (Mbps)':
                       new_bssid.other_rate = value
                       cell.bssids.append(new_bssid)
            elif len(items) == 1:
                network_list.append(cell)
                
        return network_list
    
    def _disconnect(self):
        results = subprocess.check_output(["netsh",self.card,"disconnect"],shell=True)
        
        return results
    
    def _profiles(self):
        results = subprocess.check_output(["netsh",self.card,"show","profiles"],shell=True)
        results = results.decode("ascii").replace("\r","")
        lines = results.split("\n")
        
        profiles = []
        
        for line in lines:
            line = line.split(":")
            if len(line) == 2 and "User Profile" in line[0].strip():
                profiles.append(line[1].strip())
                
        return profiles
    
    def _export_profiles(self,encrypt=False):
        profiles = self._profiles()
        current = self.current
        
        key = ['' if encrypt else 'key="clear"']
        results = []
        for profile in profiles:
            result = subprocess.check_output(["netsh",self.card,"export","profile",'name="'+profile+'"','folder="'+current+'"',key],shell=True)
            results.append(result.decode("ascii").replace("\r",""))
            
        return results
    
    def _create_profile(self):
        #create an xml file for current profile
        pass
    
    def _connect(self):
        #check if profile exists
        #check if network is open
        #if profile  not exists and not open create a profile
        #if profile exists and open create a profile no pass and connect
        # Connect to network
        pass

class net():
    
    def __init__(self,card='wlan'):
        self.card = card
        self.pc_type = self.get_platform()
        self.current = self.settings_dir()
        self.config = config()

        arg = {'card': self.card,'pc_type':self.pc_type,
                'direc': self.current,'config':self.config}
        
        systems = {'windows':win_wifi(arg)}
        self.system = systems[self.pc_type]
            
    def get_platform(self):
        try:
            plat = platform.system().lower()
        except Exception as e:
            plat = 0
            print(e)
        return plat
    
    def settings_dir(self):
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
net().sys().export()
input("Press any key to exit.")


