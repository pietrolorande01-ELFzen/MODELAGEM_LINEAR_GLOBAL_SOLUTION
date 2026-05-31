# =============================================================================
# Dataset: All Space Missions from 1957 (Kaggle)
#   Link: https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES GERAIS DE VISUALIZAÇÃO
# ---------------------------------------------------------------------------

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#f8f9fa',
    'axes.grid':        True,
    'grid.alpha':       0.4,
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'DejaVu Sans',
    'axes.titlesize':   14,
    'axes.labelsize':   12,
})

COR_PRINCIPAL = '#1a6fba'
COR_SECUNDARIA = '#e84545'
COR_TERCIARIA  = '#2ecc71'

import os, sys

print("=" * 65)
print("  GLOBAL SOLUTION — MISSÕES ESPACIAIS (1957–2022)")
print("=" * 65)

ARQUIVOS_POSSIVEIS = [
    'space_missions.csv',
    'Space Corrected.csv',
    'mission_launches.csv',
    'space_mission_dataset.csv',
]

# Busca na mesma pasta do script
PASTA = os.path.dirname(os.path.abspath(__file__))
arquivo_csv = None
for nome in ARQUIVOS_POSSIVEIS:
    caminho = os.path.join(PASTA, nome)
    if os.path.exists(caminho):
        arquivo_csv = caminho
        print(f"\nArquivo encontrado: {nome}")
        break

if arquivo_csv is None:
    print("\n[ERRO] Nenhum arquivo CSV encontrado na pasta:")
    print(f"  {PASTA}")
    print("\nColoque um dos arquivos abaixo na mesma pasta que este script:")
    for n in ARQUIVOS_POSSIVEIS:
        print(f"  - {n}")
    print("\nDownload do dataset original:")
    print("  https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957")
    sys.exit(1)

df = pd.read_csv(arquivo_csv)

cols = df.columns.tolist()
renomear = {}
if 'Company Name' in cols: renomear['Company Name'] = 'Company'
if 'Datum' in cols and 'Date' not in cols: renomear['Datum'] = 'Date'
if 'Status Rocket' in cols: renomear['Status Rocket'] = 'RocketStatus'
if 'Status Mission' in cols: renomear['Status Mission'] = 'MissionStatus'
if 'Organisation' in cols and 'Company' not in cols: renomear['Organisation'] = 'Company'
if 'Rocket_Status' in cols: renomear['Rocket_Status'] = 'RocketStatus'
if 'Mission_Status' in cols: renomear['Mission_Status'] = 'MissionStatus'


if 'Price' not in cols:
    if ' Rocket' in cols:
        renomear[' Rocket'] = 'Price'
    elif 'Rocket' in cols and pd.api.types.is_numeric_dtype(df['Rocket']):
        renomear['Rocket'] = 'Price'

df.rename(columns=renomear, inplace=True)
cols = df.columns.tolist()

# Garante coluna Price
if 'Price' not in cols:
    df['Price'] = np.nan

# Garante coluna MissionStatus
if 'MissionStatus' not in cols:
    cands = [c for c in cols if 'mission' in c.lower() and 'status' in c.lower()]
    if cands:
        df.rename(columns={cands[0]: 'MissionStatus'}, inplace=True)
    else:
        df['MissionStatus'] = 'Unknown'


# Conversões de tipo
df['Date']  = pd.to_datetime(df['Date'], errors='coerce')
df['Year']  = df['Date'].dt.year
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

print(f"\nDataset carregado com sucesso!")
print(f"  Registros totais : {len(df):,}")
print(f"  Colunas          : {list(df.columns)}")
print(f"  Período          : {df['Year'].min()} – {df['Year'].max()}")
print(f"  Missões com custo: {df['Price'].notna().sum():,} registros\n")

# ---------------------------------------------------------------------------
# EXERCÍCIO 02 — TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS
# ---------------------------------------------------------------------------
print("=" * 65)
print("  EXERCÍCIO 02 — TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS")
print("=" * 65)

# ------------------------------------------------------------------ 02a ----
# Variável quantitativa DISCRETA: Número de missões por ano (Year)
# ------------------------------------------------------------------ ------
print("\n[02a] Variável Discreta: Número de missões por ano\n")

missoes_por_ano = df.groupby('Year').size().reset_index(name='fi')
missoes_por_ano = missoes_por_ano.sort_values('Year').reset_index(drop=True)

total = missoes_por_ano['fi'].sum()
missoes_por_ano['fr']   = missoes_por_ano['fi'] / total
missoes_por_ano['fr_%'] = (missoes_por_ano['fr'] * 100).round(2)
missoes_por_ano['Fi']   = missoes_por_ano['fi'].cumsum()
missoes_por_ano['Fr_%'] = (missoes_por_ano['Fi'] / total * 100).round(2)

