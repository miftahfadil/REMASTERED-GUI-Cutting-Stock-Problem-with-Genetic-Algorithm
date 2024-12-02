from typing import List


def get_len_stock_used(num_used_stock: List[int], len_stocks_list: List[float]) -> float:
    len_stock_used: float = 0.0

    for i in range(len(len_stocks_list)):
        len_stock_used += num_used_stock[i] * len_stocks_list[i]

    return len_stock_used

def yield_rate(gene_p: List[float], len_stock_used: int) -> float:
    return sum(gene_p) / len_stock_used

def fitness(num_used_stock: List[int], len_stock_list: List[float], gene_p: List[float]) -> float: 
    len_stock_used: float = get_len_stock_used(num_used_stock, len_stock_list)
    curr_yield_rate: float = yield_rate(gene_p, len_stock_used)
    print(curr_yield_rate)

    if curr_yield_rate < 0.55:
        return (10 / 55) * curr_yield_rate
    else:
        return (2 * curr_yield_rate) - 1
    

if __name__ == "__main__":
    num_used_stock: List[int] = [1, 2, 1]
    len_stock_list: List[float] = [6.0, 4.0, 3.0]
    gene_p: List[float] = [3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5]
    fit = fitness(num_used_stock, len_stock_list, gene_p)
    print(fit)