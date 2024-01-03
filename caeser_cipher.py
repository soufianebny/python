#!/bin/env python

import sys

'''
Description: script to encode or decode a message in caesar cipher
It use english 26 letters, no digits shift.

Input:
    action: decode or encode
    message
    shift

Examples:
    caeser_cipher.py encode "hello, don't keep this secret secret" 7
    caeser_cipher.py decode "nthps whzzdvyk: uprtvbr01" 7
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def caesar(op,input_msg,shift):
    output_msg = ""
    for char in input_msg:
        if char in alphabet:
            input_index = alphabet.index(char)      
            if op == "encode":
                output_index = input_index + int(shift)
                # can be replaced by output_index = (input_index + int(shift)) % len(alphabet)
                while output_index >= len(alphabet):
                    output_index -= len(alphabet)
            elif op == "decode":
                output_index = input_index - int(shift)
                # can be replaced by output_index = (input_index - int(shift)) % len(alphabet)
                while output_index <= (-1 * len(alphabet)):
                    output_index += len(alphabet)
            output_msg += alphabet[output_index]
        else:
            output_msg += char
    print(f'output msg: {output_msg}')

if len(sys.argv) != 4:
    print("Usage: caeser_cipher.py <encode/decode> <message> <shift>")
else:
    caesar(op=sys.argv[1], input_msg=sys.argv[2].lower(), shift=sys.argv[3])

