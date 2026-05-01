"""Data access layer – pure query functions, no business logic."""
from models.database import get_db


def fetch_all_lines():
    db = get_db()
    rows = db.execute('SELECT id, name, color FROM lines ORDER BY id').fetchall()
    db.close()
    return [dict(r) for r in rows]


def fetch_stations_for_line(line_id: int):
    db = get_db()
    rows = db.execute(
        '''
        SELECT s.id, s.name, s.latitude, s.longitude, ls.sequence
        FROM stations s
        JOIN line_stations ls ON ls.station_id = s.id
        WHERE ls.line_id = ?
        ORDER BY ls.sequence
        ''',
        (line_id,)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def fetch_line_by_id(line_id: int):
    db = get_db()
    row = db.execute('SELECT id, name, color FROM lines WHERE id = ?', (line_id,)).fetchone()
    db.close()
    return dict(row) if row else None


def fetch_intervals_for_line(line_id: int):
    """
    Returns dict {(from_id, to_id): travel_time} for all segments on a line.
    Includes both directions.
    """
    db = get_db()
    rows = db.execute(
        '''
        SELECT si.from_station_id, si.to_station_id, si.travel_time_minutes
        FROM station_intervals si
        WHERE si.from_station_id IN (
            SELECT station_id FROM line_stations WHERE line_id = ?
        )
        OR si.to_station_id IN (
            SELECT station_id FROM line_stations WHERE line_id = ?
        )
        ''',
        (line_id, line_id)
    ).fetchall()
    db.close()
    return {(r['from_station_id'], r['to_station_id']): r['travel_time_minutes'] for r in rows}


def fetch_line_config(line_id: int):
    db = get_db()
    row = db.execute(
        'SELECT * FROM line_config WHERE line_id = ?', (line_id,)
    ).fetchone()
    db.close()
    return dict(row) if row else {
        'line_id': line_id,
        'start_time': '05:00',
        'end_time': '23:00',
        'frequency_minutes': 6,
        'turnaround_minutes': 8,
    }


def fetch_all_line_ids():
    db = get_db()
    rows = db.execute('SELECT id FROM lines ORDER BY id').fetchall()
    db.close()
    return [r['id'] for r in rows]
