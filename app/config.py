from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Config:
    CSV_FILE: str = 'data/estrazioni-lotto.csv'
    DATE_FORMAT: str = "%d/%m/%Y"
    CSV_DELIMITER: str = ';'
    RUOTE: Dict[str, int] = field(default_factory=lambda: {
        'BA': 1,
        'CA': 2,
        'FI': 3,
        'GE': 4,
        'MI': 5,
        'NA': 6,
        'PA': 7,
        'RO': 8,
        'TO': 9,
        'VE': 10,
        'NZ': 11
    })