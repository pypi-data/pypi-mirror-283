import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Iterable

from .genetic_optimizer import genetic_optimizer
from .structures import Polygon


# noinspection PyDefaultArgument
def best_strategy(
        num_banners: int,
        num_polygons: int = 10 ** 2,
        target_audience: dict[str, ...] = {"gender": "all", "ageFrom": 18, "ageTo": 100, "income": "abc"},
        iterations: int = 10,
) -> list[Polygon]:
    """
        Synchronously predict best strategy

        Args:
            num_banners: number of banners the company can afford
            num_polygons: number of polygons the city would be divided in (should be a full square)
            target_audience: target audience as a dict ("name" field doesn't matter)
            iterations: number of iterations

        Returns:
            Predicted strategy
    """
    value, genome = genetic_optimizer.find_optimum(
        num_banners=num_banners,
        num_polygons=num_polygons,
        TA=target_audience,
        iters=iterations
    )[0]

    return genetic_optimizer.get_polygons(genome)


# noinspection PyDefaultArgument
async def best_strategy_async(
        num_banners: int,
        num_polygons: int = 10 ** 2,
        target_audience: dict[str, ...] = {"gender": "all", "ageFrom": 18, "ageTo": 100, "income": "abc"},
        iterations: int = 10,
) -> list[Polygon]:
    """
        Asynchronous wrapper around the ``best_strategy`` function

        Args:
            num_banners: number of banners the company can afford
            num_polygons: number of polygons the city would be divided in (should be a full square)
            target_audience: target audience as a dict ("name" field doesn't matter)
            iterations: number of iterations

        Returns:
            Predicted strategy
    """
    return await asyncio.to_thread(best_strategy, num_banners, num_polygons, target_audience, iterations)
