import re
import time
import socket
import ipaddress
import subprocess
import concurrent.futures

def split(a,n):
    k, m = divmod(len(a), n)
    return list((a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)))

def ping_ips(ip_list):
    devices = []
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE
    for i in range(len(ip_list)):
        output = subprocess.Popen(['ping','-n','1','-w','500',str(ip_list[i])],stdout=subprocess.PIPE,startupinfo=info).communicate()[0]
        out = output.decode('utf-8')
        
        ip_addr = re.search(r"((\d{1,3}([.]|)){1,4})",out).group(0)
        if "Received = 1" in out:
            device = socket.gethostbyaddr(ip_addr)
            device = {"device":device[0],"ip":device[2][0]}
            devices.append(device)
        
        else:
            pass

    return devices
    
def get_network_devices():
    
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    net = ip.rsplit('.',1)[0]
    ip_list = list(ipaddress.ip_network(net+'.0/24').hosts())
    devices = []
    #info = subprocess.STARTUPINFO()
    #info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #info.wShowWindow = subprocess.SW_HIDE
    threads = 25
    ip_list = split(ip_list,threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(ping_ips, ips): ips for ips in ip_list}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                [devices.append(i) for i in data if data ]         
    return devices

start = time.time()
for item in get_network_devices():
    print("\tDevice: %s\n\t\t  %s\n"%(item["device"],item["ip"]))
dif = time.time()-start

print("Program ran in: %d seconds"%(dif))
input("Press Enter to Quit")