# Agrupar décadas para exibição compacta
missoes_por_ano['Decada'] = (missoes_por_ano['Year'] // 10) * 10
tab_decadas = missoes_por_ano.groupby('Decada').agg(
    fi=('fi', 'sum')
).reset_index()
tab_decadas['fr']   = tab_decadas['fi'] / total
tab_decadas['fr_%'] = (tab_decadas['fr'] * 100).round(2)
tab_decadas['Fi']   = tab_decadas['fi'].cumsum()
tab_decadas['Fr_%'] = (tab_decadas['Fi'] / total * 100).round(2)
tab_decadas.columns = ['Décadas', 'fi (abs.)', 'fr (rel.)', 'fr% (rel.%)', 'Fi (acum.)', 'Fr% (acum.%)']

print("  Tabela de Frequências por Década (variável discreta: ano de lançamento)")
print(tab_decadas.to_string(index=False))
print(f"\n  Total de missões: {total:,}")

# ------------------------------------------------------------------ 02b ----
# Variável quantitativa CONTÍNUA: Custo da missão em USD milhões (Price)
# ------------------------------------------------------------------ ------
print("\n[02b] Variável Contínua: Custo da missão (USD milhões)\n")

preco_valido = df['Price'].dropna()

# Regra de Sturges: k = 1 + 3,322 * log10(n)
n_preco = len(preco_valido)
k = int(np.ceil(1 + 3.322 * np.log10(n_preco)))
amp_total = preco_valido.max() - preco_valido.min()
h = amp_total / k  # amplitude de cada classe

limites = [preco_valido.min() + i * h for i in range(k + 1)]
labels_classes = [
    f"{limites[i]:.1f} |-- {limites[i+1]:.1f}"
    for i in range(k)
]

fi_cont, _ = np.histogram(preco_valido, bins=limites)
xi_cont    = [(limites[i] + limites[i+1]) / 2 for i in range(k)]
fr_cont    = fi_cont / fi_cont.sum()
Fi_cont    = fi_cont.cumsum()
Fr_cont    = (Fi_cont / fi_cont.sum() * 100).round(2)

tab_continua = pd.DataFrame({
    'Classes (USD mi)' : labels_classes,
    'Ponto médio (xi)' : [round(x, 2) for x in xi_cont],
    'fi (absoluta)'    : fi_cont,
    'fr (relativa)'    : [round(x, 4) for x in fr_cont],
    'fr% (relativa%)'  : [round(x * 100, 2) for x in fr_cont],
    'Fi (acumulada)'   : Fi_cont,
    'Fr% (acum.%)'     : Fr_cont,
})

print("  Tabela de Frequências — Custo das Missões (variável contínua)")
print(f"  n = {n_preco} | k (Sturges) = {k} | h (amplitude) = {h:.2f}")
print(tab_continua.to_string(index=False))

# ---------------------------------------------------------------------------
# EXERCÍCIO 03 — GRÁFICOS ESTATÍSTICOS
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  EXERCÍCIO 03 — GRÁFICOS ESTATÍSTICOS")
print("=" * 65)

# ------------------------------------------------------------------ 03a ----
# Gráfico 1: Série histórica de lançamentos por ano (linha + barra)
# ------------------------------------------------------------------ ------
fig1, ax1 = plt.subplots(figsize=(14, 6))

ax1.bar(
    missoes_por_ano['Year'],
    missoes_por_ano['fi'],
    color=COR_PRINCIPAL,
    alpha=0.7,
    label='Missões por ano',
    zorder=2
)
media_anual = missoes_por_ano['fi'].mean()
ax1.axhline(
    media_anual, color=COR_SECUNDARIA, linewidth=2,
    linestyle='--', label=f'Média anual ({media_anual:.1f})', zorder=3
)

ax1.set_title('Evolução Histórica de Lançamentos Espaciais (1957–2022)',
              fontsize=15, fontweight='bold', pad=15)
ax1.set_xlabel('Ano', fontsize=12, labelpad=8)
ax1.set_ylabel('Número de Missões', fontsize=12, labelpad=8)
ax1.xaxis.set_major_locator(mticker.MultipleLocator(5))
ax1.xaxis.set_minor_locator(mticker.MultipleLocator(1))
plt.xticks(rotation=45, ha='right', fontsize=9)
ax1.legend(fontsize=11)

# Anotações de eventos históricos relevantes
ax1.annotate('Corrida Espacial\n(URSS × EUA)',
             xy=(1965, missoes_por_ano[missoes_por_ano['Year']==1965]['fi'].values[0]),
             xytext=(1972, missoes_por_ano['fi'].max()*0.85),
             arrowprops=dict(arrowstyle='->', color='gray'),
             fontsize=9, color='gray')
ax1.annotate('Era SpaceX\n& comercial',
             xy=(2018, missoes_por_ano[missoes_por_ano['Year']==2018]['fi'].values[0]),
             xytext=(2010, missoes_por_ano['fi'].max()*0.90),
             arrowprops=dict(arrowstyle='->', color='gray'),
             fontsize=9, color='gray')

plt.tight_layout()
plt.savefig('grafico1_lancamentos_por_ano.png', dpi=150, bbox_inches='tight')
print("\n  Gráfico 1 salvo: grafico1_lancamentos_por_ano.png")
plt.show()

# ------------------------------------------------------------------ 03b ----
# Gráfico 2: Distribuição do status das missões (barras horizontais)
# ------------------------------------------------------------------ ------


status_counts = df['MissionStatus'].value_counts()
cores_status = {
    'Success':        COR_TERCIARIA,
    'Failure':        COR_SECUNDARIA,
    'Partial Failure':'#f39c12',
    'Prelaunch Failure':'#8e44ad',
}
cores_lista = [cores_status.get(s, '#95a5a6') for s in status_counts.index]
pct_lista   = (status_counts / status_counts.sum() * 100).round(1)

fig2, ax2 = plt.subplots(figsize=(10, 5))
bars = ax2.barh(
    status_counts.index,
    status_counts.values,
    color=cores_lista,
    edgecolor='white',
    height=0.55,
    zorder=2
)

# Rótulos de valor + percentual nas barras
for bar, val, pct in zip(bars, status_counts.values, pct_lista):
    ax2.text(
        val + status_counts.max() * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f'{val:,}  ({pct}%)',
        va='center', ha='left', fontsize=11, fontweight='500'
    )

ax2.set_title('Distribuição do Status das Missões Espaciais (1957–2022)',
              fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Número de Missões', fontsize=12, labelpad=8)
ax2.set_ylabel('Status da Missão', fontsize=12, labelpad=8)
ax2.set_xlim(0, status_counts.max() * 1.22)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()
plt.savefig('grafico2_status_missoes.png', dpi=150, bbox_inches='tight')
print("  Gráfico 2 salvo: grafico2_status_missoes.png")
plt.show()

# ---------------------------------------------------------------------------
# EXERCÍCIO 04 — ANÁLISE UNIVARIADA (ESTATÍSTICA DESCRITIVA)
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  EXERCÍCIO 04 — ANÁLISE UNIVARIADA — ESTATÍSTICA DESCRITIVA")
print("=" * 65)

def analise_univariada(serie, nome_variavel, unidade=''):
    """Calcula e exibe todas as medidas descritivas solicitadas."""
    s = serie.dropna()
    n = len(s)

    # (a) Medidas de Tendência Central
    media    = s.mean()
    mediana  = s.median()
    try:
        moda_val = stats.mode(s, keepdims=True).mode[0]
        moda_cnt = stats.mode(s, keepdims=True).count[0]
    except Exception:
        moda_val = s.mode().iloc[0]
        moda_cnt = (s == moda_val).sum()

    # (b) Medidas de Dispersão
    maximo    = s.max()
    minimo    = s.min()
    amplitude = maximo - minimo
    variancia = s.var(ddof=1)
    desvio    = s.std(ddof=1)
    cv        = (desvio / media * 100) if media != 0 else np.nan

    # (c) Separatrizes — Quartis
    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)
    q3 = s.quantile(0.75)
    iqr = q3 - q1

    print(f"\n{'─'*55}")
    print(f"  Variável: {nome_variavel}  |  n = {n:,}  {unidade}")
    print(f"{'─'*55}")
    print("  [a] Medidas de Tendência Central")
    print(f"      Média    : {media:>12.4f} {unidade}")
    print(f"      Mediana  : {mediana:>12.4f} {unidade}")
    print(f"      Moda     : {moda_val:>12.4f} {unidade}  (aparece {moda_cnt}x)")
    print("  [b] Medidas de Dispersão")
    print(f"      Máximo   : {maximo:>12.4f} {unidade}")
    print(f"      Mínimo   : {minimo:>12.4f} {unidade}")
    print(f"      Amplitude: {amplitude:>12.4f} {unidade}")
    print(f"      Variância: {variancia:>12.4f}")
    print(f"      Desv. Pad: {desvio:>12.4f} {unidade}")
    print(f"      CV       : {cv:>11.2f}%")
    print("  [c] Separatrizes — Quartis")
    print(f"      Q1 (25%) : {q1:>12.4f} {unidade}")
    print(f"      Q2 (50%) : {q2:>12.4f} {unidade}  (= Mediana)")
    print(f"      Q3 (75%) : {q3:>12.4f} {unidade}")
    print(f"      IQR      : {iqr:>12.4f} {unidade}")
    print(f"{'─'*55}")

    return {
        'serie': s, 'media': media, 'mediana': mediana,
        'moda': moda_val, 'q1': q1, 'q2': q2, 'q3': q3,
        'desvio': desvio, 'cv': cv, 'nome': nome_variavel
    }

# Análise 1 — Custo das missões (USD milhões) — VARIÁVEL CONTÍNUA
res_preco = analise_univariada(
    df['Price'], 'Custo da Missão', unidade='(USD mi)'
)

# Análise 2 — Missões por ano — VARIÁVEL DISCRETA
res_ano = analise_univariada(
    missoes_por_ano.set_index('Year')['fi'],
    'Missões por Ano', unidade='(lançamentos)'
)

# ---------------------------------------------------------------------------
# BOXPLOTS DAS DUAS VARIÁVEIS ANALISADAS
# ---------------------------------------------------------------------------
fig3, axes = plt.subplots(1, 2, figsize=(13, 6))

for ax, res, cor in zip(axes, [res_preco, res_ano], [COR_PRINCIPAL, COR_SECUNDARIA]):
    bp = ax.boxplot(
        res['serie'], vert=True, patch_artist=True,
        boxprops=dict(facecolor=cor, alpha=0.55, linewidth=1.5),
        medianprops=dict(color='black', linewidth=2.5),
        whiskerprops=dict(linewidth=1.5),
        capprops=dict(linewidth=2),
        flierprops=dict(marker='o', markersize=4, alpha=0.4,
                        markerfacecolor=cor, markeredgewidth=0)
    )
    ax.axhline(res['media'], color='red', linestyle='--',
               linewidth=1.5, label=f"Média: {res['media']:.2f}")
    ax.set_title(f"Boxplot — {res['nome']}", fontsize=13, fontweight='bold')
    ax.set_ylabel(res['nome'], fontsize=11)
    ax.set_xticks([])
    ax.legend(fontsize=10)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{x:,.1f}')
    )

