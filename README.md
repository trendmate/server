## Hosting

```
git chekcout main
git pull 
git checkout hosting
git checkout master -- config
git checkout master -- models
git checkout master -- scrapers
git checkout master -- server
git checkout master -- utils
git checkout master -- .gitignore
git checkout master -- app.py
git checkout master -- .Procfile
git checkout master -- requirements.txt
git checkout master -- runtime.txt
git checkout master -- server_requirements.txt
git checkout master -- server_setup.sh
git commit -m "v0.1"
git push
```

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

### [Scraped Images](https://drive.google.com/file/d/1WI95J600swejVn2-6vzhFRuxKfZa_gQh/view?usp=sharing)

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
