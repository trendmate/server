import pandas as pd
import os

def get_myntra(webD, path):
	webD.get("https://www.myntra.com/tshirts")

	links = []
	i = 0
	while(i < 2):
		try:
		    productInfoList = webD.find_elements_by_class_name("product-base")
		    for el in productInfoList:
		        pp1 = el.find_element_by_tag_name("a")
		        links.append(pp1.get_attribute("href"))
		    nav = webD.find_element_by_xpath("/html/body/div[2]/div/div[1]/main/div[3]/div[2]/div/div[2]/section/div[2]/ul")
		    butt = nav.find_elements_by_tag_name("li")[-1]
		    butt_anc = butt.find_element_by_tag_name("a")
		    butt_anc.click()
		except:
		    pass
		i += 1

	img_links = []
	for link in links:
		webD.get(link)
		try:
		    img_l = webD.find_element_by_xpath("/html/body/div[2]/div/div/div/main/div[2]/div[1]/div[1]/div/div[1]").get_attribute("style")[23:-3]
		    img_links.append(img_l)
		except:
		    pass

	df_myntra = pd.DataFrame(columns=["img_links"])
	df_myntra["img_links"] = img_links

	df_myntra.to_csv(os.path.join(path,'myntra.csv'))