import pytest
from systems import IntegralSystem, ReducedSystem, GuaranteedSystem

@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]

class TestIntegralSystem:
    def test_valid_combination_size(self, sample_numbers):
        system = IntegralSystem()
        combinations = system.generate_combinations(sample_numbers, 2)
        assert len(combinations) == 10  # 5C2 = 10

    def test_invalid_combination_size(self, sample_numbers):
        system = IntegralSystem()
        with pytest.raises(ValueError):
            system.generate_combinations(sample_numbers, 1)
        with pytest.raises(ValueError):
            system.generate_combinations(sample_numbers, 5)

    def test_insufficient_numbers(self):
        system = IntegralSystem()
        with pytest.raises(ValueError):
            system.generate_combinations([1, 2], 3)

class TestReducedSystem:
    def test_valid_combination_size(self, sample_numbers):
        system = ReducedSystem()
        combinations = system.generate_combinations(sample_numbers, 2)
        assert len(combinations) == 5  # Metà di 5C2

    def test_invalid_combination_size(self, sample_numbers):
        system = ReducedSystem()
        with pytest.raises(ValueError):
            system.generate_combinations(sample_numbers, 1)
        with pytest.raises(ValueError):
            system.generate_combinations(sample_numbers, 5)

    def test_insufficient_numbers(self):
        system = ReducedSystem()
        with pytest.raises(ValueError):
            system.generate_combinations([1, 2], 3)

class TestGuaranteedSystem:
    def test_valid_guarantee(self, sample_numbers):
        system = GuaranteedSystem()
        combinations = system.find_minimum_guaranteed_combinations(sample_numbers, 3, 2)
        assert len(combinations) > 0

        # Verifica che ogni combinazione contenga almeno un ambo
        for comb in combinations:
            assert system.verify_guarantee(comb, 2)

    def test_invalid_guarantee_size(self, sample_numbers):
        system = GuaranteedSystem()
        with pytest.raises(ValueError):
            system.find_minimum_guaranteed_combinations(sample_numbers, 2, 3)

    def test_optimization(self, sample_numbers):
        system = GuaranteedSystem()
        combinations = system.find_minimum_guaranteed_combinations(sample_numbers, 3, 2)
        optimized = system.optimize_combinations(combinations, 2)
        assert len(optimized) <= len(combinations)