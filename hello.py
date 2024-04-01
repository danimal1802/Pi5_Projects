# Python Script to report IP address, Run Level, CPU Temp, Date, Time on 2004A LCD screen
# Can/should run at boot time 
#
# Daniel Mitchell 1 Apr 2024

import I2C_LCD_driver
import time
import subprocess
import re
mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Pi5", 1, 0)

def get_cpu_temp():
  with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
    cpu_temp = f.read()
  return int(cpu_temp) / 1000

# Get 1-minute load average
def get_1m_load_avg():
    output = subprocess.check_output(['uptime'])
    load_avg = output.decode().split()[-3].rstrip(',')
    return load_avg

def get_ipv4_addresses():
    # Execute the `ip addr show` command to get details of all network interfaces
    result = subprocess.run(["ip", "addr", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Regular expression to match IPv4 addresses
    ipv4_pattern = re.compile(r'\binet\b\s+(\d+\.\d+\.\d+\.\d+)/\d+')
    
    # Search for IPv4 addresses in the command output
    ipv4_addresses = ipv4_pattern.findall(result.stdout)
    
    return ipv4_addresses

if __name__ == "__main__":
    ipv4_addresses = get_ipv4_addresses()
    if ipv4_addresses:
        print("IPv4 Addresses found:")
        for ip in ipv4_addresses:
            print(ip)
            mylcd.lcd_display_string("IP: "+ip, 2, 0);
    else:
        print("No IPv4 Addresses were found.")

while True:
   cpu_temp = get_cpu_temp()
   load_avg = get_1m_load_avg()
   temp_str = '{:.1f}C'.format(cpu_temp)
   mylcd.lcd_display_string("RL: "+load_avg, 3, 0)
   mylcd.lcd_display_string("CPU "+temp_str, 3, 11)
   mylcd.lcd_display_string("%s" %time.strftime("%H:%M:%S"), 4,0)
   mylcd.lcd_display_string("%s" %time.strftime("%m/%d/%Y"), 4,10)
