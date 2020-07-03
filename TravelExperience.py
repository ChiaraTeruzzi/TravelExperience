#!/usr/bin/env python
# coding: utf-8

# # Set-Up
# 
#Installo Selenium ed il WebDriver configurando lo stesso
get_ipython().system('pip install selenium')
from selenium import webdriver
#Impostazioni di "ghost browsing"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--lang=en-GB")
chrome_options.add_argument("--window-size=1920,1080")
#WebDriver
wd = webdriver.Chrome("C:\\Users\\chiara.teruzzi\\Documents\\Master\\chromedriver.exe")

#importo le librerie necessarie
import sys
import pandas
import json
import pprint

# # Scraping sito viaggi WeRoad

#URL WeRoad navigato
wd.get("https://www.weroad.it/viaggi")

#Verifico etichette scaricate dalla pagina
print(wd.find_element_by_tag_name("body").text)

#Trovo il dettaglio generico dei viaggi
list_travels = wd.find_elements_by_css_selector("div.travel-card-body")
print(len(list_travels))
print(list_travels[0].text)

#Raccolgo in un unico array (inizialmente vuoto) i dettagli di tutti i viaggi e visualizzo il risultato
import pprint
detail_travels = []
for travel in list_travels:
    title = travel.find_elements_by_css_selector("div.travel-card-content > h3 > a")[0].text
    price = travel.find_elements_by_css_selector("div.travel-card-footer  price-value")[0].text
    days = travel.find_elements_by_css_selector("div.travel-card-footer  div.text > strong")[0].text
    url = travel.find_elements_by_css_selector("div.travel-card-content > h3 > a")[0].get_attribute("href")
    detail_travels.append({'title': title,
                            'price': price,
                            'days': days,
                            'url': url})

len(detail_travels)
pprint.pprint(detail_travels)

#Tramite pandas creo un Dataframe
import pandas as pd
ds_detail_travels = pd.DataFrame(detail_travels)
ds_detail_travels.head()

#Scrivo il dataframe in un file .csv
ds_detail_travels.to_csv('ds_WRtravels.csv')


# # Scraping sito viaggi Contiki

#URL Contiki navigato
wd.get("https://www.contiki.com/eu/en/search?SortByAndOrder%5B0%5D.sortBy=rating&SortByAndOrder%5B0%5D.order=desc")

#Trovo il dettaglio generico dei viaggi
list_travels = wd.find_elements_by_css_selector("div.trip-card__wrapper")
print(len(list_travels))
print(list_travels[0].text)

##Carico tutti i viaggi in un'unica pagina e raccolgo l'informazione in list_travels

#importo la libreria time per impostare un intervallo di temo tra un'azione e l'altra
import time
#inizializzo un array vuoto
lista = []
#Leggo il testo dove è indicato il numero di elementi visualizzato nella pagina ed il numero massimo di elementi
progressivi_pagina = wd.find_elements_by_css_selector("p.pagination__progress")[0].text
lista = progressivi_pagina.split(" ")
#il secondo elemento della lista indica il numero di elementi visualizzati nella pagina corrente, il quarto il totale
counter = int(lista[1])
totale = int(lista[3])

#finchè non raggiungo il numero massimo di elementi visualizzati clicco sul tasto "Load More"
while counter < totale :
  time.sleep(2)
  try:
    #seleziono il bottone
    link = wd.find_elements_by_css_selector("button.pagination__load-more")[0]
    #eseguo lo scroll della pagina
    wd.execute_script('arguments[0].scrollIntoView(false);', link)
    #scroll up
    wd.execute_script('window.scrollBy(0, 200)')
    link.click()
  except:
    link = wd.find_elements_by_css_selector("button.pagination__load-more")[0]
    time.sleep(2)
  #incremento il counter e lo visualizzo (si dovrebbero caricare 9 elemeneti per volta)
  progressivi_pagina = wd.find_elements_by_css_selector("p.pagination__progress")[0].text
  lista = progressivi_pagina.split(" ")
  counter = int(lista[1])
  print(counter)

#leggo quindi tutti i dettagli dei viaggio
list_travels = wd.find_elements_by_css_selector("div.trip-card__wrapper")

##Raccolgo in un unico array (inizialmente vuoto) i dettagli di tutti i viaggi e visualizzo il risultato
import pprint
detail_travels = []
#per ogni viaggio nella lista viaggi assegno i diversi attributi
for travel in list_travels:
    title = travel.find_elements_by_css_selector("div  h2 > a")[0].text
    price = travel.find_elements_by_css_selector("div.pricing__price > p > span")[0].text
    days = travel.find_elements_by_css_selector("div.duration.trip-card__duration  span")[0].text
    location = travel.find_elements_by_css_selector("div.trip-card__wrapper > p > span")[0].text
    url = travel.find_elements_by_css_selector("h2.trip-card__title a")[0].get_attribute("href")
    detail_travels.append({'title': title,
                            'price': price,
                            'days': days,
                            'location': location,
                            'url':url})

len(detail_travels)
pprint.pprint(detail_travels)

#Tramite pandas creo un Dataframe
import pandas as pd
ds_detail_travels = pd.DataFrame(detail_travels)
ds_detail_travels.head()

#Scrivo il dataframe in un file .csv
ds_detail_travels.to_csv('ds_CTKtravels.csv')

