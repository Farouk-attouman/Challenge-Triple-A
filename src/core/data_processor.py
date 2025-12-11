#!/usr/bin/env python3
"""
Core Layer - Logique métier et traitement des données.
Ce module transforme les données brutes en format utilisable pour l'affichage.
"""

# Seuils pour les indicateurs colorés
THRESHOLDS = {
    "green": 50,    # 0-50%
    "orange": 80,   # 51-80%
    "red": 100,     # 81-100%
}


def get_color_class(percentage):
    """
    Détermine la classe CSS de couleur selon le pourcentage.

    Args:
        percentage: Valeur en pourcentage (0-100).

    Returns:
        Nom de la classe CSS (gauge-green, gauge-orange, gauge-red).
    """
    if percentage <= THRESHOLDS["green"]:
        return "gauge-green"
    elif percentage <= THRESHOLDS["orange"]:
        return "gauge-orange"
    else:
        return "gauge-red"


def process_system(raw_data):
    """Traite les données système."""
    system = raw_data.get("system", {})
    return {
        "hostname": system.get("hostname", "N/A"),
        "os": system.get("os", "N/A"),
        "os_version": system.get("os_version", "N/A"),
        "architecture": system.get("architecture", "N/A"),
        "boot_time": system.get("boot_time", "N/A"),
        "uptime": system.get("uptime_formatted", "N/A"),
        "python_version": system.get("python_version", "N/A"),
    }


def process_cpu(raw_data):
    """Traite les données CPU."""
    cpu = raw_data.get("cpu", {})
    percent = cpu.get("cpu_percent", 0)

    # Traitement des cores
    cores_data = []
    for i, core_percent in enumerate(cpu.get("cpu_percent_per_core", [])):
        cores_data.append({
            "id": i,
            "percent": core_percent,
            "color_class": get_color_class(core_percent),
        })

    return {
        "physical_cores": cpu.get("physical_cores", 0),
        "logical_cores": cpu.get("logical_cores", 0),
        "percent": percent,
        "percent_int": int(percent),
        "color_class": get_color_class(percent),
        "load_avg_1min": cpu.get("load_avg_1min", 0),
        "load_avg_5min": cpu.get("load_avg_5min", 0),
        "load_avg_15min": cpu.get("load_avg_15min", 0),
        "freq_current": cpu.get("cpu_freq", {}).get("current", 0),
        "freq_max": cpu.get("cpu_freq", {}).get("max", 0),
        "cores": cores_data,
    }


def process_memory(raw_data):
    """Traite les données mémoire."""
    mem = raw_data.get("memory", {})
    percent = mem.get("percent", 0)
    swap_percent = mem.get("swap_percent", 0)

    return {
        "total": mem.get("total_formatted", "N/A"),
        "used": mem.get("used_formatted", "N/A"),
        "available": mem.get("available_formatted", "N/A"),
        "percent": percent,
        "percent_int": int(percent),
        "color_class": get_color_class(percent),
        "swap_total": mem.get("swap_total_formatted", "N/A"),
        "swap_used": mem.get("swap_used_formatted", "N/A"),
        "swap_percent": swap_percent,
        "swap_percent_int": int(swap_percent),
        "swap_color_class": get_color_class(swap_percent),
    }


def process_disk(raw_data):
    """Traite les données disque."""
    disk = raw_data.get("disk", {})
    percent = disk.get("percent", 0)

    return {
        "total": disk.get("total_formatted", "N/A"),
        "used": disk.get("used_formatted", "N/A"),
        "free": disk.get("free_formatted", "N/A"),
        "percent": percent,
        "percent_int": int(percent),
        "color_class": get_color_class(percent),
    }


def process_network(raw_data):
    """Traite les données réseau."""
    net = raw_data.get("network", {})

    # Liste des interfaces
    interfaces_list = []
    for iface, ip in net.get("interfaces", {}).items():
        interfaces_list.append({"name": iface, "ip": ip})

    return {
        "bytes_sent": net.get("bytes_sent_formatted", "N/A"),
        "bytes_recv": net.get("bytes_recv_formatted", "N/A"),
        "packets_sent": net.get("packets_sent", 0),
        "packets_recv": net.get("packets_recv", 0),
        "interfaces": interfaces_list,
    }


def process_processes(raw_data):
    """Traite les données des processus."""
    procs = raw_data.get("processes", {})

    return {
        "total_count": procs.get("total_count", 0),
        "top_3_cpu": procs.get("top_3_cpu", []),
        "top_3_memory": procs.get("top_3_memory", []),
    }


def process_files(raw_data):
    """Traite les données des fichiers."""
    files = raw_data.get("files", {})

    # Conversion en liste pour l'affichage
    extensions_list = []
    for ext, data in files.get("by_extension", {}).items():
        extensions_list.append({
            "extension": ext,
            "count": data.get("count", 0),
            "size": data.get("size_formatted", "N/A"),
            "percentage": data.get("percentage", 0),
        })

    # Tri par nombre de fichiers
    extensions_list.sort(key=lambda x: x["count"], reverse=True)

    return {
        "directory": files.get("directory", "N/A"),
        "total_files": files.get("total_files", 0),
        "by_extension": extensions_list,
        "top_5_largest": files.get("top_5_largest", []),
    }


def process_all(raw_data):
    """
    Traite toutes les données pour l'affichage.

    Args:
        raw_data: Données collectées par les fonctions de system_collector.

    Returns:
        Dictionnaire avec toutes les données formatées.
    """
    return {
        "timestamp": raw_data.get("timestamp", "N/A"),
        "system": process_system(raw_data),
        "cpu": process_cpu(raw_data),
        "memory": process_memory(raw_data),
        "disk": process_disk(raw_data),
        "network": process_network(raw_data),
        "processes": process_processes(raw_data),
        "files": process_files(raw_data),
    }


