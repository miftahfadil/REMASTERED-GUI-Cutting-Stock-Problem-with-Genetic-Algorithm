from random import sample
from random import random
from typing import List
from typing import Dict

from utils.const import NUM_POPULATION


def initiate_population(len_stock_list: List[float], len_product_list: List[float]) -> List[Dict[str, List[int]|List[float]]]:
    population: List[Dict[str, List[float]|List[int]]] = []
    for i in range(NUM_POPULATION):
        gene_b: List[int]  = initiate_gene_b(len_stock_list, len_product_list)
        gene_p: List[float] = [random() for j in range(len(gene_b))]
        chromosome = {
            'gene_b': gene_b.copy(),
            'gene_p': gene_p.copy()
        }
        population.append(chromosome)

    return population

def initiate_gene_b(len_stock_list: List[float], len_product_list: List[float]) -> List[int]:
    gene_b: List[int] = []
    for product in range(len(len_product_list)):
        feasible_stock = get_feasible_stock(len_stock_list, product)
        idx_stock = sample(population=feasible_stock, k=1)[0]
        gene_b.append(idx_stock)

    return gene_b

def get_feasible_stock(len_stock_list: List[float], len_product: float) -> List[int]:
    feasible_stock: List[int] = []
    for len_stock in len_stock_list:
        if len_stock >= len_product:
            idx_stock = len_stock_list.index(len_stock)
            feasible_stock.append(idx_stock)

    return feasible_stock


if __name__ == "__main__":
    len_stock_list = [6.0, 4.0, 3.0]
    len_product_list = [3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5]

    print(initiate_population(len_stock_list, len_product_list))