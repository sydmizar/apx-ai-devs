import pandas as pd
from datetime import date, timedelta, datetime
import regex as re
JSON_FILEPATH = r"Bumeran\bumeran_scraped_data_27-05-2022_1638.json"
json_df = pd.read_json(JSON_FILEPATH)
json_df.head()
json_df["date_published"].value_counts()

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


json_df["date_published"] = json_df["date_published"].map(date_published_dict)
rows_containing_salary = json_df.loc[json_df["description"].str.contains("Salario")]
rows_containing_salary["description"] = 

split desrows_containing_salary["description"].str.split("\n")

x =re.findall("[\$]+?(\d+([,\.\d]+)?)",rows_containing_salary["description"].iloc[8])
x =re.findall("[\$]+?(\d+([,\.\d]+)?)",rows_containing_salary["description"].iloc[3])

