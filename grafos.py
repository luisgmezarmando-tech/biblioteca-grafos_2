import random
import math
import sys
from collections import deque

# Límite de recursión ampliado para soportar DFS en grafos profundos de 500 nodos
sys.setrecursionlimit(10000)


class Nodo:
    def __init__(self, id_nodo, x=0.0, y=0.0):
        self.id = id_nodo
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.id)


class Arista:
    def __init__(self, origen, destino, dirigido=False):
        self.origen = origen
        self.destino = destino
        self.dirigido = dirigido

    def __str__(self):
        conector = "->" if self.dirigido else "--"
        return f"{self.origen.id} {conector} {self.destino.id}"


class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = {}        # id_nodo -> Nodo
        self.aristas = []      # Lista de objetos Arista
        self.adyacencias = {}  # id_nodo -> lista de vecinos
        self.dirigido = dirigido

    def agregar_nodo(self, id_nodo, x=0.0, y=0.0):
        id_str = str(id_nodo)
        if id_str not in self.nodos:
            self.nodos[id_str] = Nodo(id_str, x, y)
            self.adyacencias[id_str] = []

    def agregar_arista(self, id_origen, id_destino):
        u = str(id_origen)
        v = str(id_destino)

        if u not in self.nodos:
            self.agregar_nodo(u)
        if v not in self.nodos:
            self.agregar_nodo(v)
            
        nodo_origen = self.nodos[u]
        nodo_destino = self.nodos[v]
        
        self.aristas.append(Arista(nodo_origen, nodo_destino, self.dirigido))
        self.adyacencias[u].append(v)
        if not self.dirigido:
            self.adyacencias[v].append(u)

    def guardar_graphviz(self, nombre_archivo):
        tipo_grafo = "digraph" if self.dirigido else "graph"
        conector = "->" if self.dirigido else "--"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f"{tipo_grafo} G {{\n")
            for id_nodo in self.nodos:
                f.write(f'    "{id_nodo}";\n')
            for arista in self.aristas:
                f.write(f'    "{arista.origen.id}" {conector} "{arista.destino.id}";\n')
            f.write("}\n")

    # -------------------------------------------------------------
    # MÉTODOS TAREA 2: ÁRBOLES INDUCIDOS BFS Y DFS
    # -------------------------------------------------------------

    def BFS(self, s):
        """
        Calcula el árbol inducido por BFS partiendo del nodo fuente s.
        """
        s = str(s)
        if s not in self.nodos:
            raise ValueError(f"El nodo fuente '{s}' no existe en el grafo.")

        arbol = Grafo(dirigido=self.dirigido)
        arbol.agregar_nodo(s, self.nodos[s].x, self.nodos[s].y)

        visitados = {s}
        cola = deque([s])

        while cola:
            u = cola.popleft()
            for v in self.adyacencias.get(u, []):
                if v not in visitados:
                    visitados.add(v)
                    arbol.agregar_nodo(v, self.nodos[v].x, self.nodos[v].y)
                    arbol.agregar_arista(u, v)
                    cola.append(v)

        return arbol

    def DFS_R(self, s):
        """
        Calcula el árbol inducido por DFS recursivo partiendo del nodo fuente s.
        """
        s = str(s)
        if s not in self.nodos:
            raise ValueError(f"El nodo fuente '{s}' no existe en el grafo.")

        arbol = Grafo(dirigido=self.dirigido)
        arbol.agregar_nodo(s, self.nodos[s].x, self.nodos[s].y)
        visitados = {s}

        def _dfs(u):
            for v in self.adyacencias.get(u, []):
                if v not in visitados:
                    visitados.add(v)
                    arbol.agregar_nodo(v, self.nodos[v].x, self.nodos[v].y)
                    arbol.agregar_arista(u, v)
                    _dfs(v)

        _dfs(s)
        return arbol

    def DFS_I(self, s):
        """
        Calcula el árbol inducido por DFS iterativo con pila partiendo del nodo fuente s.
        """
        s = str(s)
        if s not in self.nodos:
            raise ValueError(f"El nodo fuente '{s}' no existe en el grafo.")

        arbol = Grafo(dirigido=self.dirigido)
        visitados = set()
        pila = [(s, None)]  # (nodo_actual, nodo_padre)

        while pila:
            u, padre = pila.pop()
            if u not in visitados:
                visitados.add(u)
                arbol.agregar_nodo(u, self.nodos[u].x, self.nodos[u].y)
                if padre is not None:
                    arbol.agregar_arista(padre, u)

                # Se recorre en orden inverso para mantener consistencia con DFS recursivo
                for v in reversed(self.adyacencias.get(u, [])):
                    if v not in visitados:
                        pila.append((v, u))

        return arbol


