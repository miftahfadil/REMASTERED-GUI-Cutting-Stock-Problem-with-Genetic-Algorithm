from random import randint
from typing import List

from utils.const import NUM_POPULATION


def initiate_population(len_stock_list: List[float], amount_stock_list: List[int], len_product_list: List[float]) -> List[List[int]|List[float]]:
    population: List[List[float]|List[int]] = []
    for i in range(NUM_POPULATION):
        pass

    return population

def initiate_gene_b(len_stock_list: List[float], amount_stock_list: List[int], len_product_list: List[float]) -> List[int]:
    gene_b: List[int] = []
    curr_amount_stock: List[int] = amount_stock_list.copy() 
    for i in range(len(len_product_list)):
        idx_stock = randint(0, len(len_stock_list))
        while len_stock_list[idx_stock] < len_product_list[i]:
            idx_stock = randint(0, len(len_stock_list))
        gene_b.append(idx_stock)

    return gene_b