import pytest
from datetime import date
from src.domain.transaction import Transaction
from src.use_cases.radix_sort import radix_sort_transactions

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