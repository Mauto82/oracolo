from typing import List, Dict, Tuple
from datetime import datetime
import colorama
from colorama import Fore, Style
from tabulate import tabulate
import numpy as np
from collections import Counter

class OutputFormatter:
    def __init__(self):
        colorama.init()
        self.MAX_BARS = 50

    def format_prediction(self, date: str, wheel: str, numbers: List[int],
                         historical_data: List[List[int]]) -> str:
        """Formatta la predizione completa con statistiche e visualizzazioni"""
        try:
            formatted_date = datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')
        except ValueError:
            formatted_date = date

        output_parts = [
            "\n" + "="*50,
            self._format_basic_prediction(formatted_date, wheel, numbers),
        ]

        if historical_data:
            output_parts.extend([
                self._format_statistics(historical_data, wheel),
                self._format_frequency_chart(historical_data, wheel),
                self._format_patterns(historical_data, wheel, numbers),
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

    def _format_statistics(self, historical_data: List[List[int]], wheel: str) -> str:
        """Calcola e formatta statistiche interessanti dai dati storici"""
        if not historical_data:
            return ""

        stats = self._calculate_statistics(historical_data)

        header = [f"{Fore.CYAN}Statistiche Storiche - {wheel}{Style.RESET_ALL}"]
        data = []

        if stats['most_common']:
            data.append([f"{Fore.GREEN}Numeri più frequenti:{Style.RESET_ALL} "
                        f"{', '.join(map(str, stats['most_common']))}"])

        if stats['least_common']:
            data.append([f"{Fore.GREEN}Numeri meno frequenti:{Style.RESET_ALL} "
                        f"{', '.join(map(str, stats['least_common']))}"])

        if stats['hot_numbers']:
            data.append([f"{Fore.GREEN}Numeri caldi:{Style.RESET_ALL} "
                        f"{', '.join(map(str, stats['hot_numbers']))}"])

        return "\n" + tabulate(data, header, tablefmt="fancy_grid") if data else ""

    def _format_frequency_chart(self, historical_data: List[List[int]], wheel: str) -> str:
        """Crea un grafico ASCII delle frequenze dei numeri"""
        if not historical_data:
            return ""

        all_numbers = [num for extract in historical_data for num in extract]
        if not all_numbers:
            return ""

        freqs = Counter(all_numbers)
        max_freq = max(freqs.values())

        header = [f"\n{Fore.CYAN}Grafico Frequenze Numeri - {wheel}{Style.RESET_ALL}"]
        chart = []

        for num in sorted(freqs.keys()):
            if freqs[num] > 0:
                bar_length = int((freqs[num] / max_freq) * self.MAX_BARS)
                bar = "█" * bar_length
                chart.append(f"{Fore.GREEN}{num:02d}{Style.RESET_ALL} |"
                           f"{Fore.BLUE}{bar}{Style.RESET_ALL} ({freqs[num]})")

        return "\n".join(header + chart)

    def _format_patterns(self, historical_data: List[List[int]], wheel: str,
                        numbers: List[int]) -> str:
        """Analizza e formatta pattern interessanti nei numeri"""
        if not historical_data:
            return ""

        pairs = self._find_common_pairs(historical_data)

        header = [f"{Fore.CYAN}Pattern Individuati{Style.RESET_ALL}"]
        data = []

        if pairs:
            data.append([f"{Fore.GREEN}Coppie frequenti:{Style.RESET_ALL} "
                        f"{', '.join(f'{a}-{b}' for a, b in pairs[:3])}"])

        return "\n" + tabulate(data, header, tablefmt="fancy_grid") if data else ""

    def _calculate_statistics(self, data: List[List[int]]) -> Dict:
        """Calcola statistiche sui numeri"""
        if not data:
            return {'most_common': [], 'least_common': [], 'hot_numbers': []}

        all_numbers = [num for extract in data for num in extract]
        counter = Counter(all_numbers)

        return {
            'most_common': [num for num, _ in counter.most_common(5)],
            'least_common': [num for num, _ in sorted(counter.items(),
                                                    key=lambda x: x[1])[:5]],
            'hot_numbers': [num for num, _ in counter.most_common(3)]
        }

    def _find_common_pairs(self, data: List[List[int]]) -> List[Tuple[int, int]]:
        """Trova le coppie di numeri più frequenti"""
        if not data:
            return []

        pairs = []
        for numbers in data:
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    pairs.append(tuple(sorted([numbers[i], numbers[j]])))

        return [pair for pair, _ in Counter(pairs).most_common(3)]

    def format_error(self, message: str) -> str:
        """Formatta i messaggi di errore"""
        return f"\n{Fore.RED}Errore: {message}{Style.RESET_ALL}\n"

    def format_training_info(self, total_records: int) -> str:
        """Formatta le informazioni sull'addestramento"""
        return (
            f"\n{Fore.BLUE}Info Addestramento:{Style.RESET_ALL}\n"
            f"Record utilizzati: {total_records}\n"
        )