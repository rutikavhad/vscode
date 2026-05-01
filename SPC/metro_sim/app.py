"""
Metro Simulation – Flask Application
=====================================
Run with: python app.py
"""
import os
import sys
from flask import Flask, jsonify, request, render_template, abort

# Make local packages importable when running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.data_access import (
    fetch_all_lines,
    fetch_stations_for_line,
    fetch_line_by_id,
    fetch_intervals_for_line,
    fetch_line_config,
    fetch_all_line_ids,
)
from services.simulation import engine

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# HTML entry point
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────────────────────────────────────
# REST API
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/api/lines', methods=['GET'])
def api_lines():
    """Return all metro lines."""
    lines = fetch_all_lines()
    return jsonify(lines)


@app.route('/api/stations', methods=['GET'])
def api_stations():
    """Return ordered stations for a line."""
    line_id = request.args.get('line_id', type=int)
    if line_id is None:
        abort(400, description="line_id query parameter is required")
    stations = fetch_stations_for_line(line_id)
    if not stations:
        abort(404, description=f"No stations found for line_id={line_id}")
    return jsonify(stations)


@app.route('/api/live_trains', methods=['GET'])
def api_live_trains():
    """
    Compute and return live train positions.

    Query params
    ────────────
    line_id          : int   (optional – omit for all lines)
    speed_multiplier : float (optional, default=1.0)
    time_offset      : float minutes to add to simulation clock (optional)
    """
    line_id          = request.args.get('line_id',          type=int)
    speed_multiplier = request.args.get('speed_multiplier', default=1.0, type=float)
    time_offset      = request.args.get('time_offset',      default=0.0, type=float)

    # Clamp speed multiplier to sane range
    speed_multiplier = max(0.1, min(speed_multiplier, 100.0))

    if line_id is not None:
        line_ids = [line_id]
    else:
        line_ids = fetch_all_line_ids()

    all_trains = []
    for lid in line_ids:
        line     = fetch_line_by_id(lid)
        if not line:
            continue
        stations  = fetch_stations_for_line(lid)
        if len(stations) < 2:
            continue
        intervals = fetch_intervals_for_line(lid)
        config    = fetch_line_config(lid)

        trains = engine.compute_positions(
            line=line,
            stations=stations,
            intervals=intervals,
            config=config,
            speed_multiplier=speed_multiplier,
            time_offset=time_offset,
        )
        all_trains.extend(trains)

    return jsonify(all_trains)


@app.route('/api/line_stats', methods=['GET'])
def api_line_stats():
    """Return metadata about each line (route time, train count, etc.)."""
    line_ids = fetch_all_line_ids()
    stats = []
    for lid in line_ids:
        line      = fetch_line_by_id(lid)
        stations  = fetch_stations_for_line(lid)
        intervals = fetch_intervals_for_line(lid)
        config    = fetch_line_config(lid)

        if len(stations) < 2:
            continue

        import math
        cum = [0.0]
        for i in range(len(stations) - 1):
            fid = stations[i]['id']
            tid = stations[i+1]['id']
            t   = intervals.get((fid, tid), intervals.get((tid, fid), 2.5))
            cum.append(cum[-1] + t)

        route_time  = cum[-1]
        turnaround  = config['turnaround_minutes']
        cycle_time  = route_time * 2 + turnaround * 2
        n_trains    = max(1, math.ceil(cycle_time / config['frequency_minutes']))

        stats.append({
            'line_id':          lid,
            'line_name':        line['name'],
            'line_color':       line['color'],
            'station_count':    len(stations),
            'route_time_min':   round(route_time, 1),
            'cycle_time_min':   round(cycle_time, 1),
            'train_count':      n_trains,
            'frequency_min':    config['frequency_minutes'],
            'turnaround_min':   turnaround,
        })
    return jsonify(stats)


# ─────────────────────────────────────────────────────────────────────────────
# Error handlers
# ─────────────────────────────────────────────────────────────────────────────

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Seed if database doesn't exist yet
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metro.db')
    if not os.path.exists(db_path):
        print("Database not found – seeding now…")
        import seed
        seed.seed()

    app.run(debug=True, host='0.0.0.0', port=5000)
