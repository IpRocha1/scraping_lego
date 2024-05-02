import requests
from bs4 import BeautifulSoup
import json
import re

# Busca no site da Lego Store Brasil
def buscar_legos_lego_store_brasil():
    url = "https://www.legostore.com.br/temas/"

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/123.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    site = BeautifulSoup(response.content, "html.parser")
  
    # Lista para armazenar os resultados
    resultados = []

    script = site.find_all('script')[13].text.strip()
    # json_script = site.findAll('template', {"data-varname":"__STATE__"})
    # print(script)

    data = json.loads(script)

    padrao = re.compile(r'Product:sp-(\d+).properties.0')
    
    # priceRange.sellingPrice" - preço 'lowPrice'
    # specificationGroups.2.specifications.3 - Cod Lego - properties.12
    # specificationGroups.4.specifications.1 - num de peças - properties.1
    # "Product:sp-2015241.items({\"filter\":\"ALL\"}).0"
    
    id_produto = []

    for chave, valor in data.items():
        match = padrao.search(chave)
        if match:
            numero_produto = match.group(1)
            id_produto.append(numero_produto)
    
    # print(id_produto)
    
    print(data['Product:sp-'+id_produto[0]+'.items({\"filter\":\"ALL\"}).0']['nameComplete']) 
    print(data['Product:sp-'+id_produto[0]+'.items({\"filter\":\"ALL\"}).0']['complementName']) 
    print(data['Product:sp-'+id_produto[0]+'.specificationGroups.4.specifications.1']['values']['json'])
    print(data['$Product:sp-'+id_produto[0]+'.priceRange.sellingPrice']['lowPrice']) 
         
            
    # for chave, valor in data.items():
    #     match = padrao.search(chave)
    #     if match:
    #         numero_produto = match.group(1)
    #         nome_produto = valor['name']
    #         print(numero_produto)
    #         # print(nome_produto)

    # with open ("teste4.txt", "w") as arquivo:
    #     arquivo.write((script))
    
    # Encontrar todos os elementos que contêm informações sobre os Legos
    legos = site.findAll('template', class_= re.compile("vtex-product-summary"))

    # print(len(legos))
    # print((legos[0]))
    
    # Examinar cada lego e extrair informações relevantes
    for lego in legos:
        # print(lego)
        nome = lego.find('h3', class_=re.compile('detailsProductSummary')) #.get_text().strip()
        id_lego = lego.find("span", {"class": "legobrasil-product-0-x-specificationsProductItemTitle"})
        preco = lego.find("span", {"class": "vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--summary"})
        if nome and preco:
            resultado = {
                "Nome": nome.text.strip(),
                "ID": id_lego.text.strip(),
                "Preço": preco.text.strip()
            }
            resultados.append(resultado)
        # print(nome)
        # print(preco)
    
    # Escrever os resultados no JSON
    with open("legos_lego_store_brasil.json", "w", encoding="utf-8") as arquivo_json:
        json.dump(resultados, arquivo_json, ensure_ascii=False, indent=4)

buscar_legos_lego_store_brasil()
