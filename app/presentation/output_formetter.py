from typing import List
from datetime import datetime
import colorama
from colorama import Fore, Style
from tabulate import tabulate

class OutputFormatter:
    def __init__(self):
        colorama.init()

    def format_prediction(self, date: str, wheel: str, numbers: List[int]) -> str:
        """Formatta la predizione in modo leggibile e colorato"""
        try:
            formatted_date = datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')
        except ValueError:
            formatted_date = date

        header = [f"{Fore.CYAN}Dettagli Predizione{Style.RESET_ALL}"]
        data = [
            [f"{Fore.GREEN}Data:{Style.RESET_ALL} {formatted_date}"],
            [f"{Fore.GREEN}Ruota:{Style.RESET_ALL} {wheel.upper()}"],
            [f"{Fore.GREEN}Numeri Predetti:{Style.RESET_ALL}"]
        ]

        numbers_table = [[
            f"{Fore.YELLOW}{num:02d}{Style.RESET_ALL}"
            for num in sorted(numbers)
        ]]

        output_parts = [
            "\n" + "="*50,
            tabulate(data, header, tablefmt="fancy_grid"),
            tabulate(numbers_table, tablefmt="grid"),
            "="*50 + "\n"
        ]

        return "\n".join(output_parts)

    def format_error(self, message: str) -> str:
        """Formatta i messaggi di errore"""
        return f"\n{Fore.RED}Errore: {message}{Style.RESET_ALL}\n"

    def format_training_info(self, total_records: int) -> str:
        """Formatta le informazioni sull'addestramento"""
        return (
            f"\n{Fore.BLUE}Info Addestramento:{Style.RESET_ALL}\n"
            f"Record utilizzati: {total_records}\n"
        )