#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:16:14 2020

@author: hassanpasha
"""


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time 
import pandas as pd

#list of doc
doc_list =[]
goodtherapy_list = []

#web scraper functin 
def webscrapper(html_url):
    driver = webdriver.Chrome("/Users/hassanpasha/Documents/PashaBrb/NewOCD/practice/python_scheduler/chromedriver")
    html_doc = html_url
        
    driver.get(html_doc)
    time.sleep(5)  
    html = driver.page_source 
    data = BeautifulSoup(html, 'html.parser')
    driver.close()  
    return data 
    
for x in range(0,100):
         
    #goodtherpy
    goodtherapy = webscrapper("https://www.psychologytoday.com/us/therapists/il/chicago")
    
    goodtherapy.prettify()
    
    goodtherapy_data=goodtherapy.find_all("div",{"class":"result-row normal-result row"})
    

    for goodtherapy_data_index in goodtherapy_data:
    
        print(goodtherapy_data_index)
    
        goodtherpy_bio = goodtherapy_data_index.find("div",{"class":"result-desc"}).text 
        goodtherapy_name = goodtherapy_data_index.find("span",{"itemprop":"name"}).text 
        goodtherapy_phone = goodtherapy_data_index.find("div",{"class":"result-phone"}).text.replace(" ","") 
        
        goodtherapy_address = goodtherapy_data_index.find("div",{"class":"result-address"}).text 
        
        try:
            
            goodtherapy_jobtitle = goodtherapy_data_index.find("span",{"itemprop":"jobTitle"}).text     
        except:
            goodtherapy_jobtitle = 'Job_Null'
            
            
        
        goodtherapy_city = goodtherapy_data_index.find("span",{"itemprop":"addressLocality"}).text 
        goodtherapy_state = goodtherapy_data_index.find("span",{"itemprop":"addressRegion"}).text 
        goodtherapy_postal_code = goodtherapy_data_index.find("span",{"itemprop":"postalCode"}).text 
        goodtherapy_license_list = goodtherapy_data_index.find_all("span",{"class":"nowrap"})
        goodtherapy_license_final =''
        #bs4 tag not working so had to use string maniuplations
        for license_ in goodtherapy_license_list:
    
            goodtherapy_license = str(license_).replace('<span class="nowrap">','')
            goodtherapy_license = goodtherapy_license.replace('</span>' , '') 
            goodtherapy_license_final = goodtherapy_license + ' ' + goodtherapy_license_final
            
        
        goodtherapy_dic = {
            
                "Name": goodtherapy_name,
                "License": goodtherapy_license_final,
                "Bio":goodtherpy_bio,
                "Office":'NULL',
                "Location":f"{goodtherapy_city} {goodtherapy_state} {goodtherapy_postal_code}", 
                "Phone":goodtherapy_phone.replace('\n',''), 
            }
        
        goodtherapy_list.append(goodtherapy_dic)
        
    
    
    
    
    
    driver = webdriver.Chrome("/Users/hassanpasha/Documents/PashaBrb/NewOCD/practice/python_scheduler/chromedriver")
    html_doc = "https://www.findatherapist.com/search/"
    
    driver.get(html_doc)
    time.sleep(5)  
    html = driver.page_source 
    data = BeautifulSoup(html, 'html.parser')
    
    
    print(data.prettify())
    
    clinical_data = data.find_all('div', {'class': 'listing'})
    
    
    # clinical_data[0].find('p', {'class': 'name'}).text

    for doc in clinical_data:
        #bug: div does not exsist 
        #result : solved 
        try :
                
            Phone = doc.find('div', {'class': 'phone'}).text
        except:
            Phone = "NULL"
        
        print(doc.find('p', {'class': 'name'}).text)
        
        doc_dic = {
            
            "Name":doc.find('p', {'class': 'name'}).text,
            "License": doc.find('p', {'class': 'license'}).text,
            "Bio":doc.find('p', {'class': 'paragraph'}).text,
            "Office":doc.find('div', {'class': 'office'}).text,
            "Location":doc.find('div', {'class': 'location'}).text, 
            "Phone":Phone, 
        }

        
        doc_list.append(doc_dic)
        
    driver.close()     

#combining list 
combined_leads = doc_list + goodtherapy_list

dataframe = pd.DataFrame(doc_list)

dataframe.to_csv('combined_leads.csv', header=True)

        
    