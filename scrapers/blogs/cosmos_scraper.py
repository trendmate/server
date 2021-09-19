#Importing necessary libraries
from bs4 import BeautifulSoup
import requests

#Class to scrape blogs from vogue
class cosmoscraper:

    #Sitemap from where all the urls of the articles would be scraped at once
    cosmo_url = "https://www.cosmopolitan.com/style-beauty/fashion/"

    def get_urls(self):
        '''
        Function to return all the possible urls from the sitemap of cosmopolitan\n
        Returns:
            urls : list
        '''
        page = requests.get(self.cosmo_url)
        if int(page.status_code/100) != 2:
            pass
        
        urls = []
        soup = BeautifulSoup(page.content, 'html.parser')
        for div in soup.find_all('div', class_ = "full-item"):
            for url in div.find_all('a'):
                urls.append( self.cosmo_url + url['href'])
        
        return urls

    def get_txt_from_blog(self,url):
        '''
        Extract all the text from blogs given its URL\n
        Parameters:
            url : string - url to the target blog 
        Returns:
            text_corpus : string - All of the text from the blog in a single string
        
        Works for urls extracted from https://www.cosmopolitan.com/style-beauty/fashion/
        '''
        page = requests.get(url)

        #A successful get request would return the status code starting with 2 (For eg. 200) 
        if (page.status_code/100 != 2):
            pass
        
        soup = BeautifulSoup(page.content, 'html.parser')

        #Extracting the title
        text_corpus = soup.find_all('title')[0].get_text()

        #Extracting the content of the blog
        for txt in soup.find_all('p'):
            text_corpus = text_corpus + " " + txt.get_text()
        for txt in soup.find_all(['span','div'], class_= ["listicle-slide-hed-text", "slideshow-slide-dek"]):
            text_corpus = text_corpus + " " + txt.get_text()
        
        return text_corpus