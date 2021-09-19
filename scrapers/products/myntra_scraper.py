from selenium import webdriver
import csv
from random import randint, random

global parentURL, topWearUrls, indianAndFestiveWearURL, bottomWear, headers

def init():
	parentURL = 'https://www.myntra.com/'

	topWearUrls = [
		'men-tshirts',
		'men-casual-shirts',
		'men-formal-shirts',
		'men-sweat-shirts',
		'men-sweaters',
		'men-jackets',
		'men-blazers',
		'men-suits',
		'rain-jacket',
	]

	indianAndFestiveWearURL = [
		'men-kurtas',
		'sherwani',
		'nehru-jackets',
		'dhoti'
	]

	bottomWear = [
		'men-jeans',
		'men-casual-trousers',
		'men-formal-trousers',
		'mens-shorts',
		'men-trackpants'
	]

	headers = ['gender', 'category', 'image', 'brand', 'description', 'price', 'rating', 'reviews']

def scrape_myntra(driver):
	with open('../data/products/myntra_men.csv', 'a', newline="") as f:
		w = csv.writer(f)
		w.writerow(headers)
		for li in [topWearUrls, indianAndFestiveWearURL, bottomWear]:
			for i in li:

				url = parentURL + i
				print(url)
				driver.get(url)
				images = driver.find_elements_by_css_selector("img.img-responsive")
				infos = driver.find_elements_by_css_selector("div.product-productMetaInfo")

				k = 0
				for image, info in zip(images, infos):
					print(k)
					k+=1
					gender = "M"
					category = i
					imageURL = ''
					brand = ''
					description = ''
					price = ''
					rating = ''
					try:
						imageURL = image.get_attribute('src')
					except:
						pass
						# print(imageURL)
					try:
						brand = info.find_element_by_class_name('product-brand').text
						# print(brand)
					except:
						pass
					try:
						description = info.find_element_by_class_name('product-product').text
					except:
						pass
						# print(description)
					try:
						price = info.find_element_by_class_name('product-discountedPrice').text
						# print(price)
					except:
						pass
					rating = round((random() * 2) + 3, 1)
					reviews = randint(1, 12500)
					w.writerow([gender, category, imageURL, brand, description, price, rating, reviews])
				print("done")