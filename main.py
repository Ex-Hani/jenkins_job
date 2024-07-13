import argparse
from collections import namedtuple
from pathlib import Path

from loguru import logger

from create_questionary_fields import applicant_fields_preparing
from utils.common_func import (
    order_redefine,
    fill_template_form,
    get_field_type,
    load_json,
    get_cells,
    save_schema_to_files,
)
from field_constructor.vacancy_request_fields import create_vacancy_request_fields
from field_constructor.compensation_field import get_field_attributes
from field_constructor.availableon_field import prepare_available_on_field
from field_constructor import vacancy_fields, dictionary_field
from create_vacancy_fields import vacancy_fields_preparing
from utils.schema_utils import is_field_created


def create_all_dictionaries(
    filled_rows: list,
    rows_name: list,
    full_schema: dict,
    dictionaries: dict,
    mapping_filetypes: dict,
    disable_dict_value_capitalize: bool,
):
    Row = namedtuple(
        "Row",
        rows_name,
    )

    for row in filled_rows:
        current_row = Row(*row)
        field_type = get_field_type(current_row.field_type_rus, mapping_filetypes)

        if not current_row.dictionary_values:
            continue

        full_schema["dictionaries"] = dictionary_field.dictionary_prepare(
            current_row, dictionaries, field_type, disable_dict_value_capitalize
        )

    return full_schema


def get_params(
    current_path: Path,
    mapping_file: Path,
):
    parser = argparse.ArgumentParser(
        prog="Vacancy request creator",
        description="The script creates a structured schema, "
        "which contain json files. Schema create from an xlsx file.",
    )
    parser.add_argument(
        "--input_file",
        type=Path,
        required=True,
        help="xlsx-file to process.",
    )
    parser.add_argument(
        "--folder_name", type=str, required=True, help="output folder name"
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        default=current_path,
        help="Path to folder where need to create client schema folder",
    )
    parser.add_argument(
        "--map_file",
        type=str,
        default=mapping_file,
        help="field type mapping-file.",
    )
    parser.add_argument(
        "--org_name", type=str, default="ORG_NAME", help="organization full-name."
    )
    parser.add_argument(
        "--vacancy_file_path",
        type=Path,
        help="Path to vacancy fields xlsx-file.",
    )
    parser.add_argument(
        "--questionary_file_path",
        type=Path,
        help="Path to applicant additional fields xlsx-file.",
    )
    parser.add_argument(
        "--disable_dict_value_capitalize",
        action="store_true",
        help="If need to capitalize all dict values. False by default.",
    )

    args = parser.parse_args()

    return (
        args.input_file,
        args.folder_name,
        args.output_path,
        args.map_file,
        args.org_name,
        args.vacancy_file_path,
        args.questionary_file_path,
        args.disable_dict_value_capitalize,
    )


