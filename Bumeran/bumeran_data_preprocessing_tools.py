
from datetime import date, timedelta, datetime
from deep_translator import GoogleTranslator 
import re
import pandas as pd

def translate_job_description(text:str) -> str:

    if len(text) >= 5000: 
        # sentences = text.split(sep = '.') 
        text = text.replace('\n', ' ') 
        sentences = re.split(r'(?<=\D)\.(?=.)|(?<=\d)\.(?=\D)', text) 
        # filter_object = filter(lambda x: x != "", sentences) 
        filter_object = filter(lambda x: len(x) > 2, sentences) 
        sentences = list(filter_object) 
        filter_object = filter(lambda x: bool(re.search('[a-zA-Z]', x)), sentences)  
        sentences = list(filter_object) 
        filter_object = filter(lambda x: (sum(c.isalpha() for c in x)) > 2, sentences)
        sentences = list(filter_object) 
        translated = GoogleTranslator('es', 'en').translate_batch(sentences) 
        translated_news = '. '.join(translated) 
        return translated_news 

    else: 
        translated_news = GoogleTranslator(source='es', target='en').translate(text) 
        return translated_news 

def create_salary_regex_list(salary_text: str) -> list:
       #add steps to separate between monthly and yearly wages 
       return re.findall(r"([0-9]+,[0-9].[0-9]+)",salary_text)

def create_min_max_salary_columns(df:pd.DataFrame) -> pd.DataFrame:
       df["salary"] = df["salary"].apply(create_salary_regex_list)
       try:
              temp_min_max_salary_df = pd.DataFrame(df["salary"].apply(sorted).tolist(), columns=["min_monthly_salary","max_monthly_salary"])
              joined_df = df.join(temp_min_max_salary_df)
              return joined_df.drop("salary", axis=1)
              
       except ValueError:
              df["min_monthly_salary"] = None
              df["max_monthly_salary"] = None
              return df.drop("salary",axis=1)
       

date_published_dict = {
    "Publicado hace más de 30 días"     :  (date.today() - timedelta(days=45)).strftime(r"%d/%m/%Y")  
    ,"Publicado hace más de 15 días"    :  (date.today() - timedelta(days=22)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 15 días"           :  (date.today() - timedelta(days=15)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 14 días"           :  (date.today() - timedelta(days=14)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 13 días"           :  (date.today() - timedelta(days=13)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 12 días"           :  (date.today() - timedelta(days=12)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 11 días"           :  (date.today() - timedelta(days=11)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 10 días"           :  (date.today() - timedelta(days=10)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 9 días"            :  (date.today() - timedelta(days=9)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 8 días"            :  (date.today() - timedelta(days=8)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 7 días"            :  (date.today() - timedelta(days=7)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 6 días"            :  (date.today() - timedelta(days=6)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 5 días"            :  (date.today() - timedelta(days=5)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 4 días"            :  (date.today() - timedelta(days=4)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 3 días"            :  (date.today() - timedelta(days=3)).strftime(r"%d/%m/%Y")
    ,"Publicado hace 2 días"            :  (date.today() - timedelta(days=2)).strftime(r"%d/%m/%Y")
    ,"Publicado ayer"                   :  (date.today() - timedelta(days=1)).strftime(r"%d/%m/%Y") 
    ,"Publicado hoy"                    :   date.today().strftime(r"%d/%m/%Y")
}

schema_dict = {
    "presencial":"On-site", 
    "híbrido":"Hybrid",
    "hibrido":"Hybrid",
    "remoto":"Remote",
    "no especificado":"Unspecified" 
    } 


