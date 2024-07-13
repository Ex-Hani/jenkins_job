def prepare_available_on_field(
    available_on_operator: str,
    available_on_field_name: str,
    available_on_value: str,
    full_schema: dict,
):
    dictionaries = full_schema.setdefault("dictionaries", {})
    foreign = None

    for dict_name in dictionaries:
        if (
            dictionaries[dict_name]["code"].strip().lower()
            != available_on_field_name.strip().lower()
        ):
            continue

        for dict_items_data in dictionaries[dict_name]["items"]:
            if (
                dict_items_data["name"].strip().lower()
                == available_on_value.strip().lower()
            ):
                foreign = dict_items_data["foreign"]

    field = {
        "operator": available_on_operator,
        "field": f"{available_on_field_name}.foreign",
        "value": foreign,
    }

    return field
