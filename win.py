import subprocess
import errno
import os

from yattag import Doc, indent
# Object for BSSIDs
class BSSID():
    def __init__(self):
        self.signal = None
        self.radio = None
        self.channel = None
        self.basic_rate = None
        self.other_rate = None
    
# Object for netowrks  
class network():  
    def __init__(self):
        self.ssid = None
        self.type = None
        self.authentication = None
        self.encryption = None
        self.bssids = []
               
# Windows - run a command line program to get
    #           a list of available networks. Parse
    #           the text response to retrieve individual
    #           network information       
class windows():

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

    def _connect(self):
        #check if profile exists
        #check if network is open
        #if profile  not exists and not open create a profile
        #if profile exists and open create a profile no pass and connect
        # Connect to network

        command = ["netsh",self.card,"profiles",'ssid="'+ssid+'"','name="'+profile+'"']
        pass

    def _disconnect(self):
        command = ["netsh",self.card,"disconnect"]
        result = self._run_cmd(command)
        
        return result
    def _networks(self):
        pc_type=self.pc_type
        command = ["netsh",self.card,"show","networks","mode=bssid"]
        result = self._run_cmd(command)
        ls = result.split("\n")
        
        count = 0
        network_list = []
        cell = network()
        prev =""
        for item in ls:
            items = item.split(":")
            if(len(items)) >= 2:
                if items[0][0:4] == "SSID":
                    cell = network()
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
                       new_bssid = BSSID()
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
    
    def _profiles(self):
        command = ["netsh",self.card,"show","profiles"]
        result = self._run_cmd(command)
        lines = result.split("\n")
        
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
            command = ["netsh",self.card,"export","profile",'name="'+profile+'"','folder="'+current+'"',key]
            result = self._run_cmd(command)
            results.append(result)
            
        return results
    
    def _create_profile_xml(self,settings):
        hex_value = ''.join([hex(ord(char))[2:] for char in settings['name']]).upper()

        doc, tag, text, line= Doc().ttl()

        with tag('WLANProfile',xmlns='http://www.microsoft.com/networking/WLAN/profile/v1'):
            line('name',settings['name'])
            with tag('SSIDConfig'):
                with tag('SSID'):
                    line('HEX',hex_value)
                    line('name',settings['name'])
                        
            line('connectionType','ESS')
            line('connectionMode','manual')
            with tag('MSM'):
                    with tag('security'):
                        with tag('authEncryption'):
                            
                            line('authentication','open')
                            line('encryption','none')

                            line('useOneX','false')
                    if settings['password']:
                        with tag('sharedKey'):
                            line('keyType','passPhrase')
                            line('protected','false')
                            line('keyMaterial',settings['password'])
           
        profile_xml = indent(doc.getvalue())
        print(profile_xml)
        #create an xml file for current profile
        return profile_xml
    
    

    def _run_cmd(self,commands):
        result = subprocess.check_output(commands,shell=True)
        result = result.decode("ascii").replace("\r","")
        return result
        

