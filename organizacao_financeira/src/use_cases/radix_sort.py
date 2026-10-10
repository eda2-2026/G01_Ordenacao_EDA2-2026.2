from src.domain.transaction import Transaction

def radix_sort_transactions(transactions: list[Transaction]) -> list[Transaction]:
    """
    Ordena uma lista de transações cronologicamente usando o algoritmo Radix Sort (LSD).
    A base da ordenação é a data convertida para um inteiro (YYYYMMDD).
    
    Por enquanto, retorna a lista original apenas para fazer o teste falhar.
    """
    return transactions