import json

# Arquivos JSON
arquivo1 = '.\\legos_lego_store_brasil.json'
arquivo2 = '.\\legos_amazon_brasil.json'
arquivo3 = '.\\legos_bricklink.json'

# Funcao para carregar dados de um arquivo JSON
def carregar_dados(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

# Carregar os dados dos arquivos
dados_arquivo1 = carregar_dados(arquivo1)
dados_arquivo2 = carregar_dados(arquivo2)
dados_arquivo3 = carregar_dados(arquivo3)

# Funcao para comparar os precos dos produtos com o mesmo ID e retornar o produto com o menor preco
def encontrar_produto_menor_preco(produtos):
    menor_preco = float('inf')
    produto_menor_preco = None
    
    for produto in produtos:
        if produto['Preco'] < menor_preco:
            menor_preco = produto['Preco']
            produto_menor_preco = produto
    
    return produto_menor_preco

# Dicionario para armazenar o produto com o menor preço para cada ID
menor_preco_por_id = {}

# Percorrer os produtos de cada arquivo e encontrar o produto com o menor preço para cada ID
for dados in [dados_arquivo1, dados_arquivo2, dados_arquivo3]:
    for produto in dados:
        id_produto = produto.get('ID')  # Use .get() para acessar o valor do campo 'ID'
        preco_produto = produto.get('Preco')  # Use .get() para acessar o valor do campo 'Preco'
        
        if id_produto is not None:  # Verifica se o campo 'ID' existe
            if id_produto not in menor_preco_por_id:
                menor_preco_por_id[id_produto] = produto
            elif preco_produto is not None:
                preco_anterior = menor_preco_por_id[id_produto].get('Preco')
                if preco_anterior is not None and preco_produto < preco_anterior:
                    menor_preco_por_id[id_produto] = produto

# Imprimir os produtos com menor preço para cada ID
for id_produto, produto_menor_preco in menor_preco_por_id.items():
    print(f"ID: {id_produto}")
    print(f"Produto com menor preço: {produto_menor_preco['Nome']}")
    print(f"Preço: {produto_menor_preco['Preco']}")
    print("-" * 30)