import argparse
from collections import namedtuple
from pathlib import Path

from loguru import logger

from utils.common_func import (
    load_json,
    save_schema_to_files,
    get_cells,
    fill_template_form,
    get_field_type,
)
from field_constructor import dictionary_field


def get_params(
    current_path: Path,
    mapping_file: Path,
):
    parser = argparse.ArgumentParser(
        prog="create_dictionary",
        description="The script creates a structured file of dictionary."
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
        "--map_file",
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
        args.map_file,
        args.org_name,
        args.disable_dict_value_capitalize,
    )


def main():
    current_path = Path.cwd()
    mapping_file = current_path / "common_files" / "fields_mapping.json"

    (
        input_file,
        folder_name,
        output_path,
        map_file,
        org_name,
        disable_dict_value_capitalize,
    ) = get_params(current_path, mapping_file)

    dictionaries = {}
    full_schema = {}

    filled_rows = get_cells(input_file, 4)

    mapping_file_path = Path(map_file)
    mapping_filetypes = load_json(mapping_file_path)

    directory_name = Path() / output_path / folder_name
    directory_name.mkdir(parents=True, exist_ok=True)

    logger.info("Prepare data")

    rows_name = ["eng_field_name", "title", "field_type_rus", "dictionary_values"]
    Row = namedtuple(
        "Row",
        rows_name,
    )

    for row in filled_rows:
        current_row = Row(*row)
        field_type = get_field_type(current_row.field_type_rus, mapping_filetypes)

        logger.info("Processing field {}".format(current_row.eng_field_name))

        full_schema["dictionaries"] = dictionary_field.dictionary_prepare(
            current_row,
            dictionaries,
            field_type,
            disable_dict_value_capitalize,
        )

    logger.info("Prepare data. Done.")

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
