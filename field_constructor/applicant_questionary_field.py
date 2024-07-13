from collections import namedtuple


def create_questionary_fields(
    current_row,
    questionary_fields: dict,
    field_type: str,
    current_order: int,
    current_int_field: int,
) -> dict:
    questionary_fields_schema = questionary_fields["schema"]
    questionary_fields_schema.setdefault(current_row.eng_field_name, {})
    questionary_field_param = questionary_fields_schema[current_row.eng_field_name]
    questionary_field_param["type"] = field_type

    if field_type == "dictionary":
        questionary_field_param["dictionary"] = current_row.eng_field_name

    if isinstance(field_type, dict):
        questionary_field_param["dictionary"] = current_row.eng_field_name
        questionary_field_param["type"] = field_type["type"]
        questionary_field_param["multiple"] = True

    questionary_field_param["required"] = False

    if current_row.dict_to_profile.lower() == "да":
        questionary_field_param["show_in_profile"] = True

    if current_row.dict_as_filter == "Да":
        questionary_field_param["search_field"] = f"string_field_{current_int_field}"

        if (
                field_type == "dictionary"
                or field_type == "region"
        ):
            questionary_field_param["search_field"] = f"multi_field_{current_int_field}"

    questionary_field_param["min"] = 1
    questionary_field_param["max"] = 1
    questionary_field_param["title"] = current_row.title

    if (
        current_row.restrict_visibility
        and current_row.restrict_visibility.lower() == "да"
        and current_row.role_restrict_conf
    ):
        questionary_field_param["member_access"] = get_member_access_attrs(
            current_row.role_restrict_conf
        )

    questionary_field_param["order"] = current_order

    return questionary_fields


def get_member_access_attrs(role_restrict_conf: str) -> dict:
    member_access_attrs = {"blacklist": []}
    roles = role_restrict_conf.split(",")

    for role in roles:
        role_setting = {}
        if ":" in role:
            role_fields = tuple(role.split(":"))

            Row = namedtuple("Row", "role_name role_restriction")
            current_role = Row(*role_fields)

            role_setting["member_type"] = current_role.role_name
            role_setting["with_permissions"] = [current_role.role_restriction]
            member_access_attrs["blacklist"].append(role_setting)
            continue

        role_setting["member_type"] = role
        member_access_attrs["blacklist"].append(role_setting)

    return member_access_attrs
