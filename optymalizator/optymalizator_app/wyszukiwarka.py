import json

from optymalizator_app.helper import *
from optymalizator_app.data_import import *


def write(filter_res):
    if filter_res == None:
        return None
    df_res = df_xlsx.copy() # deep copy

    for key, value in filter_res.items():
        if (key == "ean"):
            value = [int(value)]
            df_res = df_res[df_xlsx[key].isin(value)]
        else:
            df_res = df_res[df_xlsx[key].str.lower().str.contains(value.replace('+', '\+'))]

    df_res = df_res.iloc[:, 0:8]
    json_str = df_res.to_json(orient='table', index=False)
    json_dict = json.loads(json_str)

    fields = [f['name'] for f in json_dict['schema']['fields']]
    data = [list(d.values()) for d in json_dict['data']]
    output_dict = {field: [d[i] for d in data] for i, field in enumerate(fields)}
    new_dict = {k: v for k, v in output_dict.items()}
    res_list = return_list(new_dict)
    return res_list


def read(input):
    filter_res = {}
    input = convert_to_db_shorcut(input)
    split_input = input.split(" ")

    # Extracting and cutting ean if one exists.
    ean_res = read_and_cut_ean(split_input)
    split_input = ean_res[0]
    input = " ".join(split_input)
    ean = ean_res[1]
    if (ean != ""):
        filter_res.update({"ean": ean})

    # Extracting and cutting name or substance if they exist.
    name_res = read_and_cut(split_input, all_names)
    split_input = name_res[0]
    input = " ".join(split_input)
    name = name_res[1]
    if (name != ""):
        filter_res.update({"nazwa": name})

    substance_res = read_and_cut(split_input, all_substances)
    split_input = substance_res[0]
    input = " ".join(split_input)
    substance = substance_res[1]
    if (substance != ""):
        filter_res.update({"substancja_czynna": substance})

    if (name == "" and substance == "" and ean == ""):
        return None  # TODO return error
    
    # # Extracting and cutting dose if it exists.
    dose_res = return_and_cut_number_and_unit(input)
    dose = dose_res[1]
    input = dose_res[0]
    split_input = input.split(" ")
    if (dose != ""):
        dose = one_space_between_number_and_word(dose)

    # Extracting content if it exists.
    content_res = return_and_cut_number_and_szt(input)
    content = content_res[1]
    input = content_res[0]
    split_input = input.split(" ")
    if (content != ""):
        content = one_space_between_number_and_word(content)
        filter_res.update({"zawartosc_opakowania": content})

    # Extracting form if it exists.
    form_res = return_first_number_and_abbv(input)
    form = form_res[1]
    input = form_res[0]
    if (form != ""):
        form = one_space_between_number_and_word(form)
        form.strip()
        print(form)
        filter_res.update({"postac": form})
    if (content == ""):
        if (any(char.isdigit() for char in form)):
            value_temp = filter_res["postac"]
            del filter_res["postac"]
            filter_res.update({"zawartosc_opakowania": value_temp})

    # check if input consists any of abbv_map values
    for abbv_item in abbv_list:
        if (abbv_item in input):
            input = input.replace(abbv_item, "")
            for key, value in abbv_map.items():
                if abbv_item in value:
                    abbv_item = key
                    break
            filter_res.update({"postac": abbv_item})
            break
    if (input != "" and not input.isspace()):
        return None
    
    return write(filter_res)
