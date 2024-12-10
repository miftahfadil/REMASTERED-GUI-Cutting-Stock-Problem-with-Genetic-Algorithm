from typing import Dict
from typing import List
from typing import Any

from algorithm.genetic_algorithm import genetic_algorithm


if __name__ == "__main__":
    len_stock_list: List[float] = [6.0, 4.0, 3.0]
    len_product_list: List[float] = [3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5]
    metadata: Dict[str, List[int]|list[float]|Any] = genetic_algorithm(len_stock_list, len_product_list)
    print(metadata)
    print(metadata["yield rate"])