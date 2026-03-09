import sys
import os
from Sokoban import Sokoban_Ponderado
from Buscas import dijkstra, ganancioso, a_estrela, recuperar_caminho

def ler_entrada(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = [linha.split() for linha in f if linha.strip()]
        
        if not linhas:
            print("Erro: Arquivo de entrada vazio.")
            sys.exit(1)
            
        altura = len(linhas)
        largura = len(linhas[0])
        mapa_achatado = [item for sublist in linhas for item in sublist]
        
        return mapa_achatado, largura, altura
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        sys.exit(1)

def gerar_grid_visual(problema, no_final):
    largura = problema.Largura
    altura = problema.Altura
    grid = ["⚪️"] * (largura * altura)
    
    for (px, py) in problema.paredes:
        grid[py * largura + px] = "🧱"
        
    for (ax, ay) in problema.alvos:
        grid[ay * largura + ax] = "🟢"

    caixas_finais = dict(no_final.estado[1])
    pesos_reversos = {v: k for k, v in problema.tabela_pesos.items()}
    
    for (cx, cy), peso in caixas_finais.items():
        # Se for um peso sorteado sem emoji fixo, mostra o número
        grid[cy * largura + cx] = pesos_reversos.get(peso, str(peso))

    pos_agente = no_final.estado[0]
    grid[pos_agente] = "🙎"

    linhas = []
    for i in range(0, len(grid), largura):
        linhas.append(" ".join(grid[i:i+largura]))
    return "\n".join(linhas)

def salvar_resultado(nome_arquivo, problema, resultado):
    no_final, estados_visitados = resultado
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        if no_final:
            f.write("Estado final\n")
            f.write(gerar_grid_visual(problema, no_final) + "\n\n")
            caminho = recuperar_caminho(no_final)
            f.write("Movimentos\n" + "".join(caminho) + "\n\n")
            f.write(f"Quantidades de movimentos\n{len(caminho)}\n\n")
            f.write(f"Custo total (W): {no_final.custo}\n")
            f.write(f"Estados visitados: {estados_visitados}\n")
        else:
            f.write("Sem solução encontrada para este algoritmo.")

def Solucao():
   
    if len(sys.argv) < 2:
        print("Uso: python Solucao.py entrada.txt [largura_opcional] [sortear_0_ou_1]")
        return

    caminho_entrada = sys.argv[1]
    mapa_bruto, largura_arq, altura_arq = ler_entrada(caminho_entrada)
    
    # Desafio: Tamanho lateral (largura) configurável via argumento 2
    largura = int(sys.argv[2]) if len(sys.argv) > 2 else largura_arq
    # Desafio: Ativar sorteio de caixas/pesos via argumento 3 (1 para sim, 0 para não)
    deve_sortear = int(sys.argv[3]) == 1 if len(sys.argv) > 3 else False
    
    problema = Sokoban_Ponderado(mapa_bruto, largura, altura_arq, sortear=deve_sortear)

    print(f"Executando com Largura: {largura}, Sorteio: {deve_sortear}")
    
    print("Executando Dijkstra...")
    salvar_resultado("dijkstra.txt", problema, dijkstra(problema))

    print("Executando Ganancioso...")
    salvar_resultado("ganancioso.txt", problema, ganancioso(problema))

    print("Executando A*...")
    salvar_resultado("a_estrela.txt", problema, a_estrela(problema))

    print("\nProcessamento concluído.")

if __name__ == "__main__":
    Solucao()