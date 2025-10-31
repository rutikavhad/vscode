import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

OMDB_API_KEY = "a7fd314c"  # Replace with your actual OMDB API key
OMDB_BASE = "http://www.omdbapi.com/"

marval_movies = [
  "Avengers: Infinity War",
  "Avengers: Endgame",
  "Black Panther",
  "Guardians of the Galaxy",
  "Thor: Ragnarok",
  "Captain America: The Winter Soldier",
  "Spider-Man: No Way Home",
  "Spider-Man: Homecoming",
  "Shang-Chi and the Legend of the Ten Rings",
  "Guardians of the Galaxy Vol. 3",
  "Captain America: Civil War",
  "Doctor Strange",
  "Ant-Man",
  "Spider-Man: Far From Home",
  "Avengers: Age of Ultron",
  "Captain Marvel",
  "Iron Man",
  "Black Panther: Wakanda Forever",
  "Thor: Love and Thunder",
  "Eternals",
  "Ant-Man and the Wasp",
  "Thor: The Dark World",
  "Iron Man 3",
  "Iron Man 2",
  "The Incredible Hulk",
  "Deadpool & Wolverine",
  "Fantastic Four: First Steps",
  "Spider-Man 2",
  "X-Men: Days of Future Past"

    
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
    rows = fetch_all(marval_movies)
    out = "marval_movies.csv"
    keys = FIELDS + (["Error"] if any("Error" in r for r in rows) else [])
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"✅ Saved {len(rows)} Marvel movies to {out}")
