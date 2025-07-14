# ✅ data_loader.py (Final version using correct basics file with 'startYear')
import pandas as pd
import os
import gdown

def download_datasets():
    basics_url = "https://drive.google.com/uc?id=15rOmCPA30v9insgci4-HA_DiqhCJZ7G0"
    ratings_url = "https://drive.google.com/uc?id=1dHibMcDCCEC0QvPi8Eatr8UXCa4-MtFi"

    os.makedirs("data", exist_ok=True)

    basics_path = "data/title.basics.tsv"
    ratings_path = "data/title.ratings.tsv"

    if not os.path.exists(basics_path):
        print("⬇️ Downloading title.basics.tsv...")
        gdown.download(basics_url, basics_path, quiet=False)

    if not os.path.exists(ratings_path):
        print("⬇️ Downloading title.ratings.tsv...")
        gdown.download(ratings_url, ratings_path, quiet=False)

    return basics_path, ratings_path

def load_movie_titles():
    print("📦 Ensuring datasets are available...")
    basics_path, ratings_path = download_datasets()

    print("📦 Loading title.basics.tsv and title.ratings.tsv...")

    # Load basics file (with startYear column)
    basics_df = pd.read_csv(basics_path, sep='\t', dtype=str, na_values='\\N')
    print("✅ Basics loaded. Columns:", basics_df.columns.tolist())

    # Convert numeric fields safely
    basics_df['startYear'] = pd.to_numeric(basics_df['startYear'], errors='coerce')
    basics_df['runtimeMinutes'] = pd.to_numeric(basics_df['runtimeMinutes'], errors='coerce')

    # Filter for movies only
    basics_df = basics_df[basics_df['titleType'] == 'movie']

    # Load ratings
    ratings_df = pd.read_csv(ratings_path, sep='\t', dtype={'tconst': str, 'averageRating': float, 'numVotes': int})
    print("✅ Ratings loaded. Columns:", ratings_df.columns.tolist())

    # Merge basics and ratings on 'tconst'
    merged_df = pd.merge(basics_df, ratings_df, on='tconst', how='inner')

    # Filter years between 1920 and 2024
    merged_df = merged_df[(merged_df['startYear'] >= 1920) & (merged_df['startYear'] <= 2024)]

    # Drop rows with missing important info
    merged_df.dropna(subset=['primaryTitle', 'startYear', 'genres'], inplace=True)

    print(f"🎬 Final movie dataset contains {len(merged_df)} movies between 1920–2024.")
    return merged_df.reset_index(drop=True)