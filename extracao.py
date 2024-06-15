import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leitura dos JSON
with open('produto_menor_preco.json', 'r', encoding='utf-8') as f:
    menor_preco_data = json.load(f)

# Convertendo JSON para DataFrames
df_menor_preco = pd.DataFrame(menor_preco_data)

# Remover caracteres indesejados e converter para tipo numérico
def clean_and_convert(df, price_col, pieces_col):
    df[price_col] = df[price_col].replace('[\$,]', '', regex=True).astype(float)
    df[pieces_col] = pd.to_numeric(df[pieces_col], errors='coerce')
    return df

df_menor_preco = clean_and_convert(df_menor_preco, 'Preco', 'Num Pecas')

# Garantir que os indices sejam unicos
df_all = df_menor_preco.reset_index(drop=True)

# Definindo as cores
color = [(0.99, 0.64, 0.13, 1.0),(0.83, 0.42, 0.23, 1.0), (0.86, 0.28, 0.39, 1.0)]

# 1. Grafico de Barras: Preço Medio por Loja
preco_medio_por_loja = df_all.groupby('Loja')['Preco'].mean()
plt.figure(figsize=(10, 6))
plt.grid(axis = 'y', linestyle = '--')
plt.bar(preco_medio_por_loja.index, preco_medio_por_loja.values, color=color)
plt.title('Preço Médio por Loja')
plt.xlabel('Loja')
plt.ylabel('Preço Médio (R$)')

# 2. Grafico de Pizza: Distribuicao de Produtos por Loja
distribuicao_por_loja = df_all['Loja'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(distribuicao_por_loja, labels=distribuicao_por_loja.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Produtos por Loja')

# 3. Histogramas
plt.figure(figsize=(14, 6))
# Histograma de Preços
plt.subplot(1, 2, 1)
plt.grid(axis = 'y', linestyle = '--')
sns.histplot(df_all['Preco'].dropna(), kde=True)
plt.title('Distribuição de Preços')
plt.xlabel('Preço (R$)')
plt.ylabel('Frequência')

# Histograma de Numero de Peças
plt.subplot(1, 2, 2)
plt.grid(axis = 'y', linestyle = '--')
sns.histplot(df_all['Num Pecas'].dropna(), kde=True)
plt.title('Distribuição de Número de Peças')
plt.xlabel('Número de Peças')
plt.ylabel('Frequência')

plt.tight_layout()

# 4. Grafico com o Preco Minimo e Maximo
# Calcular a media, minimo e maximo dos preços por loja
price_stats_by_store = df_all.groupby('Loja')['Preco'].agg(['mean', 'min', 'max']).reset_index()

# Plotar o preço minimo e maximo por loja
plt.figure(figsize=(10, 6))
plt.grid(axis = 'y', linestyle = '--')
sns.lineplot(data=price_stats_by_store, x='Loja', y='min', label='Mínimo', marker='o')
sns.lineplot(data=price_stats_by_store, x='Loja', y='max', label='Máximo', marker='o')
plt.title('Preço Mínimo e Máximo por Loja')
plt.xlabel('Loja')
plt.ylabel('Preço (R$)')
plt.legend()

# 5. Grafico Preço vs Numero de Peças
plt.figure(figsize=(8, 6))
plt.grid(axis = 'y', linestyle = '--')
sns.scatterplot(data=df_all, x='Num Pecas', y='Preco')
plt.title('Relação entre Preço e Número de Peças')
plt.xlabel('Número de Peças ')
plt.ylabel('Preço (R$) ')

# 6. Boxplot dos preços por loja
plt.figure(figsize=(10, 6))
plt.grid(axis = 'y', linestyle = '--')
sns.boxplot(data=df_all, x='Loja', y='Preco')
plt.title('Distribuição dos Preços por Loja')
plt.xlabel('Loja')
plt.ylabel('Preço (R$)')
# plt.xticks(rotation=45)

# 7. Estatisticas Descritivas
# Precos
estatisticas_descritivas = df_all.groupby('Loja')[['Preco', 'Num Pecas']].describe()
print(estatisticas_descritivas)

# Apresentar os graficos na tela
plt.show()