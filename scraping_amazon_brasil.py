from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import math
import re
import time

class AmazonBrasil:
    
    def __init__(self):
        self.legos = []
        
    # Busca no site da Amazon Brasil
    def scraping_amazon_brasil(self):
        url = "https://www.amazon.com.br/s?k=lego&i=toys&rh=n%3A16194299011%2Cp_89%3ALEGO"
        
        # Simulador de browser
        service = Service(ChromeDriverManager().install())
        
        chrome = webdriver.ChromeOptions()
        chrome.add_argument('--headless')
        chrome.add_argument('--no-sandbox')
        chrome.add_argument('--disable-dev-shm-usage')
        
        
        browser = webdriver.Chrome(service=service, options=chrome)
        browser.get(url)
        
        site = BeautifulSoup(browser.page_source, "html.parser")
        time.sleep(10)

        qtdItens = site.find('div', class_='a-section a-spacing-small a-spacing-top-small').text.strip()
        

        # Encontrar a posicao
        inicioQtd = qtdItens.find('mais de ')
        fimQtd = qtdItens.find(' resultados')

        qtdItens = int((qtdItens[inicioQtd + len("mais de "):fimQtd].strip()).replace('.',''))

        ultima_pagina = math.ceil((qtdItens)/24)
        
        for i in range(1, ultima_pagina + 1):
            url = f"https://www.amazon.com.br/s?k=lego&i=toys&rh=n%3A16194299011%2Cp_89%3ALEGO&page={i}"
            
            browser.get(url)
            site = BeautifulSoup(browser.page_source, "html.parser")
            
            # Encontrar os produtos 
            produtos = site.findAll('div', class_=re.compile('s-result-item s-asin'))
            
            # Padrao de regex para extrair os dados
            padrao = r'LEGO ([\w\s]+?) (\d+) (.+?) (\d+) peças'
            padrao2 = r'LEGO\s([\w\s]+?)\s(\d+)\s(\d+)\speças'
            padrao3 = r'LEGO ([\w\s]+) (\d+)'
            padrao_id_inicio = r'(\d+) LEGO ([\w\s,]+?) (\d+) peças?'
                    
            for produto in produtos:
                if len(self.legos) >= qtdItens:
                    break
                
                # Extrair informacoes do produto
                info = produto.find('span', class_=re.compile('a-text-normal')).get_text().strip()
                info = info.replace('ǀ ', '').replace(';', '').replace(' ─', '').replace('®','').replace('(','').replace(')','').replace(' Conjunto de Construção', '').replace(' Kit Incrível', '').replace('Peças', 'peças').replace('“', '').replace('”', '').replace('- ', '').replace('™', '').replace(' Kit de Construção', '').replace(':', '').replace(' Brinquedo de Construção', '').replace(' Conjuntos de Construção', '').replace(' Kit de Construção para Adultos', '').replace('-', ' ').replace('.', '').replace('Brinquedo de Construção ', '').replace('Kit de construção de carro de brincar modelo colecionável para crianças a partir dos 8 anos ', '').replace('’', '').replace('Kit de Construção ', '').replace(',', '').replace('–', '').replace('‎', '').replace('Lego', 'LEGO')
                
                # Extrair informacoes do preco
                try:
                    preco_r = produto.find('span', class_=re.compile('a-offscreen')).get_text().strip()
                    preco = float(preco_r.replace('R$', '').replace('.', '').replace(',', '.').strip())
                except AttributeError:
                    preco = None
                except ValueError:
                    preco = None
                # print(info, preco)
                
                resultado = re.match(padrao, info)
                resultado2 = re.match(padrao2, info)
                resultado3 = re.match(padrao3, info)
                resultado_id_inicio = re.match(padrao_id_inicio, info)
                # print(resultado, resultado_id_inicio)

                if resultado:
                    nome = 'Lego ' + resultado.group(1) + ' ' + resultado.group(3)
                    id_produto = resultado.group(2)
                    quantidade_pecas = resultado.group(4)
                    # print(nome)
                
                elif resultado2:
                    nome = 'Lego ' + resultado2.group(1)
                    id_produto = resultado2.group(2)
                    quantidade_pecas = resultado2.group(3)
                
                elif resultado_id_inicio:
                    nome = 'Lego ' + resultado_id_inicio.group(2)
                    id_produto = resultado_id_inicio.group(1)
                    quantidade_pecas = resultado_id_inicio.group(3)
                    # print(nome)
                
                elif resultado3:
                    nome = 'Lego ' + resultado3.group(1)
                    id_produto = resultado3.group(2)
                    quantidade_pecas = None
                    # print(nome)
                    
                else:
                    nome = info
                    id_produto = None
                    quantidade_pecas = None
                    # print(nome)
                
                lego = {
                    "Vendedor": 'Amazon Brasil',
                    "Nome": nome,
                    "ID": id_produto,
                    "Num Pecas": quantidade_pecas,
                    "Preco": preco,
                    "URL": url
                }
                
                self.legos.append(lego)
        
            # Simular rolagem da pagina
            time.sleep(10)
        
        browser.quit()
        
        print(len(self.legos))
        # Escrever os resultados no JSON
        with open("legos_amazon_brasil.json", "w", encoding="utf-8") as arquivo_json:
            json.dump(self.legos, arquivo_json, ensure_ascii=False, indent=4)

captura = AmazonBrasil()
captura.scraping_amazon_brasil()