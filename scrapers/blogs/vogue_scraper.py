import pandas as pd
import os

#Importing necessary libraries
from bs4 import BeautifulSoup
import requests


#Class to scrape blogs from vogue 
class voguescraper:
    
    #Sitemap from where all the urls of the articles would be scraped at once
    vogue_url = "https://www.vogue.com/sitemap/trends"

    def get_urls(self):
        '''
        Function to return all the possible urls from the sitemap of vogue\n
        Returns:
            urls : list
        '''
        page = requests.get(self.vogue_url)

        #A successful get request would return the status code starting with 2 (For eg. 200) 
        if int(page.status_code/100) != 2:
            #If the get request is not sucessful - pass
            pass

        #Empty list to store the URLS    
        urls = []
        soup = BeautifulSoup(page.content, 'html.parser')
        
        #Loop to extract all the urls from the <a href> tag
        for url in soup.find_all('a', href=True):
            urls.append(url['href'])
        
        return urls

    def get_txt_from_blog(self,url):
        '''
        Extract all the text from blogs given its URL\n
        Parameters:
            url : string - url to the target blog 
        Returns:
            text_corpus : string - All of the text from the blog in a single string
        
        Works for urls extracted from https://www.vogue.com/sitemap/trends
        '''
        page = requests.get(url)
        
        #The status code should be 200 if the page is read successfully
        if int(page.status_code/100) != 2:
            pass
        
        soup = BeautifulSoup(page.content, 'html.parser')

        #Extracting the title
        text_corpus = soup.find_all('title')[0].get_text()

        #Extracting the content of the blog
        for txt in soup.find_all('div', class_='grid--item body body__container article__body'):
            text_corpus = text_corpus + " " + str(txt.get_text())
        
        return text_corpus


    def get_vogue(self, webD, path):
        webD.get("https://www.vogue.in/vogue-closet/?closet=vogue_closet&filter_type=product_collection&order_by=recent&q=t+shirt&celebrity=&occasion=&price=&product-type=clothing")

        img_links = []
        i = 0
        while(i < 2):
            try:
                productInfoList = webD.find_elements_by_class_name("product-wrapper")
                for el in productInfoList:
                    pp1 = el.find_element_by_tag_name("a")
                    pp2 = pp1.find_element_by_tag_name("img")
                    img_links.append(pp2.get_property("src"))
                page_nav = webD.find_element_by_class_name("pagination")
                butts = page_nav.find_elements_by_tag_name("a")[-1]
                butts.click()
            except:
                pass
            i += 1


        df_vogue = pd.DataFrame(columns=["img_links"])
        df_vogue["img_links"] = img_links


        df_vogue.to_csv(os.path.join(path,"vogue.csv"))