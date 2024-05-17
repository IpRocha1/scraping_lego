import tkinter as tk
from tkinter import messagebox
import json

# Função para carregar dados de um arquivo JSON
def carregar_dados(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

# Função para encontrar o produto com o menor preço para um ID específico
def encontrar_menor_preco_por_id(dados, id_produto):
    menor_preco = float('inf')  # inicializar com um valor muito grande
    produto_menor_preco = None
    
    for produto in dados:
        if produto['ID'] == id_produto and produto['Preco'] < menor_preco:
            menor_preco = produto['Preco']
            produto_menor_preco = produto
    
    return produto_menor_preco

# Função para lidar com a pesquisa do produto
def pesquisar_produto():
    id_produto = entry_id.get()
    
    if not id_produto:
        messagebox.showerror("Erro", "Por favor, insira um ID de produto válido.")
        return
    
    try:
        id_produto = int(id_produto)
    except ValueError:
        messagebox.showerror("Erro", "O ID do produto deve ser um número inteiro.")
        return
    
    produto_encontrado = None
    
    # Procurar o produto com o menor preço para o ID fornecido em cada arquivo
    for nome_arquivo in arquivos_json:
        dados_arquivo = carregar_dados(nome_arquivo)
        produto = encontrar_menor_preco_por_id(dados_arquivo, id_produto)
        if produto and (not produto_encontrado or produto['Preco'] < produto_encontrado['Preco']):
            produto_encontrado = produto
    
    if produto_encontrado:
        messagebox.showinfo("Produto Encontrado", f"Nome: {produto_encontrado['Nome']}\n"
                                                  f"ID: {produto_encontrado['ID']}\n"
                                                  f"Loja: {produto_encontrado['Vendedor']}\n"
                                                  f"Preço: {produto_encontrado['Preco']}")
    else:
        messagebox.showinfo("Produto Não Encontrado", f"Não foi encontrado nenhum produto com o ID {id_produto}.")

# Arquivos JSON
arquivos_json = ['.\\legos_lego_store_brasil.json','.\\legos_amazon_brasil.json', '.\\legos_bricklink.json']

# Criar a janela principal
root = tk.Tk()
root.title("Pesquisa de Produtos")

# Criar os widgets da interface
label_id = tk.Label(root, text="ID do Produto:")
label_id.pack()

entry_id = tk.Entry(root)
entry_id.pack()

btn_pesquisar = tk.Button(root, text="Pesquisar", command=pesquisar_produto)
btn_pesquisar.pack()

# Executar o loop principal da interface
root.mainloop()