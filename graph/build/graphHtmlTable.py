def generate_matrix_for_text(g, matrix_text):
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        t = g.edges[i].t[0]
        name = g.edges[i].t[1]
        matrix_text.append([x, y, t, name])

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

def graph_to_html(g):
    matrix_text = []
    headers_text = ["Событие 1", "Событие 2", "Длительность", "Название"]
    generate_matrix_for_text(g, matrix_text)
    table_html_text = generate_html_table(matrix_text, headers_text)
    return table_html_text