import pandas as pd

# Load only required columns from title.basics.tsv
basics = pd.read_csv("data/title.basics.tsv", sep='\t', usecols=["tconst", "primaryTitle", "startYear", "genres", "titleType"], dtype=str)
basics = basics[basics["titleType"] == "movie"]
basics = basics.dropna(subset=["primaryTitle", "startYear", "genres"])
basics = basics[basics["startYear"].str.isnumeric()]
basics["startYear"] = basics["startYear"].astype(int)
basics = basics[(basics["startYear"] >= 1920) & (basics["startYear"] <= 2024)]

# Load ratings and merge
ratings = pd.read_csv("data/title.ratings.tsv", sep='\t', dtype=str)
merged = pd.merge(basics, ratings, on="tconst", how="left")

# Save the reduced dataset
merged.to_csv("data/reduced_movies.csv", index=False)
print("✅ Reduced dataset saved as data/reduced_movies.csv")