def get_template_variables(raw_data):
    """
    Génère un dictionnaire plat de variables pour le template HTML.

    Args:
        raw_data: Données collectées par les fonctions de system_collector.

    Returns:
        Dictionnaire avec toutes les variables pour substitution.
    """
    data = process_all(raw_data)
    variables = {
        # Timestamp
        "timestamp": data["timestamp"],

        # Système
        "system_hostname": data["system"]["hostname"],
        "system_os": data["system"]["os"],
        "system_os_version": data["system"]["os_version"],
        "system_architecture": data["system"]["architecture"],
        "system_boot_time": data["system"]["boot_time"],
        "system_uptime": data["system"]["uptime"],
        "system_python_version": data["system"]["python_version"],

        # CPU
        "cpu_physical_cores": data["cpu"]["physical_cores"],
        "cpu_logical_cores": data["cpu"]["logical_cores"],
        "cpu_percent": data["cpu"]["percent"],
        "cpu_percent_int": data["cpu"]["percent_int"],
        "cpu_color_class": data["cpu"]["color_class"],
        "cpu_load_1min": data["cpu"]["load_avg_1min"],
        "cpu_load_5min": data["cpu"]["load_avg_5min"],
        "cpu_load_15min": data["cpu"]["load_avg_15min"],
        "cpu_freq_current": data["cpu"]["freq_current"],
        "cpu_freq_max": data["cpu"]["freq_max"],

        # Mémoire
        "memory_total": data["memory"]["total"],
        "memory_used": data["memory"]["used"],
        "memory_available": data["memory"]["available"],
        "memory_percent": data["memory"]["percent"],
        "memory_percent_int": data["memory"]["percent_int"],
        "memory_color_class": data["memory"]["color_class"],
        "swap_total": data["memory"]["swap_total"],
        "swap_used": data["memory"]["swap_used"],
        "swap_percent": data["memory"]["swap_percent"],
        "swap_percent_int": data["memory"]["swap_percent_int"],
        "swap_color_class": data["memory"]["swap_color_class"],

        # Disque
        "disk_total": data["disk"]["total"],
        "disk_used": data["disk"]["used"],
        "disk_free": data["disk"]["free"],
        "disk_percent": data["disk"]["percent"],
        "disk_percent_int": data["disk"]["percent_int"],
        "disk_color_class": data["disk"]["color_class"],

        # Réseau
        "network_bytes_sent": data["network"]["bytes_sent"],
        "network_bytes_recv": data["network"]["bytes_recv"],
        "network_packets_sent": data["network"]["packets_sent"],
        "network_packets_recv": data["network"]["packets_recv"],

        # Processus
        "processes_total": data["processes"]["total_count"],

        # Fichiers
        "files_directory": data["files"]["directory"],
        "files_total": data["files"]["total_files"],
    }

    # Génération du HTML pour les cores CPU
    cores_html = ""
    for core in data["cpu"]["cores"]:
        cores_html += f'''
        <div class="core-item">
            <span class="core-label">Core {core["id"]}</span>
            <div class="gauge-mini">
                <div class="gauge-fill {core["color_class"]}" style="width: {core["percent"]}%;"></div>
            </div>
            <span class="core-value">{core["percent"]:.1f}%</span>
        </div>'''
    variables["cpu_cores_html"] = cores_html

    # Génération du HTML pour les interfaces réseau
    interfaces_html = ""
    for iface in data["network"]["interfaces"]:
        interfaces_html += f'<li><strong>{iface["name"]}:</strong> {iface["ip"]}</li>'
    variables["network_interfaces_html"] = interfaces_html

    # Génération du HTML pour le top 3 CPU
    top_cpu_html = ""
    for proc in data["processes"]["top_3_cpu"]:
        top_cpu_html += f'''
        <tr>
            <td>{proc["pid"]}</td>
            <td>{proc["name"]}</td>
            <td>{proc["cpu_percent"]:.1f}%</td>
            <td>{proc["memory_percent"]:.1f}%</td>
        </tr>'''
    variables["processes_top_cpu_html"] = top_cpu_html

    # Génération du HTML pour le top 3 mémoire
    top_mem_html = ""
    for proc in data["processes"]["top_3_memory"]:
        top_mem_html += f'''
        <tr>
            <td>{proc["pid"]}</td>
            <td>{proc["name"]}</td>
            <td>{proc["cpu_percent"]:.1f}%</td>
            <td>{proc["memory_percent"]:.1f}%</td>
        </tr>'''
    variables["processes_top_memory_html"] = top_mem_html

    # Génération du HTML pour les extensions de fichiers
    extensions_html = ""
    for ext in data["files"]["by_extension"]:
        extensions_html += f'''
        <tr>
            <td>{ext["extension"]}</td>
            <td>{ext["count"]}</td>
            <td>{ext["size"]}</td>
            <td>{ext["percentage"]}%</td>
        </tr>'''
    variables["files_extensions_html"] = extensions_html

    # Génération du HTML pour les fichiers les plus volumineux
    largest_html = ""
    for f in data["files"]["top_5_largest"]:
        largest_html += f'''
        <tr>
            <td title="{f["path"]}">{f["name"]}</td>
            <td>{f["size_formatted"]}</td>
        </tr>'''
    variables["files_largest_html"] = largest_html

    return variables


if __name__ == "__main__":
    # Test du module
    from src.data.system_collector import collect_all

    raw_data = collect_all(files_directory="/home")
    variables = get_template_variables(raw_data)

    for key, value in variables.items():
        if not key.endswith("_html"):
            print(f"{key}: {value}")
