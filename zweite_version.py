import psutil
import numpy as np
import pickle
import tensorflow as tf
import os
import joblib
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# Deaktiviere GPU-Warnungen
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def get_system_metrics():
    # Erhalte CPU-Zeitdaten
    cpu_times = psutil.cpu_times_percent(interval=1)
    cpu_user = cpu_times.user
    cpu_system = cpu_times.system
    cpu_idle = cpu_times.idle

    # Erhalte System-Load-Änderungen (1, 5 und 15 Minuten Durchschnitt)
    loadavg = psutil.getloadavg()
    loadavg_1min = loadavg[0]
    loadavg_5min = loadavg[1]
    loadavg_15min = loadavg[2]

    # Erhalte die CPU-Temperatur (optional, hängt vom System ab)
    try:
        cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current  # Beispiel für eine typische Linux-Temperaturabfrage
    except (KeyError, IndexError, TypeError):
        cpu_temp = None  # Falls keine Temperatur verfügbar ist

    # Erhalte die Speichernutzung
    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_free = mem.available

    # Erhalte den Swap-Speicher
    swap = psutil.swap_memory()
    swap_total = swap.total
    swap_free = swap.free

    # Erhalte Festplattennutzung
    disk_io = psutil.disk_io_counters()
    disk_read = disk_io.read_bytes
    disk_write = disk_io.write_bytes

    # Erhalte Netzwerkdaten
    net_io = psutil.net_io_counters()
    network_rx = net_io.bytes_recv
    network_tx = net_io.bytes_sent

    # Systemmetriken in ein Dictionary packen
    system_metrics = {
        'cpu_user': cpu_user,
        'cpu_system': cpu_system,
        'cpu_idle': cpu_idle,
        'loadavg_1min': loadavg_1min,
        'loadavg_5min': loadavg_5min,
        'loadavg_15min': loadavg_15min,
        'cpu_temp': cpu_temp,
        'mem_total': mem_total,
        'mem_free': mem_free,
        'swap_total': swap_total,
        'swap_free': swap_free,
        'disk_read': disk_read,
        'disk_write': disk_write,
        'network_rx': network_rx,
        'network_tx': network_tx
    }

    print("hier:::::::::::::::::::::::::::::::::::::", system_metrics)
    
    return system_metrics

def predict_cpu_frequency():
    print("🚀 Starte Vorhersage-Skript...")

    # Modell laden
    print("📦 Lade Modell...")
    model = load_model('cpu_freq_predictor.keras')
    print("✅ Modell erfolgreich geladen.")

    # Scaler laden
    print("📦 Lade Scaler (X und y)...")
    scaler_X = joblib.load("scaler_X.pkl")
    scaler_y = joblib.load("scaler_y.pkl")
    print("✅ Scaler erfolgreich geladen.")

    # Aktuelle Systemmetriken erfassen
    system_metrics = get_system_metrics()

    # Eingabedaten formatieren
    input_data = np.array(list(system_metrics.values())).reshape(1, -1)

    print(f"🧮 Eingabedaten vor Skalierung: {input_data}")

    # Eingabedaten skalieren
    scaled_input_data = scaler_X.transform(input_data)

    print(f"📏 Eingabedaten nach Skalierung: {scaled_input_data}")

    # Vorhersage auf skalierten Eingabedaten durchführen
    print("🤖 Vorhersage mit dem Modell läuft...")
    scaled_prediction = model.predict(scaled_input_data)

    # Debug-Ausgabe: Vorhersage vor Rückskalierung
    print(f"📏 Vorhersage vor Rückskalierung (skaliert): {scaled_prediction}")

    # Rückskalierung der Vorhersage
    predicted_cpu_frequency = scaler_y.inverse_transform(scaled_prediction.reshape(-1, 1))

    # Debug-Ausgabe: Rückskalierte Vorhersage
    print(f"🎉 Rückskalierte Vorhersage: {predicted_cpu_frequency[0][0]} Hz")

# Skript starten
if __name__ == "__main__":
    predict_cpu_frequency()
