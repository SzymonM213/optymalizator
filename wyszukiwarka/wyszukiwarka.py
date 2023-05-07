import pandas as pd
import re

from helper import *
from data_import import *

def read(input):
    filter_res = {}
    input = convert_to_db_shorcut(input)
    print(input)
    split_input = input.split(" ")
    print(split_input)

    # Extracting and cutting ean if one exists.
    ean_res = read_and_cut_ean(split_input)
    split_input = ean_res[0]
    input = " ".join(split_input)
    ean = ean_res[1]
    if (ean != ""):
        return filter_res.update({"ean": ean})

    # Extracting and cutting name or substance if they exist.
    name_res = read_and_cut(split_input, all_names)
    split_input = name_res[0]
    input = " ".join(split_input)
    name = name_res[1]
    if (name != ""):
        filter_res.update({"name": name})
        print("name: ")
        print(name)

    substance_res = read_and_cut(split_input, all_substances)
    split_input = substance_res[0]
    input = " ".join(split_input)
    substance = substance_res[1]
    if (substance != ""):
        filter_res.update({"substance": substance})
        print("substance: ")
        print(substance)

    if (name == "" and substance == ""):
        return None  # TODO return error
    
    # # Extracting and cutting dose if it exists.
    dose_res = return_and_cut_number_and_unit(input)
    dose = dose_res[1]
    input = dose_res[0]
    split_input = input.split(" ")
    if (dose != ""):
        dose = one_space_between_number_and_word(dose)
        filter_res.update({"dose": dose})
        print("dose: ")
        print(dose)

    # Extracting content if it exists.
    content_res = return_and_cut_number_and_szt(input)
    content = content_res[1]
    input = content_res[0]
    split_input = input.split(" ")
    if (content != ""):
        content = one_space_between_number_and_word(content)
        filter_res.update({"content": content})
        print("content: ")
        print(content)

    # Extracting form if it exists.
    form_res = return_first_number_and_abbv(input)
    form = form_res[1]
    input = form_res[0]
    if (form != ""):
        form = one_space_between_number_and_word(form)
        filter_res.update({"form": form})
        print("form: ")
        print(form)

    if ("kaps." in form):
        form = "kaps."
    elif "tabl." in form:
        form = "tabl."

    print("input: ")
    print(input)
    if (input != "" and not input.isspace()):
        print("ERROR")
        return None
    
    print(filter_res)
    return filter_res


input = " 2+0,035mg 20 kapsułek Cyproteronum + Ethinylestradiolum  20 szt.  "
read(input)


def write(filter_res):
    pass # TODO