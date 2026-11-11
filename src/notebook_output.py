"""Сворачиваемый текстовый вывод для Jupyter."""

import html
from IPython.display import HTML, display


def show_output(title, text):
    # details работает независимо от сворачивания заголовков в интерфейсе.
    content = '<details><summary>' + html.escape(title) + '</summary>'
    content = content + '<pre>' + html.escape(text) + '</pre></details>'
    display(HTML(content))
