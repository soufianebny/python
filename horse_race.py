#!/usr/bin/env python

'''
Description: 
Simple horse race game. You choose how many horses racing and bet on one of them. Optionally, you can set race tours (default 100 tours).

Example:
horse_race.py --horses 10 --bet 5
'''

import logging
import random
import argparse
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def prepare_arena(horses):
    arena = {}
    for i in range(1,horses+1):
        arena.update({f'h{i}':'0'})
    logging.info(f'#### Race ready: {arena}')
    return arena

def random_run(current_tours,length_stop):
    return random.randint(current_tours,length_stop)

def race(arena, tours):
    current_tours = ["0"]
    for tour in range(1,tours+1,1):
        logging.debug(f'Race tour: {tour}')
        for horse in arena:        
            current_horse_run = random_run(int(current_tours[-1]),tour)
            arena.update({horse:int(arena.get(horse))+current_horse_run})
            logging.debug(f'----------Horse {horse} runs: {current_horse_run}')
        current_tours.append(tour)
        logging.debug(f'----------Race status after this tour: {arena}')
    return arena

def get_race_winner(race_results,tours,bet):          
    sorted_race_results = dict(sorted(race_results.items(), key=lambda item: item[1], reverse=True))
    logging.info(f'#### Race ended, final scores: {sorted_race_results}')
    if list(sorted_race_results.keys()).index("h"+str(bet)) == 0:
        print("You win !")
    else:
        print("You lose !") 

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--horses', type=int, required=True, help="Number of horses to race.")
    parser.add_argument('-t', '--tours', type=int, required=False, default=100, help="(optional) How many tours.")
    parser.add_argument('-b', '--bet', type=int, required=True, default=False, help="Bet on one of the participating horses.")
    args = parser.parse_args()
    if not (1 <= args.bet <= args.horses):
        print("You can not bet on a horse not participating in the race.")
        sys.exit(1)  
    return args

race_args = arg_parser()
arena=prepare_arena(race_args.horses)
race_results = race(arena, race_args.tours)
get_race_winner(race_results,race_args.tours,race_args.bet)
