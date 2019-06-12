from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome

C = TypeVar("C", bound=Chromosome)  # type of the chromosome


class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT")

    def __init__(
        self,
        initial_population: List[C],
        threshold: float,
        max_generations: int = 100,
        mutation_chance: float = 0.01,
        crossover_chance: float = 0.7,
        selection_type: SelectionType = SelectionType.TOURNAMENT,
    ) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

    # use the probability distribution wheel to pick 2 parents
    # note: will not work with negative fitness results
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights=wheel, k=2))

    # choose num_participants at random and take the best 2
    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    # replace the population with a new generation of individuals
    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        # keep going until we've filled the new generation
        while len(new_population) < len(self._population):
            # pick the 2 parents
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents: Tuple[C, C] = self._pick_roulette(
                    [x.fitness() for x in self._population]
                )
            else:
                parents = self._pick_tournament(len(self._population) // 2)
            # potentially crossover the 2 parents
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        # if we have an odd number, we'll have 1 extra, so we remove it
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population  # replace reference

    # with _mutation_chance probability mutate each individual
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    # run the genetic algorithm form max_generations iterations
    # and return the best individual found
    def run(self) -> C:
        best: C = max(self._population, key=self._fitness_key)
        for generation in range(self._max_generations):
            # early exit if we beat threshold
            if best.fitness() >= self._threshold:
                return best
            print(
                f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}"
            )
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest  # found a new best
        return best  # best we found in _max_generations
