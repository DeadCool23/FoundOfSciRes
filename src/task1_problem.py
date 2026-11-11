"""Исходные данные первой задачи; доступны дочерним процессам Jupyter."""


def exact_temperature(x, z):
    return 20 + 20 * (x * (1 - x) + z * (1 - z))


def source(x, z):
    return -80


def boundary_temperature(x, z):
    if x == 0 or x == 1:
        return 20 + 20 * z * (1 - z)
    return 20 + 20 * x * (1 - x)
