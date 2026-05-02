"""
Seed the database with realistic metro data.
Uses a fictional city metro system with 3 lines.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'metro.db')

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path) as f:
        cur.executescript(f.read())

    # Clear existing data
    for table in ['station_intervals', 'line_stations', 'line_config', 'lines', 'stations']:
        cur.execute(f'DELETE FROM {table}')
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('stations','lines','line_stations','station_intervals','line_config')")

    # ─────────────────────────────────────────────────────────────────────────
    # STATIONS  (loosely based on a fictional city grid)
    # ─────────────────────────────────────────────────────────────────────────
    stations = [
        # Line 1 – Red Line (East–West corridor)
        (1,  "Airport Terminal",        28.5562, 77.1000),
        (2,  "Dwarka Sector 21",        28.5529, 77.0588),
        (3,  "Dwarka Sector 10",        28.5714, 77.0714),
        (4,  "Janakpuri West",          28.6307, 77.0830),
        (5,  "Uttam Nagar West",        28.6213, 77.0450),
        (6,  "Uttam Nagar East",        28.6228, 77.0560),
        (7,  "Nawada",                  28.6248, 77.0670),
        (8,  "Dwarka Mor",              28.6188, 77.0591),
        (9,  "Central Interchange",     28.6353, 77.2250),
        (10, "City Park",               28.6420, 77.2090),
        (11, "Old Quarter",             28.6508, 77.2300),
        (12, "East Gate",               28.6600, 77.2500),
        (13, "University North",        28.6900, 77.2100),

        # Line 2 – Blue Line (North–South corridor)
        (14, "North Terminal",          28.7500, 77.1200),
        (15, "Model Town",              28.7200, 77.1180),
        (16, "GTB Nagar",               28.7000, 77.1170),
        (17, "Vishwa Vidyalaya",        28.6890, 77.2093),
        (18, "Chandni Chowk",           28.6569, 77.2303),
        (19, "New Delhi Station",       28.6431, 77.2194),
        (20, "Rajiv Chowk Hub",         28.6333, 77.2190),
        (21, "Patel Chowk",             28.6255, 77.2148),
        (22, "Central Secretariat",     28.6138, 77.2120),
        (23, "Udyog Bhawan",            28.6110, 77.2110),
        (24, "Lok Kalyan Marg",         28.5990, 77.2050),
        (25, "South Extension",         28.5700, 77.2200),
        (26, "AIIMS Station",           28.5680, 77.2093),
        (27, "South Terminal",          28.5200, 77.2050),

        # Line 3 – Green Line (Circular / inner ring)
        (28, "Tech Hub",                28.6800, 77.1500),
        (29, "Stadium West",            28.6700, 77.1700),
        (30, "Museum Quarter",          28.6600, 77.1900),
        (31, "Art District",            28.6500, 77.2000),
        (32, "Finance Tower",           28.6350, 77.1950),
        (33, "Market Square",           28.6200, 77.1800),
        (34, "Waterfront",              28.6100, 77.1600),
        (35, "Industrial Park",         28.6050, 77.1400),
        (36, "West Bridge",             28.6100, 77.1200),
        (37, "Sports Complex",          28.6250, 77.1100),
        (38, "Convention Center",       28.6450, 77.1150),
        (39, "Innovation Hub",          28.6650, 77.1300),
    ]

    cur.executemany(
        'INSERT INTO stations (id, name, latitude, longitude) VALUES (?,?,?,?)',
        stations
    )

    # ─────────────────────────────────────────────────────────────────────────
    # LINES
    # ─────────────────────────────────────────────────────────────────────────
    lines = [
        (1, "Red Line",   "#E63946"),
        (2, "Blue Line",  "#457B9D"),
        (3, "Green Line", "#2D6A4F"),
    ]
    cur.executemany('INSERT INTO lines (id, name, color) VALUES (?,?,?)', lines)

    # ─────────────────────────────────────────────────────────────────────────
    # LINE STATIONS
    # ─────────────────────────────────────────────────────────────────────────
    line_stations = []
    red_order   = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    blue_order  = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    green_order = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]

    for seq, sid in enumerate(red_order,   1): line_stations.append((1, sid, seq))
    for seq, sid in enumerate(blue_order,  1): line_stations.append((2, sid, seq))
    for seq, sid in enumerate(green_order, 1): line_stations.append((3, sid, seq))

    cur.executemany(
        'INSERT INTO line_stations (line_id, station_id, sequence) VALUES (?,?,?)',
        line_stations
    )

    # ─────────────────────────────────────────────────────────────────────────
    # STATION INTERVALS  (minutes)
    # ─────────────────────────────────────────────────────────────────────────
    def intervals_for(order, times):
        rows = []
        for i, t in enumerate(times):
            rows.append((order[i], order[i+1], t))
            rows.append((order[i+1], order[i], t))   # reverse same time
        return rows

    red_times   = [4.0, 3.5, 3.0, 2.5, 2.5, 2.0, 2.5, 4.0, 3.5, 3.0, 3.5, 4.0]
    blue_times  = [3.5, 3.0, 3.5, 4.0, 2.5, 2.0, 2.0, 2.5, 2.0, 2.5, 4.0, 3.0, 3.5]
    green_times = [3.0, 3.5, 3.0, 3.5, 3.0, 3.5, 3.0, 3.5, 3.0, 3.5, 3.0]

    intervals = []
    intervals += intervals_for(red_order,   red_times)
    intervals += intervals_for(blue_order,  blue_times)
    intervals += intervals_for(green_order, green_times)

    cur.executemany(
        'INSERT INTO station_intervals (from_station_id, to_station_id, travel_time_minutes) VALUES (?,?,?)',
        intervals
    )

    # ─────────────────────────────────────────────────────────────────────────
    # LINE CONFIG
    # ─────────────────────────────────────────────────────────────────────────
    configs = [
        (1, 1, '05:00', '23:30', 6,  8),
        (2, 2, '05:00', '23:30', 5,  8),
        (3, 3, '06:00', '22:00', 8, 10),
    ]
    cur.executemany(
        'INSERT INTO line_config (id, line_id, start_time, end_time, frequency_minutes, turnaround_minutes) VALUES (?,?,?,?,?,?)',
        configs
    )

    conn.commit()
    conn.close()
    print("✅ Database seeded successfully.")

if __name__ == '__main__':
    seed()
