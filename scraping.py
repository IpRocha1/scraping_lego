import requests
from bs4 import BeautifulSoup
import json

# Busca no site da Lego Store Brasil
def buscar_legos_lego_store_brasil():
    url = "https://www.legostore.com.br/"
    response = requests.get(url)
    site = BeautifulSoup(response.content, "html.parser")

    # print(site)
    
    # Lista para armazenar os resultados
    resultados = []
    
    # Encontrar todos os elementos que contêm informações sobre os Legos
    legos = site.findAll("legobrasil")

    print(legos)
    
    # Examinar cada lego e extrair informações relevantes
    for lego in legos:
        nome = lego.find("h1", {"class": "legobrasil-custom-components-0-x-productNameCustom legobrasil-custom-components-0-x-productNameCustom--productDetail"})
        id_lego = lego.find("span", {"class": "legobrasil-product-0-x-specificationsProductItemTitle"})
        preco = lego.find("span", {"class": "vtex-product-price-1-x-currencyInteger"})
        if nome and preco:
            resultado = {
                "Nome": nome.text.strip(),
                "ID": id_lego.text.strip(),
                "Preço": preco.text.strip()
            }
            resultados.append(resultado)
    
    # Escrever os resultados no JSON
    with open("legos_lego_store_brasil.json", "w", encoding="utf-8") as arquivo_json:
        json.dump(resultados, arquivo_json, ensure_ascii=False, indent=4)

buscar_legos_lego_store_brasil()
