import argparse
import os
import pandas as pd
import logging

logging.basicConfig(filename="info.log", level=logging.INFO)
error_logger = logging.getLogger("error_logger")
error_logger.addHandler(logging.FileHandler("error.log"))


def convert(file_path, delete_original=False):
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            logging.info(f"File {file_path} is empty. Deleting...")
            os.remove(file_path)
            return False

        csv_file_path = file_path.replace(".xlsx", ".csv")
        df.to_csv(csv_file_path, index=False)
        logging.info(f"Converted {file_path} to {csv_file_path}")

        if delete_original:
            os.remove(file_path)
            logging.info(f"Deleted original file {file_path}")

        return True
    except Exception as e:
        error_logger.error(f"Error processing file {file_path}: {e}")
        return False


def process(stage_folder, delete_original):
    for file_name in os.listdir(stage_folder):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(stage_folder, file_name)
            convert(file_path, delete_original)


def arg():
    parser = argparse.ArgumentParser(
        description="Process Excel files in the stage folder."
    )
    parser.add_argument("stage_folder", type=str, help="Path to the stage folder")
    parser.add_argument(
        "--delete_original",
        action="store_true",
        help="Delete the original Excel files after conversion",
    )
    return parser


def main():
    parser = arg()
    args = parser.parse_args()

    process(args.stage_folder, args.delete_original)


if __name__ == "__main__":
    main()
