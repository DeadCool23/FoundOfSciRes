"""Продольно-поперечная схема установления для уравнения Пуассона."""

import time

from numerical_common import create_field, copy_field, solve_tridiagonal, residual


def solve_settling(intervals, tau, tolerance, max_iterations,
                   source_function, boundary_function, initial_value=0.0):
    """Установление для Δu=f на единичном квадрате с условиями Дирихле."""
    h = 1.0 / intervals
    r = tau / (2 * h * h)
    field = create_field(intervals, boundary_function, initial_value)
    history = []
    start = time.perf_counter()

    for iteration in range(1, max_iterations + 1):
        middle = copy_field(field)
        for n in range(1, intervals):
            a = []
            b = []
            c = []
            d = []
            for k in range(1, intervals):
                right = field[n][k] + r * (field[n - 1][k]
                        - 2 * field[n][k] + field[n + 1][k])
                right = right - tau * source_function(k * h, n * h) / 2
                if k == 1:
                    right = right + r * middle[n][0]
                if k == intervals - 1:
                    right = right + r * middle[n][intervals]
                a.append(-r)
                b.append(1 + 2 * r)
                c.append(-r)
                d.append(right)
            a[0] = 0
            c[len(c) - 1] = 0
            solution = solve_tridiagonal(a, b, c, d)
            for k in range(1, intervals):
                middle[n][k] = solution[k - 1]

        new_field = copy_field(middle)
        for k in range(1, intervals):
            a = []
            b = []
            c = []
            d = []
            for n in range(1, intervals):
                right = middle[n][k] + r * (middle[n][k - 1]
                        - 2 * middle[n][k] + middle[n][k + 1])
                right = right - tau * source_function(k * h, n * h) / 2
                if n == 1:
                    right = right + r * new_field[0][k]
                if n == intervals - 1:
                    right = right + r * new_field[intervals][k]
                a.append(-r)
                b.append(1 + 2 * r)
                c.append(-r)
                d.append(right)
            a[0] = 0
            c[len(c) - 1] = 0
            solution = solve_tridiagonal(a, b, c, d)
            for n in range(1, intervals):
                new_field[n][k] = solution[n - 1]

        field = new_field
        current_residual = residual(field, intervals, source_function)
        history.append(current_residual)
        if current_residual < tolerance:
            elapsed = time.perf_counter() - start
            return field, iteration, elapsed, history

    raise RuntimeError("Метод установления не достиг заданной невязки")
