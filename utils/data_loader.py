import pandas as pd

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load dataset from Excel or CSV."""
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Use .xlsx or .csv")
    
    # Standard formatting
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.sort_values(by=["Date", "block_no"]).reset_index(drop=True)
    df["Drawl"] = df["Drawl"].astype(float)

    return df


def save_predictions(df: pd.DataFrame, save_path: str):
    """Save prediction results to Excel or CSV based on extension."""
    if save_path.endswith(".xlsx"):
        df.to_excel(save_path, index=False)
    elif save_path.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        raise ValueError("Unsupported save format. Use .xlsx or .csv")
