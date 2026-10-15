import plotly.graph_objects as go


# Область: квадрат 0 <= x <= 1, 0 <= z <= 1.
# На каждой стороне будет number_of_intervals + 1 точек.
number_of_intervals = 50
step = 1.0 / number_of_intervals

x_values = []
z_values = []

for i in range(number_of_intervals + 1):
    x_values.append(i * step)
    z_values.append(i * step)

# Каждая строка таблицы соответствует одному значению координаты z.
temperature_values = []

for n in range(number_of_intervals + 1):
    row = []
    z = z_values[n]

    for k in range(number_of_intervals + 1):
        x = x_values[k]
        # Равномерный внутренний нагрев и отвод тепла через края.
        temperature = 20 + 20 * (x * (1 - x) + z * (1 - z))
        row.append(temperature)

    temperature_values.append(row)

# В Plotly вертикальная координата поверхности называется z.
# Поэтому нашу координату z передаём как y, а температуру — как z.
surface = go.Surface(
    x=x_values,
    y=z_values,
    z=temperature_values,
    colorscale="Viridis",
    colorbar=dict(title="Температура"),
)

figure = go.Figure(data=[surface])
figure.update_layout(
    title="Температура пластины: u(x, z) = 20 + 20[x(1 − x) + z(1 − z)]",
    scene=dict(
        xaxis_title="x",
        yaxis_title="z",
        zaxis_title="u(x, z), температура",
    ),
)

# График можно вращать и масштабировать в браузере.
figure.show()
