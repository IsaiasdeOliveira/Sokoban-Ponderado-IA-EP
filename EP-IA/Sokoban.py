import random
from Estruturas import No

class Sokoban_Ponderado:
    def __init__(self, mapa_inicial, Largura, Altura, sortear=False):
        self.mapa_inicial = mapa_inicial
        self.Largura = Largura
        self.Altura = Altura
        self.paredes = set()
        self.alvos = set()
        self.caixas_iniciais = {}
        self.posicao_agente_inicial = None
        self.tabela_pesos = {
            "1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5,
            "6️⃣": 6, "7️⃣": 7, "8️⃣": 8, "9️⃣": 9
        }

        espacos_vazios = []

        for indice, elemento in enumerate(mapa_inicial):
            if indice >= self.Largura * self.Altura: break
            
            x, y = indice % self.Largura, indice // self.Largura
            if elemento == "🧱": self.paredes.add((x, y))
            elif elemento == "🟢": self.alvos.add((x, y))
            elif elemento == "🙎": self.posicao_agente_inicial = indice
            elif elemento in self.tabela_pesos and not sortear:
                self.caixas_iniciais[(x, y)] = self.tabela_pesos[elemento]
            elif elemento == "⚪️":
                espacos_vazios.append((x, y))

        if sortear and self.alvos:
            num_caixas = min(len(self.alvos), len(espacos_vazios))
            posicoes_sorteadas = random.sample(espacos_vazios, num_caixas)
            for pos in posicoes_sorteadas:
                self.caixas_iniciais[pos] = random.randint(1, 9)
    def eh_deadlock(self, x, y):
        """Versão simplificada: Só trava se estiver em um canto que NÃO seja alvo."""
        if (x, y) in self.alvos:
            return False
        
        # Checa paredes ou limites
        p_cima = (x, y-1) in self.paredes or y-1 < 0
        p_baixo = (x, y+1) in self.paredes or y+1 >= self.Altura
        p_esq = (x-1, y) in self.paredes or x-1 < 0
        p_dir = (x+1, y) in self.paredes or x+1 >= self.Largura

        # Só considera deadlock se estiver encostado em DUAS paredes que formam um canto
        if (p_cima and p_esq) or (p_cima and p_dir) or (p_baixo and p_esq) or (p_baixo and p_dir):
            return True
        return False

    def Custo(self, no_atual, proxima_pos_agente):
        caixas_atuais = dict(no_atual.estado[1])
        x_novo, y_novo = proxima_pos_agente % self.Largura, proxima_pos_agente // self.Largura
        if (x_novo, y_novo) in caixas_atuais:
            return 1 + caixas_atuais[(x_novo, y_novo)]
        return 1

    def heuristica(self, no):
        caixas = dict(no.estado[1])
        h_total = 0
        for (cx, cy), peso in caixas.items():
            distancias = [abs(cx - ax) + abs(cy - ay) for (ax, ay) in self.alvos]
            if distancias:
                h_total += min(distancias) * peso
        return h_total

    def testar_objetivo(self, no):
        return set(dict(no.estado[1]).keys()) == self.alvos 

    def gerar_sucessores(self, no):
        nos_sucessores = []
        pos_agente = no.estado[0]
        caixas_atuais = dict(no.estado[1])
        ax, ay = pos_agente % self.Largura, pos_agente // self.Largura

        for seta, dx, dy in [("⬆️", 0, -1), ("⬇️", 0, 1), ("⬅️", -1, 0), ("➡️", 1, 0)]:
            nx, ny = ax + dx, ay + dy
            if not (0 <= nx < self.Largura and 0 <= ny < self.Altura) or (nx, ny) in self.paredes:
                continue

            idx_novo_agente = ny * self.Largura + nx

            if (nx, ny) in caixas_atuais:
                cx, cy = nx + dx, ny + dy
                # Verificação de espaço para empurrar
                if 0 <= cx < self.Largura and 0 <= cy < self.Altura and \
                   (cx, cy) not in self.paredes and (cx, cy) not in caixas_atuais:
                    
                    # Se você achar que ainda está lento, pode comentar a linha abaixo para testar
                    if self.eh_deadlock(cx, cy): continue
                    
                    novas_caixas = caixas_atuais.copy()
                    peso = novas_caixas.pop((nx, ny))
                    novas_caixas[(cx, cy)] = peso
                    estado = (idx_novo_agente, tuple(sorted(novas_caixas.items())))
                    nos_sucessores.append(No(estado, no, seta, no.custo + self.Custo(no, idx_novo_agente)))
            else:
                # Movimento simples do agente
                estado = (idx_novo_agente, no.estado[1])
                nos_sucessores.append(No(estado, no, seta, no.custo + self.Custo(no, idx_novo_agente)))
        return nos_sucessores