from selenium import webdriver
import csv
import time

# Original working code in test3.py
# DRIVER_PATH = 'E:\ChromeDriver\chromedriver_win32\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)

global parentURL, indianAndFusionWear, WesternWear, headers, rows, categories


def init():
    global parentURL, indianAndFusionWear, WesternWear, headers, rows, categories

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

    categories = {
        'women-kurtas-kurtis-suits': 'kurtas-kurtis-suits',
        'ethnic-tops': 'ethnic-tops',
        'women-ethnic-wear': 'ethnic-wear',
        'women-ethnic-bottomwear': 'ethnic-bottomwear',
        'skirts-palazzos': 'skirts-palazzos',
        'saree': 'saree',
        'dress-material': 'dress-material',
        'lehenga-choli': 'lehenga-choli',
        'dupatta-shawl': 'dupatta-shawl',
        'women-jackets': 'jackets',
        'dresses': 'dresses',
        'jumpsuits': 'jumpsuits',
        'tops': 'tops',
        'women-jeans': 'jeans',
        'women-trousers': 'trousers',
        'women-shorts-skirts': 'shorts-skirts',
        'women-shrugs': 'shrugs',
        'women-sweaters-sweatshirts': 'sweaters-sweatshirts',
        'women-jackets-coats': 'jackets-coats',
        'women-blazers-waistcoats': 'blazers-waistcoats',
    }

    headers = ['gender', 'category', 'image',
               'brand', 'description', 'price', 'discount', 'url', 'rating', 'reviews']

    rows = []


def scrape(driver):
    global parentURL, indianAndFusionWear, WesternWear, headers, rows, categories
    total = 0
    for li in [indianAndFusionWear, WesternWear]:
        for i in li:

            url = parentURL + i
            print(url)
            driver.get(url)
            time.sleep(10)
            products = driver.find_elements_by_class_name("product-base")

            k = 0
            URLS = []
            for product in products:
                print(k)
                k += 1
                gender = "F"
                category = categories[i]
                imageURL = ''
                brand = ''
                description = ''
                price = ''
                discount = '0'
                url = ''

                try:
                    URLS.append(product.find_element_by_tag_name(
                        'a').get_attribute('href'))
                    url = URLS[k]
                except:
                    URLS.append('')
                    url = URLS[k]
                    pass

                try:
                    imageURL = driver.find_element_by_xpath(
                        f'//*[@id="desktopSearchResults"]/div[2]/section/ul/li[{str(k + 1)}]/a/div[1]/div/div/div/picture/img').get_attribute('src')
                except Exception as e:
                    try:
                        imageURL = driver.find_element_by_xpath(
                            f'// *[@id="desktopSearchResults"]/div[2]/section/ul/li[{str(k + 1)}]/a/div[1]/div/div/div/picture/source').get_attribute('srcset')
                    except Exception as e:
                        pass
                    pass
                try:
                    brand = product.find_element_by_class_name(
                        'product-brand').text
                except:
                    pass
                try:
                    description = product.find_element_by_class_name(
                        'product-product').text

                except:
                    pass
                try:
                    price = product.find_element_by_class_name(
                        'product-discountedPrice').text
                except:
                    pass

                try:
                    discount = product.find_element_by_class_name(
                        'product-discountPercentage').text
                except:
                    pass

                rows.append([gender, category, imageURL, brand,
                             description, price, discount, url])

            print("done")

            for i in range(total - k, total):
                try:
                    driver.get(URLS[i])
                except:
                    pass
                time.sleep(3)
                rating = ''
                reviews = ''

                if rows[i][2] == '':
                    try:
                        rows[i][2] = driver.find_element_by_class_name(
                            'image-grid-image').value_of_css_property('background-image').lstrip('url("').rstrip('")')
                    except Exception as e:
                        print(e)
                        pass
                    print(rows[i][2])
                try:
                    rating = driver.find_element_by_xpath(
                        '//*[@id="detailedRatingContainer"]/div[2]/div[1]/div[1]/span[1]'
                    ).text
                except:
                    pass

                try:
                    reviews = driver.find_element_by_xpath(
                        '//*[@id="detailedRatingContainer"]/div[2]/div[1]/div[2]').text
                except:
                    pass

                rows[i].append(rating)
                rows[i].append(reviews)
                driver.back()
                time.sleep(3)

    with open('./data/products_data/myntra_women_new.csv', 'w', newline='\n') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
