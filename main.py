from energy_manager.predictor import predict_cpu_frequency
from energy_manager.train_model import train_model
from energy_manager.data_cleaner import SystemDataCleaner

if __name__ == "__main__":
    # Erstelle eine Instanz des SystemDataCleaner
    cleaner = SystemDataCleaner(
        input_file="system_data_2.csv", 
        output_file="system_data_cleaned.csv", 
        freq_min=400, 
        freq_max=2000
    )

    # Führe den gesamten Prozess aus (Laden, Filtern, Speichern, Statistiken)
    cleaner.run()
    train_model()
    predict_cpu_frequency()
