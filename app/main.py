import sys
from config import Config
from services.lotto_service import LottoService
from presentation.output_formatter import OutputFormatter

def main():
    if len(sys.argv) != 3:
        formatter = OutputFormatter()
        print(formatter.format_error("Uso: python main.py <data> <ruota>"))
        print("Esempio: python main.py 20240101 MI")
        sys.exit(1)

    date = sys.argv[1]
    wheel = sys.argv[2].upper()

    try:
        config = Config()
        service = LottoService(config)
        formatter = OutputFormatter()

        # Inizializza e addestra il modello
        service.initialize_predictor("decision_tree")
        service.train_model()

        # Effettua la predizione
        prediction, historical_data = service.predict(date, wheel)

        # Formatta e mostra i risultati
        print(formatter.format_prediction(
            date=date,
            wheel=wheel,
            numbers=prediction,
            historical_data=historical_data
        ))

    except Exception as e:
        formatter = OutputFormatter()
        print(formatter.format_error(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()