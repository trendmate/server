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
<<<<<<< HEAD

global model, filename, IMG_SIZE, db

db = firestore.client()

IMG_SIZE = (160, 160)
filename = 'temp.png'
=======

global model, filename, IMG_SIZE, db

db = firestore.client()

IMG_SIZE = (160, 160)
filename = './data/images/'
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf

app = Flask(__name__)


def download_image(image_url):
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

<<<<<<< HEAD
        with open(filename, 'wb') as f:
=======
        with open(filename + image_url.split('/').pop(), 'wb') as f:
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')


@app.route('/', methods=['GET'])
def home_page():
<<<<<<< HEAD
    # json_data = request.json
    # url = json_data["image_url"]
    # download_image(url)
    # image = tf.keras.preprocessing.image.load_img(
    # 	filename, target_size=IMG_SIZE,
    # )
    # input_arr = tf.keras.preprocessing.image.img_to_array(image)
    # input_arr = np.array([input_arr])
    # predictions = model.predict(input_arr)
    # print(predictions)
=======
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf
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


<<<<<<< HEAD
def flow():
    global IMG_SIZE, filename
    scraper.scrape()
    # amazon_df = pd.read_csv('./data/products_data/cloud_scraped_amazon.csv')
    myntra_men_df = pd.read_csv('./data/products_data/myntra_men.csv')
    # myntra_women_df = pd.read__csv('./data/products/myntra_women.csv')
    print(myntra_men_df['image'])
    download_image(myntra_men_df.iloc[0]['image'])

    img = tf.keras.preprocessing.image.load_img(
        filename, target_size=IMG_SIZE
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(np.argmax(score), 100 * np.max(score))
    )

    doc_ref = db.collection(u'trending_products').document()
    doc_ref.set({
        u'brand': myntra_men_df.iloc[0]['brand'],
        u'cat': myntra_men_df.iloc[0]['category'],
        u'desc': myntra_men_df.iloc[0]['description'],
        u'image': myntra_men_df.iloc[0]['image'],
        u'name': myntra_men_df.iloc[0]['description'],
        u'price': myntra_men_df.iloc[0]['price'],
        u'rating': myntra_men_df.iloc[0]['rating'],
        u'review': myntra_men_df.iloc[0]['reviews'],
        u'url': myntra_men_df.iloc[0]['url'],
        u'trendiness': np.argmax(score).item(),
    })
=======
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

>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf

def add_articles():
    res = articles.sort_articles()
    print(res)
<<<<<<< HEAD
    for x in range(0,len(res)):
        doc_ref = db.collection(u'trending_articles').document()
        doc_ref.set({
            u'heading': res.iloc[x]['heading'],
            u'author': res.iloc[x]['author'],
            u'datetime': res.iloc[x]['datetime'],
            u'below_title_summary': res.iloc[x]['below_title_summary'],
            u'img': res.iloc[x]['img'],
            u'description': res.iloc[x]['description'],
            u'img2': res.iloc[x]['img2'],
            u'description2': res.iloc[x]['description2'],
            u'trendiness': res.iloc[x]['trendiness'],
        })


def init():
    # global model
    # model = tf.keras.models.load_model('./models/vgg/')
    scraper.init()
    # flow()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=flow, trigger="interval", hours=24)
    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())
=======
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
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf


if __name__ == '__main__':
    init()
    scraper.scrape()
<<<<<<< HEAD
    add_articles()
    app.run()
=======
    # flow()
    app.run()
>>>>>>> bc8931155a5ec2d33171a250dee19f8d96c08caf
