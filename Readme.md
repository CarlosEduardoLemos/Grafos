# 📦 Projeto – Teoria dos Grafos em Python

Este projeto implementa um sistema de cálculo de rotas utilizando **teoria dos grafos**. O código foi desenvolvido em Python para resolver problemas de menor caminho e otimização de rotas de entrega, aplicando algoritmos como **Dijkstra** e uma aproximação do **Problema do Caixeiro Viajante (TSP)**.

---

## 🚀 Funcionalidades

* Representação gráfica dos pontos de entrega (vértices) e conexões entre eles (arestas).
* Cálculo do **menor caminho** entre dois pontos (Lago Norte → Lago Sul).
* Cálculo dos **menores caminhos** do Lago Norte para todos os outros pontos de entrega.
* Determinação do **caminho mais econômico para visitar todos os pontos** (aproximação do TSP).
* Cálculo do **custo monetário total** (considerando R\$20 por unidade de custo).
* Geração de relatório em **.docx**.

---

## ⚙️ Pré-requisitos

1. Ter o **Python 3.10+** instalado.
2. Criar um ambiente virtual (recomendado):

```bash
python -m venv venv
```

3. Ativar o ambiente virtual:

   * **Windows (cmd)**:

     ```bash
     venv\Scripts\activate
     ```
   * **Linux/MacOS (bash/zsh)**:

     ```bash
     source venv/bin/activate
     ```

4. Instalar as dependências:

```bash
pip install -r requirements.txt
```

---

## 📦 Dependências

As bibliotecas necessárias são:

* [networkx](https://networkx.org/) – modelagem e análise de grafos
* [matplotlib](https://matplotlib.org/) – visualização do grafo
* [python-docx](https://python-docx.readthedocs.io/) – geração de relatório em Word

Se preferir instalar manualmente:

```bash
pip install networkx matplotlib python-docx
```

---

## ▶️ Como Executar

1. Clone ou baixe o projeto.
2. Ative o ambiente virtual e instale as dependências.
3. Execute o script principal:

```bash
python main.py
```

4. O programa irá:

   * Mostrar o grafo com vértices, arestas e pesos.
   * Exibir no terminal os menores caminhos e custos.
   * Gerar o arquivo `Relatorio_Teoria_dos_Grafos.docx` com os resultados.

---

## 📂 Estrutura do Projeto

```
📁 projeto-grafos
 ┣ 📜 main.py              # Código principal do projeto
 ┣ 📜 requirements.txt     # Lista de dependências
 ┣ 📜 Relatorio_Teoria_dos_Grafos.docx  # Relatório gerado
 ┗ 📜 README.md            # Documentação do projeto
```

---

## 📝 Observações

* Cada unidade de custo equivale a **R\$20,00**.
* O relatório segue a **estrutura ABNT**, contendo introdução, arquitetura, resultados e conclusão.
* É possível adaptar o grafo para outros cenários, alterando os vértices e pesos definidos no código.
