"""Распределение узлов сетки между процессами, совместимое с Jupyter."""

import multiprocessing
import random
import time

from monte_carlo import estimate_point
from numerical_common import create_field


def calculate_point(task):
    # Функция находится в модуле, чтобы её можно было запустить через spawn.
    n, k, intervals, particles, seed, source_function, boundary_function = task
    point_seed = seed + n * (intervals + 1) + k
    generator = random.Random(point_seed)
    value, error, steps = estimate_point(
        n, k, intervals, particles, generator,
        source_function, boundary_function
    )
    return n, k, value, error, steps


def solve_monte_carlo_parallel(intervals, particles, seed, source_function,
                               boundary_function, workers):
    """Полное поле; время включает создание и завершение пула процессов.

    source_function и boundary_function должны быть функциями из .py-модуля.
    При вызове из обычного скрипта нужен блок if __name__ == '__main__'.
    """
    if particles < 2:
        raise ValueError("Нужно хотя бы две траектории на узел")
    if workers < 1:
        raise ValueError("Нужен хотя бы один процесс")
    field = create_field(intervals, boundary_function)
    standard_errors = create_field(intervals, boundary_function)
    for n in range(intervals + 1):
        for k in range(intervals + 1):
            standard_errors[n][k] = 0.0

    start = time.perf_counter()
    tasks = []
    for n in range(1, intervals):
        for k in range(1, intervals):
            tasks.append((n, k, intervals, particles, seed,
                          source_function, boundary_function))

    context = multiprocessing.get_context("spawn")
    with context.Pool(processes=workers) as pool:
        results = pool.map(calculate_point, tasks, chunksize=1)

    total_steps = 0
    for i in range(len(results)):
        n, k, value, error, steps = results[i]
        field[n][k] = value
        standard_errors[n][k] = error
        total_steps = total_steps + steps
    elapsed = time.perf_counter() - start
    return field, standard_errors, elapsed, total_steps
