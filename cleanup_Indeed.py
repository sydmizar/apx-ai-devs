# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 15:40:45 2022

@author: cmancera
"""

import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np
import re
from deep_translator import GoogleTranslator 
from googletrans import Translator

ml= pd.read_csv (r'C:\Users\cmancera\OneDrive - Apex Systems\Glassdoor\Final Output\indeed_Machine,learning_03-07-2022.csv')
#ed= pd.read_csv (r'C:\Users\cmancera\OneDrive - Apex Systems\Glassdoor\Final Output\glassdoor_english_ETL,developer_22-06-2022_1314.csv')
#ds= pd.read_csv (r'C:\Users\cmancera\OneDrive - Apex Systems\Glassdoor\Final Output\glassdoor_english_data,scientist_21-06-2022_1917.csv')


# data= pd.DataFrame()
# data= pd.concat([data, ed], ignore_index=True)
# data= pd.concat([data, ml], ignore_index=True)
# data= pd.concat([data, ds], ignore_index=True)
data= ml.copy()
#print (df)

#-------------------------------------------------------------
# ASIGN DATE WHEN IT WAS PUBLISHED

data["Date_published_final"]= "not assigned"
data["Date_scrapped"]=pd.to_datetime(data["Date_scrapped"])

for i in range(len(data)):
    
    if pd.isna(data["Date_published"][i]):
        data["Date_published_final"][i]= np.nan
    elif ("+" in data["Date_published"][i]):
        data["Date_published_final"][i]=(data["Date_scrapped"][i]- timedelta(days=30)).strftime(r"%d/%m/%Y")
        
    else:
        dias= re.findall('[0-9]+', data["Date_published"][i])
        data["Date_published_final"][i]=(data["Date_scrapped"][i]- timedelta(days=int("".join(dias)))).strftime(r"%d/%m/%Y")
        
#----------------------------------------------------------------
#SALARIO rango Minimo y maximo
data["Salary"]= data["Salary"].astype(str)

data["Salary_min"]= "not assigned"
data["Salary_max"]= "not assigned"



for i in range(len(data)):
    null_sal= False
    #if salary is null
    salary_str= ["Tiempo completo", "Medio Tiempo"]
    if (data["Salary"][i]== "nan")|(data["Salary"][i] in salary_str):
        null_sal= True
        data["Salary_min"][i]= np.nan
        data["Salary_max"][i]= np.nan
    else: 
        data["Salary"][i]= data["Salary"][i].replace(",", "")
        range_sal= re.findall('[0-9]+', data["Salary"][i])
        data["Salary_min"][i]= int(range_sal[0])
        try:
            data["Salary_max"][i]= int(range_sal[1])
        except:
            data["Salary_max"][i]= int(range_sal[0])
    

#----------------------------------------------
#Traducir vacantes en español
from time import sleep
detector = Translator()
data['Description_eng']= "not assigned"
#for i in range(50):
for i in range(len(data)):
    sleep(.1)
    null_des= False
    if pd.isna(data["Description"][i]):
        null_sal= True
        pass
    else:
        try:
            lang =detector.detect(data['Description'][i][:2000]).lang
            #print(i, lang)
        except:
            lang= "en"
            size_exceed=len(data['Description'][i]) >= 5000
            print(i,"error!", size_exceed)
        if (lang=="en")&(null_des==False):
            data['Description_eng'][i]= data['Description'][i]
        
        elif len(data['Description'][i]) >= 5000: 
            # sentences = text.split(sep = '.') 
        
            text = data['Description'][i].replace('\n', ' ') 
        
            sentences = re.split(r'(?<=\D)\.(?=.)|(?<=\d)\.(?=\D)', text) 
        
            # filter_object = filter(lambda x: x != "", sentences) 
        
            filter_object = filter(lambda x: len(x) > 2, sentences) 
        
            sentences = list(filter_object) 
        
            filter_object = filter(lambda x: bool(re.search('[a-zA-Z]', x)), sentences)  
        
            sentences = list(filter_object) 
        
            filter_object = filter(lambda x: (sum(c.isalpha() for c in x)) > 2, sentences) 
        
            sentences = list(filter_object) 
        
            translated = GoogleTranslator('es', 'en').translate_batch(sentences) 
        
            translated_des = '. '.join(translated) 
        
            data['Description_eng'][i] = translated_des

        
        else: 
            data['Description_eng'][i]= GoogleTranslator(source='es', target='en').translate(data['Description'][i]) 
            

#----------------------------------------
#Find list of skills in a list

data["Skills"]= "not assigned"
data["Description"]= data["Description"].str.lower()

skills = ["sql", "python","power bi","azure", "aws", "data factory",
          "data bricks","ssis","ssas","ssrs","etl", "tableou", "scala",
          "angular", "powerbi", "power apps","java", "lambda","UI/UX",
          "react","html","vue","agile", "scrum"]
pattern=re.compile('|'.join(skills))
#result=pattern.findall('Required skills are sql and power bi expertise')

for i in range(len(data)):
    if pd.isna(data["Description"][i]):
        pass
    else:
        des_skills= pattern.findall(data["Description"][i])
        unique= list(set(des_skills))
        data["Skills"][i]= unique
    
#---------------------------------------------
#Remove duplicated records


duplicates = data["Title_role","Company","Description","City"].duplicated()
print("Numero de vacantes duplicadas:", duplicates)
clean_data= data[~duplicates]
