


import random

def generate_password_on_set_parameters(length, special, digits, Upper, Lower, personal_alphabet=""):
    password = ""
    ALPHABET = ""
    if special: ALPHABET += r"!@#$%^&*()_-+=[]{}|:\\\"'\",.;/?"
    if digits : ALPHABET += "0123456789"
    if Upper: ALPHABET += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if Lower: ALPHABET += "abcdefghijklmnopqrstuvwxyz"
    ALPHABET += personal_alphabet
    if len(ALPHABET) > 0:
        for _ in range(length):
            password += random.choice(ALPHABET)
        return password
    else:
        return "Алфавит пуст, добавьте дополнительные символы или включите загатовленные заранее\n (*μ_μ)"
