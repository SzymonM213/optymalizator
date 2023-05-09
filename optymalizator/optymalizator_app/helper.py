import re

# File with abbreviations that are acceptable within the search engine and the shortcut name used in the database.
# Key: shortcut name used in the database, Value

abbv_map = {
    "tabl.": ["tabletki", "tabletka", "tabletek", "tab.", "tabl."],
    "kaps.": ["kapsułki", "kaps.", "kapsułka", "kapsułek", "kapsulki, kapsulka, kapsulek"],
}

abbv_list = ["tabletki", "tabletka", "tabletek", "tab.", "tabl.", "kapsułki", "kaps.", "kapsułka", "kapsułek", "kapsulki, kapsulka, kapsulek"]

unit_list = ['mg', 'g']

szt = ["szt."]


# Converts occurences of abbreviations to the shortcut name used in the database.
def convert_to_db_shorcut(text):
    for key, value in abbv_map.items():
        for v in value:
            text = text.replace(v, key)
    return text


def one_space_between_number_and_word(text):
    regex = r'(\d+\+*)(\s*)([a-zA-Z]+)'
    match = re.search(regex, text)
    if match:
        text = re.sub(regex, match.group(1) + " " + match.group(3), text, count=1)
    return text


# Checks if input consists a valid name or substance. If it does, it cuts the sequence from the input and list [input, name/substance] is returned.
def read_and_cut(split_input, all_phrases):
    for i in range(len(split_input) + 1, 1, -1):                                    # all available sequence sizes
        for j in range(0, len(split_input) - i + 2):     
            test_phrase = " ".join(split_input[j:j+i])
            test_phrase = test_phrase.lower()
            if (test_phrase in all_phrases):
                # cut test phrase from split_input
                split_input = split_input[:j] + split_input[j+i:]
                return [split_input, test_phrase]
    return [split_input, ""]


# Checks if input consists a valid ean. If it does, it cuts the sequence from the input and list [input, ean] is returned.
def read_and_cut_ean(split_input):
    regex = r'^(\d{8,14})$'
    for i in range(len(split_input)):
        match = re.search(regex, split_input[i])
        if (match):
            split_input = split_input[:i] + split_input[i+1:]
            return [split_input, match.group(1)]
    return [split_input, ""]


# Returns first occurence of the first number and abbreviations in a string.
# For example for string "50 tabl. 2 blistry po 25 tabl." it returns 50 tabl. abbv: kaps. tabl.
def return_first_number_and_abbv(text):
    regex = r'(\d+\s?\s?)(?=\s*(?:' + '|'.join(abbv_map.keys()) + '))(\s*(?:' + '|'.join(abbv_map.keys()) + '))'
    match = re.search(regex, text)
    if match:
        text = re.sub(regex, '', text, count=1)
        return [text, match.group(1) + match.group(2)]
    return [text, ""]


# Returns first occurence of the first number and units in a string. Units are: g, mg.
def return_and_cut_number_and_unit(text):
    regex = r'(\d+(?:[\.,]\d+)?(?:\+\d+(?:[\.,]\d+)?)*)(?:\s*)((' + '|'.join(unit_list) + r')\b)'
    match = re.search(regex, text)
    if match:
        text = re.sub(regex, '', text, count=1)
        return [text.strip(), match.group(1) + match.group(2)] # replace comma with dot for decimal
    return [text, ""]


# Returns first occurence of the first number and szt. in a string.
def return_and_cut_number_and_szt(text):
    regex = r'(\d+(?:\.\d+)?)\s*(szt\.?)'
    match = re.search(regex, text)
    if match:
        text = re.sub(regex, '', text, count=1)
        return [text, match.group(1) + match.group(2)]
    return [text, ""]


def return_list(data):
    new_data = {}
    for key, values in data.items():
        if key == 'nazwa_postac_dawka':
            new_keys = ['nazwa', 'postac', 'dawka']
            for value in values:
                value_parts = value.split(', ')
                for i in range(len(new_keys)):
                    new_key = new_keys[i]
                    new_value = value_parts[i]
                    if new_key in new_data:
                        new_data[new_key].append(new_value)
                    else:
                        new_data.update({new_key: [new_value]})
                    
        elif key == 'ean':
            new_data[key] = ['0' + str(value) for value in values]
        else:
            new_data[key] = values
        
    rows = [dict(zip(new_data.keys(), values)) for values in zip(*new_data.values())]

    return rows
