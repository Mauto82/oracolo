from itertools import combinations as iter_combinations
from typing import List, Set, Tuple
from .system_interface import SystemInterface

class GuaranteedSystem(SystemInterface):
    def generate_combinations(self, numbers: List[int], combination_size: int, **kwargs) -> List[Tuple[int, ...]]:
        """
        Genera combinazioni che garantiscono una vincita specifica.
        
        Args:
            numbers: Lista dei numeri base
            combination_size: Dimensione delle combinazioni da generare
            **kwargs: Parametri aggiuntivi (win_size per la garanzia)
        
        Returns:
            List[Tuple[int, ...]]: Lista delle combinazioni che garantiscono la vincita
        """
        win_size = kwargs.get('win_size', 2)
        
        if combination_size < 2 or combination_size > 4:
            raise ValueError("Il numero di elementi deve essere tra 2 e 4")
        
        if win_size < 2 or win_size > combination_size:
            raise ValueError(f"La garanzia deve essere tra 2 e {combination_size}")
        
        if len(numbers) < combination_size:
            raise ValueError(f"Servono almeno {combination_size} numeri per creare combinazioni")
        
        return self.find_minimum_guaranteed_combinations(numbers, combination_size, win_size)

    @staticmethod
    def verify_guarantee(combinations: List[Tuple[int, ...]], target_numbers: Set[int], win_size: int) -> bool:
        """
        Verifica se un insieme di combinazioni garantisce una vincita di win_size
        quando escono numeri dal set target_numbers.
        
        Args:
            combinations: Lista delle combinazioni del sistema
            target_numbers: Set di numeri che potrebbero essere estratti
            win_size: Numero minimo di numeri da indovinare per la vincita
            
        Returns:
            bool: True se il sistema garantisce la vincita, False altrimenti
        """
        # Per ogni possibile sottoinsieme di win_size numeri dal target
        for target_subset in iter_combinations(target_numbers, win_size):
            target_set = set(target_subset)
            
            # Verifica se almeno una combinazione copre questo sottoinsieme
            covered = False
            for comb in combinations:
                if len(target_set & set(comb)) >= win_size:
                    covered = True
                    break
            
            # Se nessuna combinazione copre questo sottoinsieme, non c'è garanzia
            if not covered:
                return False
        
        return True

    @staticmethod
    def find_minimum_guaranteed_combinations(numbers: List[int],
                                          system_size: int,
                                          win_size: int) -> List[Tuple[int, ...]]:
        """
        Trova il minimo insieme di combinazioni che garantisce la vincita.
        
        Per un sistema garantito N/K, genera combinazioni di dimensione K
        che garantiscono K punti se escono K numeri dai N numeri base.
        
        Args:
            numbers: Lista dei numeri base del sistema
            system_size: Numero di numeri base (N)
            win_size: Punti garantiti (K)
        """
        if system_size < win_size:
            raise ValueError(f"Impossibile garantire {win_size} punti con {system_size} numeri")
        if win_size < 2 or win_size > 4:
            raise ValueError("I punti garantiti devono essere tra 2 e 4")
        if len(numbers) < system_size:
            raise ValueError(f"Servono almeno {system_size} numeri per creare il sistema")

        # Prendi solo i primi system_size numeri
        base_numbers = sorted(numbers)[:system_size]
        
        # Genera tutte le possibili combinazioni di win_size numeri dai numeri base
        all_combinations = list(iter_combinations(base_numbers, win_size))
        
        # Per un sistema garantito, tutte le combinazioni di win_size sono necessarie
        # per garantire che qualsiasi sottoinsieme di win_size numeri dai base_numbers
        # sia coperto da almeno una combinazione
        return all_combinations

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