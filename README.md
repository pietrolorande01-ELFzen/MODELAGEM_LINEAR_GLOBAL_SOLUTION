# MODELAGEM_LINEAR_GLOBAL_SOLUTION

#  Global Solution — Sistema de Monitoramento de Missões Espaciais

**Disciplina:** MODELAGEM LINEAR PARA APRENDIZADO DE MÁQUINA

**Tema:** Sistema Inteligente de Monitoramento de Missão Espacial  

**Integrantes:**
- Pietro Lorande | RM569125
- Gustavo Bonamico Piccoli | RM 569984
- Maria Eduarda Medeiros Lemos | RM 574094

---

##  Estrutura do Projeto

```
GS_MOD_LIN/
├── global_solution_space_missions.py   # Código principal (todos os exercícios)
├── space_missions.csv                  # Base de dados
├── relatorio_global_solution.pdf       # Relatório estatístico completo
└── README.md                           # Este arquivo
```

Após a execução do script, os seguintes arquivos de gráficos serão gerados automaticamente na mesma pasta:

```
├── grafico1_lancamentos_por_ano.png
├── grafico2_status_missoes.png
├── grafico3_boxplots.png
└── grafico4_histogramas.png
```

---

##  Sobre a Base de Dados

### Identificação

| Campo        | Informação |
|--------------|------------|
| **Nome**     | All Space Missions from 1957 |
| **Fonte**    | [Kaggle — agirlcoding](https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957) |
| **Origem**   | Scraping do portal [Next Spaceflight](https://nextspaceflight.com/launches/past/) |
| **Formato**  | CSV (Comma-Separated Values) |
| **Registros**| 3.874 missões espaciais |
| **Período**  | 1957 (Sputnik) a 2022 |

### Justificativa de Escolha

O dataset foi selecionado por ser uma fonte **real, pública e verificável**, alinhada diretamente ao tema da avaliação: monitoramento operacional de missões espaciais. Ele contém variáveis operacionais críticas — custo, resultado e frequência de lançamentos — que permitem aplicar todos os conceitos estatísticos exigidos e gerar inteligência acionável sobre a indústria espacial moderna.

### Colunas da Base de Dados

| Coluna          | Tipo        | Descrição |
|-----------------|-------------|-----------|
| `Company`       | Categórica  | Empresa ou agência responsável pelo lançamento (ex: SpaceX, NASA, RVSN USSR) |
| `Location`      | Categórica  | País ou base de lançamento |
| `Date`          | Data        | Data do lançamento (formato YYYY-MM-DD) |
| `Rocket`        | Categórica  | Nome do foguete utilizado na missão |
| `RocketStatus`  | Categórica  | Status atual do foguete: `Active` ou `Retired` |
| `Price`         | Numérica contínua | Custo estimado da missão em **USD milhões** (aproximadamente 77% dos registros possuem valor nulo — comportamento esperado do dataset original) |
| `MissionStatus` | Categórica  | Resultado da missão: `Success`, `Failure`, `Partial Failure` |
| `Year`          | Numérica discreta | Ano de lançamento, extraído da coluna `Date` |

### Variáveis Utilizadas nos Exercícios

| Exercício | Variável | Tipo |
|-----------|----------|------|
| Ex. 02a — Tabela de frequências | `Year` (ano de lançamento) | Quantitativa **discreta** |
| Ex. 02b — Tabela de frequências | `Price` (custo em USD mi) | Quantitativa **contínua** |
| Ex. 03 — Gráfico 1 | `Year` × contagem de missões | Discreta |
| Ex. 03 — Gráfico 2 | `MissionStatus` | Categórica |
| Ex. 04 — Análise univariada 1 | `Price` | Contínua |
| Ex. 04 — Análise univariada 2 | Missões por ano (agrupado) | Discreta |

---

## Como Executar o Projeto

### 1. Pré-requisitos

Você precisa do **Python 3.8 ou superior** instalado. Verifique com:

```bash
python --version
```

### 2. Instalar as dependências

Abra o terminal (ou Prompt de Comando) na pasta do projeto e execute:

```bash
pip install pandas numpy matplotlib scipy
```

### 3. Organizar os arquivos

Certifique-se de que o arquivo `space_missions.csv` está **na mesma pasta** que o script `.py`:

```
GS_MOD_LIN\
  ├── global_solution_space_missions.py   
  └── space_missions.csv                 
```

> **Atenção:** o erro `FileNotFoundError: space_missions.csv` ocorre quando o CSV está em uma pasta diferente do script. Basta movê-los para a mesma pasta.

### 4. Executar o script

```bash
python global_solution_space_missions.py
```

Ou, pelo VS Code, abra o arquivo e pressione **F5** ou clique em Run.

### 5. Saída esperada

O script imprime no terminal todas as tabelas e medidas estatísticas, e salva 4 gráficos em PNG na mesma pasta.

---

##  O que o Script Faz (por exercício)

### Exercício 02 — Tabelas de Distribuição de Frequências

O script calcula automaticamente:

- **02a — Variável discreta (`Year`):** agrupa os lançamentos por década e monta a tabela com frequência absoluta (`fi`), relativa (`fr`), relativa percentual (`fr%`), acumulada (`Fi`) e acumulada percentual (`Fr%`).

- **02b — Variável contínua (`Price`):** aplica a **Regra de Sturges** (`k = 1 + 3,322 × log₁₀(n)`) para definir automaticamente o número ideal de classes e a amplitude `h`. Monta a tabela completa com ponto médio de cada classe.

### Exercício 03 — Gráficos Estatísticos

Dois gráficos são gerados e salvos em PNG:

- **Gráfico 1** (`grafico1_lancamentos_por_ano.png`): gráfico de barras com a série histórica de lançamentos por ano (1957–2022), incluindo linha de média e anotações de eventos históricos relevantes.

- **Gráfico 2** (`grafico2_status_missoes.png`): gráfico de barras horizontais com a distribuição dos resultados das missões (Sucesso / Falha / Falha Parcial), com rótulos de quantidade e percentual em cada barra.

Todos os gráficos contêm: título, rótulos dos eixos x e y, cores diferenciadas e legenda.

### Exercício 04 — Análise Univariada (Estatística Descritiva)

Para cada uma das duas variáveis (`Price` e missões por ano), o script calcula e exibe:

| Categoria | Medidas |
|-----------|---------|
| **Tendência central** | Média, Mediana, Moda |
| **Dispersão** | Máximo, Mínimo, Amplitude, Variância, Desvio Padrão, Coeficiente de Variação (CV%) |
| **Separatrizes** | Q1 (25%), Q2 (50%), Q3 (75%), IQR (Q3−Q1) |

Além disso, gera dois gráficos adicionais:
- **Gráfico 3** (`grafico3_boxplots.png`): boxplots lado a lado das duas variáveis.
- **Gráfico 4** (`grafico4_histogramas.png`): histogramas com curva de densidade KDE, média e mediana.

---

##  Compatibilidade com Diferentes Versões do Dataset

O script aceita automaticamente os seguintes nomes de arquivo (coloque **um** deles na pasta):

| Arquivo aceito | Origem |
|----------------|--------|
| `space_missions.csv` | Fornecido junto com este projeto |
| `Space Corrected.csv` | Download direto do Kaggle |
| `mission_launches.csv` | Versão alternativa do mesmo dataset |

O código também normaliza automaticamente os nomes das colunas entre as diferentes versões do dataset (Kaggle original, Maven Analytics etc.), então não é necessário editar o CSV manualmente.

---

##  Problemas Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `FileNotFoundError: space_missions.csv` | CSV em pasta diferente do `.py` | Mova ambos para a mesma pasta |
| `ModuleNotFoundError: No module named 'pandas'` | Dependência não instalada | Execute `pip install pandas numpy matplotlib scipy` |
| Gráficos não aparecem | Ambiente sem display (ex: servidor) | Os PNGs são salvos normalmente mesmo sem janela |
| `UnicodeDecodeError` | Encoding do CSV incompatível | Abra o CSV no Excel, salve como CSV UTF-8 e tente novamente |

---
