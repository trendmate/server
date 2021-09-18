## Git workflow

```
git checkout <individual branch>
git pull origin main
do your work
git add .
git commit -m "useful commit message"
git push
make a PR on github
test
Merge
```

## Getting started

```
virtualenv env
./env/Scripts/activate
pip install -r requirements.txt
```

### Server

```
flask run
```

### tests

```
pytest
```

## Structure

```
├── data // put data files (json, csv etc) here
│   ├── blog
│   ├── image
│   └── reviews
├── models // put models and their weights (.h, .pkl) here
├── notebooks // put .ipynb 's here
├── scrapers // scraper scripts
│   ├── blog
│   ├── products
│   └── social
├── tests
├── utils // misc
├── server // server files
└── app.py // server entrypoint
```

## Datasets

### [Amazon](https://nijianmo.github.io/amazon/index.html)

```
reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
asin - ID of the product, e.g. 0000013714
reviewerName - name of the reviewer
vote - helpful votes of the review
style - a disctionary of the product metadata, e.g., "Format" is "Hardcover"
reviewText - text of the review
overall - rating of the product
summary - summary of the review
unixReviewTime - time of the review (unix time)
reviewTime - time of the review (raw)
image - images that users post after they have received the product
```

## Models used

* EfficientNet
