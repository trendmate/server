import selenium
from selenium import webdriver as wb
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from products.myntra_scraper import get_myntra

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
webD = wb.Chrome(ChromeDriverManager().install(),options=chrome_options)
get_myntra(webD, './data/image_links')

