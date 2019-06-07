"""Find fibonacci sequence using memoization.

Memoization is a technique in which you store the results of 
computational tasks when they are completed so that when you 
need them again, you can look them up instead of needing to 
compute them multiple times.
"""

from typing import Dict

memo: Dict[int, int] = {0: 0, 1: 1}  # base case


def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)  # memoization
    return memo[n]


if __name__ == "__main__":
    print(fib3(5))
    print(fib3(50))
