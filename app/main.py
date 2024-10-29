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
    wheel = sys.argv[2]

    config = Config()
    service = LottoService(config)
    formatter = OutputFormatter()

    try:
        service.initialize_predictor("decision_tree")
        service.train_model()
        prediction = service.predict(date, wheel)

        print(formatter.format_prediction(date, wheel, prediction))

    except Exception as e:
        print(formatter.format_error(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()