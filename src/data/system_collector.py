#!/usr/bin/env python3
"""
Data Layer - Collecte des données système via psutil.
Ce module récupère les informations brutes du système Linux.
"""

import os
import platform
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import psutil


class SystemCollector:
    """Collecteur de données système utilisant psutil."""

    def __init__(self, files_directory: str = "/home"):
        """
        Initialise le collecteur.

        Args:
            files_directory: Répertoire à analyser pour les fichiers.
        """
        self.files_directory = files_directory

    def get_system_info(self) -> Dict[str, Any]:
        """Récupère les informations générales du système."""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        return {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime_seconds": int(uptime.total_seconds()),
            "uptime_formatted": self._format_uptime(uptime.total_seconds()),
            "python_version": platform.python_version(),
        }

    def get_cpu_info(self) -> Dict[str, Any]:
        """Récupère les informations CPU."""
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)

        return {
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "cpu_percent_per_core": cpu_percent_per_core,
            "load_avg_1min": round(load_avg[0], 2),
            "load_avg_5min": round(load_avg[1], 2),
            "load_avg_15min": round(load_avg[2], 2),
            "cpu_freq": self._get_cpu_freq(),
        }

    def get_memory_info(self) -> Dict[str, Any]:
        """Récupère les informations mémoire."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent,
            "total_formatted": self._format_bytes(mem.total),
            "available_formatted": self._format_bytes(mem.available),
            "used_formatted": self._format_bytes(mem.used),
            "swap_total": swap.total,
            "swap_used": swap.used,
            "swap_percent": swap.percent,
            "swap_total_formatted": self._format_bytes(swap.total),
            "swap_used_formatted": self._format_bytes(swap.used),
        }

    def get_disk_info(self) -> Dict[str, Any]:
        """Récupère les informations disque."""
        disk = psutil.disk_usage("/")

        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
            "total_formatted": self._format_bytes(disk.total),
            "used_formatted": self._format_bytes(disk.used),
            "free_formatted": self._format_bytes(disk.free),
        }

    def get_network_info(self) -> Dict[str, Any]:
        """Récupère les informations réseau."""
        net_io = psutil.net_io_counters()

        interfaces = {}
        net_if_addrs = psutil.net_if_addrs()
        for iface, addrs in net_if_addrs.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interfaces[iface] = addr.address
                    break

        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "bytes_sent_formatted": self._format_bytes(net_io.bytes_sent),
            "bytes_recv_formatted": self._format_bytes(net_io.bytes_recv),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "interfaces": interfaces,
        }

    def get_processes_info(self) -> Dict[str, Any]:
        """Récupère les informations sur les processus."""
        processes = []

        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                pinfo = proc.info
                processes.append({
                    "pid": pinfo["pid"],
                    "name": pinfo["name"],
                    "cpu_percent": pinfo["cpu_percent"] or 0,
                    "memory_percent": round(pinfo["memory_percent"] or 0, 2),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Tri par CPU puis par mémoire
        processes.sort(key=lambda x: (x["cpu_percent"], x["memory_percent"]), reverse=True)
        top_3_cpu = processes[:3]

        # Tri par mémoire
        processes.sort(key=lambda x: x["memory_percent"], reverse=True)
        top_3_memory = processes[:3]

        return {
            "total_count": len(processes),
            "top_3_cpu": top_3_cpu,
            "top_3_memory": top_3_memory,
        }

    def get_files_info(self, recursive: bool = True) -> Dict[str, Any]:
        """
        Analyse les fichiers dans le répertoire configuré.

        Args:
            recursive: Si True, analyse récursivement les sous-dossiers.
        """
        extensions = {
            ".txt": {"count": 0, "size": 0},
            ".py": {"count": 0, "size": 0},
            ".pdf": {"count": 0, "size": 0},
            ".jpg": {"count": 0, "size": 0},
            ".jpeg": {"count": 0, "size": 0},
            ".png": {"count": 0, "size": 0},
            ".md": {"count": 0, "size": 0},
            ".html": {"count": 0, "size": 0},
            ".css": {"count": 0, "size": 0},
            ".json": {"count": 0, "size": 0},
            ".other": {"count": 0, "size": 0},
        }

        total_files = 0
        largest_files: List[Dict[str, Any]] = []

        try:
            path = Path(self.files_directory)
            pattern = "**/*" if recursive else "*"

            for file_path in path.glob(pattern):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        ext = file_path.suffix.lower()

                        if ext in extensions:
                            extensions[ext]["count"] += 1
                            extensions[ext]["size"] += size
                        else:
                            extensions[".other"]["count"] += 1
                            extensions[".other"]["size"] += size

                        total_files += 1
                        largest_files.append({
                            "path": str(file_path),
                            "name": file_path.name,
                            "size": size,
                            "size_formatted": self._format_bytes(size),
                        })
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            pass

        # Top 5 fichiers les plus volumineux
        largest_files.sort(key=lambda x: x["size"], reverse=True)
        top_5_largest = largest_files[:5]

        # Calcul des pourcentages
        file_stats = {}
        for ext, data in extensions.items():
            if data["count"] > 0:
                percentage = (data["count"] / total_files * 100) if total_files > 0 else 0
                file_stats[ext] = {
                    "count": data["count"],
                    "size": data["size"],
                    "size_formatted": self._format_bytes(data["size"]),
                    "percentage": round(percentage, 1),
                }

        return {
            "directory": self.files_directory,
            "total_files": total_files,
            "by_extension": file_stats,
            "top_5_largest": top_5_largest,
        }

    def collect_all(self) -> Dict[str, Any]:
        """Collecte toutes les données système."""
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "processes": self.get_processes_info(),
            "files": self.get_files_info(),
        }

    def _format_bytes(self, bytes_value: int) -> str:
        """Formate les bytes en unité lisible."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.2f} PB"

    def _format_uptime(self, seconds: float) -> str:
        """Formate le temps de fonctionnement."""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)

        parts = []
        if days > 0:
            parts.append(f"{days}j")
        if hours > 0:
            parts.append(f"{hours}h")
        parts.append(f"{minutes}m")

        return " ".join(parts)

    def _get_cpu_freq(self) -> Dict[str, float]:
        """Récupère la fréquence CPU."""
        try:
            freq = psutil.cpu_freq()
            if freq:
                return {
                    "current": round(freq.current, 2),
                    "min": round(freq.min, 2),
                    "max": round(freq.max, 2),
                }
        except Exception:
            pass
        return {"current": 0, "min": 0, "max": 0}


if __name__ == "__main__":
    # Test du module
    collector = SystemCollector(files_directory="/home")
    data = collector.collect_all()

    import json
    print(json.dumps(data, indent=2, default=str))
