from flask import render_template, request, session, redirect, url_for
from app import app
import pandas as pd
from app.models.data_loader import load_movie_titles
import requests

# Load the dataset once
movies_df = load_movie_titles()

# Helper function to get movie poster from OMDb
def get_poster_url(tconst):
    try:
        api_key = "afd71581"
        url = f"http://www.omdbapi.com/?i={tconst}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster", "")
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

@app.route("/")
def index():
    years = sorted(movies_df["startYear"].dropna().unique())
    genres = sorted({g.strip() for sublist in movies_df["genres"].dropna().str.split(",") for g in sublist})
    return render_template("index.html", genres=genres, years=years)

@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    year = request.form.get("year")

    # Store filter in session
    session["genre"] = genre
    session["year"] = year

    filtered_df = movies_df.copy()

    if genre:
        filtered_df = filtered_df[filtered_df["genres"].str.contains(genre, na=False)]
    if year and year != "Any":
        filtered_df = filtered_df[filtered_df["startYear"] == int(year)]

    if filtered_df.empty:
        recommendations = pd.DataFrame()
    else:
        recommendations = filtered_df.sample(min(5, len(filtered_df)))[
            ["tconst", "primaryTitle", "startYear", "genres", "averageRating"]
        ]

    if not recommendations.empty and "tconst" in recommendations.columns:
        recommendations["poster_url"] = recommendations["tconst"].apply(get_poster_url)

    return render_template("results.html", recommendations=recommendations)

@app.route("/retry")
def retry():
    genre = session.get("genre")
    year = session.get("year")

    filtered_df = movies_df.copy()
    if genre:
        filtered_df = filtered_df[filtered_df["genres"].str.contains(genre, na=False)]
    if year and year != "Any":
        filtered_df = filtered_df[filtered_df["startYear"] == int(year)]

    if filtered_df.empty:
        recommendations = pd.DataFrame()
    else:
        recommendations = filtered_df.sample(min(5, len(filtered_df)))[
            ["tconst", "primaryTitle", "startYear", "genres", "averageRating"]
        ]

    if not recommendations.empty and "tconst" in recommendations.columns:
        recommendations["poster_url"] = recommendations["tconst"].apply(get_poster_url)

    return render_template("results.html", recommendations=recommendations)

@app.route("/reset")
def reset():
    session.clear()
    filtered_df = movies_df.sample(min(5, len(movies_df)))[
        ["tconst", "primaryTitle", "startYear", "genres", "averageRating"]
    ]
    filtered_df["poster_url"] = filtered_df["tconst"].apply(get_poster_url)
    return render_template("results.html", recommendations=filtered_df)
