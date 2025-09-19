
# 📦 Grafos: Pontos de Entrega

Este repositório apresenta um exemplo em **Python** para modelagem e análise de um grafo rodoviário de pontos de entrega, incluindo visualização, cálculo de rotas e aproximação do Caixeiro Viajante.

## Funcionalidades

- Visualização do grafo com pesos (distâncias/custos)
- Cálculo do menor caminho entre dois pontos (**Dijkstra**)
- Listagem dos menores caminhos a partir de um nó
- Aproximação do problema do **Caixeiro Viajante (TSP)**
- Cálculo de custo monetário associado à rota (ex.: R$ por unidade de distância)
- Geração automática de imagens dos grafos no diretório `IMG`
- Saída detalhada via **logging** (mensagens informativas e erros)

O código principal está em **`main.py`**. As posições dos nós são fixas para coincidir com a imagem do material.

---

## 🔧 Pré-requisitos

- **Python** 3.8 ou superior (testado até 3.11)
- **pip**

### Instalação das dependências

```bash
pip install networkx matplotlib
```
Ou:
```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

No terminal, na pasta do projeto:

```bash
python main.py
```

Por padrão, o script:
- Gera e salva imagens dos grafos em `IMG/`
- Mostra os gráficos na tela (se possível)
- Exibe no console os caminhos mínimos e rota TSP

### Argumentos de linha de comando

O script aceita diversos argumentos para personalizar a execução:

| Argumento                | Descrição                                                        |
|--------------------------|------------------------------------------------------------------|
| `--no-draw`              | Não desenha nem salva figuras                                    |
| `--show`                 | Mostra figuras interativamente                                   |
| `--shortest SRC DEST`    | Calcula e destaca o menor caminho entre SRC e DEST               |
| `--all-shortest-from SRC`| Lista todos os menores caminhos a partir de SRC                  |
| `--tsp`                  | Executa aproximação do Caixeiro Viajante                         |
| `--start NODE`           | Define nó inicial para TSP/relatórios                            |

### Exemplos de saída esperada

#### `--shortest SRC DEST`
```
INFO: Shortest path Lago Norte -> Lago Sul: ['Lago Norte', 'Esplanada', 'Asa Sul', 'Lago Sul'] with cost 18
```

#### `--all-shortest-from SRC`
```
INFO: Shortest paths from Lago Norte:
INFO: Lago Norte -> Asa Norte: path ['Lago Norte', 'Asa Norte'], cost 12
INFO: Lago Norte -> Asa Sul: path ['Lago Norte', 'Esplanada', 'Asa Sul'], cost 13
... (demais caminhos)
```

#### `--tsp`
```
INFO: Most economical route (TSP): ['Lago Norte', 'Vila Planalto', ...] with cost 54
INFO: Value in reais (multiplier 20) = R$1080.00
```

#### `--no-draw`
Nenhuma imagem será gerada ou exibida, apenas os resultados no console.

#### `--show`
As figuras dos grafos serão exibidas interativamente na tela, além de serem salvas em IMG/.

**Exemplo:**
```bash
python main.py --shortest "Lago Norte" "Lago Sul" --show
```

---

## 🖼️ Geração de Imagens

As imagens dos grafos são salvas automaticamente no diretório `IMG/` com timestamp no nome. Para desativar, use `--no-draw`.

---

## 🖥️ Uso em ambientes sem interface gráfica

Se estiver em ambiente **headless** (sem GUI), comente as linhas `plt.show()` em `main.py` ou utilize apenas a geração de arquivos (`plt.savefig`).

---

## 📂 Estrutura do código (`main.py`)

- **Definição dos pontos (vértices):**
   Lista `delivery_points` com nomes dos nós: `Asa Norte, Asa Sul, Lago Sul, Esplanada, Lago Norte, Vila Planalto`
- **Arestas com pesos:**
   Lista `connections` com tuplas `(origem, destino, peso)`
- **Visualização do grafo:**
   Funções para desenhar e salvar imagens
- **Menor caminho (Dijkstra):**
   Função para calcular e destacar o menor caminho
- **Menores caminhos a partir de um nó:**
   Função para listar todos os caminhos mínimos
- **Aproximação do TSP:**
   Função para calcular rota aproximada
- **Cálculo de custo monetário:**
   Multiplicador configurável (`MULTIPLIER_REAIS`)
- **Logs e tratamento de erros:**
   Mensagens informativas e erros via `logging`

---

## ✅ Exemplo de saída no console

```
INFO: Shortest path Lago Norte -> Lago Sul: ['Lago Norte', 'Esplanada', 'Asa Sul', 'Lago Sul'] with cost 18

INFO: Shortest paths from Lago Norte:
INFO: Lago Norte -> Asa Norte: path ['Lago Norte', 'Asa Norte'], cost 12
INFO: Lago Norte -> Asa Sul: path ['Lago Norte', 'Esplanada', 'Asa Sul'], cost 13
...

INFO: Most economical route (TSP): ['Lago Norte', 'Vila Planalto', ...] with cost 54
INFO: Value in reais (multiplier 20) = R$1080.00
```

---

## 📜 Licença e Autor

- **Autor:** Carlos Lemos
- **Licença:** MIT

---

## 🤝 Contribuição

Sugestões, correções ou melhorias são bem-vindas via **issues** ou **pull requests**.

---