"""Случайные блуждания для уравнения Пуассона на квадратной сетке."""

import math
import random
import time

from numerical_common import create_field


def walk(start_n, start_k, intervals, generator, source_function, boundary_function):
    """Одна траектория до границы с накоплением вклада источника."""
    h = 1.0 / intervals
    n = start_n
    k = start_k
    result = 0.0
    steps = 0
    while n > 0 and n < intervals and k > 0 and k < intervals:
        result = result - h * h * source_function(k * h, n * h) / 4
        direction = generator.randrange(4)
        if direction == 0:
            k = k - 1
        elif direction == 1:
            k = k + 1
        elif direction == 2:
            n = n - 1
        else:
            n = n + 1
        steps = steps + 1

    result = result + boundary_function(k * h, n * h)
    return result, steps


def estimate_point(n, k, intervals, particles, generator,
                   source_function, boundary_function):
    """Среднее, стандартная ошибка и число шагов для одной точки."""
    if particles < 2:
        raise ValueError("Нужно хотя бы две траектории")
    mean = 0.0
    squared_sum = 0.0
    total_steps = 0
    for particle in range(particles):
        value, steps = walk(n, k, intervals, generator,
                            source_function, boundary_function)
        # Последовательный подсчёт среднего и дисперсии без хранения всех путей.
        difference = value - mean
        mean = mean + difference / (particle + 1)
        squared_sum = squared_sum + difference * (value - mean)
        total_steps = total_steps + steps
    variance = squared_sum / (particles - 1)
    standard_error = math.sqrt(variance / particles)
    return mean, standard_error, total_steps


def solve_monte_carlo(intervals, particles, seed, source_function, boundary_function):
    """Вычислить всё поле на единичном квадрате методом блужданий."""
    if particles < 2:
        raise ValueError("Нужно хотя бы две траектории на узел")
    field = create_field(intervals, boundary_function)
    standard_errors = create_field(intervals, boundary_function)
    for n in range(intervals + 1):
        for k in range(intervals + 1):
            standard_errors[n][k] = 0.0
    total_steps = 0
    start = time.perf_counter()
    for n in range(1, intervals):
        for k in range(1, intervals):
            # Отдельный seed узла: результат не зависит от порядка обработки.
            point_seed = seed + n * (intervals + 1) + k
            generator = random.Random(point_seed)
            value, error, steps = estimate_point(
                n, k, intervals, particles, generator,
                source_function, boundary_function
            )
            field[n][k] = value
            standard_errors[n][k] = error
            total_steps = total_steps + steps
    elapsed = time.perf_counter() - start
    return field, standard_errors, elapsed, total_steps
