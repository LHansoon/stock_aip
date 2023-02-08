import pandas as pd
import datetime

def get_purchase_date(df, reference_date, interval):
    return df.loc[(df["date"] - reference_date).dt.days % interval == 0]

def print_hi():
    # read data and initialize var
    df_stock_price = pd.read_csv("MacroTrends_Data_Download_IBM_excel.csv")
    df_exchange_rate = pd.read_csv("USD_CAD Historical 2000.csv")
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 7, 1)

    TERM_INVEST_CAD = 191.65
    FMV_RATIO = 0
    ESPP_DISCOUNT_RATIO = 0.85
    LAST_PRICE_QUOTE = None
    LAST_EXCHANGE_RATE = None
    CMSSN_EACH_TRANS = 15
    CMSSN_EACH_SHARE = 0.1
    WISE_RECEIVE_FEE = 4.14
    WISE_EST_SEND_FEE = 7.56

    avg_purchase_price_usd = None
    total_purchased_share = None
    gross_gain = None
    est_gain = None

    # re-map column name
    df_exchange_rate.rename(mapper={"Date": "date", "Price": "exchange_rate"}, axis=1, inplace=True)
    df_stock_price.rename(mapper={"Date": "date", "Close": "price_stock"}, axis=1, inplace=True)

    # drop not needed columns
    df_exchange_rate = df_exchange_rate.drop(df_exchange_rate.columns[[2, 3, 4, 5, 6]], axis=1)
    df_stock_price = df_stock_price.drop(df_stock_price.columns[[1, 2, 3, 5, 6]], axis=1)

    # convert date to datetime
    df_exchange_rate['date'] = pd.to_datetime(df_exchange_rate['date'], format='%Y-%m-%d')
    df_stock_price['date'] = pd.to_datetime(df_stock_price['date'], format='%Y-%m-%d')

    # filter valid time frame
    start_date = max(start_date, min(df_exchange_rate['date']), min(df_stock_price['date']))
    end_date = min(end_date, max(df_exchange_rate['date']), max(df_stock_price['date']))

    # filter rows based on time frame
    df_exchange_rate = df_exchange_rate.loc[(df_exchange_rate['date'] >= start_date) & (df_exchange_rate['date'] <= end_date)]
    df_stock_price = df_stock_price.loc[(df_stock_price['date'] >= start_date) & (df_stock_price['date'] <= end_date)]

    # fill empty value
    df_time = pd.DataFrame(pd.date_range(start=start_date, end=end_date))
    df_time.columns = ["date"]
    df_exchange_rate = pd.merge(df_time, df_exchange_rate, how='left', on="date")
    df_stock_price = pd.merge(df_time, df_stock_price, how='left', on="date")

    df_exchange_rate["exchange_rate"] = df_exchange_rate["exchange_rate"].fillna(method="backfill")
    df_stock_price["price_stock"] = df_stock_price["price_stock"].fillna(method="backfill")

    # filter Monday data only for stock price
    df_stock_price = get_purchase_date(df_stock_price, datetime.datetime(2023, 2, 3), 14)
    df = pd.merge(df_stock_price, df_exchange_rate, how='left', on="date")
    LAST_PRICE_QUOTE = df.loc[df["date"] == max(df["date"])]["price_stock"]
    # LAST_PRICE_QUOTE = 136.94
    # LAST_EXCHANGE_RATE = 1.34
    LAST_EXCHANGE_RATE = df.loc[df["date"] == max(df["date"])]["exchange_rate"]

    df["purchased_price"] = df["price_stock"] * (1 + FMV_RATIO) * ESPP_DISCOUNT_RATIO
    df["purchased_share"] = TERM_INVEST_CAD / df["exchange_rate"] / df["purchased_price"]
    avg_purchase_price_usd = df["purchased_price"].mean()
    total_purchased_share = df["purchased_share"].sum()

    gross_gain = float((LAST_PRICE_QUOTE - avg_purchase_price_usd) * total_purchased_share)
    est_gain = gross_gain - CMSSN_EACH_TRANS - CMSSN_EACH_SHARE * total_purchased_share - WISE_EST_SEND_FEE - WISE_RECEIVE_FEE
    est_gain_perc = est_gain / (avg_purchase_price_usd * total_purchased_share) * 100

    est_gain_cad = float(est_gain * LAST_EXCHANGE_RATE)
    est_gain_perc_cad = est_gain_cad / (len(df.index) * TERM_INVEST_CAD) * 100

    print(f"Estimate gain: \t\t\t\t{est_gain}\t\tCAD: {est_gain_cad}")
    print(f"Estimate gain percentage: \t{est_gain_perc}%\t\tCAD: {est_gain_perc_cad}%")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

