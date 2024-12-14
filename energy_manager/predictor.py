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
    
    import os

    # Liste der zu löschenden Dateien
    files_to_delete = ['scaler_X.pkl', 'scaler_y.pkl', 'cpu_freq_predictor.keras']

    # Schleife durch die Liste und lösche jede Datei
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Datei '{file_path}' wurde erfolgreich gelöscht.")
        else:
            print(f"⚠️ Datei '{file_path}' existiert nicht.")


    # 🛠️ Debug: Überprüfe den Scaler
    print(f"🔍 Skalierungsfaktoren (scale_) für y: {scaler_y.scale_}")
    

    # Aktuelle Systemmetriken erfassen mit psutil
    system_metrics = {
        'cpu_user': psutil.cpu_times_percent(interval=1).user,  # CPU User Time in %
        'cpu_system': psutil.cpu_times_percent(interval=1).system,  # CPU System Time in %
        'cpu_idle': psutil.cpu_times_percent(interval=1).idle,  # CPU Idle Time in %
        'loadavg_1min': psutil.getloadavg()[0],  # Last 1 minute load average
        'loadavg_5min': psutil.getloadavg()[1],  # Last 5 minutes load average
        'loadavg_15min': psutil.getloadavg()[2],  # Last 15 minutes load average
        'cpu_temp': psutil.sensors_temperatures()['coretemp'][0].current,
        'mem_total': psutil.virtual_memory().total,  # Total RAM in bytes
        'mem_free': psutil.virtual_memory().available,  # Available RAM in bytes
        'mem_used_pct' : psutil.virtual_memory().percent,
        'swap_total': psutil.swap_memory().total,  # Total swap memory in bytes
        'swap_free': psutil.swap_memory().free,  # Free swap memory in bytes
        'swap_used_pct' : psutil.swap_memory().percent,
        'disk_read': psutil.disk_io_counters().read_bytes,  # Total disk read in bytes
        'disk_write': psutil.disk_io_counters().write_bytes,  # Total disk write in bytes
        'network_rx': psutil.net_io_counters().bytes_recv,  # Total received bytes
        'network_tx': psutil.net_io_counters().bytes_sent  # Total sent bytes
    }


    print("::::::::::::::::::::::::::::::::::::::::::", system_metrics)
    print("::::::::::::::::::::::::::::::::::::::::::", psutil.cpu_freq().current)  # in Mhz

    # Eingabedaten formatieren (Systemmetriken)
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

    # Setze negative Frequenzen auf 0 (physikalisch nicht möglich)
    predicted_cpu_frequency = np.maximum(predicted_cpu_frequency, 0)

    # Rückskalierte Vorhersage ausgeben
    print(f"🎉 Rückskalierte Vorhersage: {predicted_cpu_frequency[0][0]} MHz")

# Skript starten
if __name__ == "__main__":
    predict_cpu_frequency()
