import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import numpy
import random
import pandas as pd

global urls, brand_names, Description, Rating, Category, Discount, Link, Rate

def init():
    urls=['https://www.amazon.in/s?i=apparel&bbn=1968120031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968120031%2Cp_85%3A10440599031%2Cp_72%3A1318476031&s=apparels&dc&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7ad3f8fa-3670-4f37-8514-6e5bf1c9ad3e&pf_rd_r=E6PP7PBNCKCV9PKR323W&pf_rd_s=merchandised-search-3&qid=1627972541&rnid=1318475031&ref=sr_nr_p_72_1',
        'https://www.amazon.in/s?i=apparel&bbn=1968094031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968093031%2Cn%3A1968094031%2Cp_85%3A10440599031%2Cp_72%3A1318476031&s=apparels&dc&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7ad3f8fa-3670-4f37-8514-6e5bf1c9ad3e&pf_rd_r=E6PP7PBNCKCV9PKR323W&pf_rd_s=merchandised-search-3&qid=1627972580&rnid=1318475031&ref=sr_nr_p_72_1',
        'https://www.amazon.in/s?i=apparel&bbn=1968076031&rh=n%3A1968076031%2Cp_85%3A10440599031%2Cp_72%3A1318476031&s=apparels&dc&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7ad3f8fa-3670-4f37-8514-6e5bf1c9ad3e&pf_rd_r=E6PP7PBNCKCV9PKR323W&pf_rd_s=merchandised-search-3&qid=1627972606&rnid=1318475031&ref=sr_nr_p_72_1',
        'https://www.amazon.in/s?i=apparel&bbn=1968097031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968097031%2Cp_85%3A10440599031%2Cp_72%3A1318476031&s=apparels&dc&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7ad3f8fa-3670-4f37-8514-6e5bf1c9ad3e&pf_rd_r=E6PP7PBNCKCV9PKR323W&pf_rd_s=merchandised-search-3&qid=1627972641&rnid=1318475031&ref=sr_nr_p_72_1',
        'https://www.amazon.in/s?i=apparel&bbn=5836983031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968125031%2Cn%3A5836983031%2Cp_85%3A10440599031%2Cp_72%3A1318476031&s=apparels&dc&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7ad3f8fa-3670-4f37-8514-6e5bf1c9ad3e&pf_rd_r=E6PP7PBNCKCV9PKR323W&pf_rd_s=merchandised-search-3&qid=1627972668&rnid=1318475031&ref=sr_nr_p_72_1']

    items=['Tshirts','Shirts','Jeans','Short','Casual_Trousers']

    brand_names=[]
    Description=[]
    Rating=[]
    Category=[]
    Discount=[]
    Link=[]
    Rate=[]
    for j in items:
        for i in range(2,50):
            Category.append(j)

def scrape_amazon(driver):
    for url in urls:
        driver.get(url)
        for i in range(2,50):
            try:
                brand=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[2]/div/h5/span')
                brand_names.append(brand.text)
            except  NoSuchElementException:
                brand=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[1]/div/h5/span')
                brand_names.append(brand.text)
        for i in range(2,50):
            try:
                Desc=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[2]/h2/a/span')
                Description.append(Desc.text)
            except  NoSuchElementException:
                Desc=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[1]/h2/a/span')
                Description.append(Desc.text)
        for i in range(2,50):
            try:
                Desc=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[2]/h2/a/span')
                Description.append(Desc.text)
            except  NoSuchElementException:
                Desc=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[1]/h2/a/span')
                Description.append(Desc.text)
        for i in range(2,50):
            try:
                rat=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[3]/div/span[2]/a/span')
                Rating.append(rat.text)
            except  NoSuchElementException:
                rat=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[2]/div/span[2]/a/span')
                Rating.append(rat.text)

        for i in range(2,50):
            Rate.append(numpy.random.uniform(3.0, 5.0, ))

            try:
                D=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[4]/div/span[2]')
                Discount.append(D.text)
            except  NoSuchElementException:
                try:
                    D=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[3]/div[3]/div/span[2]')
                    Discount.append(D.text)
                except NoSuchElementException:
                    Discount.append(str(0))
        for link in range(2,50): 
            link=driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[2]/div/span/a/div/img')
            Link.append(link.get_attribute('src'))
            
    data_tuples = list(zip(brand_names,Description,Rating,Discount,Category,Rate,Link))

    df_1=pd.DataFrame(data_tuples,columns=['Brand','Description','Reviews','Discount','Category','Rating','Links'])
    df_1.to_csv('../data/products_data/cloud_scraped_amazon.csv', mode='a', header=False)