#!/usr/bin/env python

'''
Description: Script to generate a random password.

Input: arg1 = password length. Default 20 if arg1 not specified.
Output: the generated password

Examples:
Generate a 10 characters password: passwd_generator.py 10
Generate a 20 characters password: passwd_generator.py
'''

import random
import sys

source = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_$#@*![]+-&()|='

def randomize_source(non_randomized_source):
    # random.shuffle accepts list as input, so we transform str->list,
    # apply random.shuffle, then transform list->str
    source_to_list = list(non_randomized_source)
    for i in range(99):
        random.shuffle(source_to_list)       
    randomized_source = "".join(source_to_list)
    return randomized_source

def passwd_generator(passwd_length):
    randomized_source = randomize_source(source)
    passwd_generated = ""
    for i in range(passwd_length):
        char_generated = random.randint(0,len(randomized_source)-1)
        passwd_generated += randomized_source[char_generated]
    return passwd_generated

# def passwd_analyzer(passwd_to_analyze):
#     digit_count=0
#     alpha_lower_count=0
#     alpha_upper_count=0
#     non_alnum_count=0
#     print("Passwd length: "+str(len(passwd_to_analyze)))
#     passwd_to_analyze_list = list(passwd_to_analyze)
#     for c in passwd_to_analyze_list:
#         if c.isdigit():
#             digit_count+=1            
#         if c.islower():
#             alpha_lower_count+=1
#         if c.isupper():
#             alpha_upper_count+=1
#         if not c.isalnum():
#             non_alnum_count+=1
#     if digit_count == 0 or alpha_lower_count == 0 or alpha_upper_count == 0 or non_alnum_count == 0 :
#         print("Passwd not good enough!")
    
#     print("Number of characters by type is:",
#           "   Digits: "+str(digit_count),
#           "   Lower alpha: "+str(alpha_lower_count),
#           "   Upper alpha: "+str(alpha_upper_count),
#           "   Non alnum: "+str(non_alnum_count),sep="\n"
#           )

def arg_parser():
    if len(sys.argv) != 2:
        passwd_length = 20
    else:
        try:
            passwd_length = int(sys.argv[1])
        except ValueError:
            print("<password length> must be an integer")
            sys.exit(1)
    return passwd_length

passwd = passwd_generator(arg_parser())
print(passwd)
# passwd_analyzer(passwd)
