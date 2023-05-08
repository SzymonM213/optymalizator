import pandas as pd
import re
import json

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


def write(filter_res):
    df_res = df_xlsx.copy() # deep copy

    for key, value in filter_res.items():
        col_name = values_to_corresponding_columns.get(key)
        df_res = df_res[df_xlsx[col_name].str.lower().str.contains(value)]

    df_res = df_res.iloc[:, 1:5]
    json_str = df_res.to_json(orient='table', index=False)
    json_dict = json.loads(json_str)

    fields = [f['name'] for f in json_dict['schema']['fields']]
    data = [list(d.values()) for d in json_dict['data']]
    output_dict = {field: [d[i] for d in data] for i, field in enumerate(fields)}
    new_dict = {http_and_columns[k]: v for k, v in output_dict.items()}
    res_list = return_list(new_dict)
    print("RESULT:")
    print(res_list)

    return res_list


# input = " 2+0,035mg 20 kapsułek Cyproteronum + Ethinylestradiolum  20 szt.  "
input = "Cyproteroni acetas"
read_res = read(input)

write(read_res)
