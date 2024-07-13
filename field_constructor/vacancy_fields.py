def create_vacancy_fields(
    current_row,
    vacancy_fields: dict,
    field_type: str,
    current_order: int,
    current_int_field: int,
) -> dict:
    mandatory_field = current_row.mandatory_field.lower() == "обязательно"

    vacancy_fields_schema = vacancy_fields["schema"]
    vacancy_fields_schema.setdefault(current_row.eng_field_name, {})
    vacancy_field_param = vacancy_fields_schema[current_row.eng_field_name]
    vacancy_field_param["type"] = field_type
    if field_type == "dictionary":
        vacancy_field_param["dictionary"] = current_row.eng_field_name
    if isinstance(field_type, dict):
        vacancy_field_param["dictionary"] = current_row.eng_field_name
        vacancy_field_param["type"] = field_type["type"]
        vacancy_field_param["multiple"] = True
    vacancy_field_param["min"] = 1
    vacancy_field_param["max"] = 1
    vacancy_field_param["required"] = mandatory_field

    if getattr(current_row, "field_title_to_drag", None) is not None:
        vacancy_field_param["title"] = (
            current_row.field_title_to_drag.strip()
            if current_row.field_title_to_drag
            else current_row.title.strip()
        )
    else:
        vacancy_field_param["title"] = current_row.title.strip()

    if current_row.need_delimiter == "Да":
        vacancy_field_param["delimiter"] = True
    if (
        current_row.field_placeholder is not None
        and field_type != "dictionary"
        and not isinstance(field_type, dict)
    ):
        vacancy_field_param["placeholder"] = current_row.field_placeholder
    if current_row.dict_as_filter == "Да":
        vacancy_field_param["filterable"] = True
        vacancy_field_param["search_field"] = f"int_field_{current_int_field}"
    vacancy_field_param["order"] = current_order

    return vacancy_fields
