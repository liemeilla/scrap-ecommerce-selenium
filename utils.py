import time
import csv
import json
import re
from os import path
from datetime import datetime

config_xpath = {
    'tokopedia' : {
        'search_bar_xpath' : '//*[@id="search-container"]/form/div/div/div/input',
        'button_search_xpath' : '//*[@id="search-container"]/form/div/div/div/button',
        'next_btn_xpath' : '//div[contains(@class, "unf-coachmark__next-button")]',
        'product_wrapper_xpath' : '//*[@id="zeus-root"]//div[@data-testid="divSRPContentProducts"]//div[contains(@class, "css-")]//div[contains(@class, "css-")]//div[@data-testid="divProductWrapper"]',
        'product_name_xpath' : './/div[@data-testid="spnSRPProdName"]',
        'product_price_xpath' : './/div[@data-testid="spnSRPProdPrice"]',
        'product_loc_xpath' : './/span[@data-testid="spnSRPProdTabShopLoc"]',
        'product_total_sold_xpath' : './/div[@data-productinfo="true"]/div[2]/span[3]',
        'product_category_xpath' : '//*[@id="zeus-root"]//div[@data-testid="cntrBlockFilter"]//span[@data-testid="spnSRPLevel1Filter"]',
    }
    # can add another ecommerce
}   

class XPathElements:
    def __init__(self, driver, ecommerce):
        self.ecommerce = ecommerce
        self.driver = driver

        self.__set_search_bar_xpath(config_xpath[ecommerce]['search_bar_xpath'])
        self.__set_button_search_xpath(config_xpath[ecommerce]['button_search_xpath'])
        self.__set_next_btn_xpath(config_xpath[ecommerce]['next_btn_xpath'])
        self.__set_product_wrapper_xpath(config_xpath[ecommerce]['product_wrapper_xpath'])
        self.__set_product_name_xpath(config_xpath[ecommerce]['product_name_xpath'])
        self.__set_product_price_xpath(config_xpath[ecommerce]['product_price_xpath'])
        self.__set_product_loc_xpath(config_xpath[ecommerce]['product_loc_xpath'])
        self.__set_product_total_sold_xpath(config_xpath[ecommerce]['product_total_sold_xpath'])
        self.__set_product_category_xpath(config_xpath[ecommerce]['product_category_xpath'])

    def __set_search_bar_xpath(self, xpath):
        self.search_bar_xpath = xpath

    def __set_button_search_xpath(self, xpath):
        self.button_search_xpath = xpath

    def __set_next_btn_xpath(self, xpath):
        self.next_btn_xpath = xpath

    def __set_product_wrapper_xpath(self, xpath):
        self.product_wrapper_xpath = xpath
        
    def __set_product_name_xpath(self, xpath):
        self.product_name_xpath = xpath
        
    def __set_product_price_xpath(self, xpath):
        self.product_price_xpath = xpath
        
    def __set_product_loc_xpath(self, xpath):
        self.product_loc_xpath = xpath
        
    def __set_product_total_sold_xpath(self, xpath):
        self.product_total_sold_xpath = xpath

    def __set_product_category_xpath(self, xpath):
        self.product_category_xpath = xpath

def map_url_to_ecommerce(url):
    if url == 'https://www.tokopedia.com':
        return 'tokopedia'

def scroll_to_bottom_page(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def write_csv(data, filename):
    header = ['product_sequence', 'product_name', 'product_category', 'product_price', 'product_location', 'product_total_sold']
    
    now = datetime.now()
    csv_name = filename + "_" + str(now) + ".csv"
    with open(csv_name, 'w', encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    if path.isfile(csv_name) == True:
        print(csv_name + " is succesfully created")
    else:
        print(csv_name + " is failed to be create")
    

def write_json(data, filename):
    json_obj = json.dumps(data, indent=4)

    now = datetime.now()
    json_name = filename + "_" + str(now) + ".json"
    with open(json_name, "w") as f:
        f.write(json_obj)
    
    if path.isfile(json_name) == True:
        print(json_name + " is succesfully created")
    else:
        print(json_name + " is failed to be create")

def extract_amount_from_text(text):
    # test cases to check
    # extract_amount_from_text("3,1 rb")
    # extract_amount_from_text("45,6 rb")
    # extract_amount_from_text("1 rb")
    # extract_amount_from_text("10 rb")
    # extract_amount_from_text("0")
    # extract_amount_from_text("100")
    # extract_amount_from_text("78")
    
    re_pattern = "[0-9,]+[.\srb]*"
    raw_amount = "".join(re.findall(re_pattern, text))

    # print("raw_amount: " + str(raw_amount))

    comma_exists =  raw_amount.find(",") != -1
    ribuan_exists = raw_amount.find("rb") != -1

    amount = ((raw_amount.replace(",", "")).replace("rb", "")).replace(" ", "")

    if ribuan_exists:
        if comma_exists:
            amount += "00"
        else:
            amount += "000"

    # print("amount: " + amount)
    if amount != "":
        return int(amount)
    else:
        return int(0)
    



