from typing import Dict
from typing import List
from typing import Any
from random import random 

from .fitness import best_fit_chromosome

from utils.const import NUM_CHROM_IN_POPULATION


def selection(
    population: List[Dict[str, List[float]|List[int]|Any]]
) -> List[Dict[str, List[float]|List[int]|Any]]:
    """
    Eleminate some chromosome
    """
    selected_chromosome: List[Dict[str, List[float]|List[int]|Any]] = []

    elitist: Dict[str, List[float]|List[int]|Any] = best_fit_chromosome(population)
    selected_chromosome.append(elitist)

    rouletted: List[Dict[str, List[float]|List[int]|Any]] = roulette_wheel_selection(population)
    selected_chromosome += rouletted

    return selected_chromosome

def roulette_wheel_selection(
    population: List[Dict[str, List[float]|List[int]|Any]]
) -> List[Dict[str, List[float]|List[int]|Any]]:
    """
    Select (NUM_CHROM_IN_POPULATION - 3) chromosomes
    """
    fitness_total: float = sum([chromosome["fitness"] for chromosome in population])

    cumulative_probs: List[float] = []
    cumulative_sum: float = 0.0

    for chromosome in population:
        prob = chromosome["fitness"] / fitness_total
        cumulative_sum += prob
        cumulative_probs.append(cumulative_sum)

    selected_chromosomes: List[Dict[str, List[float]|List[int]|Any]] = []

    for _ in range(NUM_CHROM_IN_POPULATION - 3):

        rand: float = random()

        for idx, cumulative_prob in enumerate(cumulative_probs):

            if rand <= cumulative_prob:
                
                selected_chromosomes.append(population[idx])

                break

    return selected_chromosomes