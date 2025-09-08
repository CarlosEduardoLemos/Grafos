# 📦 Grafos: Pontos de Entrega

Este repositório contém um exemplo em **Python** que modela um pequeno grafo rodoviário (pontos de entrega) e demonstra operações comuns em grafos:

- ✅ Visualização do grafo com pesos (distâncias/custos)  
- ✅ Cálculo do menor caminho entre dois pontos (**Algoritmo de Dijkstra**)  
- ✅ Listagem dos menores caminhos a partir de um nó para todos os demais  
- ✅ Aproximação do problema do **Caixeiro Viajante (TSP)**  
- ✅ Cálculo de custo monetário associado a uma rota (ex.: R\$ por unidade de distância)  

O exemplo está no arquivo **`main.py`** e foi feito para reproduzir a figura fornecida no material (posições dos nós foram definidas manualmente para coincidir com a imagem).

---

## 🔧 Pré-requisitos

- **Python** 3.8+ (testado em 3.8 — deve funcionar até 3.11)
- **pip**

### Dependências

Instale com:

```bash
pip install networkx matplotlib
```

Ou crie um `requirements.txt` e instale com:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

No terminal, estando na pasta do projeto:

```bash
python main.py
```

> **Observação:** O script abre janelas com gráficos (`plt.show()`).  
> Em ambientes sem interface gráfica (headless), comente as chamadas `plt.show()` e use `plt.savefig(...)` ou configure um backend apropriado.

---

## 📂 Estrutura do código (`main.py`)

O script está organizado em blocos comentados:

1. **Definição dos pontos (vértices)**  
   Lista `locais_entrega` com nomes dos nós:  
   `Asa Norte, Asa Sul, Lago Sul, Esplanada, Lago Norte, Vila Planalto`

2. **Arestas com pesos**  
   Lista `conexoes` com tuplas `(origem, destino, peso)`.  
   Exemplo:  
   ```
   Lago Sul — Esplanada : 11
   Lago Sul — Asa Sul : 5
   Lago Norte — Esplanada : 8
   ...
   ```

3. **Visualização do grafo**  
   Usa `matplotlib` + `networkx` para desenhar o grafo com posições fixas.

4. **Menor caminho entre dois pontos (Dijkstra)**  
   Exemplo: menor caminho entre `"Lago Norte"` e `"Lago Sul"`  
   Saída esperada:  
   ```
   Menor caminho Lago Norte -> Lago Sul: ['Lago Norte', 'Esplanada', 'Asa Sul', 'Lago Sul'] com custo 18
   ```

5. **Menores caminhos a partir de um nó**  
   Itera sobre todos os destinos a partir de `"Lago Norte"`.

6. **Aproximação do Caixeiro Viajante (TSP)**  
   Usa `networkx.approximation.traveling_salesman_problem`.

7. **Cálculo de custo monetário**  
   Exemplo: R\$20 por unidade de distância.

---

## ✅ Exemplo de saída no console

```
Menor caminho Lago Norte -> Lago Sul: ['Lago Norte', 'Esplanada', 'Asa Sul', 'Lago Sul'] com custo 18

Caminhos mínimos a partir do Lago Norte:
Lago Norte -> Asa Norte: ['Lago Norte', 'Asa Norte'], custo 12
Lago Norte -> Asa Sul: ['Lago Norte', 'Esplanada', 'Asa Sul'], custo 13
...
```

## 📜 Licença e Autor

- **Autor:** Carlos Lemos  
- **Licença:** MIT (sinta-se à vontade para adaptar)  

---

## 🤝 Contribuição

Abra **issues** ou **pull requests** com sugestões, correções ou melhorias.

---