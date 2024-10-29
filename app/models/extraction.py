from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Extraction:
    data: datetime
    ruota: str
    numeri: List[int]