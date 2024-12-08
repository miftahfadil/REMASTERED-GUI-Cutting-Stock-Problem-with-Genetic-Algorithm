from typing import Dict
from typing import List
from typing import Any
from math import ceil
from random import sample
from random import randint
from random import random

from utils.const import NUM_CHROM_IN_POPULATION
from utils.const import GENE_B_MUTATION_PROB
from utils.const import GENE_B_MUTATION_LOCUS_RATIO
from utils.const import GENE_P_MUTATION_PROB
from utils.const import GENE_P_MUTATION_LOCUS_RATIO


def mutation(population: List[Dict[str, Any]], len_stock_list: List[float],
            len_product_list: list[float]) -> List[Dict[str, Any]]:
    
    num_gene_b_mutation: int = round(GENE_B_MUTATION_PROB * NUM_CHROM_IN_POPULATION)
    num_gene_b_loc: int = ceil(GENE_B_MUTATION_LOCUS_RATIO * NUM_CHROM_IN_POPULATION)

    for _ in range(num_gene_b_mutation):
        chromosome: Dict[str, List[int]|List[float]] = sample(population, 1)[0]
        gene_b: List[int] = chromosome["gene_b"]
        gene_p: List[int] = chromosome["gene_p"]

        for __ in range(num_gene_b_loc):
            idx_locus: int = randint(0, len(gene_b)-1)
            gene_b[idx_locus] = randint(0, len(len_stock_list)-1)
            
            while len_stock_list[gene_b[idx_locus]] < len_product_list[idx_locus]:
                gene_b[idx_locus] = randint(0, len(len_stock_list)-1)
            
            gene_p[idx_locus] = random()
    
    num_gene_p_mutation: int = round(GENE_P_MUTATION_PROB * NUM_CHROM_IN_POPULATION)
    num_gene_p_loc: int = ceil(GENE_P_MUTATION_LOCUS_RATIO * NUM_CHROM_IN_POPULATION)

    for _ in range(num_gene_p_mutation):
        chromosome: Dict[str, List[int]|List[float]] = sample(population, 1)[0]
        gene_p: List[float] = chromosome["gene_p"]

        for __ in range(num_gene_p_loc):
            idx_locus: int = randint(0, len(gene_p)-1)
            gene_p[idx_locus] = random()

    return population

