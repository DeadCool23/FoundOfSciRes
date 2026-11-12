"""Обычные табличные и текстовые блоки для вывода в Jupyter."""

from IPython.display import Markdown, display


def _cell(value):
    """Подготовить значение для безопасной Markdown-таблицы."""
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def show_table(title, headers, rows):
    """Показать несворачиваемую Markdown-таблицу с заголовком."""
    lines = ["### " + title, ""]
    lines.append("| " + " | ".join(_cell(value) for value in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(_cell(value) for value in row) + " |")
    display(Markdown("\n".join(lines)))


def show_note(text):
    """Показать обычный несворачиваемый Markdown-текст."""
    display(Markdown(text))
