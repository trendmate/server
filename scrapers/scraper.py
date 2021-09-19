import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import products.amazon_scraper as amazon
import products.myntra_scraper as myntra

global display, driver

def init():
    display = Display(visible=0, size=(1920, 1080)).start()
    driver=webdriver.Chrome(ChromeDriverManager().install())
    amazon.init()
    myntra.init()

def scrape():
    amazon.scrape_amazon(driver)
    myntra.scrape_myntra(driver)
