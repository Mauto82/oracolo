# app/cli.py
import cmd
import sys
import os
from datetime import datetime
from typing import Optional
from config import Config
from services.lotto_service import LottoService
from services.format_converter import FormatConverter
from presentation.output_formatter import OutputFormatter

class LottoConsole(cmd.Cmd):
    intro = f"""\033[1m{'-'*50}
Benvenuto in Oracolo!
Digita 'help' o '?' per la lista dei comandi.
{'-'*50}\033[0m"""
    prompt = '\033[94m(oracolo)\033[0m '

    def __init__(self, stdout=None):
        """Inizializza la console"""
        super().__init__()
        self.stdout = stdout or sys.stdout
        
        # Inizializzazione dei componenti
        self.config = Config()
        self.service = LottoService(self.config)
        self.formatter = OutputFormatter()
        self.converter = FormatConverter(self.config)

        # Inizializzazione del modello (skip in test mode)
        if not hasattr(self.stdout, 'getvalue'):  # Non è uno StringIO
            try:
                print("Inizializzazione del modello in corso...", file=self.stdout)
                self.service.initialize_predictor("decision_tree")
                self.service.train_model()
                print("Modello inizializzato con successo!\n", file=self.stdout)
            except Exception as e:
                print(f"Errore durante l'inizializzazione: {str(e)}\n", file=self.stdout)

    def _convert_date_format(self, date: str) -> str:
        """Converte la data dal formato DD/MM/YYYY a YYYYMMDD"""
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            return date_obj.strftime('%Y%m%d')
        except ValueError:
            raise ValueError("Formato data non valido. Usa DD/MM/YYYY (es: 01/01/2024)")

    def do_predict(self, arg: str) -> None:
        """
        Effettua una predizione per una data e ruota specifiche.
        Uso: predict <data> <ruota>
        Esempio: predict 01/01/2024 MI
        """
        args = arg.split()
        if len(args) != 2:
            error_msg = self.formatter.format_error(
                "Uso corretto: predict <data> <ruota>\n"
                "Esempio: predict 01/01/2024 MI"
            )
            print(error_msg, file=self.stdout)
            return

        date, wheel = args
        try:
            service_date = self._convert_date_format(date)
            prediction, historical_data = self.service.predict(service_date, wheel.upper())
            output = self.formatter.format_prediction(date, wheel, prediction, historical_data)
            print(output, file=self.stdout)
        except ValueError as e:
            error_msg = self.formatter.format_error(f"Errore: {str(e)}")
            print(error_msg, file=self.stdout)
        except Exception as e:
            error_msg = self.formatter.format_error(f"Errore imprevisto: {str(e)}")
            print(error_msg, file=self.stdout)

    def do_ruote(self, arg: str) -> None:
        """
        Mostra la lista delle ruote disponibili.
        Uso: ruote
        """
        print("\nRuote disponibili:", file=self.stdout)
        for ruota in sorted(self.config.RUOTE.keys()):
            print(f"- {ruota}", file=self.stdout)
        print(file=self.stdout)

    def do_stats(self, arg: str) -> None:
        """
        Mostra le statistiche per una ruota specifica.
        Uso: stats <ruota>
        Esempio: stats MI
        """
        if not arg:
            print(self.formatter.format_error("Specifica una ruota. Esempio: stats MI"),
                  file=self.stdout)
            return

        wheel = arg.upper()
        try:
            current_date = datetime.now().strftime('%Y%m%d')
            _, historical_data = self.service.predict(current_date, wheel)
            if historical_data:
                print(self.formatter.format_statistics(historical_data, wheel), file=self.stdout)
                print(self.formatter.format_frequency_chart(historical_data, wheel), file=self.stdout)
            else:
                print(self.formatter.format_error(
                    f"Nessun dato storico trovato per la ruota {wheel}"),
                    file=self.stdout)
        except ValueError as e:
            print(self.formatter.format_error(str(e)), file=self.stdout)

    def do_convert(self, arg: str) -> None:
        """
        Converte il file storico nel formato utilizzato dall'applicazione.
        Uso: convert [input_file] [output_file]
        Se non specificati, usa i file configurati in Config.
        """
        args = arg.split()

        # Usa i path dalla configurazione se non specificati
        input_file = self.config.HISTORICAL_SOURCE_FILE
        output_file = self.config.HISTORICAL_OUTPUT_FILE

        if len(args) >= 1:
            input_file = args[0]
            # Se il path non è assoluto, lo considera relativo alla directory data/
            if not os.path.isabs(input_file):
                input_file = os.path.join('data', input_file)

        if len(args) >= 2:
            output_file = args[1]
            if not os.path.isabs(output_file):
                output_file = os.path.join('data', output_file)

        try:
            # Assicurati che la directory di output esista
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            self.converter.convert_lotto_format(input_file, output_file)
            print(f"\nConversione completata con successo!", file=self.stdout)
            print(f"File convertito salvato in: {output_file}\n", file=self.stdout)
        except Exception as e:
            print(self.formatter.format_error(f"Errore durante la conversione: {str(e)}"),
                  file=self.stdout)

    def do_sistema(self, arg: str) -> None:
        """
        Crea un sistema basato sulla predizione per una data e ruota specifiche.

        Uso: sistema <data> <ruota> <tipo> [parametri]

        Tipi disponibili:
            - integrale N: Tutte le possibili combinazioni di N numeri (2-4)
            - ridotto N: Un sottoinsieme ottimizzato di combinazioni di N numeri (2-4)
            - garantito N/P: Sistema che garantisce P punti con N numeri

        Esempi:
            sistema 01/01/2024 MI integrale 2    # Tutte le combinazioni di 2 numeri
            sistema 01/01/2024 MI ridotto 3      # Sistema ridotto con terzine
            sistema 01/01/2024 MI garantito 3/2  # Sistema che garantisce ambo su 3 numeri
        """
        args = arg.split()
        if len(args) < 3:
            error_msg = self.formatter.format_error(
                "Uso corretto: sistema <data> <ruota> <tipo> [parametri]\n"
                "Esempio: sistema 01/01/2024 MI integrale 2"
            )
            print(error_msg, file=self.stdout)
            return

        date, wheel, system_type = args[:3]
        params = args[3] if len(args) > 3 else None

        try:
            # Ottiene la predizione
            service_date = self._convert_date_format(date)
            prediction, _ = self.service.predict(service_date, wheel.upper())

            # Genera il sistema in base al tipo richiesto
            if system_type.lower() == 'integrale':
                if not params:
                    raise ValueError("Specificare il numero di numeri per combinazione (2-4)")
                n = int(params)
                output = self.formatter.format_integral_system(prediction, n)

            elif system_type.lower() == 'ridotto':
                if not params:
                    raise ValueError("Specificare il numero di numeri per combinazione (2-4)")
                n = int(params)
                output = self.formatter.format_reduced_system(prediction, n)

            elif system_type.lower() == 'garantito':
                if not params or '/' not in params:
                    raise ValueError("Specificare numeri/punti (es: 3/2)")
                nums, win = map(int, params.split('/'))
                output = self.formatter.format_guaranteed_system(prediction, nums, win)

            else:
                raise ValueError(f"Tipo sistema '{system_type}' non valido")

            print(output, file=self.stdout)

        except ValueError as e:
            error_msg = self.formatter.format_error(f"Errore: {str(e)}")
            print(error_msg, file=self.stdout)
        except Exception as e:
            error_msg = self.formatter.format_error(f"Errore imprevisto: {str(e)}")
            print(error_msg, file=self.stdout)

    def do_clear(self, arg: str) -> None:
        """
        Pulisce lo schermo.
        Uso: clear
        """
        if hasattr(self.stdout, 'getvalue'):  # In test mode
            return
            
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.intro, file=self.stdout)

    def do_help(self, arg: str) -> None:
        """Mostra l'help dei comandi disponibili"""
        if arg:
            # Help specifico per un comando
            super().do_help(arg)
        else:
            print("\nComandi disponibili:", file=self.stdout)
            print("  predict <data> <ruota>  - Effettua una predizione", file=self.stdout)
            print("     formato data: DD/MM/YYYY (es: 01/01/2024)", file=self.stdout)
            print("  sistema <data> <ruota> <tipo> [params] - Crea sistemi di gioco", file=self.stdout)
            print("     tipi: integrale N, ridotto N, garantito N/P", file=self.stdout)
            print("  stats <ruota>          - Mostra statistiche per una ruota", file=self.stdout)
            print("  ruote                  - Mostra le ruote disponibili", file=self.stdout)
            print("  convert                - Converte il file storico nel formato dell'app", file=self.stdout)
            print("  clear                  - Pulisce lo schermo", file=self.stdout)
            print("  help                   - Mostra questo messaggio", file=self.stdout)
            print("  quit                   - Esci dal programma", file=self.stdout)
            print("\nEsempi:", file=self.stdout)
            print("  predict 01/01/2024 MI", file=self.stdout)
            print("  sistema 01/01/2024 MI integrale 2", file=self.stdout)
            print("  stats MI", file=self.stdout)
            print("  convert", file=self.stdout)
            print(file=self.stdout)

    def do_quit(self, arg: str) -> bool:
        """
        Esce dal programma.
        Uso: quit
        """
        print("\nArrivederci!\n", file=self.stdout)
        return True

    def default(self, line: str) -> None:
        """Gestisce i comandi non riconosciuti"""
        print(self.formatter.format_error(
            f"Comando non riconosciuto: {line}\n"
            "Usa 'help' per vedere i comandi disponibili."
        ), file=self.stdout)

    def emptyline(self) -> None:
        """Non fa nulla quando viene premuto solo Enter"""
        pass

def main():
    """Entry point dell'applicazione"""
    try:
        LottoConsole().cmdloop()
    except KeyboardInterrupt:
        print("\nArrivederci!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nErrore imprevisto: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()