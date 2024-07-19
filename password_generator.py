


import random

def generate_password(length, special, digits, Upper, Lower, personal_alphabet=""):
    password = ""
    ALPHABET = ""
    if special: ALPHABET += r"!@#$%^&*()_-+=[]{}|:\\\"'\",.;/?"
    if digits : ALPHABET += "0123456789"
    if Upper: ALPHABET += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if Lower: ALPHABET += "abcdefghijklmnopqrstuvwxyz"
    ALPHABET += personal_alphabet
    for _ in range(length):
        password += random.choice(ALPHABET)
    return password