def main():
    current_path: Path = Path.cwd()
    mapping_file = current_path / "common_files" / "fields_mapping.json"

    (
        input_file,
        folder_name,
        output_path,
        map_file,
        org_name,
        vacancy_file_path,
        questionary_file_path,
        disable_dict_value_capitalize,
    ) = get_params(current_path, mapping_file)

    filled_rows = get_cells(input_file, 13)
    filled_rows = [row for row in filled_rows]

    full_schema = {
        "vacancy_request": {
            "name": "",
            "attendee_hint": "",
            "attendee_required": None,
            "schema": {},
        },
        "vacancy_fields": {"schema": {}},
        "dictionaries": {},
        "questionary": {"schema": {}},
    }

    mapping_file_path = Path(map_file)
    mapping_filetypes = load_json(mapping_file_path)
    forbidden_field_names_path = (
        current_path / "common_files" / "forbidden_vacancy_field_names.json"
    )
    forbidden_field_names = load_json(forbidden_field_names_path)
    errors = []

    output_directory = Path() / output_path / folder_name
    output_directory.mkdir(parents=True, exist_ok=True)

    logger.info("Prepare data")

    current_order = 1
    current_int_field = 1

    rows_name = [
        "eng_field_name",
        "title",
        "field_type_rus",
        "dictionary_values",
        "field_placeholder",
        "mandatory_field",
        "drag_field_to_vacancy",
        "field_title_to_drag",
        "dict_as_filter",
        "need_delimiter",
        "available_on_operator",
        "available_on_field_name",
        "available_on_value",
    ]
    Row = namedtuple(
        "Row",
        rows_name,
    )

    for row in filled_rows:
        current_row = Row(*row)
        field_type = get_field_type(current_row.field_type_rus, mapping_filetypes)
        mandatory_field = current_row.mandatory_field.lower() == "обязательно"
        compensation_field_data = {}
        available_on_field_data = {}

        if is_field_created(full_schema, current_row.eng_field_name):
            logger.info(
                "Row {} was processed before. Skip.".format(current_row.eng_field_name)
            )
            continue

        logger.info("Processing field {}".format(current_row.eng_field_name))

        if field_type == "compensation":
            compensation_field_data = get_field_attributes(mandatory_field)

        if current_row.available_on_operator is not None:
            create_all_dictionaries(
                filled_rows,
                rows_name,
                full_schema,
                full_schema["dictionaries"],
                mapping_filetypes,
                disable_dict_value_capitalize,
            )

            available_on_field_data = prepare_available_on_field(
                current_row.available_on_operator,
                current_row.available_on_field_name,
                current_row.available_on_value,
                full_schema,
            )

            if available_on_field_data["value"] is None:
                error_message = (
                    "AvailableOn field. Foreign was not found "
                    "by name '{}' in dictionary '{}'. "
                    "Skip.".format(
                        current_row.available_on_value,
                        current_row.available_on_field_name,
                    )
                )
                logger.error(error_message)
                errors.append(error_message)

        full_schema["vacancy_request"] = create_vacancy_request_fields(
            current_row,
            full_schema["vacancy_request"],
            field_type,
            compensation_field_data,
            available_on_field_data,
            current_order,
        )

        if (
            field_type == "dictionary" or isinstance(field_type, dict)
        ) and not current_row.dictionary_values:
            error_message = (
                "There is no any values for dict field '{}'. "
                "Skip.".format(
                    current_row.eng_field_name,
                )
            )
            logger.error(error_message)
            errors.append(error_message)
            continue

        full_schema["dictionaries"] = dictionary_field.dictionary_prepare(
            current_row,
            full_schema["dictionaries"],
            field_type,
            disable_dict_value_capitalize,
        )

        if not (
            current_row.title
            and current_row.field_title_to_drag
            and current_row.eng_field_name not in forbidden_field_names["items"]
        ):
            continue

        full_schema["vacancy_fields"] = vacancy_fields.create_vacancy_fields(
            current_row,
            full_schema["vacancy_fields"],
            field_type,
            current_order,
            current_int_field,
        )

        if current_row.dict_as_filter == "Да":
            current_int_field += 1

        if not current_row.dictionary_values:
            continue

        full_schema["dictionaries"] = dictionary_field.dictionary_prepare(
            current_row,
            full_schema["dictionaries"],
            field_type,
            disable_dict_value_capitalize,
        )

    if questionary_file_path:
        logger.info("Start preparing applicant additional fields file.")
        additional_fields_filled_rows = get_cells(questionary_file_path, 8)
        applicant_fields_preparing(
            additional_fields_filled_rows,
            mapping_filetypes,
            forbidden_field_names,
            full_schema,
            disable_dict_value_capitalize,
        )
        logger.info("Done. Start preparing applicant additional fields file.")

    if vacancy_file_path:
        logger.info("Check vacancy fields file for new fields.")
        vacancy_filled_rows = get_cells(vacancy_file_path, 9)
        vacancy_fields_preparing(
            vacancy_filled_rows,
            mapping_filetypes,
            forbidden_field_names,
            full_schema,
            disable_dict_value_capitalize,
        )
        logger.info("Done. Check vacancy fields file for new fields.")

    logger.info("Prepare data. Done.")

    full_schema["vacancy_fields"]["schema"] = order_redefine(
        full_schema["vacancy_fields"]["schema"]
    )

    full_schema["vacancy_request"]["schema"] = order_redefine(
        full_schema["vacancy_request"]["schema"]
    )

    full_schema["questionary"]["schema"] = order_redefine(
        full_schema["questionary"]["schema"]
    )

    full_schema[
        "vacancy_request_file_name"
    ] = f"schema_vacancy_request_{folder_name}.json"
    full_schema[
        "vacancy_fields_file_name"
    ] = f"schema_vacancy_fields_{folder_name}.json"
    full_schema[
        "questionary_fields_file_name"
    ] = f"schema_applicant_questionary_{folder_name}.json"

    logger.info("Fill template.")

    if not is_field_created(full_schema, "account_region"):
        full_schema["template_form"] = fill_template_form(
            full_schema,
            org_name,
            folder_name,
        )
    else:
        full_schema["template_form"] = fill_template_form(
            full_schema,
            org_name,
            folder_name,
            True,
        )
        logger.warning("Please add use-vacancy-regions to account_setting table.")
    logger.info("Fill template. Done.")

    logger.info("Save all data to files.")
    save_schema_to_files(full_schema, output_directory)
    logger.info("Save all data to files. Done.")

    if len(errors) > 0:
        logger.error(
            "Some errors found. Please check. \nErrors list: \n{}".format(*errors)
        )

    division_file_path = Path(output_directory, full_schema["template_form"]["division"])
    if "division" in full_schema["template_form"] and not Path.is_file(
        division_file_path
    ):
        logger.warning(
            "File '{}' not created in schema. Please check division file, before create stand.".format(
                full_schema["template_form"]["division"],
            )
        )


if __name__ == "__main__":
    main()
