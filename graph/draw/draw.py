from graph.classes import Node, Edge, Graph

import copy

import networkx as nx
import matplotlib.pyplot as plt

from pyvis.network import Network
import webbrowser


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

def draw_graph(g, highlighted_edges, node_matrices):

    # Список рёбер (может быть неориентированным или ориентированным)

    G = nx.DiGraph()  # Для ориентированного графа


    # Добавляем рёбра в граф
    #G.add_weighted_edges_from(edges)
    for i in range(len(g.edges)):
        x, y, weight = g.edges[i]
        G.add_edge(x, y, weight=weight)

    #Копия графа
    G_numeric = nx.Graph()

    for i in range(len(g.edges)):
        x, y, weight = g.edges[i]
        G_numeric.add_edge(x, y, weight=weight[0]+10*len(weight[1]))

    # Позиции узлов
    pos = nx.spring_layout(G_numeric, k=20, iterations=100)
    x_positions = {node: i for i, node in enumerate(G.nodes)}
    cnt_nodes = 0
    for i in range(len(g.edges)):
        x, y, weight = g.edges[i]
        cnt_nodes = max(cnt_nodes, x, y)

    d = [0] * (cnt_nodes+1)
    for i in range(cnt_nodes+1):
        for j in range(len(g.edges)):
            x, y, weight = g.edges[j]
            d[y] = max(d[y], d[x] + 1)

    # Обновляем позицию для каждой вершины, сохраняя y-координату
    #for node in pos:
     #   pos[node][0] = d[node]  # Меняем только координату по X
     #  pos[node][1] = node  # Меняем только координату по Y

    #pos = graphviz_layout(G_numeric, prog='dot')
    # Визуализация графа
    plt.figure(figsize=(8, 6))
    #Рисуем граф
    edge_widths = [3 if (u, v) in highlighted_edges or (v, u) in highlighted_edges else 2 for u, v in G.edges]
    edge_colors = ["black" if (u, v) in highlighted_edges or (v, u) in highlighted_edges else "gray" for u, v in G.edges]

    #nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=500, edge_color=edge_colors, font_size=10, width=edge_widths)

    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=500)
    nx.draw_networkx_edges(
         G, pos,
         edge_color=edge_colors,
         width=edge_widths,
         arrowsize=40,  # Увеличиваем размер стрелок
         min_source_margin=20,  # Смещение начала рёбер
         min_target_margin=20,  # Смещение конца рёбер
    )

    #Рисуем параметры ребер
    # Добавляем подписи весов рёбер
    edge_labels = nx.get_edge_attributes(G, "weight")
    formatted_edge_labels = {edge: f"({w[0]}, {w[1]})" for edge, w in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, font_size=10, label_pos=0.5, font_color="red")

    for node, (x, y) in pos.items():
        # Получаем матрицу для вершины
        matrix = node_matrices.get(node, [[0, 0], [0, 0]])
        # Формируем текст для отображения в формате a b\nc d
        text = f"{matrix[0][0]} {matrix[0][1]}\n{matrix[1][0]} {matrix[1][1]}"
        # Добавляем текст на граф
        plt.text(
            x, y, text,
            fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
            #bbox=dict(facecolor="white", edgecolor="black", boxstyle="circle,pad=0.5"),  # Круглая рамка
        )

    plt.title("Graph with 2x2 Matrices in Nodes")
    plt.axis('off')
    #plt.show()

    net = Network(notebook=True, directed=True)
    net.from_nx(G_numeric)
    for edge in net.edges:
        edge['arrows'] = 'to'  # Стрелка будет направлена от исходной вершины к конечной

    # Устанавливаем физические свойства
    net.force_atlas_2based(gravity=-60, central_gravity=0.01, spring_length=150, spring_strength=0.05)

    #net.show("graph.html")

    for edge in net.edges:
        edge['color'] = 'green'  # Устанавливаем синий цвет для рёбер
        edge['width'] = 2  # Устанавливаем толщину рёбер

    # Настройка цвета и размера вершин
    for node in net.nodes:
        node['color'] = 'skyblue'  # Устанавливаем красный цвет для вершин
        node['size'] = 20  # Устанавливаем размер вершин


        node_id = node['id']
        if(node_id == 1):
            node['color'] = 'lightgreen'
        if(node_id == cnt_nodes):
            node['color'] = 'yellow'

        node['shape'] = 'circle'  # Текст будет внутри
        if node_id in node_matrices:
            # Форматируем строку матрицы для отображения
            #matrix_str = f"<b>{matrix[0][0]} {matrix[0][1]}<br>{matrix[1][0]} {matrix[1][1]}</b>"
            matrix_str = "\n".join(" ".join(map(str, row)) for row in node_matrices[node_id])
            node['label'] = f"{matrix_str}"  # Добавляем матрицу в качестве метки
            node['font'] = {"size": 16}

    print(highlighted_edges)

    for edge in net.edges:
        edge['width'] = 2  # Устанавливаем толщину рёбер
        if (edge['from'], edge['to']) in highlighted_edges or (edge['to'], edge['from']) in highlighted_edges:  # Если ребро в списке выделенных
            edge['color'] = 'red'  # Выделяем ребро оранжевым цветом
        else:
            edge['color'] = 'gray'  # Для других рёбер цвет синий

        # Добавление веса рёбер
        edge_value = G[edge['from']][edge['to']]['weight'][0]
        edge_name = G[edge['from']][edge['to']]['weight'][1]
        edge['label'] = f"{edge_value}; {edge_name}"  # Вставляем вес как всплывающее сообщение
        edge['font'] = {'size': 20}  # Увеличиваем размер шрифта

    headers_edges = ["(i, j)", "t(i,j)", "Трн(i,j)", "Tро(i,j)","Tпн(i,j)","Тпо(i,j)","Rп(i,j)","Rс(i,j)"]

    matrix_edges = []
    for i in range(1, cnt_nodes+1):
        for el in g.e[i]:
            cur_line = []
            cur_line.append((el.x, el.y))
            cur_line.append(el.t)
            cur_line.append(el.Trn)
            cur_line.append(el.Tro)
            cur_line.append(el.Tpo)
            cur_line.append(el.Tpn)
            cur_line.append(el.Rp)
            cur_line.append(el.Rc)
            matrix_edges.append(copy.deepcopy(cur_line))

    html_content = net.generate_html()
    table_html_edges = generate_html_table(matrix_edges, headers_edges)

    headers_nodes = ["Событие i","Тр(i)","Тп(i)","R(i)"]
    matrix_nodes = []
    for i in range(1,cnt_nodes+1):
        cur_line = []
        cur_line.append(i)
        cur_line.append(g.nodes[i].Tr)
        cur_line.append(g.nodes[i].Tp)
        cur_line.append(g.nodes[i].R)
        matrix_nodes.append(copy.deepcopy(cur_line))

    table_html_nodes = generate_html_table(matrix_nodes, headers_nodes)
    #html_content = net.generate_html()
    #html_content = html_content.replace(
    #    "</body>",
    #    f"<h3 style='text-align: center;'>Временные параметры работ</h3>{table_html}</body>"
    #)

    #with open("graph.html", "w", encoding="utf-8") as f:
    #    f.write(html_content)

    matrix_paths = []

    cur_path = 0
    for lst in g.list_of_critical_paths:
        cur_line = []
        cur_path += 1
        cur_line.append(str(cur_path))
        for i in range(1, len(lst)):
            for edge in net.edges:
                if(edge['from'] == lst[i - 1] and edge['to'] == lst[i] or edge['to'] == lst[i - 1] and edge['from'] == lst[i]):
                    edge_name = G[edge['from']][edge['to']]['weight'][1]
                    cur_line.append(edge_name)
                    break
        cur_line2 = [cur_line[0]]
        for i in range(len(cur_line) - 1, 0, -1):
            cur_line2.append(cur_line[i])
        cur_line = copy.deepcopy(cur_line2)
        matrix_paths.append(cur_line)

    table_critical_paths = generate_html_table_critical_paths(matrix_paths, "Критические пути")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Граф и таблицы</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 20px;
            }}
            .tables-container {{
                width: 80%;
                margin: 20px auto;
            }}
            .table-container {{
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <h2>Граф</h2>
        {html_content}  <!-- Граф PyVis -->
        <h3>Временные параметры работ</h3>
        {table_html_edges}  <!-- Первая таблица -->
        <h4>Рассчетные варианты событий</h4>
        {table_html_nodes}  <!-- Вторая таблица -->
        <h5>Критические пути (до 10)</h5>
        {table_critical_paths}  <!-- Вторая таблица -->
    </body>
    </html>
    """
    with open("graph.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    #net.show("graph.html")
    file_path = "graph.html"
    #net.show(file_path)

    # Открываем граф в браузере
    webbrowser.open(file_path)


def draw(g):
    node_matrices = dict()
    highlighted_edges = []
    for i in range(1, len(g.nodes)):
        node_matrices[i] = [[i, g.nodes[i].Tr], [g.nodes[i].R, g.nodes[i].Tp]]
    for lst in g.list_of_critical_paths:
        for i in range(1, len(lst)):
            highlighted_edges.append((lst[i - 1], lst[i]))

    #draw_graph(g, highlighted_edges, node_matrices)



