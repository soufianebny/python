#!/usr/bin/env python

'''
Description: Get news articles using https://newsapi.org/

Examples:
Top news & search in top news:
    Top UK sport news:
        news_api.py top -o gb -c sports

    Search for android in top US news:
        news_api.py top -o us -c technology -k android

Search:
    Search yesterday linux related news:
        news_api.py search -k linux

Advanced search:
    Search Red Hat related news. Use quotes to get exact match:
        news_api.py search -k '"Red Hat"'

    More search this time using AND keywords:
        news_api.py search -k 'systemd AND "blue screen of death"' -f 2023-12-01

    Search linux related news since the given date and show the 50 first ones:
        news_api.py search -k linux -f 2023-12-24 -n 50
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

def get_top_headlines(country,category,nb_news,keyword):
    '''https://newsapi.org/docs/endpoints/top-headlines'''
    try:
        headers = {'Authorization': NEWSAPI_APIKEY}
        if keyword:
            params = {'country':country, 'category':category, 'pageSize': nb_news, 'q':keyword}
        else:
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

def main():
    get_APIKEY()
    parser = argparse.ArgumentParser()
    parser.add_argument("function", 
                        nargs="?",
                        choices=['top', 'search'],
                        # default='top',
                        )
    args, sub_args = parser.parse_known_args()

    if args.function == "top":
        parser =  argparse.ArgumentParser()
        parser.add_argument('-o', '--country', type=str, required=True, 
                            help="The 2-letter ISO 3166-1 code of the country you want to get headlines for.")
        parser.add_argument('-c', '--category', type=str, required=False, default='general', 
                            choices=['general','business','entertainment','health','science','sports','technology'],
                            help="(Optional, default: general) The category you want to get headlines for.")
        parser.add_argument('-k', '--keyword', type=str, required=False, 
                            help='''Keywords or a phrase to search for.''')
        parser.add_argument('-n', '--nb_news', type=int, required=False, default='20',
                            help="(Optional, default: 20) The number of results to return. Max 100.")
        args = parser.parse_args(sub_args)
        get_top_headlines(country=args.country, category=args.category, nb_news=args.nb_news, keyword=args.keyword)

    elif args.function == "search":
        parser =  argparse.ArgumentParser()
        parser.add_argument('-k', '--keyword', type=str, required=True, 
                            help='''Keywords or phrases to search for in the article title and body.''')
        parser.add_argument('-f', '--from_date', type=str, required=False, default=get_date(1),
                            help="(Optional, default: yesterday) A date and optional time for the oldest article allowed. This should be in ISO 8601 format (e.g. 2023-12-25 or 2023-12-25T19:42:14).")
        parser.add_argument('-n', '--nb_news', type=int, required=False, default='20',
                            help="(Optional, default: 20) The number of results to return. Max 100.")
        args = parser.parse_args(sub_args)
        search_news(keyword=args.keyword, from_date=args.from_date, nb_news=args.nb_news)

main()
