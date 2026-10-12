import csv
import time
from datetime import datetime
from typing import IO, Tuple
from src.domain.transaction import Transaction
from src.use_cases.radix_sort import radix_sort_transactions
from src.use_cases.bucket_sort import bucket_sort_by_amount

class StatementOrganizerService:
    """
    Serviço responsável por orquestrar a ingestão de dados, 
    ordenação cronológica (Radix), categorização (Bucket) e benchmark de tempo.
    """
    
    @staticmethod
    def process_csv_file(file: IO[bytes]) -> Tuple[dict[str, list[Transaction]], dict[str, float]]:
        """
        Retorna uma tupla contendo:
        1. Os baldes categorizados.
        2. Dicionário com os resultados do benchmark em milissegundos.
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
            except (ValueError, KeyError):
                continue
                
        # ---  BENCHMARK DE PERFORMANCE ---
        
        # 1. Testando o algoritmo nativo do Python (Timsort: O(n log n))
        native_list = transactions.copy()
        start_native = time.perf_counter()
        native_list.sort(key=lambda tx: tx.date)
        end_native = time.perf_counter()
        time_native_ms = (end_native - start_native) * 1000

        # 2. Testando o NOSSO algoritmo (Radix Sort: O(n))
        start_radix = time.perf_counter()
        sorted_by_date = radix_sort_transactions(transactions)
        end_radix = time.perf_counter()
        time_radix_ms = (end_radix - start_radix) * 1000
        
        benchmark_results = {
            "native_ms": time_native_ms,
            "radix_ms": time_radix_ms
        }
        
        # --- CATEGORIZAÇÃO ---
        categorized_buckets = bucket_sort_by_amount(sorted_by_date)
        
        return categorized_buckets, benchmark_results