from itertools import combinations
from typing import List, Tuple
from .system_interface import SystemInterface

class ReducedSystem(SystemInterface):
    """Implementa un sistema ridotto che genera un sottoinsieme ottimizzato di combinazioni"""

    def generate_combinations(self, numbers: List[int], combination_size: int, **kwargs) -> List[Tuple[int, ...]]:
        """
        Genera un sottoinsieme ottimizzato di combinazioni usando una strategia intelligente.

        Args:
            numbers: Lista dei numeri base
            combination_size: Dimensione delle combinazioni da generare
            **kwargs: Parametri aggiuntivi (reduction_factor per il livello di riduzione)

        Returns:
            List[Tuple[int, ...]]: Lista delle combinazioni ottimizzate

        Raises:
            ValueError: Se i parametri non sono validi
        """
        if combination_size < 2 or combination_size > 4:
            raise ValueError("Il numero di elementi deve essere tra 2 e 4")

        if len(numbers) < combination_size:
            raise ValueError(f"Servono almeno {combination_size} numeri per creare combinazioni")

        # Parametro di riduzione (default 0.5 = 50% delle combinazioni)
        reduction_factor = kwargs.get('reduction_factor', 0.5)
        if not 0.1 <= reduction_factor <= 0.9:
            reduction_factor = 0.5

        # Genera tutte le combinazioni
        all_combinations = list(combinations(sorted(numbers), combination_size))
        
        # Calcola il numero target di combinazioni
        target_count = max(1, int(len(all_combinations) * reduction_factor))
        
        # Strategia di selezione intelligente
        if len(all_combinations) <= target_count:
            return all_combinations
        
        # Algoritmo di selezione distribuita per massimizzare la copertura
        selected_combinations = self._select_distributed_combinations(
            all_combinations, target_count, numbers
        )

        if not selected_combinations:
            raise ValueError("Nessuna combinazione generata")

        return selected_combinations
    
    def _select_distributed_combinations(self, all_combinations: List[Tuple[int, ...]], 
                                       target_count: int, 
                                       numbers: List[int]) -> List[Tuple[int, ...]]:
        """
        Seleziona combinazioni distribuite per massimizzare la copertura dei numeri.
        
        Args:
            all_combinations: Tutte le combinazioni possibili
            target_count: Numero target di combinazioni da selezionare
            numbers: Lista dei numeri base
            
        Returns:
            List[Tuple[int, ...]]: Combinazioni selezionate
        """
        if target_count >= len(all_combinations):
            return all_combinations
            
        selected = []
        remaining = all_combinations.copy()
        
        # Contatore per tracciare la frequenza di ogni numero nelle combinazioni selezionate
        number_frequency = {num: 0 for num in numbers}
        
        # Seleziona la prima combinazione (quella con numeri più distribuiti)
        first_comb = self._find_most_distributed_combination(remaining, numbers)
        selected.append(first_comb)
        remaining.remove(first_comb)
        
        # Aggiorna le frequenze
        for num in first_comb:
            number_frequency[num] += 1
        
        # Seleziona le rimanenti combinazioni bilanciando la distribuzione
        while len(selected) < target_count and remaining:
            best_combination = None
            best_score = float('-inf')
            
            for comb in remaining:
                # Calcola il punteggio basato su:
                # 1. Numeri meno frequenti (per bilanciare)
                # 2. Distanza dalle combinazioni già selezionate
                score = self._calculate_combination_score(comb, number_frequency, selected)
                
                if score > best_score:
                    best_score = score
                    best_combination = comb
            
            if best_combination:
                selected.append(best_combination)
                remaining.remove(best_combination)
                
                # Aggiorna le frequenze
                for num in best_combination:
                    number_frequency[num] += 1
        
        return selected
    
    def _find_most_distributed_combination(self, combinations: List[Tuple[int, ...]], 
                                         numbers: List[int]) -> Tuple[int, ...]:
        """Trova la combinazione con numeri più distribuiti nell'intervallo."""
        if not combinations:
            return combinations[0]
            
        best_comb = combinations[0]
        best_distribution = 0
        
        for comb in combinations:
            # Calcola la distribuzione come somma delle distanze tra numeri consecutivi
            sorted_comb = sorted(comb)
            distribution = sum(sorted_comb[i+1] - sorted_comb[i] for i in range(len(sorted_comb)-1))
            
            if distribution > best_distribution:
                best_distribution = distribution
                best_comb = comb
                
        return best_comb
    
    def _calculate_combination_score(self, combination: Tuple[int, ...], 
                                   number_frequency: dict, 
                                   selected_combinations: List[Tuple[int, ...]]) -> float:
        """
        Calcola il punteggio di una combinazione per la selezione.
        
        Punteggio più alto = combinazione più desiderabile
        """
        # Punteggio base: favorisce numeri meno frequenti
        frequency_score = sum(1.0 / (number_frequency[num] + 1) for num in combination)
        
        # Punteggio diversità: favorisce combinazioni diverse da quelle già selezionate
        diversity_score = 0
        for selected in selected_combinations:
            # Penalizza sovrapposizioni eccessive
            overlap = len(set(combination) & set(selected))
            diversity_score += 1.0 / (overlap + 1)
        
        # Punteggio distribuzione: favorisce numeri ben distribuiti
        sorted_comb = sorted(combination)
        if len(sorted_comb) > 1:
            distribution_score = sum(sorted_comb[i+1] - sorted_comb[i] for i in range(len(sorted_comb)-1))
            distribution_score = distribution_score / len(sorted_comb)
        else:
            distribution_score = 0
        
        # Combina i punteggi con pesi
        total_score = (frequency_score * 0.4 + 
                      diversity_score * 0.4 + 
                      distribution_score * 0.2)
        
        return total_score