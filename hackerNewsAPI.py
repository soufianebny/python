#!/usr/bin/env python

import requests,sys
from operator import itemgetter

'''
Description: Get best stories from news.ycombinator.com (API doc: https://github.com/HackerNews/API).

Input:
     arg1 = number of articles to fetch. Default 10.
Output:
     Articles sorted by score.

Examples:
hackerNewsAPI.py 5
'''

def get_best_stories_ids(nb_article):
    ''' get IDs of best stories '''
    try:
        r = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json')
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    response = r.json()
    best_article_IDs = []
    for article in response[:nb_article]:
        best_article_IDs.append(article)
    return best_article_IDs

def get_stories_by_id(best_stories_IDs):
    ''' get information (title, url, ...) of stories by ID '''
    stories = []
    for story_id in best_stories_IDs:
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
        #work-around: sometimes stories miss url section
        stories_dict["Link"] = response["url"] if "url" in response else "None"
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

best_stories = get_best_stories_ids(arg_parser())
get_stories_by_id(best_stories)
