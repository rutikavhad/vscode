"""Data access layer – PostgreSQL version"""

from services.db import get_connection


# ─────────────────────────────────────────────────────────────
# LINES
# ─────────────────────────────────────────────────────────────

def fetch_all_lines():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT route_id, route_name
        FROM routes
        ORDER BY route_id
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "color": "#FF5733"  # temporary color
        }
        for r in rows
    ]


def fetch_line_by_id(line_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT route_id, route_name
        FROM routes
        WHERE route_id = %s
    """, (line_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "color": "#FF5733"
    }


def fetch_all_line_ids():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT route_id FROM routes ORDER BY route_id")

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]


# ─────────────────────────────────────────────────────────────
# STATIONS
# ─────────────────────────────────────────────────────────────

def fetch_stations_for_line(line_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.station_id, s.station_name, s.lat, s.lng, rs.station_order
        FROM route_stations rs
        JOIN stations s ON s.station_id = rs.station_id
        WHERE rs.route_id = %s
        ORDER BY rs.station_order
    """, (line_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "latitude": r[2],
            "longitude": r[3],
            "order": r[4]
        }
        for r in rows
    ]


# ─────────────────────────────────────────────────────────────
# INTERVALS
# ─────────────────────────────────────────────────────────────

def fetch_intervals_for_line(line_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT from_station, to_station, travel_time_min
        FROM station_intervals
        WHERE route_id = %s
    """, (line_id,))

    rows = cur.fetchall()
    conn.close()

    return {
        (r[0], r[1]): r[2]
        for r in rows
    }


# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

def fetch_line_config(line_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT frequency_minutes, turnaround_minutes, dwell_time_min
        FROM line_config
        WHERE route_id = %s
        LIMIT 1
    """, (line_id,))

    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "frequency_minutes": row[0],
            "turnaround_minutes": row[1],
            "dwell_time_min": row[2]   # ⭐ NEW
        }

    return {
        "frequency_minutes": 6,
        "turnaround_minutes": 8,
        "dwell_time_min": 2
    }