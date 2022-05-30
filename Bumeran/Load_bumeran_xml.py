from datetime import datetime
from urllib.request import Request, urlopen
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json
import time
import locale
locale.setlocale(locale.LC_TIME, '')


def read_bumeran_xml_url() -> str:
    """
    Reads the .xml file with all the links containing a job post,
    to avoid being identified as a bot, the headers were changed and a timeout of 10s was added. 
    """

    BUMERAN_XML_URL = r"https://www.bumeran.com.mx/sitemap_avisos_bum.xml"
    bumeran_xml_request = Request(BUMERAN_XML_URL, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(bumeran_xml_request,timeout=10).read()
    

def convert_keywords_list_to_str(RAW_KEYWORDS_LIST:list) -> str:
    """
    Converts a list of keywords into a single string, a regex to identify either "/" or "-"
    is added at the beginning of each keyword, all white spaces are replaced with "-", the end of all keywords
    are concatenated with a "-" and all the keywords are joined with an "|" operator.
    
    Example: 
    ["data","datos","data engineer"] -> '(/|-)data-|(/|-)datos-|(/|-)data-engineer-'
    """
    return '|'.join(['(/|-)' + keyword.replace(' ','-').lower() + "-" for keyword in RAW_KEYWORDS_LIST])


def convert_raw_xml_to_filtered_list(bumeran_xml_raw:str, processed_keywords:str) -> list:
    """
    Convert bumeran xml file to a pandas series to then extract only the urls that contains any of the keywords
    Urls filtered will be returned as a list
    """
    bumeran_raw_df = pd.read_xml(bumeran_xml_raw)['loc']
    positions_filtered_df = bumeran_raw_df[bumeran_raw_df.str.contains(processed_keywords, regex=True)]
    return positions_filtered_df.tolist()


def start_webdriver() -> webdriver.Chrome:
    """
    initialize Selenium Chrome Webdriver
    """
    WEBDRIVER_PATH = r"chromedriver.exe"
    return webdriver.Chrome(executable_path=WEBDRIVER_PATH)


def scrape_job_url(driver:webdriver.Chrome, url:str, raw_keywords_list:list)-> dict:    
    """
    Extract the information necessary from each url
    a couple try/except conditions were added since some time the elements change their xPath.

    returns a dict object containing all job info required from the url argument
    """
    xPath_dict = {
    "JOB_TITLE_XPATH"         : '//*[@id="header-component"]/div[1]/div/h1'
    ,"COMPANY_XPATH"           : '//*[@id="header-component"]/div[1]/div/a/h3'
    ,"COMPANY_RATE_XPATH"      : ''
    ,"SALARY_XPATH"            : '//*[@id="section-detalle"]/div[1]/div/div/div/ul[2]/li[2]/h2'
    ,"CITY_XPATH"              : '//*[@id="section-detalle"]/div[1]/div/div/div/ul[1]/li[2]/a/h2'
    ,"REMOTE_SCHEMA_XPATH"     : '//*[@id="section-detalle"]/div[1]/div/div/div/ul[1]/li[3]/a/h2'
    ,"DESCRIPTION_XPATH"       : '//*[@id="section-detalle"]/div[2]/div/div[1]'
    ,"DATE_PUBLISHED_XPATH"    : '//*[@id="section-detalle"]/div[1]/div/div/div/ul[1]/li[1]/h2'
    }

    driver.get(url)

    time.sleep(3)

    job_info = dict()

    try: 
        job_info['keyWords']            = raw_keywords_list
        job_info['title_role']          = driver.find_element_by_xpath(xPath_dict["JOB_TITLE_XPATH"]).text
        job_info['description']         = driver.find_element_by_xpath(xPath_dict["DESCRIPTION_XPATH"]).text
        job_info['date_published']      = driver.find_element_by_xpath(xPath_dict["DATE_PUBLISHED_XPATH"]).text
        job_info['schema']              = driver.find_element_by_xpath(xPath_dict["REMOTE_SCHEMA_XPATH"]).text
        job_info['consulted_datetime']  = datetime.now().strftime(r"%d/%m/%Y, %H:%M")
        job_info['source']              = url
        job_info['company_rate']        = None #driver.find_element_by_xpath(COMPANY_RATE_XPATH).text
        job_info['salary']              = driver.find_element_by_xpath(xPath_dict["SALARY_XPATH"]).text

        #xPaths that already have caused an exception
        try:
            job_info['company']         = driver.find_element_by_xpath(xPath_dict["COMPANY_XPATH"]).text
        except NoSuchElementException:
            job_info['company']         = driver.find_element_by_xpath(xPath_dict["COMPANY_XPATH"][:-4] + 'span/h3').text

        try:
            job_info['city']            = driver.find_element_by_xpath(xPath_dict["CITY_XPATH"]).text
        except NoSuchElementException:
            job_info['city']            = driver.find_element_by_xpath(xPath_dict["CITY_XPATH"][:-4] + 'span/h2').text
    
    except Exception as e:
        print(e) 

    return job_info

def scrape_job_urls(filtered_jobs_urls_list:list, RAW_KEYWORDS_LIST:list) -> list:
    """
    Iterates through the list of urls filtered and then appends all the job information
    returned from the scrape_job_url function to a list 
    """
    webdriver = start_webdriver()
    jobs_info_list = list()

    for index_number,job_url in enumerate(filtered_jobs_urls_list):
        if index_number + 1 % 30 == 0: 
            #webdriver = start_webdriver()
            break
        scraped_url = scrape_job_url(driver = webdriver, url=job_url, raw_keywords_list=RAW_KEYWORDS_LIST)
        jobs_info_list.append(scraped_url)
    
    return jobs_info_list

def json_dump_job_info(jobs_info:list) -> None:
    """
    Gives .json format to the list containing the information for all the jobs filtered by keywords
    """
    output_filename = f'bumeran_scraped_data_{datetime.now().strftime(r"%d-%m-%Y_%H%M")}.json'
    with open(output_filename, 'w+', encoding='utf-8') as outfile:
        json.dump(jobs_info,outfile,ensure_ascii=False,indent=4)
  
def main(RAW_KEYWORDS_LIST:list) -> None:
    """
    Main function that will be excecuted to run web scraper and export the information to a .json format
    """
    bumeran_xml = read_bumeran_xml_url()
    processed_keywords = convert_keywords_list_to_str(RAW_KEYWORDS_LIST)
    filtered_jobs_urls_list = convert_raw_xml_to_filtered_list(bumeran_xml_raw = bumeran_xml, processed_keywords=processed_keywords)
    scraped_jobs_info = scrape_job_urls(filtered_jobs_urls_list, RAW_KEYWORDS_LIST)
    json_dump_job_info(scraped_jobs_info)


if __name__ == '__main__':
    RAW_KEYWORDS_LIST = ["desarrollador"]#["data","datos","data engineer"] #,"inteligencia de negocios","ingeniero de datos","cientifico de datos","frontend developer","front","web"]
    main(RAW_KEYWORDS_LIST=RAW_KEYWORDS_LIST)

#TODO: Question - log steps and errors? 
#TODO: Question - is it better to store all scraped data in a local list and then dump a single time a new .json file? Any suggestion? maybe using a generator?
#TODO: Task - Process fields accordingly (convert date_published text to date), obtain salary/skills/prestaciones from body
