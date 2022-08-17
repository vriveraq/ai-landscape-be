import pandas as pd
import urllib
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def getData(url: str):
    '''This function scrappes the company name, website, 
       and region of companies from the AI4Belgium wepage.
       Returns a DataFrame'''
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page)
    data = soup.findAll(attrs={"data-region": True})
    
    regions = []
    links = []
    names = []
    # Extract relevant data
    for row in data:
        region = row['data-region']
        link = row.find('a').get('href')
        name = row.find('a').get_text()

        regions.append(region)  
        links.append(link) 
        names.append (name)

    zipped = list(zip(names,links, regions))
    df = pd.DataFrame(zipped, columns=['Company Name', 'Link', 'Region'])    
    return df


def createDriver(headless=True):
    chrome_options = Options()
    if headless:  # 👈 Optional condition to "hide" the browser window
        chrome_options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) 
    # 👆  Creation of the "driver" that we're using to interact with the browser

    driver.implicitly_wait(40) 
    # 👆 How much time should Selenium wait until an element is able to interact
    return driver

def getAddress(name:str):
    ''' This function scrappes a company's address using Google search and maps
    '''
    query = urllib.parse.quote(' \' '+ name)   
    driver = createDriver()  # Method defined in previous examples
    url = 'https://www.google.com/search?q='+query 
    
    try:    
        driver.get(url)
        driver.find_element(By.XPATH,'/html/body/div[3]/div[3]/span/div/div/div/div[3]/div[1]/button[2]').click();
        address = driver.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "LrzXr", " " ))]').text
    except:    
        address = ''

    if address == '':
         url = 'https://www.google.com/maps/search/'+query
         driver.get(url)
         driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click();
         try:    
             address = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]/div[2]/div[1]').text
         except:
             address = ''
    driver.quit();
    
    return address   