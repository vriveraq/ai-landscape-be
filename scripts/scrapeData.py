import re
import time
import pandas as pd
import requests
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver(url):
    """Creates Selenium driver for a specific url. 
       Input: url (str)
       Output: driver (Selenium driver object) 
    """
    # Setup Selenium WebDriver
    print("Setting up WebDriver...")
    # Use ChromeDriverManager to automatically handle the ChromeDriver path
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Headless option to avoid opening web browser
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Navigate to the page. We include the full URL.
    driver.get(url)
    print(f"Navigating to {url}")
    return driver

def click_cookie(driver,cookie_xpath):
    """Mananges GDPR banner by accepting cookies based on element XPath
       Input: driver (Selenium driver object)
    """
    try:
        # Wait for GDPR Banner to load and reject optional cookies
        time.sleep(5) 
        driver.find_element(By.XPATH, cookie_xpath).click()
        print("Cookie banner managed!")
    except:
        print("No GDPR cookie banner found! Continue ...")

def extract_company_data(root_url, company_item_css, iframe_css = None):
    """Extracts elements in website list based on CSS selector. Has the option to manage content in iframe.
       Input: root_url(str), company_item_css(str), iframe_css (None(default) or str)
       Output: company_data (dict) 
    """

    # Create driver
    driver = create_driver(root_url)

    # Define Xpath for GDPR banner and consenting to cookies
    cookie_xpath ='//*[@id="fedconsent"]/div[1]/div/div/div/div/ul/li[3]/button'
    click_cookie(driver, cookie_xpath)

    # --- 1. Define Selectors ---
    wait = WebDriverWait(driver, 10) # Wait for elements to load
    dataset =[]
    try:
        # If iframe_css provided switch to the iframe
        if iframe_css != None:
            print("Attempting to locate and switch to the iframe...")
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, iframe_css))
            )
            print("✅ Successfully switched to the iframe! WARNING: Script is build to only scrape first page!")

        # Find the element based on provided CSS selector
        company_items = driver.find_elements(By.CSS_SELECTOR, company_item_css.replace(" > div:nth-child(1)", " > div "))
        print(f"✅ Found the company item element(s)! Count: {len(company_items)}")

        # Loop through all companies items extracted from url
        for company in company_items:
            company_data={}
            try:
                link_element = company.find_element(By.TAG_NAME, "a")
                # Extract the URL (href)
                url = link_element.get_attribute("href")
                text_header = company.find_element(By.TAG_NAME, "h2")
                name = text_header.find_element(By.TAG_NAME,"a").text
            except Exception as e:
                url = None
                name = None
                print(f"Warning: Could not fully extract data from url for{name}. Error: {e}")
                continue
            try:       
                # Find the image element inside the link
                image_src = None
                image_element = link_element.find_element(By.TAG_NAME, "img")
                # Extract the image source (src)
                image_src = image_element.get_attribute("src")
            except Exception as e:
                print(f"Warning: Could not fully extract data from image.")
                continue
            try:
                headers = company.find_elements(By.TAG_NAME, "h4")
                header_info = company.find_elements(By.TAG_NAME, "span")
                
            except Exception as e:
                print(f"Warning: Could not fully extract data from headers. Error: {e}")
                continue
            
            # Create dictionary containing all information a specific company
            company_data["name"] = name
            company_data["url"] = url
            company_data["logo"] = image_src
            for header, info in zip(headers, header_info[1:]):
                company_data[header.text.lower()] = info.text
        
            # Store each company dictionary in list  
            dataset.append(company_data)
    except Exception as e:
        print(f"❌ Scraping failed after switching to iframe. Error: {e}")
        
    finally:
        # Switch back to the main document context
        if iframe_css != None:
            driver.switch_to.default_content()
            print("Switched back to default content.")
            driver.close()
    return dataset

def save_list_dict_to_csv(list_dict, output_file_path):
    """ Saves list of dictionaries to CSV file 
        Input: list_dict (list), output_file_path (str)
        Returns: df (DataFrame)
    """
    
    df = pd.DataFrame(list_dict)
    df.to_csv(output_file_path,index=False)
    return df

def scrape_pages_ai4belgium(pages = 18):
    company_item_css = "div.grid.grid-cols-4.gap-3.mb-2 > div:nth-child(1)"
    combined_data = pd.DataFrame()
    num_pages = pages
    for page_num in range(1,num_pages+1):
        print(f"Page {page_num}")
        suburl = f"https://community.ai4belgium.be/en/ai-landscape?nav=0&page={page_num}"
        print(suburl)
        dataset = extract_company_data(suburl, company_item_css)
        df = pd.DataFrame(dataset)
        combined_data = pd.concat([combined_data,df], ignore_index=True)
    combined_data.to_csv("../data/raw_scraped_dataset.csv", index = False)
    return combined_data

def extract_from_dom_tree_CBE(url, xpath):
    response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    soup = BeautifulSoup(response.content,"html.parser")
    # Convert to etree for XPath
    dom = etree.HTML(str(soup))
    try: 
        street= dom.xpath(xpath+'[1]')[0].replace("\xa0"," ")
        zip_code, city = dom.xpath(xpath+'[2]')[0].split("\xa0") 
    except:
         street, zip_code, city =  None, None, None
    return [street, zip_code, city]

def extract_address_CBE(company_name):
       # Extract street address using XPath
        try:
            # We use the exact name search 
            cbe_url = f"https://kbopub.economie.fgov.be/kbopub/zoeknaamexactform.html?natuurlijkPersoon=vestiging&searchWord=&firmName=&_oudeBenaming=on&establishmentname={company_name}&rechtsvormFonetic=ALL&firstName=&postcode=&postgemeente1=&filterEnkelActieve=true&_filterEnkelActieve=on&actionNPRP=Search"
            exact_name_xpath = '//*[@id="vestiginglist"]/tbody/tr/td[6]/text()'
            return extract_from_dom_tree_CBE(cbe_url, exact_name_xpath)     
        except:
            # If that fails, we use the general name search
            cbe_url = f"https://kbopub.economie.fgov.be/kbopub/zoeknaamfonetischform.html?lang=en&searchWord={company_name}&_oudeBenaming=on&pstcdeNPRP=&postgemeente1=&ondNP=true&_ondNP=on&ondRP=true&_ondRP=on&rechtsvormFonetic=ALL&vest=true&_vest=on&filterEnkelActieve=true&_filterEnkelActieve=on&actionNPRP=Search"
            general_name_xpath = '//*[@id="onderneminglistfonetisch"]/tbody/tr/td[6]/text()'
            return extract_from_dom_tree_CBE(cbe_url, general_name_xpath)   


