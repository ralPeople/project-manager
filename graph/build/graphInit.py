import copy
import sys
from collections import defaultdict, deque
from typing import List, Tuple
from graph.classes import Node, Edge, Graph
from Exceptions.exceptions import InvalidEdgeException, InvalidNodeException

INF = float("inf")

from tkinter import messagebox

S, T = None, None
e = defaultdict(list)
e2 = defaultdict(list)
path_list = []

def error(message):
    print(f"ERROR: {message}")
    messagebox.showinfo("Ошибка", message)
    sys.exit(0)

def solve(g):
    global S, T

    n = g.n

    nodes = [Node() for _ in range(n + 1)]
    nodes[S].Tr = 0
    print("S =",S)
    print("T =",T)


    for i in range(2, n + 1):
        for edge in e2[i]:
            nodes[i].Tr = max(nodes[i].Tr, nodes[edge.y].Tr + edge.t)

    nodes[T].Tp = nodes[T].Tr

    for i in range(n - 1, 0, -1):
        for edge in e[i]:
            nodes[i].Tp = min(nodes[i].Tp, nodes[edge.y].Tp - edge.t)

    for i in range(1, n + 1):
        nodes[i].x = i
        nodes[i].R = nodes[i].Tp - nodes[i].Tr

    for i in range(1, n + 1):
        print(f"Node number {nodes[i].x} | Tr = {nodes[i].Tr:4} | Tp = {nodes[i].Tp:4} | R = {nodes[i].R:4}")

    for i in range(1, n + 1):
        for edge in e[i]:
            edge.info.Trn = nodes[i].Tr
            edge.info.Tro = nodes[i].Tr + edge.t

            edge.info.Tpo = nodes[edge.y].Tp
            edge.info.Tpn = nodes[edge.y].Tp - edge.t

            edge.info.Rp = nodes[edge.y].Tp - nodes[i].Tr - edge.t
            edge.info.Rc = nodes[edge.y].Tr - nodes[i].Tr - edge.t

    W = 12
    print(f"{'(i,j)':>6}{'t(i,j)':>{W}}{'Trn(i,j)':>{W}}{'Tro(i,j)':>{W}}{'Tpn(i,j)':>{W}}{'Tpo(i,j)':>{W}}{'Rp(i,j)':>{W}}{'Rc(i,j)':>{W}}")
    for i in range(1, n + 1):
        for edge in e[i]:
            print(f"{i},{edge.y:>{6}}{edge.t:>{W}}{edge.info.Trn:>{W}}{edge.info.Tro:>{W}}{edge.info.Tpn:>{W}}{edge.info.Tpo:>{W}}{edge.info.Rp:>{W}}{edge.info.Rc:>{W}}")

    path = []
    cnt = 0
    global path_list
    path_list = []

    def print_path():
        path_list.append(copy.deepcopy(path))
        print(" -> ".join(map(str, path[::-1])))

    def dfs(x):
        nonlocal cnt
        if cnt > 9:
            return
        if x == 1:
            print_path()
            cnt += 1
            return
        for edge in e2[x]:
            if nodes[edge.y].R == 0:
                path.append(copy.deepcopy(edge.y))
                dfs(edge.y)
                path.pop()

    for i in range(1,n+1):
        print(i)
        for j in range(len(e2[i])):
            print(e2[i][j].x, e2[i][j].y)
    print("\nList of critical paths:")
    path.append(n)
    dfs(n)
    path.pop()

    g.list_of_critical_paths = copy.deepcopy(path_list)
    g.nodes = copy.deepcopy(nodes)
    g.e = copy.deepcopy(e)
    g.e2 = copy.deepcopy(e2)

    if cnt > 10:
        print(f"WARNING: graph has at least {cnt} critical paths!")
    elif cnt > 1:
        print(f"WARNING: graph has {cnt} critical paths!")
    return


def mark_source(g, in_degree, out_degree):
    global S, T
    sources = sum(1 for x in in_degree[1:] if x == 0)
    sinks = sum(1 for x in out_degree[1:] if x == 0)

    if sources != 1:
        raise InvalidNodeException("В графе больше одного начального события")
    if sinks != 1:
        raise InvalidNodeException("В графе больше одного конечного события")
    S = 1
    T = g.n


def build_graph(g):
    global e, e2
    in_degree = [0] * (g.n + 1)
    out_degree = [0] * (g.n + 1)
    e = defaultdict(list)
    e2 = defaultdict(list)

    par = set()
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        weight = g.edges[i].t
        if (x, y) in par:
            raise InvalidEdgeException(f"В графе есть кратные ребра {x} -> {y}")
        if x >= y:
            raise InvalidEdgeException(f"В графе номер начального события не меньше номера конечного: {x} и {y}")
        par.add((x, y))
        edge = Edge(x, y, weight[0])
        e[x].append(edge)
        edge = Edge(y, x, weight[0])
        e2[y].append(edge)
        in_degree[y] += 1
        out_degree[x] += 1

    mark_source(g, in_degree, out_degree)

    for i in range(1, g.n + 1):
        for el in e[i]:
            print(i, el.y, el.t)

    solve(g)