# -------------------------------------------------------------
# MODELOS DE GENERACIÓN (PROYECTO 1)
# -------------------------------------------------------------

def grafoMalla(m, n, dirigido=False):
    g = Grafo(dirigido)
    for i in range(m):
        for j in range(n):
            g.agregar_nodo(f"n_{i}_{j}")
            
    for i in range(m):
        for j in range(n):
            origen = f"n_{i}_{j}"
            if i < m - 1:
                destino_x = f"n_{i+1}_{j}"
                g.agregar_arista(origen, destino_x)
            if j < n - 1:
                destino_y = f"n_{i}_{j+1}"
                g.agregar_arista(origen, destino_y)
    return g

def grafoErdosRenyi(n, m, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i))
        
    aristas_creadas = set()
    while len(aristas_creadas) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            arista = (u, v) if dirigido else tuple(sorted([u, v]))
            if arista not in aristas_creadas:
                aristas_creadas.add(arista)
                g.agregar_arista(str(u), str(v))
    return g

def grafoGilbert(n, p, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i))
        
    for u in range(n):
        for v in range(n):
            if u != v and (dirigido or u < v):
                if random.random() < p:
                    g.agregar_arista(str(u), str(v))
    return g

def grafoGeografico(n, r, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i), x=random.random(), y=random.random())
        
    nodos_lista = list(g.nodos.values())
    for i in range(n):
        for j in range(i + 1, n):
            nodo1 = nodos_lista[i]
            nodo2 = nodos_lista[j]
            distancia = math.sqrt((nodo1.x - nodo2.x)**2 + (nodo1.y - nodo2.y)**2)
            if distancia <= r:
                g.agregar_arista(nodo1.id, nodo2.id)
                if dirigido:
                    g.agregar_arista(nodo2.id, nodo1.id)
    return g

def grafoBarabasiAlbert(n, d, dirigido=False):
    g = Grafo(dirigido)
    for i in range(d):
        g.agregar_nodo(str(i))
        
    for i in range(d):
        for j in range(i + 1, d):
            g.agregar_arista(str(i), str(j))
            if dirigido:
                g.agregar_arista(str(j), str(i))
                
    grados = []
    for arista in g.aristas:
        grados.append(arista.origen.id)
        grados.append(arista.destino.id)
        
    for i in range(d, n):
        nodo_nuevo = str(i)
        g.agregar_nodo(nodo_nuevo)
        
        objetivos = set()
        while len(objetivos) < d and len(grados) > 0:
            candidato = random.choice(grados)
            if candidato != nodo_nuevo:
                objetivos.add(candidato)
                
        for obj in objetivos:
            g.agregar_arista(nodo_nuevo, obj)
            grados.append(nodo_nuevo)
            grados.append(obj)
            
    return g

def grafoDorogovtsevMendes(n, dirigido=False):
    g = Grafo(dirigido)
    for i in range(3):
        g.agregar_nodo(str(i))
        
    g.agregar_arista("0", "1")
    g.agregar_arista("1", "2")
    g.agregar_arista("2", "0")
    
    for i in range(3, n):
        nodo_nuevo = str(i)
        g.agregar_nodo(nodo_nuevo)
        arista_elegida = random.choice(g.aristas)
        g.agregar_arista(nodo_nuevo, arista_elegida.origen.id)
        g.agregar_arista(nodo_nuevo, arista_elegida.destino.id)
        
    return g