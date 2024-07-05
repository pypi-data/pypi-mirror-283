import re

def parse_string(input_string):
    # Calculate counts
    num_chars = len(input_string)
    num_words = len(input_string.split())
    num_special_chars = len(re.findall(r'[^\w\s]', input_string))
    num_numbers = len(re.findall(r'\d', input_string))

    return {
        "characters": num_chars,
        "words": num_words,
        "special_characters": num_special_chars,
        "numbers": num_numbers
    }
