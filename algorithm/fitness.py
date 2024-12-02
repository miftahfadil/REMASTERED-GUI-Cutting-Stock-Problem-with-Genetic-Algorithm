from typing import List


def get_len_stock_used(num_used_stock: List[int], len_stocks_list: List[float]) -> float:
    len_stock_used: float = 0.0

    for i in range(len(len_stocks_list)):
        len_stock_used += num_used_stock[i] * len_stocks_list[i]

    return len_stock_used

def yield_rate(len_product_list: List[float], len_stock_used: int) -> float:
    return sum(len_product_list) / len_stock_used

def fitness(num_used_stock: List[int], len_stock_list: List[float], len_product_list: List[float]) -> float: 
    len_stock_used: float = get_len_stock_used(num_used_stock, len_stock_list)
    curr_yield_rate: float = yield_rate(len_product_list, len_stock_used)

    if curr_yield_rate < 0.55:
        return (10 / 55) * curr_yield_rate
    else:
        return (2 * curr_yield_rate) - 1