from abc import ABC, abstractmethod
from typing import List, Tuple

class SystemInterface(ABC):
    """Interfaccia base per tutti i sistemi di gioco"""

    @abstractmethod
    def generate_combinations(self, numbers: List[int], combination_size: int, **kwargs) -> List[Tuple[int, ...]]:
        """
        Genera le combinazioni per il sistema.

        Args:
            numbers: Lista dei numeri base
            combination_size: Dimensione delle combinazioni da generare
            **kwargs: Parametri aggiuntivi specifici del sistema

        Returns:
            List[Tuple[int, ...]]: Lista delle combinazioni generate

        Raises:
            ValueError: Se i parametri non sono validi
        """
        pass