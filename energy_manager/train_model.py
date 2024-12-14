import os
import logging
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import RobustScaler  # Ändere StandardScaler auf RobustScaler
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import joblib


# Zeige alle Logs an
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # Zeigt alle Logs
tf.get_logger().setLevel(logging.INFO)  # Erzwinge Ausgabe von TensorFlow-Logs

def train_model():
    # Fehlerbehandlung für das Laden der Daten
    try:
        # Lade die gesammelten Daten
        data = pd.read_csv("system_data_cleaned.csv")
    except FileNotFoundError:
        print("Fehler: 'system_data_cleaned.csv' nicht gefunden!")
        return
    except pd.errors.EmptyDataError:
        print("Fehler: Die CSV-Datei ist leer!")
        return
    
    # Features und Labels extrahieren
    X = data[[
        "cpu_user", "cpu_system", "cpu_idle",
        "loadavg_1min", "loadavg_5min", "loadavg_15min",
        "cpu_temp", "mem_total", "mem_free", 
        "mem_used_pct",  # 🆕 Hinzufügen
        "swap_total", "swap_free", 
        "swap_used_pct",  # 🆕 Hinzufügen
        "disk_read", "disk_write", 
        "network_rx", "network_tx"
    ]].values

    y = data["cpu_freq"].values.reshape(-1, 1)  # Als Spalte

    # Standardisierung der Eingabedaten und Labels
    scaler_X = RobustScaler()
    scaler_y = RobustScaler()

    # Skaliere die Eingabedaten (X)
    X = scaler_X.fit_transform(X)

    # Skaliere die Ausgabedaten (y) - CPU-Frequenz
    y = scaler_y.fit_transform(y)

    # Trainiere das Modell
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Definiere das Modell
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),  # Dynamische Eingabegröße, basierend auf den Features
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1)  # Keine Aktivierungsfunktion für die Ausgabeschicht
    ])

    # Kompiliere und trainiere das Modell mit MeanSquaredError als Verlustfunktion
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss=tf.keras.losses.MeanSquaredError())  # Verlustfunktion geändert

    # Frühzeitiges Stoppen (EarlyStopping), um das Modell vor Überanpassung zu schützen
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Modelltraining
    history = model.fit(X_train, y_train, epochs=15, batch_size=16, validation_split=0.2, callbacks=[early_stopping])

    # Überprüfe, ob es extreme Ausreißer in den Trainingsdaten gibt
    print(f"Min und Max der Eingabedaten: {np.min(X_train, axis=0)}, {np.max(X_train, axis=0)}")

    # Zeige die Trainingsverluste an
    print(f"Trainingsverluste: {history.history['loss']}")

    # Teste das Modell
    test_loss = model.evaluate(X_test, y_test)
    print(f"Testverlust: {test_loss}")

    # Modell speichern
    model.save("cpu_freq_predictor.keras")
    
    # Scaler speichern
    with open("scaler_X.pkl", "wb") as f:
        pickle.dump(scaler_X, f)  # Speichert den Scaler für die Eingabedaten

    with open("scaler_y.pkl", "wb") as f:
        pickle.dump(scaler_y, f)  # Speichert den Scaler für die Ausgabedaten

    # 🛠️ Debug: Überprüfe den Scaler nach dem Training
    print(f"🛠️ Skalierungsfaktoren (scale_) für y: {scaler_y.scale_}")

    print("Scaler und Modell gespeichert.")
        
    # Lade den Scaler für die Zielvariable (y)
    scaler_y = joblib.load('scaler_y.pkl')

    # Überprüfe den Skaler
    print(f"Skalierungsfaktoren für y: {scaler_y.scale_}")

    # Führe die Vorhersage durch
    scaled_prediction = model.predict(X_test)
    predicted_cpu_frequency = scaler_y.inverse_transform(scaled_prediction.reshape(-1, 1))

    # Ausgabe der Vorhersage
    print(f"📏 Vorhersage vor Rückskalierung (skaliert): {scaled_prediction}")
    print(f"🎉 Rückskalierte Vorhersage (MHz): {predicted_cpu_frequency[0][0]} MHz")

    print(f"Skalierungsfaktoren für y: {scaler_y.scale_}")

    print("###########################")
    print(f"🔍 Eingabe-Scaler (scale_): {scaler_X.scale_}")


if __name__ == "__main__":
    train_model()
