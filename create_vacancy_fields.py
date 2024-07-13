import argparse
from collections import namedtuple
from pathlib import Path
from typing import Union, Any, Iterable

from loguru import logger

from utils.schema_utils import is_field_created
from utils.common_func import (
    get_field_type,
    load_json,
    get_cells,
    fill_template_form,
    save_schema_to_files,
    order_redefine,
)
from field_constructor import vacancy_fields, dictionary_field


def vacancy_fields_preparing(
    filled_rows: Iterable,
    mapping_filetypes: dict,
    forbidden_field_names: dict,
    full_schema: dict,
    disable_dict_value_capitalize: bool,
):
    current_order = 1
    current_int_field = 1

    rows_name = [
        "eng_field_name",
        "title",
        "field_type_rus",
        "dictionary_values",
        "field_placeholder",
        "mandatory_field",
        "dict_as_filter",
        "drag_to_excel_report",
        "need_delimiter",
    ]
    Row = namedtuple(
        "Row",
        rows_name,
    )

    for row in filled_rows:
        current_row = Row(*row)
        field_type = get_field_type(current_row.field_type_rus, mapping_filetypes)

        logger.info("Processing field {}".format(current_row.eng_field_name))

        if is_field_created(full_schema, current_row.eng_field_name, "vacancy_fields"):
            logger.info(
                "Row {} was processed before. Skip.".format(current_row.eng_field_name)
            )
            continue

        if not (
            current_row.title
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

    return full_schema


def get_params(
    current_path: Path,
    mapping_file: Path,
):
    parser = argparse.ArgumentParser(
        prog="Create vacancy fields",
        description="The script creates a structured file of vacancy fields. "
        "The schema is generated from the xlsx file.",
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
        "--output_path", type=Path, default=current_path, help="output folder name"
    )
    parser.add_argument(
        "--mapping_file",
        type=str,
        default=mapping_file,
        help="field type mapping-file.",
    )
    parser.add_argument(
        "--org_name", type=str, default="ORG_NAME", help="organization full-name."
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
        args.mapping_file,
        args.org_name,
        args.disable_dict_value_capitalize,
    )


def main():
    current_path = Path.cwd()
    mapping_file_path = Path(current_path / "common_files" / "fields_mapping.json")

    (
        input_file,
        folder_name,
        output_path,
        mapping_file_path,
        org_name,
        disable_dict_value_capitalize,
    ) = get_params(current_path, mapping_file_path)

    directory_name: Union[Path, Any] = Path() / output_path / folder_name
    directory_name.mkdir(parents=True, exist_ok=True)

    filled_rows = get_cells(input_file, 9)

    mapping_filetypes: dict = load_json(mapping_file_path)
    forbidden_field_names_path = (
        current_path / "common_files" / "forbidden_vacancy_field_names.json"
    )
    forbidden_field_names: dict = load_json(forbidden_field_names_path)

    full_schema = {
        "vacancy_fields": {"schema": {}},
        "dictionaries": {},
    }

    logger.info("Prepare data")
    full_schema = vacancy_fields_preparing(
        filled_rows,
        mapping_filetypes,
        forbidden_field_names,
        full_schema,
        disable_dict_value_capitalize,
    )
    logger.info("Prepare data. Done.")

    full_schema["vacancy_fields"]["schema"] = order_redefine(
        full_schema["vacancy_fields"]["schema"]
    )

    vacancy_fields_file_name = f"schema_vacancy_fields_{folder_name}.json"
    full_schema["vacancy_fields_file_name"] = vacancy_fields_file_name

    logger.info("Fill template.")
    full_schema["template_form"] = fill_template_form(
        full_schema,
        org_name,
        folder_name,
    )
    logger.info("Fill template. Done.")

    logger.info("Save all data to files.")
    save_schema_to_files(full_schema, directory_name)
    logger.info("Save all data to files. Done.")


if __name__ == "__main__":
    main()