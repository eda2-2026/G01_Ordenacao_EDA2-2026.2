import csv
from datetime import datetime
from typing import IO
from src.domain.transaction import Transaction
from src.use_cases.radix_sort import radix_sort_transactions
from src.use_cases.bucket_sort import bucket_sort_by_amount

class StatementOrganizerService:
    """
    Serviço responsável por orquestrar a ingestão de dados, 
    ordenação cronológica (Radix) e categorização (Bucket).
    """
    
    @staticmethod
    def process_csv_file(file: IO[bytes]) -> dict[str, list[Transaction]]:
        """
        Recebe um arquivo CSV binário (do upload do Streamlit),
        converte para entidades e processa a ordenação completa.
        """
        transactions = []
        
        content = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)
        
        for row in reader:
            try:
                tx_date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
                tx = Transaction(
                    date=tx_date,
                    description=row["Description"],
                    amount=float(row["Amount"])
                )
                transactions.append(tx)
            except (ValueError, KeyError) as e:
                continue
                
        # Fase 1: Ordenação temporal O(n) garantindo estabilidade
        sorted_by_date = radix_sort_transactions(transactions)
        
        # Fase 2: Distribuição O(n) preservando a ordem temporal
        categorized_buckets = bucket_sort_by_amount(sorted_by_date)
        
        return categorized_buckets