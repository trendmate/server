import selenium
from pyvirtualdisplay import Display
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import scrapers.products.amazon_scraper as amazon
import scrapers.products.myntra_men_scraper as myntra_men
import scrapers.products.myntra_women_scraper as myntra_women
import scrapers.blogs.vogue as vogue

global display, driver

def init():
<<<<<<< HEAD
    display = Display(visible=0, size=(1920, 1080)).start()
    global driver
    driver=webdriver.Chrome(ChromeDriverManager().install())
    # amazon.init()
    # myntra_men.init()
    # myntra_women.init()
=======
    global driver, display
    # display = Display(visible=0, size=(1920, 1080)).start()
    driver=webdriver.Chrome(ChromeDriverManager().install())
    amazon.init()
    myntra_men.init()
    myntra_women.init()
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf
    vogue.init()

def scrape():
    vogue.scrape(driver)
<<<<<<< HEAD
    # myntra_men.scrape(driver)
    # amazon.scrape_amazon(driver)
    # myntra_women.scrape(driver)
=======
    myntra_men.scrape(driver)
    amazon.scrape_amazon(driver)
    myntra_women.scrape(driver)
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf
