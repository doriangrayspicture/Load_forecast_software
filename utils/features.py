from datetime import timedelta, date
import pandas as pd

def get_lag_dates(predict_date, days):
    """
    Return list of lag dates (oldest → newest) as plain date objects.
    Example: if predict_date = 2024-10-10 and days=7,
    it will return [2024-10-03, ..., 2024-10-09].
    """
    # Ensure predict_date is a date object
    if hasattr(predict_date, "date"):
        predict_date = predict_date.date()
    return [(predict_date - timedelta(days=i)) for i in range(days, 0, -1)]


def prepare_features(df, lag_dates, block_no, predict_date):
    """
    Create features for one block.
    Ensures dates are compared as plain date objects to avoid mismatches.
    """
    # Normalize dataframe dates to plain date objects
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    # Normalize lag_dates to plain date objects
    lag_dates = [pd.to_datetime(d).date() for d in lag_dates]

    # Filter block data
    block_data = df[df["block_no"] == block_no].copy()

    # Select only lag days
    block_data_lag = block_data[block_data["Date"].isin(lag_dates)].copy()

    # Check if we got all required lag days
    if block_data_lag.shape[0] != len(lag_dates):
        missing = set(lag_dates) - set(block_data_lag["Date"])
        raise ValueError(
            f"Missing {len(missing)} days of data for block {block_no}: {sorted(missing)}"
        )

    # 1. Lag features
    lag_values = block_data_lag.sort_values("Date")["Drawl"].values.tolist()

    # 2. Static features from most recent lag date
    last_day_row = block_data_lag[block_data_lag["Date"] == lag_dates[-1]]
    if last_day_row.empty:
        raise ValueError(
            f"Missing static feature row for block {block_no} on {lag_dates[-1]}"
        )

    day_of_week = predict_date.weekday()
    temp = last_day_row["temperature"].values[0]
    holiday = 0  # placeholder

    static_features = [block_no, day_of_week, temp, holiday]

    # 3. Final combined feature vector
    feature_row = lag_values + static_features

    return feature_row
