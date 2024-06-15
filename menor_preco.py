import json

# Carregar os arquivos JSON
with open('legos_amazon_brasil.json', 'r', encoding='utf-8') as f:
    amazon_brasil_data = json.load(f)

with open('legos_lego_store_brasil.json', 'r', encoding='utf-8') as f:
    lego_store_brasil_data = json.load(f)
    
with open('legos_bricklink.json', 'r', encoding='utf-8') as f:
    bricklink_data = json.load(f)

# Funcao para extrair a primeira parte do ID
def extrair_id_basico(produto_id):
    if produto_id:
        partes = produto_id.split('-')
        id_basico = partes[0]
        return id_basico
    else:
        return None

# Funcao para atualizar "Num Pecas" se estiver faltando
def atualizar_num_pecas(menor_produto, novo_produto):
    if menor_produto.get('Num Pecas') is None and novo_produto.get('Num Pecas') is not None:
        menor_produto['Num Pecas'] = novo_produto['Num Pecas']
    return menor_produto

# Criar um dicionario para armazenar o produto com menor preço para cada ID
menor_preco_dict = {}

# Funcao para processar produtos de uma lista de dados
def processar_produtos(data, valor):
    for produto in data:
        produto.update({'Loja': valor})
        produto_id = extrair_id_basico(produto.get('ID'))
        if len(str(produto_id)) > 3:
            preco = produto.get('Preco')
            if produto_id is not None and preco is not None:
                if produto_id not in menor_preco_dict:
                    menor_preco_dict[produto_id] = produto
                else:
                    if preco < menor_preco_dict[produto_id]['Preco']:
                        menor_preco_dict[produto_id] = atualizar_num_pecas(produto, menor_preco_dict[produto_id])
                    else:
                        menor_preco_dict[produto_id] = atualizar_num_pecas(menor_preco_dict[produto_id], produto)

# Processar os produtos de cada fonte de dados
processar_produtos(amazon_brasil_data, 'Amazon Brasil')
processar_produtos(lego_store_brasil_data, 'Lego Store Brasil')
processar_produtos(bricklink_data, 'Bricklink')

# Converter o dicionário em uma lista para salvar em JSON
menor_preco_list = list(menor_preco_dict.values())

# Salvar o resultado em um novo arquivo JSON
with open('produto_menor_preco.json', 'w', encoding='utf-8') as f:
    json.dump(menor_preco_list, f, ensure_ascii=False, indent=4)