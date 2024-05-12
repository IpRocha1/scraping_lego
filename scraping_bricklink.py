from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import math
import re
import urllib.parse

class BrickLink:
    
    def __init__(self):
        self.legos = []
    
    def scraping_brick_link(self):
        url = "https://www.bricklink.com/catalogList.asp?pg=1&catLike=W&sortBy=N&sortAsc=A&sz=50&catType=S"
        
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
        info_qtd_itens = site.find('div', {'class':'catalog-list__pagination--top l-clear-left', 'b':''}).text.strip()
        
        # Padrao de regex para extrair o número de itens
        padrao = r'(\d+) Items Found'
        
        # Procurar por correspondências no texto
        correspondencia = re.search(padrao, info_qtd_itens)
        
        # Extrair o número de itens da pagina
        if correspondencia:
            qtd_itens = correspondencia.group(1)
        
        # Calculo da ultima pagina
        ultima_pagina = math.ceil(int(qtd_itens)/50)
        
        # Percorrer cada pagina na busca de itens
        for i in range(1, ultima_pagina + 1):
            print('pagina', i)
            url_pag = f'https://www.bricklink.com/catalogList.asp?pg={i}&catLike=W&sortBy=N&sortAsc=A&sz=50&catType=S'
           
            browser.get(url_pag)
            site = BeautifulSoup(browser.page_source, "html.parser")
            
            # Captura dos numeros de IDs
            captura_ids = site.find_all(lambda tag: tag.name == 'a' and "/v2/catalog/catalogitem.page?" in tag.get('href', ''))
            
            for captura_id in captura_ids:
                num_id = captura_id.text.strip()
                
                # print('------------------------------------------')
                # print('id: ',num_id)
                
                # URL base
                url_base = f'https://www.bricklink.com/v2/catalog/catalogitem.page?S={num_id}#T=S&'
                
                # Parametros da URL
                param = {"O": '{"ss":"BR","cond":"N","loc":"BR","ca":"26","iconly":0}'}
                
                # Codificacao do parametro
                encoded_params = urllib.parse.urlencode(param)
                
                # Construicao da URL completa
                url_id = f"{url_base}{encoded_params}"
                # print(url_id)
                
                browser.get(url_id)
                site_id = BeautifulSoup(browser.page_source, "html.parser")                
                
                captura_info_produto = site_id.find_all('tr', class_=re.compile('pciItemContents'))

                # print('Quantidade de produtos:',len(captura_info_produto))
                
                # qtd_produtos_captura = site_id.find('div', id_ =re.compile('_idStoreResultListSection'))
                
                # # qtd_produtos = qtd_produtos_captura[:-6]
                # print(qtd_produtos_captura)
                
                if len(captura_info_produto) > 0:
                    num_peca_r = site_id.find_all('a', class_='links')
                    num_peca = num_peca_r[1].text.strip()
                    
                    for info_produto in captura_info_produto:
                        vendedor = info_produto.find('span', {'class':'pspStoreName'}).text.strip()
                        nome = info_produto.find('a', {'class':'pciItemNameLink'}).text.strip()
                        preco_r = info_produto.find('td', {'style':'text-align: right;'}).text.strip()
                        # print(vendedor)
                        
                        # Encontrar a posicao do primeiro "BRL" e do "("
                        inicioPpreco = preco_r.find('BRL')
                        fimPpreco = preco_r.find('(')
                        
                        # Extrair a substring entre "BRL" e "("
                        preco_id = preco_r[inicioPpreco + len("BRL"):fimPpreco].strip()
                        try:
                            preco = float(preco_id)
                        except ValueError:
                            preco = None
                        
                        # print(num_id[:-2], num_peca[:-6], vendedor, nome, preco)
                        
                        if vendedor != '[%strStorename%]':
                            lego = {
                                "Vendedor": vendedor,
                                "Nome": nome,
                                "ID": num_id,
                                "Num Pecas": num_peca[:-6],
                                "Preco": preco
                            }
                            self.legos.append(lego)
                
        browser.quit()
        
        print(len(self.legos))
        # Escrever os resultados no JSON
        with open("legos_bricklink.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(self.legos, arquivo_json, ensure_ascii=False, indent=4)

captura = BrickLink()
captura.scraping_brick_link()