def is_field_created(
    full_schema: dict,
    field_name: str,
    search_path: str = "vacancy_request",
):
    if field_name in full_schema[search_path]["schema"].keys():
        return True
    return False
