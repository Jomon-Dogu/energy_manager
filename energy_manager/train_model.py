import os
import logging
import tensorflow as tf
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
        data = pd.read_csv("energy_manager/system_data.csv")
    except FileNotFoundError:
        print("Fehler: 'energy_manager/system_data.csv' nicht gefunden!")
        return
    except pd.errors.EmptyDataError:
        print("Fehler: Die CSV-Datei ist leer!")
        return
    
    # Features und Labels extrahieren
    X = data[[
        "cpu_user", "cpu_system", "cpu_idle",
        "loadavg_1min", "loadavg_5min", "loadavg_15min",
        "cpu_temp", "mem_total", "mem_free",
        "swap_total", "swap_free", "disk_read",
        "disk_write", "network_rx", "network_tx"
    ]].values
    y = data["cpu_freq"].values.reshape(-1, 1)  # Als Spalte
    
    # Standardisierung der Eingabedaten und Labels
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X = scaler_X.fit_transform(X)  # Skaliert die Eingabedaten
    y = scaler_y.fit_transform(y)  # Skaliert die Ausgabedaten (CPU-Frequenz)
    
    # Trainiere das Modell
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(15,)),  # 15 Features
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    
    # Kompiliere und trainiere das Modell mit MeanSquaredError als Verlustfunktion
 #   model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
  #                loss=tf.keras.losses.MeanSquaredError())  # Verlustfunktion geändert
   
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss=tf.keras.losses.MeanSquaredError())  # Verlustfunktion geändert


    history = model.fit(X_train, y_train, epochs=30, batch_size=16, verbose=1)  # WICHTIG: verbose=1
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

    print("Scaler und Modell gespeichert.")
        
    # Lade den Scaler für die Zielvariable (y)
    scaler_y = joblib.load('scaler_y.pkl')

    # Überprüfe den Skaler
    print(f"Skalierungsfaktoren für y: {scaler_y.scale_}")
    print(f"Skalierungs-Mittelwert für y: {scaler_y.mean_}")

    # Führe die Vorhersage durch
    scaled_prediction = model.predict(X_test)
    predicted_cpu_frequency = scaler_y.inverse_transform(scaled_prediction.reshape(-1, 1))

    # Ausgabe der Vorhersage
    print(f"📏 Vorhersage vor Rückskalierung (skaliert): {scaled_prediction}")
    print(f"🎉 Rückskalierte Vorhersage (MHz): {predicted_cpu_frequency[0][0]} MHz")


if __name__ == "__main__":
    train_model()
