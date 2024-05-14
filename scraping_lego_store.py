import requests
from bs4 import BeautifulSoup
import json
import math
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Busca no site da Lego Store Brasil
def scraping_lego_store_brasil():
    url = "https://www.legostore.com.br/temas/"

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/123.0.0.0 Safari/537.36'}

    # Simulador de browser
    service = Service(ChromeDriverManager().install())
        
    chrome = webdriver.ChromeOptions()
    chrome.add_argument('--headless')
    chrome.add_argument('--no-sandbox')
    chrome.add_argument('--disable-dev-shm-usage')
    
    browser = webdriver.Chrome(service=service, options=chrome)
    browser.get(url)

    site = BeautifulSoup(browser.page_source, "html.parser")
    
    # Quantidade de itens
    qtd_itens = site.find('div', class_=re.compile("vtex-search-result-3-x-totalProducts-")).text.strip()
    print((qtd_itens))
    
    ultima_pagina = math.ceil(int(qtd_itens[:-9])/48)

    browser.quit()
    time.sleep(10)
    
    for i in range(1, ultima_pagina + 1):
        url_pag = f'https://www.legostore.com.br/temas/?page={i}'
        response = requests.get(url_pag, headers=headers)
        site = BeautifulSoup(response.content, "html.parser")
    
        # Captura do json na página
        script = site.find_all('script')[13].text.strip()
        print(script)

        # Leitura do json
        data = json.loads(script)
    
        # Salvar o json
        with open(f".\\json_lego_store\\{i}.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(data, arquivo_json, ensure_ascii=False, indent=4)
    
scraping_lego_store_brasil()   
    