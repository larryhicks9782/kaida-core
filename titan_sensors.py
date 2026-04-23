import psutil
import os

def get_system_vitals():
    # RAM Usage
    ram = psutil.virtual_memory()
    # Disk Usage (in the Baltimore Node directory)
    disk = psutil.disk_usage(os.getcwd())
    # CPU Load
    cpu = psutil.cpu_percent(interval=0.1)
    
    vitals = {
        "cpu_load": f"{cpu}%",
        "ram_used": f"{ram.percent}%",
        "disk_free": f"{disk.free // (2**30)} GB",
        "active_dir": os.getcwd()
    }
    return vitals

def get_directory_scan():
    # List files to give her "vision" of the workspace
    return [f for f in os.listdir('.') if os.path.isfile(f)]

