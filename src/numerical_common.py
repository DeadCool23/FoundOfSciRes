"""Общие операции для сеточных задач. Матрицы хранятся как списки строк."""

import math


def create_field(intervals, boundary_function, initial_value=0.0):
    """Создать поле на единичном квадрате с заданными границами."""
    field = []
    for n in range(intervals + 1):
        row = []
        for k in range(intervals + 1):
            if n == 0 or n == intervals or k == 0 or k == intervals:
                value = boundary_function(k / intervals, n / intervals)
            else:
                value = initial_value
            row.append(value)
        field.append(row)
    return field


def copy_field(field):
    result = []
    for n in range(len(field)):
        row = []
        for k in range(len(field[n])):
            row.append(field[n][k])
        result.append(row)
    return result


def solve_tridiagonal(a, b, c, d):
    size = len(d)
    p = [0.0] * size
    q = [0.0] * size
    result = [0.0] * size

    p[0] = -c[0] / b[0]
    q[0] = d[0] / b[0]
    for i in range(1, size):
        denominator = b[i] + a[i] * p[i - 1]
        p[i] = -c[i] / denominator
        q[i] = (d[i] - a[i] * q[i - 1]) / denominator

    result[size - 1] = q[size - 1]
    for i in range(size - 2, -1, -1):
        result[i] = p[i] * result[i + 1] + q[i]
    return result


def residual(field, intervals, source_function):
    """Максимальная невязка уравнения Лапласа/Пуассона на квадрате."""
    h = 1.0 / intervals
    maximum = 0.0
    for n in range(1, intervals):
        for k in range(1, intervals):
            laplacian = (field[n][k - 1] + field[n][k + 1]
                         + field[n - 1][k] + field[n + 1][k]
                         - 4 * field[n][k]) / (h * h)
            value = abs(laplacian - source_function(k * h, n * h))
            if value > maximum:
                maximum = value
    return maximum


def calculate_errors(field, intervals, exact_function):
    maximum = 0.0
    squared_sum = 0.0
    count = 0
    h = 1.0 / intervals
    for n in range(1, intervals):
        for k in range(1, intervals):
            difference = field[n][k] - exact_function(k * h, n * h)
            if abs(difference) > maximum:
                maximum = abs(difference)
            squared_sum = squared_sum + difference * difference
            count = count + 1
    return maximum, math.sqrt(squared_sum / count)


def draw_surface(axes, x_values, z_values, field, title, minimum, maximum):
    # Matplotlib требует двумерные массивы для поверхности.
    import numpy as np

    x_grid = []
    z_grid = []
    for n in range(len(z_values)):
        x_row = []
        z_row = []
        for k in range(len(x_values)):
            x_row.append(x_values[k])
            z_row.append(z_values[n])
        x_grid.append(x_row)
        z_grid.append(z_row)

    surface = axes.plot_surface(
        np.array(x_grid), np.array(z_grid), np.array(field),
        cmap="viridis", vmin=minimum, vmax=maximum
    )
    axes.set_xlabel("x")
    axes.set_ylabel("z")
    axes.set_zlabel("Температура")
    axes.set_title(title)
    axes.set_zlim(minimum, maximum)
    return surface


def show_surface(x_values, z_values, field, title, minimum, maximum):
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(8, 6))
    axes = figure.add_subplot(111, projection="3d")
    surface = draw_surface(axes, x_values, z_values, field, title, minimum, maximum)
    figure.colorbar(surface, ax=axes, shrink=0.65, label="Температура")
    plt.show()
