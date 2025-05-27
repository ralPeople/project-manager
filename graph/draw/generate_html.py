def generate_html_table(matrix, headers):
    table_html = "<table border='1' style='border-collapse: collapse; text-align: center;'>"
    # Добавляем заголовки
    table_html += "<tr>"
    for header in headers:
        table_html += f"<th>{header}</th>"
    table_html += "</tr>"

    # Добавляем строки матрицы
    for row in matrix:
        table_html += "<tr>"
        for value in row:
            table_html += f"<td>{value}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html


def generate_html_table_critical_paths(matrix, header):
    """
    Генерирует HTML для таблицы с переменным числом элементов в строках.
    У заголовка есть только первый столбец.
    """
    table_html = "<table border='1' style='border-collapse: collapse; width: 80%; margin: 10px auto;'>"

    # Добавляем заголовок только для первого столбца
    table_html += "<tr>"
    table_html += f"<th>{header}</th>"
    table_html += "</tr>"

    # Заполняем строки таблицы
    for row in matrix:
        table_html += "<tr>"
        for index, cell in enumerate(row):
            if index == 0:  # Первая ячейка
                table_html += f"<td style='font-weight: bold;'>{cell}</td>"
            else:  # Остальные ячейки
                table_html += f"<td>{cell}</td>"
        table_html += "</tr>"

    table_html += "</table>"
    return table_html




