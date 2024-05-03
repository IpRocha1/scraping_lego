import os
import json
import re

class legoStore:
    
    def __init__(self):
        self.resultados = []

    def captura_produtos(self):
        
        # Listar os arquivos JSON
        arquivos = [arq for arq in os.listdir('./json_lego_store') if arq.lower().endswith('.json')]
               
        for arquivo in arquivos:
            
            # Armazenar os IDs de cada produto do JSON
            id_produtos = []
            
            # Abrir arquivo e ler o seu conteudo
            with open(f'.\json_lego_store\\{arquivo}', "r", encoding="utf-8") as f:
                data = json.load(f)
            
            padrao = re.compile(r'Product:sp-(\d+).properties.0')
            
            # Gerar a lista de IDs dos produtos
            for chave, valor in data.items():
                match = padrao.search(chave)
                if match:
                    numero_produto = match.group(1)
                    id_produtos.append(numero_produto)
        
            for id in id_produtos:
                
                #Tratando a excecao que nem todos os produtos possuem informacao da quantidade de pecas
                try:
                    num_pecas = data['Product:sp-'+id+'.properties.1']['values']['json'][0]
                except KeyError:
                    num_pecas = None
                    
                resultado = {
                    "Nome": data['Product:sp-'+id+'.items({\"filter\":\"ALL\"}).0']['nameComplete'],
                    "ID": data['Product:sp-'+id+'.items({\"filter\":\"ALL\"}).0']['complementName'],
                    "Num Pecas": num_pecas,
                    "Preço": data['$Product:sp-'+id+'.priceRange.sellingPrice']['lowPrice']
                }
                self.resultados.append(resultado)     
    
        print(len(self.resultados))
         # Escrever os resultados no JSON
        with open("legos_lego_store_brasil.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(self.resultados, arquivo_json, ensure_ascii=False, indent=4)

        
captura = legoStore()
captura.captura_produtos()    