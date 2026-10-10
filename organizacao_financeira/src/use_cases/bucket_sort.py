from src.domain.transaction import Transaction

def bucket_sort_by_amount(transactions: list[Transaction]) -> dict[str, list[Transaction]]:
    """
    Distribui as transações em 3 'baldes' de acordo com o valor (amount).
    Como a lista de entrada já deve estar ordenada cronologicamente (pelo Radix Sort),
    a distribuição linear em dicionários (arrays) matematicamente preserva a ordem original.
    Complexidade: O(n).
    """

    buckets: dict[str, list[Transaction]] = {
        "Micro": [],
        "Medium": [],
        "High": []
    }

    for tx in transactions:
        if tx.amount <= 50.0:
            buckets["Micro"].append(tx)
        elif tx.amount <= 200.0:
            buckets["Medium"].append(tx)
        else:
            buckets["High"].append(tx)

    return buckets