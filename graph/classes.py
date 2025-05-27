INF = float("inf")
NEG_INF = float("-inf")


class EdgeInformation:
    def __init__(self):
        self.Trn = None
        self.Tro = None
        self.Tpo = None
        self.Tpn = None
        self.Rp = None
        self.Rc = None
        self.name = ""


class EdgeLite:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t


class Edge(EdgeLite):
    def __init__(self,x, y, t):
        super().__init__(x, y, t)
        self.info = EdgeInformation()


class Node:
    def __init__(self):
        self.x = None
        self.Tr = NEG_INF
        self.Tp = INF
        self.R = None


class Graph:
    def __init__(self, n, m, edges):
        self.n = n
        self.m = m
        self.edges = edges