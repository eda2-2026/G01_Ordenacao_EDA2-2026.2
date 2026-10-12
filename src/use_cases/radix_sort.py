from src.domain.transaction import Transaction

def _counting_sort_by_digit(transactions: list[Transaction], exp: int) -> list[Transaction]:
    """
    Ordena a lista de transações baseando-se apenas em um dígito específico (definido por 'exp').
    Usa o algoritmo Counting Sort, que é O(n) e, o mais importante, é um algoritmo ESTÁVEL.
    """
    n = len(transactions)
    output = [None] * n
    count = [0] * 10  # Base 10 (0 a 9)

    for tx in transactions:
        date_int = tx.get_date_as_integer()
        digit = (date_int // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        tx = transactions[i]
        date_int = tx.get_date_as_integer()
        digit = (date_int // exp) % 10
        
        output[count[digit] - 1] = tx
        count[digit] -= 1

    return output


def radix_sort_transactions(transactions: list[Transaction]) -> list[Transaction]:
    """
    Ordena uma lista de transações cronologicamente usando Radix Sort (LSD).
    Complexidade de tempo: O(d * n), onde 'd' é a quantidade de dígitos da data.
    """
    if not transactions:
        return []

    max_date_int = max(tx.get_date_as_integer() for tx in transactions)

    sorted_transactions = transactions.copy()
    
    exp = 1
    while max_date_int // exp > 0:
        sorted_transactions = _counting_sort_by_digit(sorted_transactions, exp)
        exp *= 10

    return sorted_transactions