from Estruturas import FilaPrioridade, No

def recuperar_caminho(no_final):
    caminho = []
    atual = no_final
    while atual and atual.no_pai:
        caminho.append(atual.aresta)
        atual = atual.no_pai
    return caminho[::-1]

def dijkstra(problema):
    estado_ini = (problema.posicao_agente_inicial, tuple(sorted(problema.caixas_iniciais.items())))
    no_inicial = No(estado_ini, None, None, custo=0)
    fila = FilaPrioridade()
    fila.push(no_inicial, 0)
    visitados = {}
    expandidos = 0
    while not fila.esta_vazio():
        prioridade, no = fila.pop()
        if problema.testar_objetivo(no): return no, expandidos
        if no.estado in visitados and visitados[no.estado] <= no.custo: continue
        visitados[no.estado] = no.custo
        expandidos += 1
        for suc in problema.gerar_sucessores(no):
            if suc.estado not in visitados or visitados[suc.estado] > suc.custo:
                fila.push(suc, suc.custo)
    return None, expandidos

def a_estrela(problema):
    estado_ini = (problema.posicao_agente_inicial, tuple(sorted(problema.caixas_iniciais.items())))
    no_inicial = No(estado_ini, None, None, custo=0)
    no_inicial.heuristica = problema.heuristica(no_inicial)
    fila = FilaPrioridade()
    fila.push(no_inicial, no_inicial.custo + no_inicial.heuristica)
    visitados = {}
    expandidos = 0
    while not fila.esta_vazio():
        prioridade, no = fila.pop()
        if problema.testar_objetivo(no): return no, expandidos
        if no.estado in visitados and visitados[no.estado] <= no.custo: continue
        visitados[no.estado] = no.custo
        expandidos += 1
        for suc in problema.gerar_sucessores(no):
            suc.heuristica = problema.heuristica(suc)
            if suc.estado not in visitados or visitados[suc.estado] > suc.custo:
                fila.push(suc, suc.custo + suc.heuristica)
    return None, expandidos

def ganancioso(problema):
    estado_ini = (problema.posicao_agente_inicial, tuple(sorted(problema.caixas_iniciais.items())))
    no_inicial = No(estado_ini, None, None, custo=0)
    fila = FilaPrioridade()
    fila.push(no_inicial, problema.heuristica(no_inicial))
    visitados = set()
    expandidos = 0
    while not fila.esta_vazio():
        prioridade, no = fila.pop()
        if problema.testar_objetivo(no): return no, expandidos
        if no.estado in visitados: continue
        visitados.add(no.estado)
        expandidos += 1
        for suc in problema.gerar_sucessores(no):
            if suc.estado not in visitados:
                fila.push(suc, problema.heuristica(suc))
    return None, expandidos