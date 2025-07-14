import pandas as pd
import os

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
basics_path = os.path.join(base_dir, 'title.basics.tsv')
ratings_path = os.path.join(base_dir, 'title.ratings.tsv')
output_path = os.path.join(base_dir, 'reduced_movies.csv')

# Load datasets
print("Loading datasets...")
basics = pd.read_csv(basics_path, sep='\t', dtype=str)
ratings = pd.read_csv(ratings_path, sep='\t', dtype=str)

# Filter movies only
print("Filtering movies from 1920–2024...")
df = basics[basics['titleType'] == 'movie']
df = df[['tconst', 'primaryTitle', 'startYear', 'genres']]
df = df.dropna()
df = df[df['startYear'].str.isnumeric()]
df['startYear'] = df['startYear'].astype(int)
df = df[(df['startYear'] >= 1920) & (df['startYear'] <= 2024)]

# Merge with ratings
print("Merging with ratings...")
merged = pd.merge(df, ratings, on='tconst', how='left')
merged = merged.dropna(subset=['averageRating'])

# Sample a subset to keep file small
print("Sampling reduced dataset...")
reduced = merged.sample(n=1000, random_state=42)

# Save to CSV
reduced.to_csv(output_path, index=False)
print(f"✅ Reduced dataset saved as: {output_path}")
