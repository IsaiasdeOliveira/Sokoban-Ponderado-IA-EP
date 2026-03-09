# EP: Sokoban Ponderado

Este projeto implementa um resolvedor otimizado para  **Sokoban Ponderado** utilizando algoritmos de busca em espaço de estados: **Dijkstra**, **Ganancioso (Greedy)** e **A***. O objetivo é minimizar o custo total de transporte das caixas até os alvos, considerando que cada caixa possui um peso específico.

---

##  Modelagem do Problema

### Representação Interna e Estados
Internamente, o estado do problema é representado por uma tupla imutável para garantir a integridade dos dados e permitir a comparação eficiente:
* **Posição do Agente**: Armazenada como um índice linear ($y \times \text{Largura} + x$), otimizando a memória e a velocidade de acesso.
* **Posição das Caixas**: Representada por uma tupla de pares `((x, y), peso)`. Esta estrutura é **sempre ordenada** antes da criação de qualquer nó para ser mais eficiente.
   
### Função Sucessora
A função sucessora expande o nó atual explorando as direções (⬆️, ⬇️, ⬅️, ➡️):
* **Validação**: Verifica se a próxima célula é uma parede ou limite do grid.
* **Lógica de Empurrão**: Se o agente encontra uma caixa, o sucessor só é gerado se houver um espaço livre atrás dela.
* **Poda por Deadlock**: Implementamos uma verificação antecipada. Se um empurrão colocar uma caixa em um "canto morto" (duas paredes adjacentes que não são alvos), o sucessor é descartado imediatamente.

### Função Objetivo
A busca termina com sucesso quando o conjunto de coordenadas de todas as caixas no estado atual coincide exatamente com o conjunto de coordenadas dos alvos (`🟢`) definidos no mapa.

---

## ⚖️ Custo e Heurística

### Cálculo de Custo ($W$)
O custo de transição entre estados reflete o esforço físico real:
* **Movimento Simples**: Custo = $1$.
* **Movimento de Transporte (Empurrar)**: Custo = $1 + \text{peso da caixa}$.
* **Relaxamento**: Os algoritmos Dijkstra e A* utilizam um dicionário de custos para permitir o relaxamento de arestas, atualizando o caminho caso uma rota mais barata para um mesmo estado seja encontrada.

### Função Heurística e Admissibilidade
A heurística adotada é a **Soma das Distâncias de Manhattan Ponderada**:
$$h(n) = \sum (|x_{caixa} - x_{alvo}| + |y_{caixa} - y_{alvo}|) \times peso\_caixa$$

**Por que a Heurística é admissível?**
1.  **Estimativa Otimista**: Ela assume que a caixa se move em linha reta, ignorando obstáculos e a necessidade do agente manobrar ao redor da caixa para empurrá-la.
2.  **Custo Mínimo**: Como o custo real de empurrar é sempre $\geq 1 + \text{peso}$, e a heurística ignora o custo do agente e os desvios, ela nunca superestima o custo real ($h(n) \leq h^*(n)$).
3.  **Garantia de Otimalidade**: Por ser admissível, o algoritmo **A*** garante encontrar a solução de custo mínimo global.

---
## Tabela Comparativa de Desempenho

| Tamanho do Grid | Métrica | Dijkstra | Ganancioso | A* (Otimizado) |
| :--- | :--- | :--- | :--- | :--- |
| **8 x 8** | Estados Expandidos | *2.456* | *69* | *464* |
| | Custo Total (W) | *36* | *36* | *36* |
| | Quantidades de Movimentos | *10* | *10* | *10* |
| **16 x 16** | Estados Expandidos | *1.472.621* | *11.788* | *545.227* |
| | Custo Total (W) | *38* | *91* | *65* |
| | Quantidades de Movimentos | *38* | *58* | *38* |
| **24 x 24** | Estados Expandidos | *102.404* | *85.133* | *98.439* |
| | Custo Total (W) | *329* | *329* | *329* |
| | Quantidades de Movimentos | *177* | *177* | *177* |
| **64 x 64** | Estados Expandidos | *N/A* | *N/A* | [Ver Docs](./docs/modelagem.md) |
| | Custo Total (W) | - | *N/A* | *N/A* |
| | Quantidades de Movimentos | *N/A* | *N/A* | *N/A* |

---

## 📖 Documentação Adicional
Para detalhes sobre o fluxograma de estados, diagramas Mermaid e justificativa técnica da escalabilidade do grid 64x64, acesse:
👉 **[Documentação de Modelagem Técnica](./docs/modelagem.md)**

## 🛠️ Instruções de Execução

O programa utiliza `Solucao.py` para processar os mapas e gerar os arquivos de saída (`dijkstra.txt`, `ganancioso.txt`, `a_estrela.txt`).

```bash
python Solucao.py [arquivo_mapa] [largura_opcional] [sortear_0_ou_1]