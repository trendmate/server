import pandas as pd
import numpy as np
import nltk
from pytrends.request import TrendReq
import statsmodels.api as sm

import spacy
nlp = spacy.load("en_core_web_sm")
from collections import Counter
from string import punctuation

def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp(text.lower())
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result

def sort_articles():
    df = pd.read_csv('./data/blog_data/example_vogue.csv')
    text= []
    for index, row in df.iterrows():
        strin = row['heading'] + ' ' + row['author'] + ' ' + row['below_title_summary'] + ' ' + row['description'] + ' ' + row['description2']
        text += [strin,]
    
    result = []
    for x in text:
        keywords = set(get_hotwords(x))
        words = set(nltk.corpus.words.words())
        f = lambda x: " ".join(w for w in nltk.wordpunct_tokenize(x) if w.lower() in words)
        res = set(map(f,keywords))
        res = [x for x in res if x and len(x)>1]
        result += [res,]
    pytrends = TrendReq(hl='en-US', tz=360)
    datas = []

    for res in result:
        data = pd.DataFrame()
        res = list(res)

        for x in range(0, 10):
            kw_list = [res[x],]
            pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='IN', gprop='')
            data[res[x]] = pytrends.interest_over_time()[res[x]]
        changes = []

        for word in data:
            inp = data[word]
            decomposition = sm.tsa.seasonal_decompose(inp, model='additive')
            mod = sm.tsa.statespace.SARIMAX(inp,
                                            order=(0, 0, 1),
                                            seasonal_order=(1, 1, 1, 12),
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            pred = results.get_prediction(start=pd.to_datetime('2019-10-20'), end=pd.to_datetime('2022-1-19'), dynamic=False)
            end = pred.predicted_mean['2021-09-26']
            start = pred.predicted_mean['2021-09-19']
            change_per = (end-start)/start*100
            print(change_per)
            changes += [change_per,]
        
        datas += [sorted(changes)[len(changes)-1],]

    res_dct = {i: datas[i] for i in range(0, len(datas))}
    res_dct = dict(sorted(res_dct.items(), key=lambda item: item[1]))
    k = 0
    pd_result = pd.DataFrame(columns=df.columns)
    for key in res_dct:
        pd_result.loc[df.index[key]] = df.iloc[key]
        pd_result.loc[key, 'trendiness'] = res_dct[key]
        k+=1
        if k>10:
            continue
    return pd_result
