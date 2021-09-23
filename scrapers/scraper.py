import selenium
# from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import scrapers.products.amazon_scraper as amazon
import scrapers.products.myntra_men_scraper as myntra_men
import scrapers.products.myntra_women_scraper as myntra_women

global display, driver

def init():
    # display = Display(visible=0, size=(1920, 1080)).start()
    global driver
    driver=webdriver.Chrome(ChromeDriverManager().install())
    amazon.init()
    myntra_men.init()
    myntra_women.init()

def scrape():
    myntra_men.scrape(driver)
    # amazon.scrape_amazon(driver)
    # myntra_women.scrape(driver)
