import csv
import time
import psutil

# Datei für die Datenspeicherung
output_file = "system_data.csv"

# Header der CSV-Datei
header = [
    "cpu_user", "cpu_system", "cpu_idle",
    "loadavg_1min", "loadavg_5min", "loadavg_15min",
    "cpu_freq", "cpu_temp",
    "mem_total", "mem_free", "mem_used_pct", "swap_total", "swap_free", "swap_used_pct",
    "disk_read", "disk_write",
    "network_rx", "network_tx"
]

# Funktion zum Einlesen der CPU-Auslastung
def read_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
    cpu_times = psutil.cpu_times_percent(interval=1, percpu=False)
    cpu_user_pct = cpu_times.user
    cpu_system_pct = cpu_times.system
    cpu_idle_pct = cpu_times.idle
    return cpu_user_pct, cpu_system_pct, cpu_idle_pct

# Funktion zum Einlesen der Systemlast
def read_loadavg():
    load_1min, load_5min, load_15min = psutil.getloadavg()
    return load_1min, load_5min, load_15min

# Funktion zum Einlesen der CPU-Frequenz
def read_cpu_freq():
    cpu_freq = psutil.cpu_freq().current  # in MHz !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return cpu_freq

# Funktion zum Einlesen der CPU-Temperatur
def read_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else None
        return cpu_temp
    except Exception as e:
        print(f"Fehler beim Auslesen der Temperatur: {e}")
        return None

# Funktion zum Einlesen von Speicher- und Swap-Statistiken
def read_memory_stats():
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    mem_total = virtual_memory.total  # in Bytes
    mem_free = virtual_memory.available  # in Bytes
    mem_used = virtual_memory.used  # in Bytes
    mem_used_pct = virtual_memory.percent  # in %
    
    swap_total = swap_memory.total  # in Bytes
    swap_free = swap_memory.free  # in Bytes
    swap_used = swap_memory.used  # in Bytes
    swap_used_pct = swap_memory.percent  # in %

    return mem_total, mem_free, mem_used_pct, swap_total, swap_free, swap_used_pct

# Funktion zum Einlesen der Festplattenstatistiken
def read_disk_stats():
    disk_io = psutil.disk_io_counters()
    disk_read = disk_io.read_bytes  # in Bytes
    disk_write = disk_io.write_bytes  # in Bytes
    return disk_read, disk_write

# Funktion zum Einlesen der Netzwerkstatistiken
def read_network_stats():
    net_io = psutil.net_io_counters()
    network_rx = net_io.bytes_recv  # in Bytes
    network_tx = net_io.bytes_sent  # in Bytes
    return network_rx, network_tx

# Funktion zum Sammeln der Daten und Schreiben in die CSV-Datei
def collect_data(duration=60*60, interval=1):
    """
    Sammle Daten über eine bestimmte Dauer (in Sekunden) und schreibe sie in die CSV-Datei.
    :param duration: Gesamtdauer der Datensammlung in Sekunden.
    :param interval: Zeitintervall zwischen zwei Messungen in Sekunden.
    """
    start_time = time.time()

    # CSV-Datei initialisieren, wenn sie nicht existiert
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)  # Schreibe den Header

    while time.time() - start_time < duration:
        # Daten auslesen
        cpu_user, cpu_system, cpu_idle = read_cpu_usage()
        load_1min, load_5min, load_15min = read_loadavg()
        cpu_freq = read_cpu_freq()
        cpu_temp = read_cpu_temperature()
        mem_total, mem_free, mem_used_pct, swap_total, swap_free, swap_used_pct = read_memory_stats()
        disk_read, disk_write = read_disk_stats()
        network_rx, network_tx = read_network_stats()

        # Zeile zusammenstellen
        row = [
            cpu_user, cpu_system, cpu_idle,
            load_1min, load_5min, load_15min,
            cpu_freq, cpu_temp,
            mem_total, mem_free, mem_used_pct, swap_total, swap_free, swap_used_pct,
            disk_read, disk_write,
            network_rx, network_tx
        ]

        # Daten in die CSV schreiben
        with open(output_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(f"Gesammelte Daten: {row}")

        # Wartezeit zwischen den Messungen
        time.sleep(interval)

if __name__ == "__main__":
    collect_data()