fig3.suptitle('Análise Univariada — Distribuição das Variáveis (Boxplot)',
              fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('grafico3_boxplots.png', dpi=150, bbox_inches='tight')
print("\n  Boxplots salvos: grafico3_boxplots.png")
plt.show()

# ---------------------------------------------------------------------------
# HISTOGRAMAS COM CURVA DE DENSIDADE
# ---------------------------------------------------------------------------
fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5))

for ax, res, cor in zip(axes4, [res_preco, res_ano], [COR_PRINCIPAL, COR_SECUNDARIA]):
    s = res['serie']
    ax.hist(s, bins='auto', color=cor, alpha=0.65,
            edgecolor='white', linewidth=0.6, density=True, zorder=2)
    xmin, xmax = s.min(), s.max()
    xs = np.linspace(xmin, xmax, 300)
    kde = stats.gaussian_kde(s)
    ax.plot(xs, kde(xs), color='black', linewidth=2, label='Densidade (KDE)')
    ax.axvline(res['media'],   color='red',    linestyle='--', linewidth=1.8,
               label=f"Média {res['media']:.1f}")
    ax.axvline(res['mediana'], color='orange', linestyle=':',  linewidth=1.8,
               label=f"Mediana {res['mediana']:.1f}")
    ax.set_title(f"Histograma — {res['nome']}", fontsize=13, fontweight='bold')
    ax.set_xlabel(res['nome'], fontsize=11, labelpad=8)
    ax.set_ylabel('Densidade', fontsize=11, labelpad=8)
    ax.legend(fontsize=9)

fig4.suptitle('Distribuição de Frequências com Curva de Densidade',
              fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('grafico4_histogramas.png', dpi=150, bbox_inches='tight')
print("  Histogramas salvos: grafico4_histogramas.png")
plt.show()

# ---------------------------------------------------------------------------
# ENCERRAMENTO - CONCLUSÃO DE ARQUIVOS
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("  EXECUÇÃO CONCLUÍDA COM SUCESSO")
print("  Arquivos gerados:")
print("    grafico1_lancamentos_por_ano.png")
print("    grafico2_status_missoes.png")
print("    grafico3_boxplots.png")
print("    grafico4_histogramas.png")
print("=" * 65)
