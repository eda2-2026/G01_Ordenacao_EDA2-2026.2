import pytest
from datetime import date
from src.domain.transaction import Transaction
from src.use_cases.radix_sort import radix_sort_transactions
from src.use_cases.bucket_sort import bucket_sort_by_amount

@pytest.fixture
def unsorted_transactions() -> list[Transaction]:
    """
    Cria uma lista de transações desordenadas para servir de base para os testes.
    Inclui duas transações na mesma data para testarmos a estabilidade do algoritmo.
    """
    return [
        Transaction(date=date(2025, 12, 1), description="Ifood", amount=45.0),
        Transaction(date=date(2024, 5, 15), description="Uber", amount=20.0),
        Transaction(date=date(2025, 1, 10), description="Amazon", amount=250.0),
        Transaction(date=date(2024, 5, 15), description="Bakery", amount=15.0), 
    ]

def test_radix_sort_by_date_maintains_stability(unsorted_transactions):
    """
    Verifica se o algoritmo Radix Sort ordena as transações cronologicamente.
    Também verifica a estabilidade: o 'Uber' apareceu antes da 'Bakery' na lista original,
    então mesmo tendo a mesma data, o 'Uber' deve continuar antes na lista ordenada.
    """
    sorted_list = radix_sort_transactions(unsorted_transactions)
    
    # Verifica o primeiro elemento (a data mais antiga)
    assert sorted_list[0].date == date(2024, 5, 15)
    assert sorted_list[0].description == "Uber"
    
    # Verifica a estabilidade (mesma data, ordem original mantida)
    assert sorted_list[1].date == date(2024, 5, 15)
    assert sorted_list[1].description == "Bakery" 
    
    # Verifica o último elemento (a data mais recente)
    assert sorted_list[-1].date == date(2025, 12, 1)



def test_bucket_sort_separates_by_value_categories():
    """
    Verifica se o Bucket Sort separa corretamente as transações em 3 categorias (baldes)
    baseado no valor (amount): Micro (0-50), Medium (50-200) e High (>200).
    A ordem original das datas dentro de cada balde DEVE ser preservada (Estabilidade).
    """
    # Lista já ordenada por data (simulando a saída do Radix Sort)
    pre_sorted_transactions = [
        Transaction(date=date(2025, 1, 1), description="Coffee", amount=5.0),    # Micro
        Transaction(date=date(2025, 1, 2), description="Rent", amount=1200.0),   # High
        Transaction(date=date(2025, 1, 3), description="Groceries", amount=150.0),# Medium
        Transaction(date=date(2025, 1, 4), description="Uber", amount=25.0),     # Micro
    ]

    buckets = bucket_sort_by_amount(pre_sorted_transactions)

    # Verifica se foram criados os 3 baldes exatos
    assert len(buckets) == 3
    assert "Micro" in buckets
    assert "Medium" in buckets
    assert "High" in buckets

    # Verifica os tamanhos corretos
    assert len(buckets["Micro"]) == 2
    assert len(buckets["Medium"]) == 1
    assert len(buckets["High"]) == 1

    # Verifica a estabilidade cronológica dentro do balde "Micro"
    # O "Coffee" era mais antigo que o "Uber", então deve continuar sendo o primeiro.
    assert buckets["Micro"][0].description == "Coffee"
    assert buckets["Micro"][1].description == "Uber"