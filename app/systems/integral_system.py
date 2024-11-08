from itertools import combinations
from typing import List, Tuple
from .system_interface import SystemInterface

class IntegralSystem(SystemInterface):
    """Implementa un sistema integrale che genera tutte le possibili combinazioni"""

    def generate_combinations(self, numbers: List[int], combination_size: int, **kwargs) -> List[Tuple[int, ...]]:
        """
        Genera tutte le possibili combinazioni dei numeri dati.

        Args:
            numbers: Lista dei numeri base
            combination_size: Dimensione delle combinazioni da generare

        Returns:
            List[Tuple[int, ...]]: Lista di tutte le combinazioni possibili

        Raises:
            ValueError: Se i parametri non sono validi
        """
        if combination_size < 2 or combination_size > 4:
            raise ValueError("Il numero di elementi deve essere tra 2 e 4")

        if len(numbers) < combination_size:
            raise ValueError(f"Servono almeno {combination_size} numeri per creare combinazioni")

        return list(combinations(sorted(numbers), combination_size))