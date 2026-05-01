# 🚇 Metro Live — Real-Time Train Simulator

A full-stack Flask application that **mathematically simulates** metro train movement in real-time. No timetables or stored positions — every train's location is computed on-the-fly using modular cycle arithmetic and linear GPS interpolation.

---

## Architecture Overview

```
metro_sim/
├── app.py                    # Flask routes (REST API)
├── schema.sql                # SQLite schema
├── seed.py                   # Database seed data (3 lines, 39 stations)
├── metro.db                  # Auto-generated SQLite database
├── requirements.txt
├── models/
│   └── database.py           # SQLite connection helper
├── services/
│   ├── simulation.py         # 🧠 Core simulation engine
│   └── data_access.py        # DB query layer
└── templates/
    └── index.html            # Frontend: Leaflet map + real-time UI
```

---

## Quick Start

### 1. Clone / Download

```bash
cd metro_sim
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the Database

```bash
python seed.py
```

### 4. Run the Server

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/lines` | GET | All metro lines (id, name, color) |
| `/api/stations?line_id=N` | GET | Ordered stations for a line |
| `/api/live_trains` | GET | Live positions for all lines |
| `/api/live_trains?line_id=N` | GET | Live positions for one line |
| `/api/live_trains?speed_multiplier=10` | GET | Simulation at 10× speed |
| `/api/line_stats` | GET | Route metadata (train count, cycle time, etc.) |

### Sample Response — `/api/live_trains`

```json
[
  {
    "train_id": 3,
    "line_id": 1,
    "line_name": "Red Line",
    "line_color": "#E63946",
    "direction": "UP",
    "status": "RUNNING",
    "from_station": "Janakpuri West",
    "to_station": "Uttam Nagar West",
    "progress": 0.4231,
    "lat": 28.6267,
    "lng": 77.0619,
    "next_station": "Uttam Nagar West",
    "eta_minutes": 1.5
  }
]
```

---

## Simulation Engine — How It Works

### Cycle Model

```
cycle_time = route_time + turnaround + route_time + turnaround
```

Each train has an **offset** based on its index:

```
offset = train_index × frequency_minutes
train_time = (current_time_minutes - offset) % cycle_time
```

### Phases within a Cycle

| Phase | Condition | Behaviour |
|---|---|---|
| UP direction | `0 ≤ train_time < route_time` | Moving from first → last station |
| Turnaround at END | `route_time ≤ train_time < route_time + turnaround` | Stationary at last station |
| DOWN direction | `route_time + turnaround ≤ train_time < 2×route_time + turnaround` | Moving last → first station |
| Turnaround at START | `2×route_time + turnaround ≤ train_time < cycle_time` | Stationary at first station |

### GPS Interpolation

Between stations, position is linearly interpolated:

```python
lat = lat1 + (lat2 - lat1) * progress
lng = lng1 + (lng2 - lng1) * progress
```

Where `progress = elapsed_time_in_segment / segment_duration`.

---

## Metro Lines (Seed Data)

| Line | Stations | Frequency | Turnaround | Active Trains |
|---|---|---|---|---|
| Red Line | 13 | 6 min | 8 min | ~16 |
| Blue Line | 14 | 5 min | 8 min | ~18 |
| Green Line | 12 | 8 min | 10 min | ~13 |

---

## Frontend Features

- **Dark-themed map** using CartoDB Dark tiles via Leaflet.js
- **Animated train markers** with directional arrows, pulse animation
- **Line toggles** — show/hide individual metro lines
- **Speed multiplier** — simulate at up to 60× real-time for testing
- **Live train list** — scrollable sidebar with ETA to next station
- **Click-to-focus** — clicking a train card flies the map to that train
- **Popup on click** — click any train marker for detailed info
- **Auto-refresh** — every 5 seconds via `fetch()`

---

## Key Constraints (By Design)

- ✅ **No live positions stored in DB** — everything is computed in real-time
- ✅ **No timetable tables** — frequency + math drives everything
- ✅ **Stateless API** — each request independently computes all train states
- ✅ **Multi-line** — all lines run concurrently and independently

---

## Extending the System

**Add a new line:**
1. Insert stations into `stations` table
2. Insert line into `lines` table
3. Add `line_stations` entries with `sequence`
4. Add `station_intervals` for each segment
5. Add `line_config` with frequency and turnaround

**No code changes needed** — the engine is fully data-driven.
