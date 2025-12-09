# Challenge Triple A - Main File

import os

from monitor import (
    get_cpu_info,
    get_memory_info,
    get_system_info,
    get_network_info,
    get_top_processes,
    analyze_files,
    get_color_class,
    generate_html
)

def main():
    print("=== Challenge Triple A - Monitoring Dashboard ===\n")
    print("📊 Collecte des données système")


    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    system_info = get_system_info()
    network_info = get_network_info()
    top_processes = get_top_processes()

    path_file = "/home/farouk/challenge-triple-a/Challenge-Triple-A"
    file_stats, total_files = analyze_files(path_file)

    data = {
        'hostname': system_info['hostname'],
        'os_name': system_info['os_name'],
        'uptime': system_info['uptime'],
        'users_count': system_info['users_count'],
        'cpu_count': cpu_info['cpu_count'],
        'cpu_freq': cpu_info['cpu_freq'],
        'cpu_percent': cpu_info['cpu_percent'],
        'cpu_color': get_color_class(cpu_info['cpu_percent']),
        'ram_total': memory_info['ram_total'],
        'ram_used': memory_info['ram_used'],
        'ram_percent': memory_info['ram_percent'],
        'ram_color': get_color_class(memory_info['ram_percent']),
        'ip_address': network_info['ip_address'],
        'processes_cpu': top_processes['all_cpu'],
        'processes_ram': top_processes['all_ram'],
        'top_3': top_processes['top_3'],
        'file_stats': file_stats,
        'total_files': total_files
    }

    print("\n ⏳ Génération du dashboard HTML...")
    generate_html(data)
    
    print("\n ✅ Dashboard généré ! Ouvrir 'index.html'.")

if __name__ == "__main__":
    main()
