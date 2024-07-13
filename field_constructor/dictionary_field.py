from uuid import uuid4


def dictionary_prepare(
    current_row,
    dictionaries: dict,
    field_type: str,
    disable_dict_value_capitalize: bool,
) -> dict:

    if not (
        (current_row.dictionary_values and isinstance(field_type, dict))
        or (current_row.dictionary_values and field_type == "dictionary")
    ):
        return dictionaries

    dictionary_name = f"dictionary_{current_row.eng_field_name}.json"
    dictionaries.setdefault(dictionary_name, {})
    dict_data = dictionaries[dictionary_name]
    dict_data["name"] = current_row.title
    dict_data["code"] = current_row.eng_field_name

    items = []
    dict_values = current_row.dictionary_values.split("\n")

    for dict_value in dict_values:
        value = dict_value.strip().capitalize()

        if disable_dict_value_capitalize:
            value = dict_value.strip()

        dict_data = {
            "name": value,
            "foreign": f"{uuid4()}",
        }
        items.append(dict_data)

    dictionaries[dictionary_name]["items"] = items

    return dictionaries
