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
Keywords= "ETL,Developer"
listKeywords = "-".join(Keywords.split(','))
characters= str(len(listKeywords)+7)
#page_end= '-empleos-SRCH_KO0,'
page_end= '-jobs-SRCH_IL.0,6_IN169_KO7,'
page_extension= '.htm'
#page = 'https://www.glassdoor.com.mx/Empleo/' + listKeywords + page_end + characters + page_extension
page = 'https://www.glassdoor.com.mx/Job/mexico-' + listKeywords + page_end + characters + page_extension

#https://www.glassdoor.com/Job/mexico-data-engineer-jobs-SRCH_IL.0,6_IN169_KO7,20.htm

driver.get(page)
sleep(random.uniform(5.0,10.0))

#get number of pages
boton_number= driver.find_element(By.XPATH,'//*[@id="MainCol"]/div[2]/div/div[2]').text
print(boton_number)
numero_paginas = int(boton_number[-2:])

#creamos df vacio
jobs_df = pd.DataFrame(columns = ['Title_role', 'Company','City','Salary','Company_rate','Description', 'Date_published','Date_scrapped','Keywords', 'Source'])
jobs_list = list()



for i in range(numero_paginas):
    sleep(random.uniform(2.0,4.0))
    jobcards= driver.find_elements(By.XPATH,'//li[contains(@class,"react-job-listing")]')   
    
    
    for element,job in enumerate(jobcards, start=1):
        print(element,job)
        
        sleep(random.uniform(1.0,3.0))
        job.click()
        sleep(random.uniform(3.0,4.0))
        try:
            mostrar_mas =driver.find_element(By.XPATH,'//*[@class="css-t3xrds e856ufb2"]')
            mostrar_mas.click() 
        except:
            pass
        sleep(random.uniform(1.0,2.0))
        
        try:
            title_role = job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/a/span').text
        except:
            title_role = np.nan
        
        try:
            company = job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/div[1]/a/span').text
        except:
            company = np.nan
              
        source = 'Glassdoor.com'
        print(company, title_role)
        
        try:
            city=job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/div[2]/span').text
        except:
            city= np.nan
        
        try:
            salary=job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/div[3]/div[1]/span').text
        except:
            salary= np.nan
        
        try:
            company_rate=job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[1]/span').text
        except:
            company_rate= np.nan
        
        try:
            date_published=job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/div[3]/div[2]/div[2]').text
        except:
            try:
                date_published=job.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li['+str(element)+']/div[2]/div[2]/div/div[2]').text
            except:
                date_published= np.nan
        
        try:
            description=job.find_element(By.XPATH,'//*[@id="JobDescriptionContainer"]').text
        except:
            try:
                description=job.find_element(By.XPATH,'//*[@id="JobDescriptionContainer"]/div[1]/div[1]').text
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
        
    next_boton= driver.find_element(By.XPATH,'//button[@class="nextButton css-1hq9k8 e13qs2071"]')
    sleep(random.uniform(1.0,2.0))
    next_boton.click()


output_filename_csv = f'glassdoor_{Keywords}_{datetime.now().strftime(r"%d-%m-%Y")}.csv'
jobs_df.to_csv(output_filename_csv)
output_filename = f'glassdoor_english_{Keywords}_{datetime.now().strftime(r"%d-%m-%Y")}.json'
with open(output_filename, 'w+', encoding='utf-8') as outfile:
    json.dump(jobs_list,outfile,ensure_ascii=False,indent=4)
    



#%%


# Data Analyst 
# Data Engineer 
# Data Scientist 

# BI Developer 
# BI Engineer 
# ETL Developer 
# Machine Learning Engineer 
