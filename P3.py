import pandas as pd
import os
import argparse
import logging

logging.basicConfig(filename="info.log", level=logging.INFO)
error_logger = logging.getLogger("error_logger")
error_logger.addHandler(logging.FileHandler("error.log"))


class MarketDataAnalyzer:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_data(self):
        try:
            files = [f for f in os.listdir(self.folder_path) if f.endswith(".csv")]
            dfs = []
            for file in files:
                df = pd.read_csv(os.path.join(self.folder_path, file), skiprows=2)
                dfs.append(df)
            logging.info("Data loaded successfully.")
            return pd.concat(dfs, ignore_index=True)
        except Exception as e:
            error_logger.error(f"Error in loading data: {e}")
            return pd.DataFrame()

    def top_traded_symbols(self, df, top_n=10):
        try:
            df["حجم"] = pd.to_numeric(df["حجم"], errors="coerce")
            top_symbols = df.groupby("نماد")["حجم"].sum().nlargest(top_n)
            logging.info(f"Top traded symbols: {top_symbols}")
            return top_symbols
        except Exception as e:
            error_logger.error(f"Error in top_traded_symbols: {e}")
            return pd.Series()

    def top_price_increase(self, df, top_n=10):
        try:
            df["قیمت پایانی - مقدار"] = pd.to_numeric(
                df["قیمت پایانی - مقدار"], errors="coerce"
            )
            df["اولین"] = pd.to_numeric(df["اولین"], errors="coerce")
            df["PriceChange"] = df["قیمت پایانی - مقدار"] - df["اولین"]
            top_increase = df.groupby("نماد")["PriceChange"].sum().nlargest(top_n)
            logging.info(f"Top symbols with price increase: {top_increase}")
            return top_increase
        except Exception as e:
            error_logger.error(f"Error in top_price_increase: {e}")
            return pd.Series()

    def top_price_decrease(self, df, top_n=10):
        """Find top N symbols with the highest price decrease."""
        try:
            df["PriceChange"] = df["قیمت پایانی - مقدار"] - df["اولین"]
            top_decrease = df.groupby("نماد")["PriceChange"].sum().nsmallest(top_n)
            logging.info(f"Top symbols with price decrease: {top_decrease}")
            return top_decrease
        except Exception as e:
            error_logger.error(f"Error in top_price_decrease: {e}")
            return pd.Series()


def main(folder_path):
    try:
        analyzer = MarketDataAnalyzer(folder_path)
        df = analyzer.load_data()

        logging.info("Top Traded Symbols:")
        logging.info(analyzer.top_traded_symbols(df))

        logging.info("\nTop Symbols with Price Increase:")
        logging.info(analyzer.top_price_increase(df))

        logging.info("\nTop Symbols with Price Decrease:")
        logging.info(analyzer.top_price_decrease(df))
    except Exception as e:
        error_logger.error(f"Error in main function: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Market Data")
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing CSV files"
    )
    args = parser.parse_args()
    main(args.folder_path)


def top_price_increase(self, df, top_n=10):
    df["قیمت پایانی - مقدار"] = pd.to_numeric(
        df["قیمت پایانی - مقدار"], errors="coerce"
    )
    df["اولین"] = pd.to_numeric(df["اولین"], errors="coerce")

    df["PriceChange"] = df["قیمت پایانی - مقدار"] - df["اولین"]

    return df.groupby("نماد")["PriceChange"].sum().nlargest(top_n)
