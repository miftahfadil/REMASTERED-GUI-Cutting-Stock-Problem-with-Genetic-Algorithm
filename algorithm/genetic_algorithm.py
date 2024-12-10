from typing import List
from typing import Dict
from typing import Any

from .initiate_population import initiate_population
from .assortment_calculation import population_assortment
from .snipping_and_revise import snipping_rate
from .snipping_and_revise import revise_gene_p
from .selection import selection
from .crossover import crossover
from .mutation import mutation
from .fitness import get_len_stock_used
from .fitness import yield_rate_calc
from .fitness import best_fit_chromosome

from utils.const import DESTINED_YIELD_RATE
from utils.const import MAX_GENERATION


def genetic_algorithm(
    len_stock_list: List[float],
    len_product_list: List[float]
) -> Dict[str, List[int]|List[float]|Any]:
    
    population: List[Dict[str, List[int]|List[float]|Any]] = initiate_population(len_stock_list, len_product_list)

    yield_rate: float = 0.0
    gen_counter: int = 0

    while yield_rate < DESTINED_YIELD_RATE and gen_counter < MAX_GENERATION:
        modified_population: List[Dict[str, List[int]|List[float]|Any]] = []

        assorted_population: List[Dict[str, List[int]|List[float]|Any]] = population_assortment(population,
                                                                                                len_stock_list,
                                                                                                len_product_list)
        
        for assorted_chromosome in assorted_population:
            
            assorted_chromosome["snip_rates"] = snipping_rate(assorted_chromosome, len_stock_list)
            modified_chromosome: Dict[str, List[int]|List[float]|Any] = revise_gene_p(assorted_chromosome, len_stock_list)
            modified_population.append(modified_chromosome)
        
        selected_chromosomes: List[Dict[str, List[float]|List[int]|Any]] = selection(population=modified_population)
        childs: List[Dict[str, List[float]|List[int]|Any]] = crossover(selected_chromosomes)
        population = selected_chromosomes.copy() + childs.copy()

        population = mutation(population, len_stock_list, len_product_list)

        population = population_assortment(population, len_stock_list, len_product_list)

        best_chromosome: Dict[str, List[float]|List[int]|Any] = best_fit_chromosome(population)

        len_stock_used: float = get_len_stock_used(num_used_stock=best_chromosome["num_used_stock"],
                                                   len_stocks_list=len_stock_list)
        yield_rate = yield_rate_calc(len_product_list, len_stock_used)
        best_chromosome["yield rate"] = yield_rate

        gen_counter += 1

    return best_chromosome

if __name__ == "__main__":
    len_stock_list: List[float] = [6.0, 4.0, 3.0]
    len_product_list: List[float] = [3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5]
    metadata: Dict[str, List[int]|list[float]|Any] = genetic_algorithm(len_stock_list, len_product_list)
    print(metadata)
    print(metadata["yield rate"])