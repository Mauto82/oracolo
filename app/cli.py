# app/cli.py
import cmd
import sys
import os
from datetime import datetime
from typing import Optional
from config import Config
from services.lotto_service import LottoService
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
            print("  predict <data> <ruota> - Effettua una predizione", file=self.stdout)
            print("     formato data: DD/MM/YYYY (es: 01/01/2024)", file=self.stdout)
            print("  stats <ruota>         - Mostra statistiche per una ruota", file=self.stdout)
            print("  ruote                 - Mostra le ruote disponibili", file=self.stdout)
            print("  clear                 - Pulisce lo schermo", file=self.stdout)
            print("  help                  - Mostra questo messaggio", file=self.stdout)
            print("  quit                  - Esci dal programma", file=self.stdout)
            print("\nEsempi:", file=self.stdout)
            print("  predict 01/01/2024 MI", file=self.stdout)
            print("  stats MI", file=self.stdout)
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