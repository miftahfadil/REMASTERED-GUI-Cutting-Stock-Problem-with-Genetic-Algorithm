from typing import Dict
from typing import List
from typing import Any


def snipping_rate(
    assorted_chromosome: Dict[str, List[float]|List[int]|Any],
    len_stock_list: List[float]
) -> List[float]:
    """
    Calculate snipping rate of each stock in a chromosome
    """

    flatten_patterns: List[List[int]] = assorted_chromosome["flatten"].copy()
    num_used_stock: List[int] = assorted_chromosome["num_used_stock"].copy()

    snip_rate: List[float] = []

    for i in range(len(len_stock_list)):

        flattened_sum: float = round(sum(flatten_patterns[i]), 1)

        if num_used_stock[i] > 0:
            used_stock_length: float = (num_used_stock[i] * len_stock_list[i])
            
        else:
            used_stock_length: float = len_stock_list[i]
        
        snip_rate.append(1 - (flattened_sum/used_stock_length))
    
    return snip_rate
        
def revise_gene_p(
    assorted_chromosome: Dict[str, List[float]|List[int]|Any],
    len_stock_list: List[float]
) -> Dict[str, List[float]|List[int]|Any]:
    """
    Revise gene p by snipping rate
    """
    gene_b: List[int] = assorted_chromosome["gene_b"]
    gene_p: List[float] = assorted_chromosome["gene_p"]
    
    snip_rate: List[float] = snipping_rate(assorted_chromosome, len_stock_list)

    for i in range(len(gene_p)):
        gene_p[i] = snip_rate[gene_b[i]]

    assorted_chromosome["snip_rate"] = snip_rate

    return assorted_chromosome


if __name__ == "__main__":
    pass