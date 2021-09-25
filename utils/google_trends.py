from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["Shirt"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='IN', gprop='')

print(pytrends.interest_over_time())