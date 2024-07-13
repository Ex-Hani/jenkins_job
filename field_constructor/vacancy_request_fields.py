def create_vacancy_request_fields(
    current_row,
    vacancy_request_form: dict,
    field_type: str,
    inner_compensation_field: dict,
    available_on_field_data: dict,
    current_order: int,
) -> dict:
    system_field_not_drag_to_vacancy = ["position", "account_division", "money"]

    mandatory_field = current_row.mandatory_field.lower() == "обязательно"

    if current_row.title:
        vacancy_request_schema = vacancy_request_form.setdefault("schema")
        vacancy_request_schema.setdefault(current_row.eng_field_name, {})
        vacancy_request_field = vacancy_request_schema[current_row.eng_field_name]
        vacancy_request_field["type"] = field_type

        if field_type == "dictionary":
            vacancy_request_field["dictionary"] = current_row.eng_field_name

        if isinstance(field_type, dict):
            vacancy_request_field["dictionary"] = current_row.eng_field_name
            vacancy_request_field["type"] = field_type["type"]
            vacancy_request_field["multiple"] = True

        vacancy_request_field["min"] = 1
        vacancy_request_field["max"] = 1
        vacancy_request_field["required"] = mandatory_field
        vacancy_request_field["title"] = current_row.title.strip()

        if current_row.need_delimiter == "Да":
            vacancy_request_field["delimiter"] = True

        if (
            current_row.field_placeholder is not None
            and field_type != "dictionary"
            and not isinstance(field_type, dict)
        ):
            vacancy_request_field["placeholder"] = current_row.field_placeholder

        if field_type == "compensation":
            vacancy_request_field["fields"] = inner_compensation_field

        if current_row.available_on_operator is not None:
            vacancy_request_field["availableOn"] = available_on_field_data

        if (
            current_row.drag_field_to_vacancy.lower() == "да"
            and current_row.eng_field_name not in system_field_not_drag_to_vacancy
        ):
            vacancy_request_field["vacancy_field"] = current_row.eng_field_name

        vacancy_request_field["order"] = current_order

    return vacancy_request_form
