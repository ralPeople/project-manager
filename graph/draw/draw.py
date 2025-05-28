from graph.classes import Node, Edge, Graph

import copy

import networkx as nx
import matplotlib.pyplot as plt


from graph.draw.generate_html import generate_html_table, generate_html_table_critical_paths

from pyvis.network import Network
from graph.build.graphHtmlTable import graph_to_html

import webbrowser

def generate_matrix_for_text(g, matrix_text):
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        t = g.edges[i].t[0]
        name = g.edges[i].t[1]
        matrix_text.append([x, y, t, name])


def generate_matrix_for_critical(g, net, G, matrix_paths):
    cur_path = 0
    for lst in g.list_of_critical_paths:
        cur_line = []
        cur_path += 1
        cur_line.append(str(cur_path))
        for i in range(1, len(lst)):
            for edge in net.edges:
                if (edge['from'] == lst[i - 1] and edge['to'] == lst[i] or edge['to'] == lst[i - 1] and edge['from'] ==
                        lst[i]):
                    edge_name = G[edge['from']][edge['to']]['weight'][1]
                    cur_line.append(edge_name)
                    break
        cur_line2 = [cur_line[0]]
        for i in range(len(cur_line) - 1, 0, -1):
            cur_line2.append(cur_line[i])
        cur_line = copy.deepcopy(cur_line2)
        matrix_paths.append(cur_line)


def generate_matrix_for_edges(g, matrix_edges, cnt_nodes):
    for i in range(1, cnt_nodes+1):
        for el in g.e[i]:
            cur_line = []
            cur_line.append((el.x, el.y))
            cur_line.append(el.t)
            cur_line.append(el.info.Trn)
            cur_line.append(el.info.Tro)
            cur_line.append(el.info.Tpo)
            cur_line.append(el.info.Tpn)
            cur_line.append(el.info.Rp)
            cur_line.append(el.info.Rc)
            matrix_edges.append(copy.deepcopy(cur_line))


def generate_matrix_for_nodes(g, matrix_nodes, cnt_nodes):
    for i in range(1, cnt_nodes + 1):
        cur_line = []
        cur_line.append(i)
        cur_line.append(g.nodes[i].Tr)
        cur_line.append(g.nodes[i].Tp)
        cur_line.append(g.nodes[i].R)
        matrix_nodes.append(copy.deepcopy(cur_line))


def set_nodes_style(net, cnt_nodes, node_matrices):
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


def set_edges_style(G, net, highlighted_edges):
    for edge in net.edges:
        edge['color'] = 'green'  # Устанавливаем синий цвет для рёбер
        edge['width'] = 2  # Устанавливаем толщину рёбер

    for edge in net.edges:
        edge['arrows'] = 'to'  # Стрелка будет направлена от исходной вершины к конечной

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

def draw_process(g, highlighted_edges, node_matrices):

    # Список рёбер (может быть неориентированным или ориентированным)
    G = nx.DiGraph()  # Для ориентированного графа
    # Добавляем рёбра в граф
    #G.add_weighted_edges_from(edges)
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        weight = g.edges[i].t
        G.add_edge(x, y, weight=weight)

    #Копия графа
    G_numeric = nx.Graph()

    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        weight = g.edges[i].t
        G_numeric.add_edge(x, y, weight=weight[0]+10*len(weight[1]))

    # Позиции узлов
    pos = nx.spring_layout(G_numeric, k=20, iterations=100)
    x_positions = {node: i for i, node in enumerate(G.nodes)}
    cnt_nodes = 0
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        cnt_nodes = max(cnt_nodes, x, y)

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


    # Устанавливаем физические свойства
    net.force_atlas_2based(gravity=-60, central_gravity=0.01, spring_length=150, spring_strength=0.05)

    #net.show("graph.html")


    # Настройка цвета и размера вершин


    print(highlighted_edges)
    set_nodes_style(net, cnt_nodes, node_matrices)
    set_edges_style(G, net, highlighted_edges)

    headers_edges = ["(i, j)", "t(i,j)", "Трн(i,j)", "Tро(i,j)","Tпн(i,j)","Тпо(i,j)","Rп(i,j)","Rс(i,j)"]

    #Генерируем выводимые параметры для ребер
    matrix_edges = []
    generate_matrix_for_edges(g, matrix_edges, cnt_nodes)

    #Генерируем html таблицы
    html_content = net.generate_html()
    table_html_edges = generate_html_table(matrix_edges, headers_edges)

    headers_nodes = ["Событие i", "Тр(i)", "Тп(i)", "R(i)"]

    #Генерируем матрицы для вершин
    matrix_nodes = []
    generate_matrix_for_nodes(g, matrix_nodes, cnt_nodes)

    table_html_nodes = generate_html_table(matrix_nodes, headers_nodes)

    #Генерируем матрицу критических путей
    matrix_paths = []
    generate_matrix_for_critical(g, net, G, matrix_paths)

    #Генерируем матрицу с текстом ввода
    #matrix_text = []
    #headers_text = ["Событие 1", "Событие 2", "Длительность", "Название"]
    #generate_matrix_for_text(g, matrix_text)
    #table_html_text = generate_html_table(matrix_text, headers_text)
    table_html_text = graph_to_html(g)


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
        Зеленая: стартовая вершина, желтая: конечная
        {html_content}  <!-- Граф PyVis -->
        <h3>Временные параметры работ</h3>
        {table_html_edges}  <!-- Первая таблица -->
        <h4>Рассчетные варианты событий</h4>
        {table_html_nodes}  <!-- Вторая таблица -->
        <h5>Критические пути (до 10)</h5>
        {table_critical_paths}  <!-- Вторая таблица -->
        <h6>Введенная таблица в формате текста</h6>
        {table_html_text}  <!-- Вторая таблица --> 
    </body>
    </html>
    """
    #with open("graph.html", "w", encoding="utf-8") as f:
    #    f.write(html_content)
    #net.show("graph.html")
    #file_path = "graph.html"
    #net.show(file_path)

    # Открываем граф в браузере
    #webbrowser.open(file_path)

    return html_content


def draw_graph(g):
    plt.clf()
    node_matrices = dict()
    highlighted_edges = []
    for i in range(1, len(g.nodes)):
        node_matrices[i] = [[i, g.nodes[i].Tr], [g.nodes[i].R, g.nodes[i].Tp]]

    for edge in g.edges:
        if g.nodes[edge.y].R == 0 and g.nodes[edge.y].Tr == g.nodes[edge.x].Tr + edge.t[0]:
            highlighted_edges.append((edge.x, edge.y))

    #for lst in g.list_of_critical_paths:
    #    for i in range(1, len(lst)):
    #        highlighted_edges.append((lst[i - 1], lst[i]))

    return draw_process(g, highlighted_edges, node_matrices)




