#!/usr/bin/env python

'''
Description: Get news articles from https://newsapi.org/

Examples:
Top 5 morocco news:
    news_api.py get_top_headlines -o ma -n 5

Top england sport news:
    news_api.py get_top_headlines -o gb -c sports

Search yesterday real madrid news:
    news_api.py search_news -k "real madrid"

Search linux related news since the given date and show the 50 first ones.
    news_api.py search_news -k linux -f 2023-12-24 -n 50
    '''

import argparse
import requests
import json
from datetime import datetime, timedelta
import sys
import os

def get_APIKEY():
    try:
        global NEWSAPI_APIKEY
        NEWSAPI_APIKEY = os.environ['NEWSAPI_APIKEY']
    except KeyError:
        print("Could not find the NEWSAPI_APIKEY env. variable. Make sure it is set and exported.")
        sys.exit(1)
    else:
        return NEWSAPI_APIKEY

def articles_formatter(articles):
    for article in articles:
        print(f'Title: {article['title']}')
        print(f'URL:   {article['url']}')
        print()

def get_date(days_delta):
    today = datetime.now()
    yesterday = today - timedelta(days=days_delta)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    return formatted_yesterday

def get_top_headlines(country,category,nb_news):
    '''https://newsapi.org/docs/endpoints/top-headlines'''
    try:
        headers = {'Authorization': NEWSAPI_APIKEY}
        params = {'country':country, 'category':category, 'pageSize': nb_news}
        r = requests.get('https://newsapi.org/v2/top-headlines', headers=headers, params=params)
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    articles = json.loads(r.text)['articles']
    articles_formatter(articles)

def search_news(keyword,from_date,nb_news):
    '''https://newsapi.org/docs/endpoints/everything''' 
    try:
        headers = {'Authorization': NEWSAPI_APIKEY}
        params = {'q':keyword, 'from':from_date, 'sortBy': 'relevancy', 'pageSize': nb_news}
        r = requests.get('https://newsapi.org/v2/everything', headers=headers, params=params)
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    articles = json.loads(r.text)['articles']
    articles_formatter(articles)

#Todo
def search_in_top_headlines():
    '''https://newsapi.org/docs/endpoints/top-headlines'''
    pass

def main():
    get_APIKEY()
    parser = argparse.ArgumentParser()
    parser.add_argument("function", 
                        nargs="?",
                        choices=['get_top_headlines', 'search_news'],
                        default='get_top_headlines',
                        )
    args, sub_args = parser.parse_known_args()

    if args.function == "get_top_headlines":
        parser =  argparse.ArgumentParser()
        parser.add_argument('-o', '--country', type=str, required=True, 
                            help="The 2-letter ISO 3166-1 code of the country you want to get headlines for.")
        parser.add_argument('-c', '--category', type=str, required=False, default='general', 
                            choices=['general','business','entertainment','health','science','sports','technology'],
                            help="(Optional, default: general) The category you want to get headlines for.")
        parser.add_argument('-n', '--nb_news', type=int, required=False, default='20', choices=range(1,101),
                            help="(Optional, default: 20) The number of results to return. 100 is the maximum.")
        args = parser.parse_args(sub_args)
        get_top_headlines(country=args.country, category=args.category, nb_news=args.nb_news)

    elif args.function == "search_news":
        parser =  argparse.ArgumentParser()
        parser.add_argument('-k', '--keyword', type=str, required=True, 
                            help='''Keywords or phrases to search for in the article title and body.
                            Advanced search is supported here:
                            Surround phrases with quotes (") for exact match.
                            Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
                            Prepend words that must not appear with a - symbol. Eg: -bitcoin
                            Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
                            ''')
        parser.add_argument('-f', '--from_date', type=str, required=False, default=get_date(1),
                            help="(Optional, default: yesterday) A date and optional time for the oldest article allowed. This should be in ISO 8601 format (e.g. 2023-12-25 or 2023-12-25T19:42:14).")
        parser.add_argument('-n', '--nb_news', type=int, required=False, default='20', choices=range(1,101),
                            help="(Optional, default: 20) The number of results to return. 100 is the maximum.")
        args = parser.parse_args(sub_args)
        search_news(keyword=args.keyword, from_date=args.from_date, nb_news=args.nb_news)

main()
