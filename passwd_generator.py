#!/usr/bin/env python

'''
Description: Script to generate a random password/passphrase.

Input:
    password length. Default 20.
    generator type, simple or complex. Default complex.
    boolean switch to enable password analysis.

Examples:
Generate a 20 characters password:
    passwd_generator.py
Generate a 10 characters password:
    passwd_generator.py -l 10
Generate an 8 characters password and analyze it:
    passwd_generator.py -l 8 -a
'''

import argparse
import random

source = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_$#@*![]+-&()|='
source_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
source_letters_lower = 'abcdefghijklmnopqrstuvwxyz'
source_letters_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
source_numbers = '0123456789'
source_special_char = '_$#@*![]+-&()|=.'

def randomizer(non_randomized_source):
    # random.shuffle accepts list as input, so we transform str->list,
    # apply random.shuffle, then transform list->str
    source_to_list = list(non_randomized_source)
    for i in range(99):
        random.shuffle(source_to_list) 
    randomized_source = "".join(source_to_list)
    return randomized_source

def passwd_generator(passwd_length):
    randomized_source = randomizer(source)
    passwd_generated = ""
    for i in range(passwd_length):
        generated_random = random.randint(0,len(randomized_source)-1)
        passwd_generated += randomized_source[generated_random]
    return passwd_generated

def complex_passwd_generator(passwd_length):
    # the generated password may have 30% letters (50% lower 50% upper), 30% numbers and 40% special characters.
    # in some cases (depending on password length), mix characters are used to get to 100%.
    # TODO: this method is predictive. Change the code to have "at least 1 upper, 1 lower and 1 special char"
    nb_letter = ((passwd_length*30) // 100)
    nb_letter_lower = ((nb_letter*50) // 100)
    nb_letter_upper = nb_letter - nb_letter_lower
    nb_number = ((passwd_length*30) // 100)
    nb_special_char = ((passwd_length*40) // 100)
    nb_mix = passwd_length - (nb_letter+nb_number+nb_special_char)

    randomized_source_letters_lower = randomizer(source_letters_lower)
    randomized_source_letters_upper = randomizer(source_letters_upper)
    randomized_source_numbers = randomizer(source_numbers)
    randomized_source_special_char = randomizer(source_special_char)
    randomized_source_mix = randomizer(source)

    passwd_generated = ""
    generated_letters_lower = ""
    generated_letters_upper = ""
    generated_numbers = ""
    generated_special_characters = ""
    generated_mix = ""

    for l in range(nb_letter_lower):
        generated_random = random.randint(0,len(randomized_source_letters_lower)-1)
        generated_letters_lower = randomized_source_letters_lower[generated_random]
        passwd_generated += generated_letters_lower

    for u in range(nb_letter_upper):
        generated_random = random.randint(0,len(randomized_source_letters_upper)-1)
        generated_letters_upper = randomized_source_letters_upper[generated_random]
        passwd_generated += generated_letters_upper

    for n in range(nb_number):
        generated_random = random.randint(0,len(randomized_source_numbers)-1)
        generated_numbers = randomized_source_numbers[generated_random]
        passwd_generated += generated_numbers

    for s in range(nb_special_char):
        generated_random = random.randint(0,len(randomized_source_special_char)-1)
        generated_special_characters = randomized_source_special_char[generated_random]
        passwd_generated += generated_special_characters

    for m in range(nb_mix):
        generated_random = random.randint(0,len(randomized_source_mix)-1)
        generated_mix = randomized_source_mix[generated_random]
        passwd_generated += generated_mix

    return randomizer(passwd_generated)

def password_analyzer(passwd_to_analyze):
    digit_count=0
    lower_count=0
    upper_count=0
    special_char_count=0
    print(f'Password: {passwd_to_analyze}')
    print(f'Length: {len(passwd_to_analyze)}')
    passwd_to_analyze_list = list(passwd_to_analyze)
    for c in passwd_to_analyze_list:
        if c.isdigit():
            digit_count+=1            
        if c.islower():
            lower_count+=1
        if c.isupper():
            upper_count+=1
        if not c.isalnum():
            special_char_count+=1
    if digit_count == 0 or lower_count == 0 or upper_count == 0 or special_char_count == 0 :
        print("Password quality not good enough!")
    
    print("Number of characters by type:",
          "   Number: "+str(digit_count),
          "   Lower letter: "+str(lower_count),
          "   Upper letter: "+str(upper_count),
          "   Special char: "+str(special_char_count),sep="\n"
          )

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', type=str, required=False, default="complex", choices=['simple','complex'], 
                    help="Choose between simple and complex password generator.")
parser.add_argument('-l', '--length', type=int, required=False, default=20, help="(optional) set password length.")
parser.add_argument('-a', '--analyse', action='store_true', required=False, help="(optional) show password analysis.")
args = parser.parse_args()
if args.type == "simple":
    passwd = passwd_generator(args.length)
else:
    passwd = complex_passwd_generator(args.length)

if args.analyse:
    password_analyzer(passwd)
else:
    print(passwd)
