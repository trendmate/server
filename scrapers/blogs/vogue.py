from selenium import webdriver
import csv

DRIVER_PATH = 'E:\ChromeDriver\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

dictionary = {
    "https://www.vogue.in/vogue-closet/collection/kiara-advanis-smocked-dress-is-all-the-rage-in-sage/": "1150434",
    "https://www.vogue.in/vogue-closet/collection/diana-pentys-on-trend-white-shirt-and-blue-jeans-look-will-become-your-go-to-evening-ensemble/": "1150497",
    "https://www.vogue.in/vogue-closet/collection/4-trackpants-from-disha-patanis-wardrobe-that-prove-that-activewear-isnt-reserved-for-the-gym/": "1150454",
    "https://www.vogue.in/vogue-closet/collection/kareena-kapoor-khans-denim-on-denim-airport-look-is-a-fun-spin-on-the-classic-shirt-and-jeans-combination/": "1150400",
    "https://www.vogue.in/vogue-closet/collection/6-times-sonam-kapoor-ahuja-proved-that-florals-are-the-way-to-go-pictures/": "1150370",
    "https://www.vogue.in/vogue-closet/collection/kriti-sanons-white-tube-top-matching-flared-jeans-are-a-y2k-fashion-revival/": "1150356",
    "https://www.vogue.in/vogue-closet/collection/checks-please-deepika-padukone-is-a-vision-in-green/": "1150295",
    "https://www.vogue.in/vogue-closet/collection/alia-bhatt-makes-a-case-for-monsoon-cool-in-an-all-white-kurta-and-pants-combination/": "1150270",
    "https://www.vogue.in/vogue-closet/collection/11-ananya-panday-crop-tops-youll-want-to-cop/": "1150250",
    "https://www.vogue.in/vogue-closet/collection/malavika-mohanan-aces-elevated-casuals-in-a-leopard-print-sports-bra-and-cycling-shorts/": "1150180",
    "https://www.vogue.in/vogue-closet/collection/we-cant-get-enough-of-this-stunning-blue-suit-jacqueline-fernandez-wore-to-a-film-screening/": "1150087",
    "https://www.vogue.in/vogue-closet/collection/7-stylish-bags-from-janhvi-kapoors-closet-that-make-for-the-perfect-plus-one/": "1150134",
    "https://www.vogue.in/vogue-closet/collection/7-eye-catching-looks-that-prove-kiara-advani-loves-a-pink-moment/": "1150100",
    "https://www.vogue.in/vogue-closet/collection/5-fab-fitness-looks-from-malaika-aroras-closet-that-will-inspire-you-to-get-moving/": "1149972",
    "https://www.vogue.in/vogue-closet/collection/6-unique-resort-wear-outfits-from-mira-rajput-kapoors-closet-that-are-perfect-for-your-next-getaway/": "1149870",
    "https://www.vogue.in/vogue-closet/collection/kareena-kapoor-khan-gives-us-a-lesson-in-colour-blocking/": "1149970",
    "https://www.vogue.in/vogue-closet/collection/malaika-arora-chose-an-ivory-toned-kaftan-with-golden-motifs-for-lounging-in-with-sister-amrita-arora/": "1149842",
    "https://www.vogue.in/vogue-closet/collection/sonam-kapoor-ahuja-chose-a-cropped-blouse-and-skirt-ensemble-in-black-and-white-for-a-night-out/": "1149047",
    "https://www.vogue.in/vogue-closet/collection/sara-ali-khan-chooses-a-white-button-down-for-a-day-at-the-beach/": "1149121",
    "https://www.vogue.in/vogue-closet/collection/katrina-kaif-donned-a-lavender-corset-dress-for-a-day-out-in-turkey/": "1149018",
    "https://www.vogue.in/vogue-closet/collection/anushka-sharma-orange-bikini-black-strapless-swimsuit-pool-beach/": "1148892",
    "https://www.vogue.in/vogue-closet/collection/kriti-sanon-black-white-neon-checkered-dress-gold-necklace-sneakers-mumbai-airport/": "1148816",
    "https://www.vogue.in/vogue-closet/collection/karisma-kapoor-brown-blazer-white-tshirt-trousers-sunglasses-bag-flats-mumbai-airport/": "1148684",
    "https://www.vogue.in/vogue-closet/collection/priyanka-chopra-designer-pantsuits-pink-blue-black-blazers-trousers/": "1148602",
    "https://www.vogue.in/vogue-closet/collection/sara-ali-khan-unique-quirky-bags-pink-glitter-kit-kat-pictures/": "1148483",
}

columns = [
    "heading",
    "author",
    "datetime",
    "below_title_summary",
    "img",
    "description",
    "img2",
    "description2",
    "img3",
    "description3",
    "celebrity",
    "price",
    "occasion"
]

with open('vogue.csv', 'a', newline="") as f:
    w = csv.writer(f)
    w.writerow(columns)
    for url, id in dictionary.items():
        driver.get(url)
        heading = ""
        author = ""
        datetime = ""
        below_title_summary = ""
        img = ""
        description = ""
        img2 = ""
        description2 = ""
        img3 = ""
        description3 = ""
        celebrity = ""
        price = ""
        occasion = ""



        try:
            heading = driver.find_element_by_xpath(f'//*[@id="post-{id}"]/header/h1').text
        except:
            pass
        try:
            author = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/header/div[2]/address/ul/li/a/span').text
        except:
            pass
        try:
            datetime = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/header/div[2]/time').text
        except:
            pass
        try:
            below_title_summary = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/header/h2').text
        except:
            pass
        try:
            img = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/header/figure/img').get_attribute('src')
        except:
            pass
        try:
            description = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[1]/p[1]').text
        except:
            pass
        try:
            img2 = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[1]/p[2]/a/img').get_attribute('src')
        except:
            pass
        try:
            description2 = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[1]/p[3]').text
        except:
            pass
        try:
            description3 = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[1]/p[4]').text
        except:
            pass
        try:
            img3 = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[1]/div/div/div[1]/img').get_attribute('src')
        except:
            pass
        
        try:
            celebrity = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[3]/ul[1]/li[2]/a').text
        except:
            pass

        try:
            price = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[3]/ul[3]/li[2]/a').text
        except:
            pass

        try:
            occasion = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[3]/ul[2]/li[2]/a').text
        except:
            pass

        try:
            productType = driver.find_element_by_xpath(
                f'//*[@id="post-{id}"]/div[3]/ul[4]/li[2]/a').text
        except:
            pass
        
        w.writerow([heading,
                    author,
                    datetime,
                    below_title_summary,
                    img,
                    description,
                    img2,
                    description2,
                    img3,
                    description3,
                    celebrity,
                    price,
                    occasion])


driver.close()
