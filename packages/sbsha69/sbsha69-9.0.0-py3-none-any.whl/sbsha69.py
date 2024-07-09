import random

def sbsha69(data):
    reversed_data = data[::-1]  # Reverse the input string
    char_list = list(reversed_data)  # Convert to list of characters
    random.shuffle(char_list)  # Shuffle the list
    shuffled_data = ''.join(char_list)  # Join shuffled characters
    return shuffled_data
