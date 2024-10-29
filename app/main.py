import sys
from config import Config
from services.lotto_service import LottoService

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <date> <wheel>")
        sys.exit(1)

    date = sys.argv[1]
    wheel = sys.argv[2]

    config = Config()
    service = LottoService(config)

    try:
        service.initialize_predictor("decision_tree")
        service.train_model()
        prediction = service.predict(date, wheel)

        print(f'Previsioni per data: {date}; ruota: {wheel}')
        print(f'Numeri previsti: {prediction}')
    except Exception as e:
        print(f"Errore durante la predizione: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()