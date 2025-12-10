#!/usr/bin/env python3
"""
Core Layer - Logique métier et traitement des données.
Ce module transforme les données brutes en format utilisable pour l'affichage.
"""

from typing import Dict, Any, List


class DataProcessor:
    """Processeur de données pour préparer l'affichage."""

    # Seuils pour les indicateurs colorés
    THRESHOLDS = {
        "green": 50,    # 0-50%
        "orange": 80,   # 51-80%
        "red": 100,     # 81-100%
    }

    def __init__(self, raw_data: Dict[str, Any]):
        """
        Initialise le processeur avec les données brutes.

        Args:
            raw_data: Données collectées par SystemCollector.
        """
        self.raw_data = raw_data

    def get_color_class(self, percentage: float) -> str:
        """
        Détermine la classe CSS de couleur selon le pourcentage.

        Args:
            percentage: Valeur en pourcentage (0-100).

        Returns:
            Nom de la classe CSS (gauge-green, gauge-orange, gauge-red).
        """
        if percentage <= self.THRESHOLDS["green"]:
            return "gauge-green"
        elif percentage <= self.THRESHOLDS["orange"]:
            return "gauge-orange"
        else:
            return "gauge-red"

    def process_system(self) -> Dict[str, Any]:
        """Traite les données système."""
        system = self.raw_data.get("system", {})
        return {
            "hostname": system.get("hostname", "N/A"),
            "os": system.get("os", "N/A"),
            "os_version": system.get("os_version", "N/A"),
            "architecture": system.get("architecture", "N/A"),
            "boot_time": system.get("boot_time", "N/A"),
            "uptime": system.get("uptime_formatted", "N/A"),
            "python_version": system.get("python_version", "N/A"),
        }

    def process_cpu(self) -> Dict[str, Any]:
        """Traite les données CPU."""
        cpu = self.raw_data.get("cpu", {})
        percent = cpu.get("cpu_percent", 0)

        # Traitement des cores
        cores_data = []
        for i, core_percent in enumerate(cpu.get("cpu_percent_per_core", [])):
            cores_data.append({
                "id": i,
                "percent": core_percent,
                "color_class": self.get_color_class(core_percent),
            })

        return {
            "physical_cores": cpu.get("physical_cores", 0),
            "logical_cores": cpu.get("logical_cores", 0),
            "percent": percent,
            "percent_int": int(percent),
            "color_class": self.get_color_class(percent),
            "load_avg_1min": cpu.get("load_avg_1min", 0),
            "load_avg_5min": cpu.get("load_avg_5min", 0),
            "load_avg_15min": cpu.get("load_avg_15min", 0),
            "freq_current": cpu.get("cpu_freq", {}).get("current", 0),
            "freq_max": cpu.get("cpu_freq", {}).get("max", 0),
            "cores": cores_data,
        }

    def process_memory(self) -> Dict[str, Any]:
        """Traite les données mémoire."""
        mem = self.raw_data.get("memory", {})
        percent = mem.get("percent", 0)
        swap_percent = mem.get("swap_percent", 0)

        return {
            "total": mem.get("total_formatted", "N/A"),
            "used": mem.get("used_formatted", "N/A"),
            "available": mem.get("available_formatted", "N/A"),
            "percent": percent,
            "percent_int": int(percent),
            "color_class": self.get_color_class(percent),
            "swap_total": mem.get("swap_total_formatted", "N/A"),
            "swap_used": mem.get("swap_used_formatted", "N/A"),
            "swap_percent": swap_percent,
            "swap_percent_int": int(swap_percent),
            "swap_color_class": self.get_color_class(swap_percent),
        }

    def process_disk(self) -> Dict[str, Any]:
        """Traite les données disque."""
        disk = self.raw_data.get("disk", {})
        percent = disk.get("percent", 0)

        return {
            "total": disk.get("total_formatted", "N/A"),
            "used": disk.get("used_formatted", "N/A"),
            "free": disk.get("free_formatted", "N/A"),
            "percent": percent,
            "percent_int": int(percent),
            "color_class": self.get_color_class(percent),
        }

    def process_network(self) -> Dict[str, Any]:
        """Traite les données réseau."""
        net = self.raw_data.get("network", {})

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

    def process_processes(self) -> Dict[str, Any]:
        """Traite les données des processus."""
        procs = self.raw_data.get("processes", {})

        return {
            "total_count": procs.get("total_count", 0),
            "top_3_cpu": procs.get("top_3_cpu", []),
            "top_3_memory": procs.get("top_3_memory", []),
        }

    def process_files(self) -> Dict[str, Any]:
        """Traite les données des fichiers."""
        files = self.raw_data.get("files", {})

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

    def process_all(self) -> Dict[str, Any]:
        """
        Traite toutes les données pour l'affichage.

        Returns:
            Dictionnaire avec toutes les données formatées.
        """
        return {
            "timestamp": self.raw_data.get("timestamp", "N/A"),
            "system": self.process_system(),
            "cpu": self.process_cpu(),
            "memory": self.process_memory(),
            "disk": self.process_disk(),
            "network": self.process_network(),
            "processes": self.process_processes(),
            "files": self.process_files(),
        }

    def get_template_variables(self) -> Dict[str, Any]:
        """
        Génère un dictionnaire plat de variables pour le template HTML.

        Returns:
            Dictionnaire avec toutes les variables pour substitution.
        """
        data = self.process_all()
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
    from src.data.system_collector import SystemCollector

    collector = SystemCollector(files_directory="/home")
    raw_data = collector.collect_all()

    processor = DataProcessor(raw_data)
    variables = processor.get_template_variables()

    for key, value in variables.items():
        if not key.endswith("_html"):
            print(f"{key}: {value}")
