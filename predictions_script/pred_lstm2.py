# predictions_script/pred_lstm.py
def run_prediction(data_file, predict_date):
    import os
    import json
    import joblib
    import pandas as pd
    
    from tensorflow.keras.models import load_model
    from utils.data_loader import load_dataset, save_predictions
    from utils.features import get_lag_dates, prepare_features
    from utils.metric import evaluate_predictions  # fixed name

    RESULTS_DIR = "results"
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # === Use modern Keras model format (.keras) ===
    model_dir = "../resources/LSTM/lag15"
    model_path = os.path.join(model_dir, "lstm_model.keras") 
    
    model = load_model(model_path, compile=False)  # no need to compile for prediction

    # Load scalers
    scaler_X = joblib.load(os.path.join(model_dir, "scaler_X.pkl"))
    scaler_y = joblib.load(os.path.join(model_dir, "scaler_y.pkl"))

    # Load dataset
    df = load_dataset(data_file)

    # --- Ensure Date columns are datetime.date ---
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.date
    predict_date = pd.to_datetime(predict_date).date()

    # Get lag dates
    lag_dates = [d.date() if isinstance(d, pd.Timestamp) else d for d in get_lag_dates(predict_date, 15)]

    # Filter lag data
    df_lag = df[df["Date"].isin(lag_dates)].copy()
    if df_lag.shape[0] < 96 * 15:
        raise ValueError(
            f"Insufficient data to predict {predict_date}. "
            f"Expected 15 full days, got {df_lag['Date'].nunique()} days."
        )

    # Make predictions block by block
    predictions = []
    for block_no in range(1, 97):
        feature_row = prepare_features(
            df_lag[df_lag["block_no"] == block_no],
            lag_dates,
            block_no,
            predict_date
        )
        X_input = scaler_X.transform([feature_row])
        X_input = X_input.reshape((1, 1, len(feature_row)))
        y_pred_scaled = model.predict(X_input, verbose=0)
        y_pred = scaler_y.inverse_transform(y_pred_scaled)[0][0]
        predictions.append([predict_date, block_no, y_pred])

    # Save predictions
    df_pred = pd.DataFrame(predictions, columns=["Date", "block_no", "Predicted_Drawl"])
    pred_file = os.path.join(RESULTS_DIR, f"predictions_{predict_date}.xlsx")
    save_predictions(df_pred, pred_file)

    # Compute metrics if actuals exist
    df_true = df[df["Date"] == predict_date][["Date", "block_no", "Drawl"]]
    metrics = {}
    if not df_true.empty:
        metrics, _ = evaluate_predictions(df_true, df_pred)

    # Save metrics JSON
    metrics_file = os.path.join(RESULTS_DIR, f"metrics_{predict_date}.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=4)

    return df_pred, metrics
