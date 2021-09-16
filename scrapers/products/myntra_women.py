from selenium import webdriver
import csv
from random import random

DRIVER_PATH = 'E:\ChromeDriver\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

parentURL = 'https://www.myntra.com/'

indianAndFusionWear = [
    'women-kurtas-kurtis-suits',
    'ethnic-tops',
    'women-ethnic-wear',
    'women-ethnic-bottomwear',
    'skirts-palazzos',
    'saree',
    'dress-material',
    'lehenga-choli',
    'dupatta-shawl',
    'women-jackets',
]

WesternWear = [
    'dresses',
    'jumpsuits',
    'tops',
    'women-jeans',
    'women-trousers',
    'women-shorts-skirts',
    'women-shrugs',
    'women-sweaters-sweatshirts',
    'women-jackets-coats',
    'women-blazers-waistcoats',
]

# dictionary = {}
headers = ['gender', 'category', 'image',
           'brand', 'description', 'price', 'rating']


with open('myntra_women.csv', 'a', newline='') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for li in [indianAndFusionWear, WesternWear]:
        for i in li:

            url = parentURL + i
            print(url)
            driver.get(url)
            images = driver.find_elements_by_css_selector("img.img-responsive")
            infos = driver.find_elements_by_css_selector(
                "div.product-productMetaInfo")

            k = 0
            for image, info in zip(images, infos):
                print(k)
                k += 1
                gender = "F"
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
                    brand = info.find_element_by_class_name(
                        'product-brand').text
                    # print(brand)
                except:
                    pass
                try:
                    description = info.find_element_by_class_name(
                        'product-product').text
                except:
                    pass
                    # print(description)
                try:
                    price = info.find_element_by_class_name(
                        'product-discountedPrice').text
                    # print(price)
                except:
                    pass
                rating = round((random() * 2) + 3, 1)
                w.writerow([gender, category, imageURL,
                            brand, description, price, rating])
            print("done")

            # w.writerows(rows)
            # for row in rows:
            #     print(row)

driver.quit()
