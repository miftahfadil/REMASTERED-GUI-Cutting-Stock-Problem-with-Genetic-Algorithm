from typing import Dict
from typing import List
from typing import Any
from random import random
from random import sample


def crossover(selected_chromosome: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    parents: List[Dict[str, Any]] = select_parents(selected_chromosome)
    childs: List[Dict[str, Any]] = []

    for i, parent in enumerate(parents):
        gene_b_child: List[int] = parent["gene_b"].copy()
        gene_p_child: List[float] = parent["gene_p"].copy()

        for j, snip_rate in enumerate(gene_p_child):
            crossover_param: float = control_crossover_parameter(snip_rate)
            rand: float = random()

            if crossover_param > rand:
                par_id: int = i % 2 
                gene_b_child[j] = parents[par_id]["gene_b"][j]
                gene_p_child[j] = parents[par_id]["gene_p"][j]
        
        childs.append(
            {
                "gene_b" : gene_b_child,
                "gene_p" : gene_p_child
            }
        )
    
    return childs

def select_parents(parent_candidate: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sample(parent_candidate, 2)

def control_crossover_parameter(snip_rate: float) -> float:
    
    if snip_rate < 0.05:
    
        return 2400 * pow(base=snip_rate, exp=3)
    
    else:
    
        return min(0.8 * pow(base=snip_rate - 0.05, exp=1/4) + 0.3, 1)