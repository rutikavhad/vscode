import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

OMDB_API_KEY = "YOUR_OMDB_API_KEY"  # Replace with your actual OMDB API key
OMDB_BASE = "http://www.omdbapi.com/"

marvel_movies = [
    "Iron Man",
    "The Incredible Hulk",
    "Iron Man 2",
    "Thor",
    "Captain America: The First Avenger",
    "The Avengers",
    "Iron Man 3",
    "Thor: The Dark World",
    "Captain America: The Winter Soldier",
    "Guardians of the Galaxy",
    "Avengers: Age of Ultron",
    "Ant-Man",
    "Captain America: Civil War",
    "Doctor Strange",
    "Guardians of the Galaxy Vol. 2",
    "Spider-Man: Homecoming",
    "Thor: Ragnarok",
    "Black Panther",
    "Avengers: Infinity War",
    "Avengers: Endgame"
]

FIELDS = [
    "Title","Year","Runtime","Genre","Director","Writer","Actors",
    "Plot","Language","Country","imdbRating","imdbVotes","imdbID","BoxOffice","Production"
]

def fetch_one(title):
    params = {"apikey": OMDB_API_KEY, "t": title}
    r = requests.get(OMDB_BASE, params=params, timeout=10)
    data = r.json()
    if data.get("Response") == "True":
        return {f: data.get(f, "") for f in FIELDS}
    else:
        return {"Title": title, "Error": data.get("Error", "No data")}

def fetch_all(movie_list):
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(fetch_one, m): m for m in movie_list}
        for fut in as_completed(futures):
            results.append(fut.result())
    return results

if __name__ == "__main__":
    rows = fetch_all(marvel_movies)
    out = "marvel_movies.csv"
    keys = FIELDS + (["Error"] if any("Error" in r for r in rows) else [])
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"✅ Saved {len(rows)} Marvel movies to {out}")
