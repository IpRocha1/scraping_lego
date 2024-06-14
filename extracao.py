import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load JSON data from files
with open('legos_amazon_brasil.json', 'r', encoding='utf-8') as f:
    amazon_brasil_data = json.load(f)

with open('legos_bricklink.json', 'r', encoding='utf-8') as f:
    bricklink_data = json.load(f)

with open('legos_lego_store_brasil.json', 'r', encoding='utf-8') as f:
    lego_store_brasil_data = json.load(f)

# Convert JSON data to DataFrames
df_amazon_brasil = pd.DataFrame(amazon_brasil_data)
df_bricklink = pd.DataFrame(bricklink_data)
df_lego_store_brasil = pd.DataFrame(lego_store_brasil_data)

# Add a source column to each DataFrame
df_amazon_brasil['Loja'] = 'Amazon Brasil'
df_bricklink['Loja'] = 'Bricklink'
df_lego_store_brasil['Loja'] = 'Lego Store Brasil'



# Concatenate DataFrames into a single DataFrame
df_all = pd.concat([df_amazon_brasil, df_bricklink, df_lego_store_brasil])

# Display basic information about the combined DataFrame
df_all.info(), df_all.head()

# 1. Gráfico de Barras: Preço Médio por Loja
preco_medio_por_loja = df_all.groupby('Loja')['Preco'].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x=preco_medio_por_loja.index, y=preco_medio_por_loja.values)
plt.title('Preço Médio por Loja')
plt.xlabel('Loja')
plt.ylabel('Preço Médio (R$)')
plt.xticks(rotation=45)
plt.show()

# 2. Gráfico de Pizza: Distribuição de Produtos por Loja
distribuicao_por_loja = df_all['Loja'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(distribuicao_por_loja, labels=distribuicao_por_loja.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Produtos por Loja')
plt.show()

# 3. Histograma: Variação de Preços
plt.figure(figsize=(10, 6))
sns.histplot(df_all['Preco'].dropna(), kde=True)
plt.title('Variação de Preços dos Produtos Lego')
plt.xlabel('Preço (R$)')
plt.ylabel('Frequência')
plt.show()

# 4. Estatísticas Descritivas: Preços
estatisticas_descritivas = df_all.groupby('Loja')['Preco'].describe()
print(estatisticas_descritivas)

# Verificar duplicatas
print("Duplicatas antes da remoção:")
print(df_all.duplicated().sum())

# Remover duplicatas
df_all = df_all.drop_duplicates()

print("Duplicatas após a remoção:")
print(df_all.duplicated().sum())