
#  CPU Frequency Prediction System

##  **Inhaltsverzeichnis**
1. [Projektübersicht](#projektübersicht)
2. [Funktionen der Skripte](#funktionen-der-skripte)
3. [Installation](#installation)
4. [Verwendung](#verwendung)
5. [Technologien](#technologien)
6. [Dateibeschreibung](#dateibeschreibung)

---

##  **Projektübersicht**
Dieses Projekt zielt darauf ab, die CPU-Frequenz basierend auf verschiedenen Systemmetriken wie CPU-Auslastung, Speichernutzung, Festplattennutzung, Netzwerkstatistiken und Temperatur vorherzusagen. Das System besteht aus drei Hauptskripten, die zusammenarbeiten, um die Daten zu sammeln, ein neuronales Netz zu trainieren und schließlich die CPU-Frequenz vorherzusagen.

---

##  **Funktionen der Skripte**

### 1️ **read_system_data.py**
    Dieses Skript sammelt Systemmetriken und speichert sie in der Datei `system_data.csv`.

- **Gesammelte Metriken**:
  - CPU-Auslastung (User, System, Idle)
  - Load Average (1, 5 und 15 Minuten)
  - CPU-Frequenz und Temperatur
  - Speicher- und Swap-Nutzung (total, frei, Prozent)
  - Festplattennutzung (Bytes gelesen/geschrieben)
  - Netzwerkstatistiken (Bytes empfangen/gesendet)

- **Funktionsweise**:
  - Alle Metriken werden alle `interval` Sekunden (standardmäßig 1 Sekunde) gesammelt.
  - Die Daten werden als Zeilen in der Datei `system_data.csv` gespeichert.
  - Das Skript läuft für eine bestimmte `duration` (standardmäßig 1 Stunde).

###  **train_model.py**
Das Training des neuronalen Netzes erfolgt mit den gesammelten Systemmetriken.

- **Schritte**:
  1. **Daten laden**: Lädt die Datei `system_data.csv`.
  2. **Vorverarbeitung**: Teilt die Daten in Features (X) und Zielwerte (y = CPU-Frequenz).
  3. **Daten skalieren**: Standardisiert die Daten mit `StandardScaler`.
  4. **Modelltraining**: Trainiert ein neuronales Netz mit 5 Schichten.
  5. **Speichern**: Speichert das trainierte Modell als `cpu_freq_predictor.keras`, sowie die Scaler `scaler_X.pkl` und `scaler_y.pkl`.
  6. **Validierung**: Führt Vorhersagen auf den Testdaten durch und zeigt die Ergebnisse an.

### **predictor.py**
Führt eine Echtzeitvorhersage der CPU-Frequenz auf Basis der aktuellen Systemmetriken durch.

- **Schritte**:
  1. **Modell laden**: Lädt das trainierte Modell `cpu_freq_predictor.keras` und die Scaler `scaler_X.pkl` und `scaler_y.pkl`.
  2. **Systemmetriken erfassen**: Erfasst die aktuellen Systemmetriken mit `psutil`.
  3. **Vorhersage durchführen**: Skaliert die Eingabedaten, führt die Vorhersage mit dem Modell durch und skaliert die Ausgabe zurück.
  4. **Ergebnis anzeigen**: Gibt die vorhergesagte CPU-Frequenz in MHz aus.

---

##  **Installation**
1. **Python-Pakete installieren**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Abhängigkeiten**:
   - `tensorflow`: Zum Training und der Vorhersage des neuronalen Netzes.
   - `psutil`: Zum Erfassen der Systemmetriken.
   - `scikit-learn`: Zum Skalieren der Eingabedaten.
   - `pandas`: Zum Lesen und Verarbeiten von CSV-Dateien.

---

## **Verwendung**

### 🔍 **1. Systemmetriken sammeln**
Führe das Skript `read_system_data.py` aus, um Systemmetriken in der Datei `system_data.csv` zu sammeln.
```bash
python read_system_data.py
```

###  **2. Modell trainieren**
Führe das Trainingsskript aus, um das Modell zu trainieren:
```bash
python train_model.py
```

###  **3. Vorhersage der CPU-Frequenz**
Führe das Vorhersage-Skript aus:
```bash
python predictor.py
```

---

##  **Technologien**
- **Programmiersprache**: Python
- **Bibliotheken**:
  - `TensorFlow`: Aufbau des neuronalen Netzes.
  - `scikit-learn`: Skalierung der Eingabedaten.
  - `psutil`: Erfassen der Systemmetriken.
  - `pandas`: Verarbeitung von CSV-Dateien.

---

##  **Dateibeschreibung**
| **Datei**          | **Beschreibung**                                   |
|-------------------|---------------------------------------------------|
| `energy_manager/data_cleaner.py`   | Das Skript SystemDataCleaner lädt Systemdaten aus CSV-Datei, filtert CPU-Frequenzwerte außerhalb eines definierten Bereichs und speichert die bereinigten Daten in einer neuen CSV-Datei |
| `energy_manager/data_gen.py`   | generiert synthetische Daten |
| `energy_manager/predictor.py`     | Führt die Vorhersage der CPU-Frequenz durch.        |
| `energy_manager/read_system_data.py` | Sammelt und speichert die Systemmetriken in `system_data.csv`. |
| `energy_manager/train_model.py`   | Trainiert das neuronale Netz und speichert das Modell sowie die Scaler. |
| `MANIFEST.in`   | Nötig um externe Daten in Python Paket zu inkludieren |
| `README.md`   | Readme Datei |
| `gen_input_data.csv`   | synthetische Daten |
| `main.py`   | Testskript/Demonstrator |
| `pyproject.toml`   | Definiert die Eigenschaften des Paketes |
| `requirements.txt`   | benötigte externe Pakete |
| `system_data.csv`  | CSV-Datei mit gesammelten Systemmetriken (automatisch generiert). |
| `system_data_2.csv`   | Kollektion verschiedener Messreihen von ausgelesenen Hardwarewerten |
| `system_data_cleaned.csv`   | ausgelesene Hardwarewerte, bereinigt mittels energy_manager/data_cleaner.py um patologische Datenwerte |
| `cpu_freq_predictor.keras` | Gespeichertes neuronales Netzmodell (automatisch generiert). |
| `scaler_X.pkl`     | Scaler für Eingabedaten (automatisch generiert).    |
| `scaler_y.pkl`     | Scaler für Zielvariable (CPU-Frequenz) (automatisch generiert). |


## **Installation via pip**

pip install https://github.com/Jomon-Dogu/energy_manager/releases/download/v0.0.1/energy_manager-0.0.1-py3-none-any.whl
