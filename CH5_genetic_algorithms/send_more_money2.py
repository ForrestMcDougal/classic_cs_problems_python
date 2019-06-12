from __future__ import annotations
from typing import Tuple, List
from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from random import shuffle, sample
from copy import deepcopy


class SendMoreMoney2(Chromosome):
    def __init__(self, letters: List[str]) -> None:
        self.letters: List[str] = letters

    def fitness(self) -> float:
        s: int = self.letters.index("S")
        e: int = self.letters.index("E")
        n: int = self.letters.index("N")
        d: int = self.letters.index("D")
        m: int = self.letters.index("M")
        o: int = self.letters.index("O")
        r: int = self.letters.index("R")
        y: int = self.letters.index("Y")
        send: int = s * 1_000 + e * 100 + n * 10 + d
        more: int = m * 1_000 + o * 100 + r * 10 + e
        money: int = m * 10_000 + o * 1_000 + n * 100 + e * 10 + y
        difference: int = abs(money - (send + more))
        return 1 / (difference + 1)

    @classmethod
    def random_instance(cls) -> SendMoreMoney2:
        letters = ["S", "E", "N", "D", "M", "O", "R", "Y", " ", " "]
        shuffle(letters)
        return SendMoreMoney2(letters)

    def crossover(self, other: SendMoreMoney2) -> Tuple[SendMoreMoney2, SendMoreMoney2]:
        child1: SendMoreMoney2 = deepcopy(self)
        child2: SendMoreMoney2 = deepcopy(other)
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        l1, l2 = child1.letters[idx1], child2.letters[idx2]
        child1.letters[child1.letters.index(l2)], child1.letters[idx2] = (
            child1.letters[idx2],
            l2,
        )
        child2.letters[child2.letters.index(l1)], child2.letters[idx1] = (
            child2.letters[idx1],
            l1,
        )
        return child1, child2

    def mutate(self) -> None:  # swap two letters' locations
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        self.letters[idx1], self.letters[idx2] = self.letters[idx2], self.letters[idx1]

    def __str__(self) -> str:
        s: int = self.letters.index("S")
        e: int = self.letters.index("E")
        n: int = self.letters.index("N")
        d: int = self.letters.index("D")
        m: int = self.letters.index("M")
        o: int = self.letters.index("O")
        r: int = self.letters.index("R")
        y: int = self.letters.index("Y")
        send: int = s * 1_000 + e * 100 + n * 10 + d
        more: int = m * 1_000 + o * 100 + r * 10 + e
        money: int = m * 10_000 + o * 1_000 + n * 100 + e * 10 + y
        difference: int = abs(money - (send + more))
        return f"{send} + {more} = {money} Difference: {difference}"


if __name__ == "__main__":
    initial_population: List[SendMoreMoney2] = [
        SendMoreMoney2.random_instance() for _ in range(1_000)
    ]
    ga: GeneticAlgorithm[SendMoreMoney2] = GeneticAlgorithm(
        initial_population=initial_population,
        threshold=1.0,
        max_generations=1_000,
        mutation_chance=0.2,
        crossover_chance=0.7,
        selection_type=GeneticAlgorithm.SelectionType.ROULETTE,
    )
    result: SendMoreMoney2 = ga.run()
    print(result)
