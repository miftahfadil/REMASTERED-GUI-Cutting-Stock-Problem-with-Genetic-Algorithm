from typing import Dict
from typing import List

from numpy import array


def assortment_calc(chromosome: Dict[str, List[int]|List[float]],
                    len_product_list: List[float],
                    len_stock_list: List[float])-> Dict[str, List[float]|List[int]|List[List[int]]]:
    """
    Generate cutting patterns for each chromosome
    """
    gene_b: List[int] = chromosome['gene_b'].copy()
    gene_p: List[float] = chromosome['gene_p'].copy()
    
    patterns: List[List[List[int]]] = [[[]] for _ in range(len(len_stock_list))]
    num_used_stock: List[int] = [0 for _ in range(len(len_stock_list))]

    curr_assigned_stock: int = gene_b[0]

    for i in range(len(len_product_list)):

        if num_used_stock[gene_b[i]] == 0:
            num_used_stock[gene_b[i]] = 1

        if curr_assigned_stock != gene_b[i]:
            curr_assigned_stock = gene_b[i]
        
        assigned: bool = False
        
        for pattern in patterns[curr_assigned_stock]:

            if (gene_b[i] == curr_assigned_stock and
                sum(pattern) + len_product_list[i] <= len_stock_list[curr_assigned_stock]):

                pattern.append(len_product_list[i])
                assigned = True
                
                break
        
        if not assigned:
            
            pattern[curr_assigned_stock].append([len_product_list[i]])
            patterns[gene_b] += 1
    
    flatten: List[List[int]] = flatten_patterns(patterns)

    assorted_chromosome: Dict[str, List[float]|List[int]|List[List[int]]] = {
        "gene_b" : gene_b,
        "gene_p" : gene_p,
        "patterns": patterns,
        "flatten": flatten,
        "num_used_stock": num_used_stock
    }

    return assorted_chromosome

def flatten_patterns(patterns: List[List[List[int]]]) -> List[List[int]]:
    """
    flatten patterns based on assigned stock
    """
    return [array(pattern).flatten().tolist() for pattern in patterns]


if __name__ == "__main__":
    patterns = [[[2.7], [1.4], [2.2], [2.8]], [[1.6]], [[5.0], [4.0]]]
    flatten = flatten_patterns(patterns)
    print(flatten)