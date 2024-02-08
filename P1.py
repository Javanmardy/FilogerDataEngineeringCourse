import argparse
import os
import datetime
import requests
import logging

logging.basicConfig(filename="info.log", level=logging.INFO)
error_logger = logging.getLogger("error_logger")
error_logger.addHandler(logging.FileHandler("error.log"))


def file(url, destination):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(destination, "wb") as file:
                file.write(response.content)
            logging.info(f"Downloaded market data for {destination}")
            return True
        else:
            error_logger.error(
                f"Failed to download file at {url}. Status code: {response.status_code}"
            )
            return False
    except Exception as e:
        error_logger.error(f"Error downloading file at {url}. Error: {e}")
        return False


def market(start_date, end_date, stage_folder):
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() not in [3, 4]:  # Skip Thursdays and Fridays
            formatted_date = current_date.strftime("%Y%m%d")
            url = f"http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d={formatted_date}"
            file_name = f"market_data_{current_date}.xlsx"
            file_path = os.path.join(stage_folder, file_name)

            file(url, file_path)
        current_date += datetime.timedelta(days=1)


def arg():
    parser = argparse.ArgumentParser(
        description="Download market data for a specific date range."
    )
    parser.add_argument(
        "start_date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "end_date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="End date (YYYY-MM-DD)",
    )
    parser.add_argument("stage_folder", type=str, help="Path to the stage folder")
    return parser


def main():
    parser = arg()
    args = parser.parse_args()

    if not os.path.exists(args.stage_folder):
        os.makedirs(args.stage_folder)

    market(args.start_date, args.end_date, args.stage_folder)


if __name__ == "__main__":
    main()
