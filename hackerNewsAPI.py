#!/usr/bin/env python

import requests,sys
from operator import itemgetter

'''
Description: Get top stories from news.ycombinator.com (API doc: https://github.com/HackerNews/API).

Input:
     arg1 = number of articles to fetch. Default 10.
Output:
     Articles sorted by score.

Examples:
hackerNewsAPI.py 5
'''

def getTopStoriesID(nb_article):
    ''' Get IDs of top stories '''
    try:
        r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    response = r.json()
    top_article_IDs = []
    for article in response[:nb_article]:
        top_article_IDs.append(article)
    return top_article_IDs

def getStoriesInfos(top_stories_IDs):
    '''using ID, for each ID (each story) get its informaton (title, ...etc)'''
    stories = []
    for story_id in top_stories_IDs:
        stories_dict = {}
        try:
            r = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
            r.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
            sys.exit(1)
        response = r.json()

        # for each story, store its info into the dict "stories_dict" (this dict is overwrited on each iteration)
        # then append it to the list "stories"
        # without using list, the dict will be overwrited each time (because we use the same Keys)
        stories_dict["Title"] = response["title"]
        stories_dict["Score"] = response["score"]
        stories_dict["Link"] = response["url"]
        stories.append(stories_dict)

    #sort by Score
    stories = sorted(stories,key=itemgetter('Score'),reverse=True)

    for story in stories:
        print(f'Title: {dict(story)["Title"]}')
        print(f'Score: {dict(story)["Score"]}')
        print(f'Link: {dict(story)["Link"]}')
        print()

def arg_parser():
    if len(sys.argv) != 2:
        nb_article = 10
    else:
        try:
            nb_article = int(sys.argv[1])
        except ValueError:
            print("<nb_article> must be an integer")
            sys.exit(1)
    return nb_article

top_stories = getTopStoriesID(arg_parser())
getStoriesInfos(top_stories)
