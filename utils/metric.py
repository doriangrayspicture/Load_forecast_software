import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def calculate_metrics(y_true, y_pred):
    """
    Returns common regression metrics.
    y_true: array-like of actual values
    y_pred: array-like of predicted values
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2": r2
    }

def evaluate_predictions(df_true, df_pred):
    """
    Merge actual and predicted values and compute metrics.
    Both dfs must have columns: ["Date", "block_no", "Drawl"/"Predicted_Drawl"]
    """
    merged = pd.merge(
        df_true, df_pred,
        on=["Date", "block_no"],
        how="inner"
    )
    metrics = calculate_metrics(
        merged["Drawl"].values,
        merged["Predicted_Drawl"].values
    )
    return metrics, merged
