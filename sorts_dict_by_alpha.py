import argparse
from pathlib import Path

from utils.common_func import load_json, save_schema_to_json


def main():
    parser = argparse.ArgumentParser(
        prog="The script sorts a dictionary data alphabetically",
        description="",
    )
    parser.add_argument(
        "file_path",
        type=Path,
        help="dictionary file to process.",
    )
    args = parser.parse_args()

    dictionary_data = load_json(args.file_path)

    dictionary_data["items"].sort(key=lambda dictionary: dictionary["name"])

    save_schema_to_json(dictionary_data, args.file_path)


if __name__ == "__main__":
    main()
