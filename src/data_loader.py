import pandas as pd
import numpy as np

STYLE_COLORS = {
    "Pack": "#38bdf8",
    "Bowl": "#f59e0b",
    "Cup": "#10b981",
    "Tray": "#a855f7",
    "Box": "#f43f5e",
    "Bar": "#ec4899",
    "Can": "#6366f1",
    "Unknown": "#64748b"
}

def load_ramen_data(csv_path="data/ramen_ratings.csv"):
    df = pd.read_csv(csv_path)
    df["Style_Color"] = df["Style"].map(STYLE_COLORS).fillna("#64748b")
    
    # Compute Brand Aggregates
    brand_stats = df.groupby("Brand").agg(
        review_count=("Stars", "count"),
        avg_stars=("Stars", "mean"),
        country=("Country", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "Unknown"),
        top_ten_count=("Is_Top_Ten", "sum")
    ).reset_index()
    
    return df, brand_stats
