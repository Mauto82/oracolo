import pytest
import sys
from main import main

def test_main_with_valid_arguments(monkeypatch):
    test_args = ['main.py', '20240101', 'MI']
    monkeypatch.setattr(sys, 'argv', test_args)

    # Non dovrebbe sollevare eccezioni
    main()

def test_main_with_invalid_arguments(monkeypatch):
    test_args = ['main.py', '20240101']  # Manca un argomento
    monkeypatch.setattr(sys, 'argv', test_args)

    with pytest.raises(SystemExit):
        main()