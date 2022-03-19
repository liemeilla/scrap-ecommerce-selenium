from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import XPathElements, map_url_to_ecommerce, scroll_to_bottom_page, write_csv, write_json, extract_amount_from_text

# config 
CHROME_DRIVER_PATH = '/Users/bella/WebDriver/bin/chrome-97/chromedriver'
CHROME_VERSION = '97.0'
SELENIUM_VERSION = '3.141.0'

class EcommerceScraper:
    def setUp(self):
        config = {
            "chrome_driver_path" : CHROME_DRIVER_PATH,
            "chrome_version" : CHROME_VERSION,
            "selenium_version" : SELENIUM_VERSION
        }

        self.config = config
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.done_scrapping = False

    def tearDown(self):
        if self.done_scrapping == True:
            self.driver.quit()
    
    def scrapByTopic(self, topic, url):
        driver = self.driver

        config_xpath = XPathElements(driver, map_url_to_ecommerce(url))

        # go to url
        driver.get(url)

        # searching topic
        try:
            searchBar = driver.find_element_by_xpath(config_xpath.search_bar_xpath)
            buttonSearch = driver.find_element_by_xpath(config_xpath.button_search_xpath)
        except:
            print("catch error when find element search bar and button search by XPATH")

        # type topic into search bar and click button search
        searchBar.send_keys(topic)
        buttonSearch.click()

        # click next button
        if config_xpath.next_btn_xpath != "":
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, config_xpath.next_btn_xpath))
                )
            except:
                print("catch error when find element next button by XPATH")

            next_btn = driver.find_element_by_xpath(config_xpath.next_btn_xpath)
            next_btn.click()

        scroll_to_bottom_page(driver)
        
        product_elements = driver.find_elements_by_xpath(config_xpath.product_wrapper_xpath)
        product_category_elm = driver.find_element_by_xpath(config_xpath.product_category_xpath)

        i = 1
        products = []
        for pe in product_elements:
            product_name = ""
            product_price = ""
            product_loc = ""
            product_total_sold = ""

            retry = 0
            success = False
            while retry < 3 and not success:
                try:
                    product_name = pe.find_element_by_xpath(config_xpath.product_name_xpath).text
                    product_price = pe.find_element_by_xpath(config_xpath.product_price_xpath).text
                    product_loc = pe.find_element_by_xpath(config_xpath.product_loc_xpath).text
                    product_total_sold = pe.find_element_by_xpath(config_xpath.product_total_sold_xpath).text
                    product_category = product_category_elm.text
                except:
                    retry += 1
                    if retry == 3:
                        print("catch error when try to find element of product details")
                    
                success = True

            product = {
                "product_sequence" : i,
                "product_name" : product_name,
                "product_category" : product_category,
                "product_price" : product_price,
                "product_location" : product_loc,
                "product_total_sold" : extract_amount_from_text(product_total_sold),
            }
            i += 1

            products.append(product)
        
        # print("products:")
        # print(products)

        # write to json and csv
        separator = "_"
        prefix_filename = separator.join([map_url_to_ecommerce(url), topic])
        write_csv(products, prefix_filename)
        write_json(products, prefix_filename)

        self.done_scrapping = True



# Main Program

keyword = "atasan wanita"
website_url = 'https://www.tokopedia.com'

scrapper = EcommerceScraper()
scrapper.setUp()
scrapper.scrapByTopic(topic=keyword, url=website_url)
scrapper.tearDown()



