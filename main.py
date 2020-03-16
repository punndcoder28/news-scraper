import feedparser as fp
import json
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime

LIMIT = 4

data = {}
data['newspapers'] = {}

with open('data.json') as data_file:
    companies = json.load(data_file)

count = 1

for company, value in companies.items():
    d = fp.parse(value['rss'])
    print("Downloading articles from ", company)
    newsPaper = {
        "rss": value['rss'],
        "link": value['link'],
        "articles": []
    }
    for entry in d.entries:
        if hasattr(entry, 'published'):
            if count > LIMIT:
                break
            article = {}
            article['link'] = entry.link
            date = entry.published
            print(date)
            article['published'] = date
            try:
                content = Article(entry.link)
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            article['title'] = content.title
            article['text'] = content.text
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, ", url: ", entry.link)
            count = count + 1
    count = 1
    data['newspapers'][company] = newsPaper

try:
    with open('scraped_articles.json', 'w') as outfile:
        json.dump(data, outfile)
except Exception as e: print(e)