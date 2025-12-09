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

def get_top_processes():
    #Retrieve all information about the processes
    processes = []
    
    # Collection of all processes with their information
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Full list of processes with CPU consumption
    processes_cpu = []
    for proc in processes:
        if proc['cpu_percent'] > 0:
            processes_cpu.append({
                'name': proc['name'],
                'pid': proc['pid'],
                'cpu': round(proc['cpu_percent'], 1)
            })
    # Sorted by CPU in descending order
    processes_cpu = sorted(processes_cpu, key=lambda x: x['cpu'], reverse=True)
    
    # Complete list of processes with RAM consumption
    processes_ram = []
    for proc in processes:
        if proc['memory_percent'] > 0:  
            processes_ram.append({
                'name': proc['name'],
                'pid': proc['pid'],
                'memory': round(proc['memory_percent'], 1)
            })
    # Sorted by RAM in descending order
    processes_ram = sorted(processes_ram, key=lambda x: x['memory'], reverse=True)
    
    # Top 3 most resource-intensive processes
    top_3 = []

    # A score is created for each process (CPU + RAM).
    for proc in processes:
        score = proc['cpu_percent'] + proc['memory_percent']
        if score > 0:
            top_3.append({
                'name': proc['name'],
                'pid': proc['pid'],
                'cpu': round(proc['cpu_percent'], 1),
                'memory': round(proc['memory_percent'], 1),
                'score': round(score, 1)
            })
    # Sort by score in descending order and keep the top 3
    top_3 = sorted(top_3, key=lambda x: x['score'], reverse=True)[:3]
    
    return {
        'all_cpu': processes_cpu,
        'all_ram': processes_ram,
        'top_3': top_3
    }

def analyze_files(directory_path):
    extensions = {'.txt': 0, '.py': 0, '.pdf': 0, '.jpg': 0}
    total_files = 0

    try:
        for root, dirs, files in os.walk(directory_path):
          for file in files:
            total_files +=1
            ext = os.path.splitext(file)[1].lower()
            if ext in extensions:
               extensions[ext] += 1

    except PermissionError:
       print(f"Permission denied to access {directory_path}")
       
    # Calculating percentages
    file_stats = []
    for ext, count in extensions.items():
       percentage = (count / total_files * 100) if total_files > 0 else 0
       file_stats.append({
          'extension': ext,
          'count': count,
          'percentage': round(percentage, 1)
       })
    
    return file_stats, total_files



       
            

           

              



