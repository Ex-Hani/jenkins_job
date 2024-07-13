def get_field_attributes(is_field_required: str) -> dict:

    inner_fields = {
        "compensation_from": {
            "type": "string",
            "placeholder": "От",
            "title": " ",
            "required": is_field_required,
            "order": 1,
        },
        "compensation_to": {
            "type": "string",
            "placeholder": "До",
            "title": " ",
            "required": is_field_required,
            "order": 2,
        },
    }

    return inner_fields
