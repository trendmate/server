import os
import pandas as pd

def get_flipkart(webD, path):
	webD.get("https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts")

	links = []
	names = []
	ratings = []
	no_revs_list = []
	img_links = []
	count = 1
	while(count < 25):
		productInfoList = webD.find_elements_by_class_name("_2mylT6")
		for el in productInfoList:
		    link = el.get_attribute("href")
		    links.append(link)
		    
		next_page = webD.find_elements_by_class_name("_3fVaIS")[-1]
		webD.get(next_page.get_attribute("href"))
		count += 1

	for link in links:
		webD.get(link)
		try:
		    name = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]").text
		    rating = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/div/span[1]/div").text
		    no_revs = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/div/span[2]").text
		    no_revs = no_revs.split()[0]
		    img_link = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img").get_attribute("src")
		    names.append(name)
		    ratings.append(rating)
		    no_revs_list.append(no_revs)
		    img_links.append(img_link)
		except:
		    pass
		try:
		    name = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]").text
		    rating = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div/div/span[1]/div").text
		    no_revs = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div/div/span[2]").text
		    no_revs = no_revs.split()[0]
		    img_link = webD.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img").get_attribute("src")
		    names.append(name)
		    ratings.append(rating)
		    no_revs_list.append(no_revs)
		    img_links.append(img_link)
		except:
		    pass

	df_flipkart = pd.DataFrame(columns=["name", "rating", "no_of_reviews", "img_links"])
	df_flipkart["name"] = names
	df_flipkart["rating"] = ratings
	df_flipkart["no_of_reviews"] = no_revs_list
	df_flipkart["img_links"] = img_links

	df_flipkart.to_csv(os.path.join(path,"df_flipkart.csv"))
	