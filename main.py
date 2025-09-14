import argparse
from pathlib import Path
import pandas as pd
from src.ingest_clean import load_and_clean
from src.eda import daily_sales, kpis
from src.forecasting import sarima_forecast

def main(csv: str):
    df, date_col = load_and_clean(csv)
    print("Rows:", len(df), "| Date column:", date_col)
    print("Date range:", df[date_col].min(), "→", df[date_col].max())
    print("KPIs:", kpis(df))
    ts = daily_sales(df)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    ts.to_csv("data/processed/daily_sales.csv", index=False)
    print("Saved daily sales to data/processed/daily_sales.csv")
    fc, mape = sarima_forecast(df, date_col=date_col, horizon_days=30)
    fc.to_csv("data/processed/forecast_30d.csv", index=False)
    print("Saved 30-day forecast to data/processed/forecast_30d.csv | MAPE:", mape)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to your coffee sales CSV")
    args = ap.parse_args()
    main(args.csv)
