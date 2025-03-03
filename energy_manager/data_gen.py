import pandas as pd
from ctgan import CTGAN
from sklearn.preprocessing import MinMaxScaler



csv_datei = "../gen_input_data.csv"  # Ersetze mit dem tatsächlichen Pfad zur CSV-Datei

df = pd.read_csv(csv_datei)
print("Originaldaten")
print(df.head())  # Zeigt die ersten Zeilen der CSV-Datei an

# 📌 2. Skalieren der numerischen Daten
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# 📌 3. Trainiere das CTGAN-Modell
model = CTGAN(epochs=300)  # Mehr Epochs für bessere Qualität
model.fit(df_scaled)

# 📌 4. Generiere synthetische Daten
synthetic_data = model.sample(100)  # Statt num_rows=10

# 📌 5. Rücktransformation der Daten
synthetic_data_original_scale = pd.DataFrame(scaler.inverse_transform(synthetic_data), columns=df.columns)

# 📌 6. Ausgabe der synthetischen Daten

print("synthetische Daten")
print(synthetic_data_original_scale)
for index, row in synthetic_data_original_scale.iterrows():
    print(row.to_dict())  # Gibt jede Zeile als Dictionary aus