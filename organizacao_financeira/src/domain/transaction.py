from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    """
    Represents a single financial transaction.
    """
    date: date
    description: str
    amount: float

    def get_date_as_integer(self) -> int:
        """
        Converts the date to an integer format (YYYYMMDD) 
        to be used by the Radix Sort algorithm.
        """
        return int(self.date.strftime("%Y%m%d"))