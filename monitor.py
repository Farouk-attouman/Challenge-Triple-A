"""
Challenge Tripe A : System Monitoring Dashboard
"""

import psutil
import platform
import socket
from datetime import datetime
import os

def get_cpu_info():
   # Collects information about the processor
   cpu_count = psutil.cpu_count(logical=True)
   cpu_freq = psutil.cpu_freq()
   cpu_percent = psutil.cpu_percent(interval=1)
   
   return {
      'cpu_count' : cpu_count,
      'cpu_freq' : round(cpu_freq.current, 2) if cpu_freq else 0,
      'cpu_percent' : cpu_percent
   }

def get_memory_info():
   # Collects memory information
   memory = psutil.virtual_memory()
   return{
      'ram_total':round(memory.total / (1024**3), 2),
      'ram_used': round(memory.used / (1024**3), 2),
      'ram_percent': memory.percent
   }

def get_system_info():
   # Collects general system information
   boot_time = datetime.fromtimestamp(psutil.boot_time())
   uptime_seconds = (datetime.now() - boot_time).total_seconds()
   
   # Readable uptime
   days = int(uptime_seconds // 86400)
   hours = int((uptime_seconds % 86400) // 3600)
   minutes = int((uptime_seconds % 3600) // 60)
   
   # String format
   uptime_str = f"{days}j {hours}h {minutes}m"

   return {
      'hostname' : socket.gethostname(),
      'os_name' : f"{platform.system()} {platform.release()}",
      'boot_time' : boot_time.strftime("%Y-%m-%d %H:%M:%S"),
      'uptime': uptime_str,
      'users_count': len(psutil.users)
   }

def get_network_info():
   # Retrieves the primary IP address
    try:
      
      # Creating a UDP socket to test external connectivity
      socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      
      #C onnecting to an external server to determine the IP address
      test_serveur = ("8.8.8.8", 80)
      socket_udp.connect(test_serveur)
      
      # Retrieving the local IP address
      ip_address = socket_udp.getsockname()[0]
      socket_udp.close()

      return {'ip_address' : ip_address}
   
    except:
      return {'ip_address': '127.0.0.1' }
    

