import requests
from bs4 import BeautifulSoup
import json
import math

# Busca no site da Lego Store Brasil
def scraping_lego_store_brasil():
    # url = "https://www.legostore.com.br/temas/"

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/123.0.0.0 Safari/537.36'}

    # response = requests.get(url, headers=headers)
    # site = BeautifulSoup(response.content, "html.parser")
    
    # json_script = site.find_all('template', {"data-varname":"__STATE__", "script":""})
    # print((json_script))
    
    # Quantidade de itens
    qtd_itens = 1342
    
    ultima_pagina = math.ceil(int(qtd_itens)/48)
    
    for i in range(1, ultima_pagina + 1):
        url_pag = f'https://www.legostore.com.br/temas/?page={i}'
        response = requests.get(url_pag, headers=headers)
        site = BeautifulSoup(response.content, "html.parser")
    
        # Captura do json na página
        script = site.find_all('script')[13].text.strip()
        
        # Leitura do json
        data = json.loads(script)
    
        # Salvar o json
        with open(f".\\json_lego_store\\{i}.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(data, arquivo_json, ensure_ascii=False, indent=4)
        
scraping_lego_store_brasil()   
    