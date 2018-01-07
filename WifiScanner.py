
import subprocess

# Windows - run a command line program to get
#           a list of available networks. Parse
#           the text response to retrieve individual
#           names and 
def get_network_list():
    
    results = subprocess.check_output(["netsh","wlan","show","all"],shell=True)
    results = results.decode("ascii")
    results = results.replace("\r","")
    ls = results.split("\n")
    count = 0
    network_list = []
    network_dict = {}
    prev =""
    for item in ls:
        items = item.split(":")
        if(len(items)) == 2:
            if prev == "SSID":
                network_list.append(network_dict)
                network_dict = {}
                count = 0
            if items[0][0:4] == "SSID":
                network_dict[items[0][0:4].strip()] = items[1].strip()
                count+=1
            elif prev != "SSID":
                network_dict[items[0].strip()] = items[1].strip()
                
            prev = items[0][0:4]
    return network_list  

for network in get_network_list():
    if network['SSID']:
        print("%s\n  %s\n"%(network['SSID'],network['Authentication']))
input("Press any key to quit")
