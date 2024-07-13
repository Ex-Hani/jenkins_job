import argparse
from pathlib import Path

from utils.common_func import load_json, save_schema_to_json, order_redefine


def main():
    parser = argparse.ArgumentParser(
        prog="order redefine",
        description="The script redefine order in json-file.",
    )
    parser.add_argument(
        "file_path",
        type=Path,
        help="Path to vacancy request or vacancy field file.",
    )
    args = parser.parse_args()

    schema_to_dict = load_json(args.file_path)
    schema_to_dict["schema"] = order_redefine(schema_to_dict["schema"])

    save_schema_to_json(schema_to_dict, args.file_path)


if __name__ == "__main__":
    main()
