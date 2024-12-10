from typing import Dict
from typing import List
from typing import Any


def get_len_stock_used(num_used_stock: List[int], len_stocks_list: List[float]) -> float:
    len_stock_used: float = 0.0

    for i in range(len(len_stocks_list)):
        len_stock_used += num_used_stock[i] * len_stocks_list[i]

    return len_stock_used

def yield_rate_calc(len_product_list: List[float], len_stock_used: int) -> float:
    return sum(len_product_list) / len_stock_used

def fitness(num_used_stock: List[int], len_stock_list: List[float], len_product_list: List[float]) -> float: 
    len_stock_used: float = get_len_stock_used(num_used_stock, len_stock_list)
    curr_yield_rate: float = yield_rate_calc(len_product_list, len_stock_used)

    if curr_yield_rate < 0.55:
        return (10 / 55) * curr_yield_rate
    else:
        return (2 * curr_yield_rate) - 1

def best_fit_chromosome(
    population: List[Dict[str, List[float]|List[int]|Any]]
) -> Dict[str, List[float]|List[int]|Any]:
    """
    Select a chromosom with highest fitness
    """
    return sorted(population,key=lambda chromosome: chromosome['fitness'], reverse=True)[0]

if __name__ == "__main__":
    num_used_stock: List[int] = [1, 2, 1]
    len_stock_list: List[float] = [6.0, 4.0, 3.0]
    len_product_list: List[float] = [3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5]
    fit = fitness(num_used_stock, len_stock_list, len_product_list)
    print(fit)