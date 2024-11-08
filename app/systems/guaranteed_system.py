from itertools import combinations as iter_combinations
from typing import List, Set, Tuple
from .system_interface import SystemInterface

class GuaranteedSystem:
    @staticmethod
    def verify_guarantee(combination: Tuple[int, ...], win_size: int) -> bool:
        """
        Verifica se una combinazione garantisce la vincita richiesta.
        """
        # Usa iter_combinations invece di combinations
        winning_combs = set(iter_combinations(combination, win_size))
        return len(winning_combs) > 0

    @staticmethod
    def find_minimum_guaranteed_combinations(numbers: List[int],
                                          system_size: int,
                                          win_size: int) -> List[Tuple[int, ...]]:
        """
        Trova il minimo insieme di combinazioni che garantisce la vincita.
        """
        if system_size < win_size:
            raise ValueError(f"Impossibile garantire {win_size} punti con {system_size} numeri")
        if win_size < 2 or win_size > 4:
            raise ValueError("I punti garantiti devono essere tra 2 e 4")
        if len(numbers) < system_size:
            raise ValueError(f"Servono almeno {system_size} numeri per creare il sistema")

        # Usa iter_combinations invece di combinations
        all_combinations = list(iter_combinations(sorted(numbers), system_size))

        guaranteed_combs = [
            comb for comb in all_combinations
            if GuaranteedSystem.verify_guarantee(comb, win_size)
        ]

        if not guaranteed_combs:
            raise ValueError(
                f"Impossibile garantire {win_size} punti con le combinazioni di {system_size} numeri"
            )

        return guaranteed_combs

    @staticmethod
    def optimize_combinations(combinations: List[Tuple[int, ...]],
                            win_size: int) -> List[Tuple[int, ...]]:
        """
        Ottimizza le combinazioni rimuovendo quelle ridondanti.
        """
        all_win_combs: Set[Tuple[int, ...]] = set()
        for comb in combinations:
            # Usa iter_combinations invece di combinations
            all_win_combs.update(iter_combinations(comb, win_size))

        result = [combinations[0]]
        # Usa iter_combinations invece di combinations
        current_win_combs = set(iter_combinations(combinations[0], win_size))

        for comb in combinations[1:]:
            # Usa iter_combinations invece di combinations
            new_win_combs = set(iter_combinations(comb, win_size))
            if not new_win_combs.issubset(current_win_combs):
                result.append(comb)
                current_win_combs.update(new_win_combs)

            if current_win_combs == all_win_combs:
                break

        return result