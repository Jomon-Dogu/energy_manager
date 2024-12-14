import pandas as pd

class SystemDataCleaner:
    def __init__(self, input_file: str, output_file: str, freq_min: int = 400, freq_max: int = 2000):
        """
        Initialisiert den SystemDataCleaner.
        
        Parameter:
        - input_file (str): Pfad zur Eingabedatei (CSV-Datei).
        - output_file (str): Pfad zur Ausgabedatei (CSV-Datei, die die bereinigten Daten speichert).
        - freq_min (int): Mindestgrenze für die Frequenzfilterung.
        - freq_max (int): Höchstgrenze für die Frequenzfilterung.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.data = None  # Originaldaten
        self.filtered_data = None  # Gefilterte Daten

    def load_data(self):
        """Lädt die Systemdaten aus einer CSV-Datei."""
        try:
            self.data = pd.read_csv(self.input_file)
            print(f"✅ Systemdaten erfolgreich geladen. Anzahl der Einträge: {len(self.data)}")
        except FileNotFoundError:
            print(f"❌ Fehler: Datei '{self.input_file}' wurde nicht gefunden.")
        except Exception as e:
            print(f"❌ Fehler beim Laden der Datei: {e}")

    def filter_outliers(self):
        """Filtert Frequenzen außerhalb des Bereichs [freq_min, freq_max]."""
        if self.data is not None:
            # Überprüfen, ob die Spalte 'cpu_freq' existiert
            if 'cpu_freq' in self.data.columns:
                self.filtered_data = self.data[(self.data['cpu_freq'] >= self.freq_min) & 
                                               (self.data['cpu_freq'] <= self.freq_max)]
                print(f"✅ Ausreißer entfernt. Neue Anzahl der Einträge: {len(self.filtered_data)}")
            else:
                print("❌ Fehler: 'cpu_freq'-Spalte wurde in den Daten nicht gefunden.")
        else:
            print("❌ Fehler: Daten wurden nicht geladen. Rufe 'load_data()' auf.")

    def save_cleaned_data(self):
        """Speichert die gefilterten Daten in einer neuen CSV-Datei."""
        if self.filtered_data is not None:
            try:
                self.filtered_data.to_csv(self.output_file, index=False)
                print(f"✅ Bereinigte Datei wurde erfolgreich gespeichert unter '{self.output_file}'.")
            except Exception as e:
                print(f"❌ Fehler beim Speichern der Datei: {e}")
        else:
            print("❌ Fehler: Es gibt keine gefilterten Daten zum Speichern. Rufe 'filter_outliers()' auf.")

    def show_statistics(self):
        """Zeigt die Statistik der CPU-Frequenz vor und nach der Filterung an."""
        if self.data is not None:
            print("\n📊 Statistik der CPU-Frequenz vor der Filterung:")
            print(self.data['cpu_freq'].describe())
        
        if self.filtered_data is not None:
            print("\n📊 Statistik der CPU-Frequenz nach der Filterung:")
            print(self.filtered_data['cpu_freq'].describe())

    def run(self):
        """Führt den vollständigen Prozess aus (Laden, Filtern, Speichern und Statistiken anzeigen)."""
        self.load_data()
        self.show_statistics()  # Statistik vor der Filterung
        self.filter_outliers()
        self.show_statistics()  # Statistik nach der Filterung
        self.save_cleaned_data()
