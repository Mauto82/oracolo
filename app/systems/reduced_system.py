from itertools import combinations
from typing import List, Tuple
from .system_interface import SystemInterface

class ReducedSystem(SystemInterface):
    """Implementa un sistema ridotto che genera un sottoinsieme ottimizzato di combinazioni"""

    def generate_combinations(self, numbers: List[int], combination_size: int, **kwargs) -> List[Tuple[int, ...]]:
        """
        Genera un sottoinsieme ottimizzato di combinazioni.

        Args:
            numbers: Lista dei numeri base
            combination_size: Dimensione delle combinazioni da generare

        Returns:
            List[Tuple[int, ...]]: Lista delle combinazioni ottimizzate

        Raises:
            ValueError: Se i parametri non sono validi
        """
        if combination_size < 2 or combination_size > 4:
            raise ValueError("Il numero di elementi deve essere tra 2 e 4")

        if len(numbers) < combination_size:
            raise ValueError(f"Servono almeno {combination_size} numeri per creare combinazioni")

        # Genera tutte le combinazioni e seleziona un sottoinsieme ottimizzato
        all_combinations = list(combinations(sorted(numbers), combination_size))

        # Per ora selezioniamo una ogni due combinazioni
        # In futuro si può implementare un algoritmo più sofisticato
        reduced_combinations = all_combinations[::2]

        if not reduced_combinations:
            raise ValueError("Nessuna combinazione generata")

        return reduced_combinations