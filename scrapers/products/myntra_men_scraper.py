from selenium import webdriver
import csv
import time

# Original working code in test3.py
# DRIVER_PATH = 'E:\ChromeDriver\chromedriver_win32\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)

global parentURL, topWearUrls, indianAndFestiveWearURL, bottomWear, headers, rows, categories

def init():
    global parentURL, topWearUrls, indianAndFestiveWearURL, bottomWear, headers, rows, categories
        
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
        'dhoti',
    ]

    bottomWear = [
        'men-jeans',
        'men-casual-trousers',
        'men-formal-trousers',
        'mens-shorts',
        'men-trackpants',
    ]

    categories = {
        'men-tshirts': 'tshirts',
        'men-casual-shirts': 'casual-shirts',
        'men-formal-shirts': 'formal-shirts',
        'men-sweat-shirts': 'sweat-shirts',
        'men-sweaters': 'sweaters',
        'men-jackets': 'jackets',
        'men-blazers': 'blazers',
        'men-suits': 'suits',
        'rain-jacket': 'rain-jacket',
        'men-kurtas': 'kurtas',
        'sherwani': 'sherwani',
        'nehru-jackets': 'nehru-jackets',
        'dhoti': 'dhoti',
        'men-jeans': 'jeans',
        'men-casual-trousers': 'casual-trousers',
        'men-formal-trousers': 'formal-trousers',
        'mens-shorts': 'shorts',
        'men-trackpants': 'trackpants',
    }

    headers = ['gender', 'category', 'image',
            'brand', 'description', 'price', 'discount', 'url', 'rating', 'reviews']


    rows = []

def scrape(driver):
    global parentURL, topWearUrls, indianAndFestiveWearURL, bottomWear, headers, rows, categories
    total = 0
    for li in [topWearUrls, indianAndFestiveWearURL, bottomWear]:
        for i in li:

            url = parentURL + i
            print(url)
            driver.get(url)
            time.sleep(10)
            products = driver.find_elements_by_class_name("product-base")
            # products = [products[0]]
            k = 0
            URLS = []
            for product in products:
                print(k)
                k += 1
                total += 1
                gender = "M"
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
                print(url)
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

    with open('./data/products_data/myntra_men_new.csv', 'w', newline='\n') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
