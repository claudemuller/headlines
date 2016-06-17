import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib.parse
import requests

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}
DEFAULTS = {'publication': 'bbc',
            'city': 'Johannesburg,ZA'}
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/' \
               'weather?q={}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
CURRENCY_URL = 'https://openexchangerates.org/api/latest.json?app_id=fe3ad607fc1c49f8a52454385be23afe'

@app.route('/')
def home():
    # Get customised headlines based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    # Get customised weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template('home.html',
                           articles=articles,
                           weather=weather)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = requests.get(url).text
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']}

    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)
