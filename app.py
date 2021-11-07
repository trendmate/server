# server
from flask import Flask, request
import os
import re
from dateutil import parser

# AI
import tensorflow as tf
import numpy as np
import pandas as pd

# downloader
import requests
import shutil

# scheduling libs
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# ours
import scrapers.scraper as scraper
import server.articles as articles

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(
    './config/trend-mate-firebase-adminsdk-b6xj0-a86d62f4f5.json')
firebase_admin.initialize_app(cred)

global model, filename, IMG_SIZE, db

db = firestore.client()

IMG_SIZE = (160, 160)
filename = './data/images/'

app = Flask(__name__)


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def download_image(image_url):
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename + image_url.split('/').pop(), 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')


@app.route('/', methods=['GET'])
def home_page():
    return 'Server is On!'


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


def add_products():
    global IMG_SIZE, filename
    amazon_df = pd.read_csv('./data/products_data/Amazon_Women.csv')
    # myntra_men_df = pd.read_csv('./data/products_data/myntra_men.csv')
    # myntra_women_df = pd.read_csv('./data/products_data/myntra_women.csv')


    for index, row in amazon_df.iterrows():
        try:
            download_image(row['Links'])
            img = tf.keras.preprocessing.image.load_img(
                filename + row['Links'].split('/').pop(), target_size=IMG_SIZE
            )
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                "This image most likely belongs to {} with a {:.2f} percent confidence."
                .format(np.argmax(score), 100 * np.max(score))
            )

            review_no = list(map(int, re.findall(
                r'\d+', str(row['Reviews'])))) if row['Reviews'] is not None else 0
            review_no = review_no[0] if len(review_no) > 0 else 0

            perc = int((row['Discount'][(row['Discount'].index('(')+1):(len(row['Discount'])-2)]).replace(',',''))
            dis = int((row['Discount'][(row['Discount'].index('₹')+1):(row['Discount'].index(' ',(row['Discount'].index(' ')+1)))]).replace(',',''))

            price = dis/perc*100

            # price = row['price'] if isinstance(
            #     row['price'], float) else float(row['price'][4:])

            doc_ref = db.collection(u'temp_products').document()
            doc_ref.set({
                u'brand': row['Brand'],
                u'category': row['Category'],
                u'description': row['Description'],
                u'image': row['Links'],
                u'title': row['Description'],
                u'price': price,
                u'rating': row['Rating'],
                u'review_no': review_no,
                # [int(i) for i in row['reviews'].split() if i.isdigit()][0],
                # row['reviews'][0:row['reviews'].index('k')],011
                u'share_no': 0,
                u'trendiness': int(np.argmax(score)),  # pm_prob,
                u'confidence': float(100 * np.max(score)),
                u'url': '',
                u'demographic': 'men',
                u'store': 'amazon',
                u'occasion': '',
            })

            print(index)
        
        except:
            pass

    # for index, row in amazon_df.iterrows():

    #     download_image(row['image'])
    #     img = tf.keras.preprocessing.image.load_img(
    #         filename + row['image'].split('/').pop(), target_size=IMG_SIZE
    #     )
    #     img_array = tf.keras.preprocessing.image.img_to_array(img)
    #     img_array = tf.expand_dims(img_array, 0)  # Create a batch

    #     predictions = model.predict(img_array)
    #     score = tf.nn.softmax(predictions[0])

    #     print(
    #         "This image most likely belongs to {} with a {:.2f} percent confidence."
    #         .format(np.argmax(score), 100 * np.max(score))
    #     )

    #     review_no = list(map(int, re.findall(
    #         r'\d+', str(row['reviews'])))) if row['reviews'] is not None else 0
    #     review_no = review_no[0] if len(review_no) > 0 else 0

    #     price = row['price'] if isinstance(
    #         row['price'], float) else float(row['price'][4:])

    #     doc_ref = db.collection(u'temp_products').document()
    #     doc_ref.set({
    #         u'brand': row['brand'],
    #         u'category': '',
    #         u'description': row['description'],
    #         u'image': row['image'],
    #         u'title': row['description'],
    #         u'price': price,
    #         u'rating': row['rating'],
    #         u'review_no': review_no,
    #         # [int(i) for i in row['reviews'].split() if i.isdigit()][0],
    #         # row['reviews'][0:row['reviews'].index('k')],011
    #         u'share_no': 0,
    #         u'trendiness': int(np.argmax(score)),  # pm_prob,
    #         u'confidence': float(100 * np.max(score)),
    #         u'url': row['url'],
    #         u'demographic': 'men',
    #         u'store': 'myntra',
    #         u'occasion': '',
    #     })

        # download_image(row['image'])
        # img = mpimg.imread(filepath + row['image'].split('/').pop())
        # img = resize(img, (320, 192, 3))

        # #Find the encoding for it
        # temp_arr = []
        # temp_arr.append(img)
        # img_enc = encoder.predict(np.array(temp_arr))
        # flattened_enc = img_enc.flatten()

        # #Predict its popularity
        # pm_prob = pm_model.predict(np.array([flattened_enc]))
        # pm_prob = pm_prob[0][0]
        # print("The predicted popularity is", pm_prob)


def add_articles():
    res = articles.sort_articles()
    res.to_csv('./data/blog_data/articles_sorted.csv')
    print(res)
    for x in range(0, len(res)):
        doc_ref = db.collection(u'temp_articles').document()
        doc_ref.set({
            u'title': res.iloc[x]['heading'],
            u'by': res.iloc[x]['author'],
            u'dateTime': firestore.SERVER_TIMESTAMP,
            u'medias': [{u'mediaId': '', u'type': 0, u'url': res.iloc[x]['img'], u'title': '', }, {u'mediaId': '', u'type': 0, u'url': res.iloc[x]['img2'], u'title': '', },],
            u'share_no': 0,
            u'tags': [],
            u'description': str(res.iloc[x]['description']) + '\n' + str(res.iloc[x]['description2']) + '\n' + str(res.iloc[x]['below_title_summary']),
            u'products': [],
            u'trendiness': res.iloc[x]['trendiness'],
        })

def stringToTimeStamp(s):
    mqtt_timestamp = parser.parse(s)
    mqtt_timestamp_rfc3339 = rfc3339(mqtt_timestamp, utc=True, use_system_timezone=False)
    return mqtt_timestamp

def flow():
    add_products()
    # add_articles()


def init():
    global encoder, pm_model, model
    # print("Tf Version : " + tf.__version__)
    # model = tf.keras.models.load_model('./models/image_model.h5')
    # encoder = tf.keras.models.load_model('encoder', compile=False)
    # pm_model = tf.keras.models.load_model('pm_model', compile=False)
    scraper.init()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=flow, trigger="interval", hours=24)
    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())

def addBrands():
    myntra_men_new = pd.read_csv('./data/products_data/myntra_men_scraped_data_complete.csv')
    for index, row in myntra_men_new.iterrows():
        print(row)
        doc_ref = db.collection(u'brands').document(row['brand'])
        doc_ref.set({
            u'name':row['brand']
        })

if __name__ == '__main__':
    # init()
    # scraper.scrape()
    # flow()
    addBrands()
    app.run()
