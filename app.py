# server
from flask import Flask, request

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
    amazon_df = pd.read_csv('./data/products_data/cloud_scraped_amazon.csv')
    myntra_men_df = pd.read_csv('./data/products_data/myntra_men.csv')
    myntra_women_df = pd.read_csv('./data/products_data/myntra_women.csv')

    for index, row in myntra_men_df.iterrows():

        download_image(row['image'])
        img = tf.keras.preprocessing.image.load_img(
            filename + row['image'].split('/').pop(), target_size=IMG_SIZE
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(np.argmax(score), 100 * np.max(score))
        )

        doc_ref = db.collection(u'products').document()
        doc_ref.set({
            u'brand': row['brand'],
            u'category': row['category'],
            u'description': row['description'],
            u'image': row['image'],
            u'title': row['title'],
            u'price': row['price'],
            u'rating': row['rating'],
            u'review_no': len(row['reviews']),
            u'share_no': 0,
            u'trendiness': np.argmax(score).item(),
            u'url': row['url'],
            u'demographic': '',
            u'store': '',
            u'occasion': '',
        })


def add_articles():
    res = articles.sort_articles()
    print(res)
    for x in range(0, len(res)):
        doc_ref = db.collection(u'articles').document()
        doc_ref.set({
            u'title': res.iloc[x]['heading'],
            u'by': res.iloc[x]['author'],
            u'dateTime': res.iloc[x]['datetime'],
            u'medias': [res.iloc[x]['img'],res.iloc[x]['img2'],],
            u'share_no': 0,
            u'tags': [],
            u'description': res.iloc[x]['description'] + '\n' + res.iloc[x]['description2'] + '\n' +res.iloc[x]['below_title_summary'],
            u'products': [],
            u'trendiness': res.iloc[x]['trendiness'],
        })


def flow():
    add_products()
    add_articles()


def init():
    global model
    model = tf.keras.models.load_model('./models/vgg/')
    scraper.init()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=flow, trigger="interval", hours=24)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    init()
    scraper.scrape()
    # flow()
    app.run()
