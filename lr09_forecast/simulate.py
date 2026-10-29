"""Monte Carlo прогноз за історією velocity (ЛР9, крок 4).

Використання:
    python3 simulate.py <remaining_points> <velocity через кому> [simulations] [seed]
Приклад:
    python3 simulate.py 220 21,17 10000 1
"""
import math
import random
import sys


def one_run(remaining, history):
    """Одна симуляція: скільки спринтів треба, щоб залишок дійшов до нуля."""
    sprints = 0
    while remaining > 0:
        remaining -= random.choice(history)  # випадковий спринт з моєї історії
        sprints += 1
    return sprints


def forecast(remaining, history, simulations=10000, seed=None):
    if max(history) <= 0:
        raise ValueError("у історії немає жодного спринта з points > 0: цикл не завершиться")
    if seed is not None:
        random.seed(seed)
    results = sorted(one_run(remaining, history) for _ in range(simulations))
    # P50 і P85: найменше число, нижче або на рівні якого лежить 50% / 85% результатів
    p50 = results[math.ceil(0.50 * simulations) - 1]
    p85 = results[math.ceil(0.85 * simulations) - 1]
    return p50, p85, results


if __name__ == "__main__":
    remaining = float(sys.argv[1])
    history = [float(x) for x in sys.argv[2].split(",")]
    sims = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else None
    p50, p85, res = forecast(remaining, history, sims, seed)
    print(f"залишок {remaining:g}, історія {history}, прогонів {sims}")
    print(f"P50 = {p50} спринтів, P85 = {p85} спринтів, мінімум {res[0]}, максимум {res[-1]}")
