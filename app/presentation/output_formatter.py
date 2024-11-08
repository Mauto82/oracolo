# app/presentation/output_formatter.py
from typing import List, Dict, Tuple
from datetime import datetime
import colorama
from colorama import Fore, Style
from tabulate import tabulate
from collections import Counter
from itertools import combinations
from systems import IntegralSystem, ReducedSystem, GuaranteedSystem

class OutputFormatter:
    def __init__(self):
        colorama.init()
        self.MAX_BARS = 50  # Lunghezza massima delle barre nel grafico

    def format_prediction(self, date: str, wheel: str, numbers: List[int],
                         historical_data: List[List[int]]) -> str:
        """Formatta la predizione completa con statistiche e visualizzazioni"""
        try:
            formatted_date = datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        except ValueError:
            formatted_date = date

        output_parts = [
            "\n" + "="*50,
            self._format_basic_prediction(formatted_date, wheel, numbers),
        ]

        if historical_data:
            output_parts.extend([
                self.format_statistics(historical_data, wheel),
                self.format_frequency_chart(historical_data, wheel),
            ])

        output_parts.append("="*50 + "\n")
        return "\n".join(filter(None, output_parts))

    def _format_basic_prediction(self, date: str, wheel: str,
                               numbers: List[int]) -> str:
        """Formatta la predizione base con data, ruota e numeri"""
        header = [f"{Fore.CYAN}Dettagli Predizione{Style.RESET_ALL}"]
        data = [
            [f"{Fore.GREEN}Data:{Style.RESET_ALL} {date}"],
            [f"{Fore.GREEN}Ruota:{Style.RESET_ALL} {wheel.upper()}"],
            [f"{Fore.GREEN}Numeri Predetti:{Style.RESET_ALL}"]
        ]

        numbers_table = [[
            f"{Fore.YELLOW}{num:02d}{Style.RESET_ALL}"
            for num in sorted(numbers)
        ]]

        return (
            tabulate(data, header, tablefmt="fancy_grid") + "\n" +
            tabulate(numbers_table, tablefmt="grid")
        )

    def format_statistics(self, historical_data: List[List[int]], wheel: str) -> str:
        """Formatta le statistiche dei numeri estratti"""
        if not historical_data:
            return ""

        # Calcola le statistiche
        all_numbers = [num for extract in historical_data for num in extract]
        counter = Counter(all_numbers)

        most_common = counter.most_common(5)
        least_common = sorted(counter.items(), key=lambda x: x[1])[:5]

        # Prepara i dati per la tabella
        header = [f"{Fore.CYAN}Statistiche - {wheel}{Style.RESET_ALL}"]
        data = [
            [f"{Fore.GREEN}Numeri più frequenti:{Style.RESET_ALL} " +
             ", ".join(f"{num:02d}({count})" for num, count in most_common)],
            [f"{Fore.GREEN}Numeri meno frequenti:{Style.RESET_ALL} " +
             ", ".join(f"{num:02d}({count})" for num, count in least_common)],
            [f"{Fore.GREEN}Numeri totali analizzati:{Style.RESET_ALL} {len(all_numbers)}"],
            [f"{Fore.GREEN}Estrazioni analizzate:{Style.RESET_ALL} {len(historical_data)}"],
        ]

        return "\n" + tabulate(data, header, tablefmt="fancy_grid")

    def format_frequency_chart(self, historical_data: List[List[int]], wheel: str) -> str:
        """Crea un grafico ASCII delle frequenze dei numeri"""
        if not historical_data:
            return ""

        # Calcola le frequenze
        all_numbers = [num for extract in historical_data for num in extract]
        counter = Counter(all_numbers)

        if not counter:
            return ""

        max_freq = max(counter.values())

        # Crea l'header del grafico
        output = [f"\n{Fore.CYAN}Grafico Frequenze - {wheel}{Style.RESET_ALL}"]

        # Crea le barre del grafico
        for num in range(1, 91):  # Numeri da 1 a 90
            if num in counter:
                freq = counter[num]
                bar_length = int((freq / max_freq) * self.MAX_BARS)
                bar = "█" * bar_length
                output.append(
                    f"{Fore.GREEN}{num:02d}{Style.RESET_ALL} |"
                    f"{Fore.BLUE}{bar}{Style.RESET_ALL} ({freq})"
                )
            else:
                output.append(f"{Fore.GREEN}{num:02d}{Style.RESET_ALL} |")

        return "\n".join(output)

    def format_integral_system(self, numbers: List[int], n: int) -> str:
        """
        Formatta un sistema integrale.

        Args:
            numbers: Lista dei numeri base
            n: Numero di numeri per combinazione

        Returns:
            str: Output formattato del sistema
        """
        try:
            system = IntegralSystem()
            combinations = system.generate_combinations(numbers, n)

            output = [
                "\n" + "="*50,
                f"SISTEMA INTEGRALE {n} NUMERI",
                "="*50,
                f"\nNumeri base: {', '.join(map(str, sorted(numbers)))}"
                f"\nCombinazioni di {n} numeri:",
                "-"*50
            ]

            for i, comb in enumerate(combinations, 1):
                output.append(f"{i:2d}) {' - '.join(map(str, comb))}")

            output.extend([
                "-"*50,
                f"Totale combinazioni: {len(combinations)}",
                "="*50 + "\n"
            ])

            return '\n'.join(output)

        except ValueError as e:
            return self.format_error(str(e))

    def format_reduced_system(self, numbers: List[int], n: int) -> str:
        """
        Formatta un sistema ridotto.

        Args:
            numbers: Lista dei numeri base
            n: Numero di numeri per combinazione

        Returns:
            str: Output formattato del sistema
        """
        try:
            system = ReducedSystem()
            combinations = system.generate_combinations(numbers, n)

            output = [
                "\n" + "="*50,
                f"SISTEMA RIDOTTO {n} NUMERI",
                "="*50,
                f"\nNumeri base: {', '.join(map(str, sorted(numbers)))}"
                f"\nCombinazioni ridotte di {n} numeri:",
                "-"*50
            ]

            for i, comb in enumerate(combinations, 1):
                output.append(f"{i:2d}) {' - '.join(map(str, comb))}")

            output.extend([
                "-"*50,
                f"Totale combinazioni: {len(combinations)}",
                "="*50 + "\n"
            ])

            return '\n'.join(output)

        except ValueError as e:
            return self.format_error(str(e))

    def format_guaranteed_system(self, numbers: List[int], nums: int, win: int) -> str:
        """
        Formatta un sistema garantito.

        Args:
            numbers: Lista dei numeri base
            nums: Numero di numeri per combinazione
            win: Numero di punti garantiti

        Returns:
            str: Output formattato del sistema
        """
        try:
            system = GuaranteedSystem()
            combinations = system.find_minimum_guaranteed_combinations(numbers, nums, win)
            optimized_combs = system.optimize_combinations(combinations, win)

            output = [
                "\n" + "="*50,
                f"SISTEMA GARANTITO {nums}/{win}",
                "="*50,
                f"\nNumeri base: {', '.join(map(str, sorted(numbers)))}"
                f"\nCombinazioni che garantiscono {win} punti con {nums} numeri:",
                "-"*50
            ]

            for i, comb in enumerate(optimized_combs, 1):
                output.append(f"{i:2d}) {' - '.join(map(str, comb))}")

            output.extend([
                "-"*50,
                f"Totale combinazioni: {len(optimized_combs)}",
                f"Vincita garantita: {win} punti",
                "="*50 + "\n"
            ])

            return '\n'.join(output)

        except ValueError as e:
            return self.format_error(str(e))

    def format_error(self, message: str) -> str:
        """Formatta i messaggi di errore"""
        return f"\n{Fore.RED}Errore: {message}{Style.RESET_ALL}\n"

    def format_training_info(self, total_records: int) -> str:
        """Formatta le informazioni sull'addestramento"""
        return (
            f"\n{Fore.BLUE}Info Addestramento:{Style.RESET_ALL}\n"
            f"Record utilizzati: {total_records}\n"
        )