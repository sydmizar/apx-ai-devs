# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:26:45 2022

@author: Claudia Mancera
"""


import random
from time import sleep
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import json


#driver= webdriver.Chrome('./chromedriver.exe')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
Keywords= "Machine,learning"

listKeywords = "%20".join(Keywords.split(','))
page = 'https://mx.indeed.com/jobs?q=' + listKeywords


driver.get(page)
sleep(random.uniform(5.0,10.0))

#get number of pages
#boton_number= driver.find_element(By.XPATH,'//*[@id="MainCol"]/div[2]/div/div[2]').text
#print(boton_number)
#numero_paginas = int(boton_number[-2:])
numero_paginas = 100

#creamos df vacio
jobs_df = pd.DataFrame(columns = ['Title_role', 'Company','City','Salary','Company_rate','Description', 'Date_published',
                                  'Date_scrapped','Keywords', 'Source'])
jobs_list = list()

for i in range(numero_paginas):
    
    sleep(random.uniform(1.0,4.0))
    #jobcards= driver.find_elements(By.XPATH,'//ul[@class="jobsearch-ResultsList"]/li/div[not(@class="mosaic-zone")]')   
    jobcards= driver.find_elements(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li') 
    
    
    
    for element,job in enumerate(jobcards, start=1):
        print(element,job)
        sleep(random.uniform(1.0,4.0))
        try:
            job.click()
        except:
            continue
        sleep(random.uniform(1.0,3.0))
    
        
        try:
            title_role = job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/a').text
            #//*[@id="jobTitle-cbf2ab492cfecf81"]
            #//*[@id="viewJobSSRRoot"]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/h1/span
            #//*[@id="viewJobSSRRoot"]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/h1
        except:
            title_role = np.nan
        #//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/span[1]/a
        try:
            company = job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/span[1]').text
        except:
            company = np.nan

              
        source = 'Indeed.com'
        print(element,company, title_role)
        
        try:
            city=job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div').text
        except:
            city= np.nan
        
        try:
            salary=job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[3]/div/div').text
        except:
            salary= np.nan
        
        try:
            company_rate=job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/span[2]/a/span/span').text
        except:
            company_rate= np.nan
        
        try:
            date_published=job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div[1]/span[1]').text
        except:
            try:
                date_published=job.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]/ul/li['+str(element)+']/div/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/td/div[1]/span[1]').text
            except:
                date_published= np.nan
        
        try:
            description=job.find_element(By.XPATH,'//*[@id="jobDescriptionText"]').text
            #//*[@id="viewJobSSRRoot"]/div[2]/div[1]/div/div/div/div[1]/div/div[2]
        except:
            description= np.nan
            
        
        
        
        jobs_df = pd.concat([jobs_df, pd.DataFrame.from_records([{ 'Title_role': title_role,
                                                                   'Company' : company, 
                                                                   'City' : city,
                                                                  'Salary' : salary,
                                                                 'Company_rate' : company_rate, 
                                                                 'Date_published': date_published,
                                                                 'Date_scrapped': date.today(),
                                                                 'Description': description,
                                                                 'Keywords': Keywords,
                                                                 'Source' : source }])], ignore_index=True)
        jobs_dic= {'Title_role': title_role,
                   'Company' : company, 
                   'City' : city,
                   'Salary' : salary,
                   'Company_rate' : company_rate, 
                   'Date_published': date_published,
                   'Date_scrapped': str(date.today()),
                   'Description': description,
                   'Keywords': Keywords,
                   'Source' : source }
        
        jobs_list.append(jobs_dic) 
        
    if i== 0:
        next_num= 2
    elif i== 1:
        next_num= 4  
    else:
        next_num=5
    try:
        next_boton=driver.find_element(By.XPATH,'//*[@data-testid="pagination-page-next"]') 
    except:
        try:
            next_boton= driver.find_element(By.XPATH,'//*[@id="resultsCol"]/nav/div/ul/li['+str(next_num)+']')
        except:
            break
    


    sleep(random.uniform(1.0,4.0))
    next_boton.click()
    

output_filename_csv = f'indeed_{Keywords}_{datetime.now().strftime(r"%d-%m-%Y")}.csv'
jobs_df.to_csv(output_filename_csv)
output_filename = f'indeed_english_{Keywords}_{datetime.now().strftime(r"%d-%m-%Y")}.json'
with open(output_filename, 'w+', encoding='utf-8') as outfile:
    json.dump(jobs_list,outfile,ensure_ascii=False,indent=4)

 

    
