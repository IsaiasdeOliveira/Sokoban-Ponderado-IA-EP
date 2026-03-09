import heapq

class No:
    def __init__(self, estado, no_pai=None, aresta=None, custo=0.0, heuristica=0.0):
        self.estado = estado
        self.no_pai = no_pai
        self.aresta = aresta
        self.custo = custo
        self.heuristica = heuristica

    def __repr__(self):
        return str(self.estado)

    def __lt__(self, outro):
        return (self.custo + self.heuristica) < (outro.custo + outro.heuristica)

class FilaPrioridade:
    def __init__(self):
        self.heap = []

    def push(self, no, prioridade):
        # Armazenamos como uma tupla (prioridade, no)
        heapq.heappush(self.heap, (prioridade, no))
        
    def pop(self):
        if self.esta_vazio():
           return (None, None)
        # Retorna a tupla (prioridade, no)
        return heapq.heappop(self.heap)

    def esta_vazio(self):
        return len(self.heap) == 0

def no_caminho(no):
    caminho = [no.estado]
    while no.no_pai is not None:
        caminho.append(no.estado)
        no = no.no_pai
    caminho.reverse()
    return caminho

def vertice_caminho(no):
    caminho = []
    while no.no_pai is not None:
        if no.aresta is not None: 
            caminho.append(no.aresta)
        no = no.no_pai
    caminho.reverse()
    return caminho