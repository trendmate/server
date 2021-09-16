import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures


urls = {
	'Tech': ['https://www.instagram.com/azur_laptop/', 'https://www.instagram.com/kouba_dealz/'],

	'Clothes': ['https://www.instagram.com/vog_dz/', 'https://www.instagram.com/miss.chic.dz/', 'https://www.instagram.com/ramseys_luxury/',
				'https://www.instagram.com/la_baronne_alg/'],

	'Shoes' : ['https://www.instagram.com/oscar._.shop/', 'https://www.instagram.com/zara_el_biar/', 
			'https://www.instagram.com/coquette_chaussure_1mai_alger/', 'https://www.instagram.com/anso.dz/'],

	'Sport' : ['https://www.instagram.com/dzprofoot', 'https://www.instagram.com/footland.dz/', 'https://www.instagram.com/dzfreestyle/',
				'https://www.instagram.com/pumaalgeria_fans/'],

	'Deco': ['https://www.instagram.com/handmade_art_dz/', 'https://www.instagram.com/unlimited_passion_art/'],

	'Accessories' : ['https://www.instagram.com/ilyes_bijoux/', 'https://www.instagram.com/jadedesignalger/', 'https://www.instagram.com/boutique_sf_/'],

	'Cosmetics' : ['https://www.instagram.com/grossomodo_cosmetics/', 'https://www.instagram.com/cosmetique_walid_kouba__/', 
					'https://www.instagram.com/paradis_vert_cosmetics/', 'https://www.instagram.com/concentredebienetre/'],

	'Terroir' : ['https://www.instagram.com/greenminddz/', 'https://www.instagram.com/maison_du_terroir_algerien/', 'https://www.instagram.com/leterroirdesgourmets/', 
				'https://www.instagram.com/ecomarketdz/', 'https://www.instagram.com/bahjamadinalgerie/'],

	'Handmade-Soap' : ['https://www.instagram.com/murjcosmetics/', 'https://www.instagram.com/lyderme_savonnerie_artisanale/']
}


# # Sequential Version
def get_products(category):
	products = []
	for url in urls[category]:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, features="lxml")
		script = soup.findAll('script', {'type': 'text/javascript'})[3].text
		raw_data = script.replace(';', '').replace('window._sharedData = ', '')
		jsondata = json.loads(raw_data)
		user_data = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']
		posts = user_data['edge_owner_to_timeline_media']['edges']
		for post in posts:
			products.append(post)
	return products

# Parallel Version
# def get_products(category):
# 	products = []
# 	with concurrent.futures.ThreadPoolExecutor() as executor:
# 		results = executor.map(get_products_by_shop, urls[category])
# 	for result in results:
# 		for post in result:
# 			products.append(post)			
# 	return products

def get_products_by_shop(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	script = soup.findAll('script', {'type': 'text/javascript'})[3].text
	raw_data = script.replace(';', '').replace('window._sharedData = ', '')
	jsondata = json.loads(raw_data)
	user_data = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']
	posts = user_data['edge_owner_to_timeline_media']['edges']
	return posts

# JSON Version
def get_products_json(category):
	products = []
	for i in range(0, len(urls[category])):
		filename = 'data/' + category + str(i) + '.json'
		with open(filename) as json_file:
			data = json.load(json_file)
			jsondata = json.loads(data)
			user_data = jsondata['entry_data']['ProfilePage'][0]['graphql']['user']
			posts = user_data['edge_owner_to_timeline_media']['edges']
			for post in posts:
				products.append(post)
	return products


# @app.route('/shop/<category>/<int:numpage>')
# def shop(category, numpage):
# 	if numpage == 1:
# 		products = get_products_json(category)
# 		likes = [products[i]['node']['edge_liked_by']['count'] for i in range(0, len(products))]
# 		img = [products[i]['node']['display_url'] for i in range(0, len(products))]
# 		shop = [products[i]['node']['owner']['username'] for i in range(0, len(products))]
# 		descr = []
# 		for i in range(0, len(products)):
# 			if not products[i]['node']['edge_media_to_caption']['edges']:
# 				descr.append("No description available.")
# 			else:
# 				descr.append(products[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
# 		link = [('https://www.instagram.com/p/' + products[i]['node']['shortcode']) for i in range(0, len(products))]
# 	else:
# 		img = request.args.getlist('img')
# 		likes = request.args.getlist('likes')
# 		likes = list(map(int, likes))
# 		shop = request.args.getlist('shop')
# 		descr = request.args.getlist('descr')
# 		link = request.args.getlist('link')

# 	return render_template('shop.html', category=category, likes=likes, img=img, shop=shop, descr=descr, link=link, numpage=numpage)

# Heroku
# @app.route('/shop/<category>/<int:numpage>')
def shop(category, numpage):
	
	products = get_products(category)
	likes = [products[i]['node']['edge_liked_by']['count'] for i in range(0, len(products))]
	#img = [products[i]['node']['display_url'] for i in range(0, len(products))]
	img = [f"https://instagram-shop-scraper.herokuapp.com/static/img/core-img/{category}.jpg" for _ in range(0, len(products))]
	shop = [products[i]['node']['owner']['username'] for i in range(0, len(products))]
	descr = []
	for i in range(0, len(products)):
		if not products[i]['node']['edge_media_to_caption']['edges']:
				descr.append("No description available.")
		else:
			descr.append(products[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
	link = [('https://www.instagram.com/p/' + products[i]['node']['shortcode']) for i in range(0, len(products))]

	return [category, likes, img, shop, descr, link, numpage]


# @app.route('/product_details/<category>/<shop>', methods=['GET'])
# def product_details(category, shop):
# 	img = request.args['img']
# 	likes = request.args['likes']
# 	descr = request.args['descr']
# 	link = request.args['link']
# 	return render_template('product-details.html', category=category, shop=shop, likes=likes, descr=descr, img=img, link=link)

print(shop("Clothes", 1))