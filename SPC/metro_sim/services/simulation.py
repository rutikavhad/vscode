"""
Metro Train Simulation Engine
==============================
All train positions are computed mathematically from the current system time.
No positions are stored in the database.

Cycle model
-----------
  cycle_time = route_time_up + turnaround + route_time_down + turnaround

For each train offset (0, freq, 2*freq, ...):
  train_time = (now_minutes - offset) % cycle_time

Phases:
  [0 .. route_time)                       → UP   direction
  [route_time .. route_time+turnaround)   → TURNAROUND at last station
  [route_time+turnaround .. 2*route_time+turnaround) → DOWN direction
  [2*route_time+turnaround .. cycle_time) → TURNAROUND at first station
"""

from __future__ import annotations
import time
import math
from typing import List, Dict, Any, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _now_minutes(speed_multiplier: float = 1.0, time_offset: float = 0.0) -> float:
    """Return current simulation time in minutes (with optional speed-up)."""
    real_minutes = time.time() / 60.0
    return real_minutes * speed_multiplier + time_offset


def _interpolate(lat1, lng1, lat2, lng2, progress):
    """Linear interpolation between two GPS points."""
    lat = lat1 + (lat2 - lat1) * progress
    lng = lng1 + (lng2 - lng1) * progress
    return lat, lng


def _haversine_km(lat1, lng1, lat2, lng2):
    """Approximate great-circle distance in km."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# ─────────────────────────────────────────────────────────────────────────────
# Core simulation
# ─────────────────────────────────────────────────────────────────────────────

class SimulationEngine:
    """
    Stateless engine: given line data, computes all live train positions
    for a given moment in time.
    """

    def compute_positions(
        self,
        line: Dict,
        stations: List[Dict],
        intervals: Dict[tuple, float],
        config: Dict,
        speed_multiplier: float = 1.0,
        time_offset: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Compute current positions for all trains on a line.

        Parameters
        ----------
        line        : {id, name, color}
        stations    : ordered list of {id, name, latitude, longitude}
        intervals   : {(from_id, to_id): travel_time_minutes}
        config      : {frequency_minutes, turnaround_minutes}
        speed_multiplier: real-time speed factor (1 = real-time, 10 = 10× faster)
        time_offset : additional minutes offset (for testing)

        Returns
        -------
        List of train position dicts.
        """
        freq       = config['frequency_minutes']
        turnaround = config['turnaround_minutes']

        # Build cumulative travel times along the route (UP direction)
        # cum_times[i] = minutes from station[0] to station[i]
        cum_times = self._cumulative_times(stations, intervals)
        route_time = cum_times[-1]  # total one-way travel time

        cycle_time = route_time + turnaround + route_time + turnaround

        now = _now_minutes(speed_multiplier, time_offset)

        # Number of trains = ceil(cycle_time / freq)
        n_trains = max(1, math.ceil(cycle_time / freq))

        results = []
        for train_idx in range(n_trains):
            offset_minutes = train_idx * freq
            train_time = (now - offset_minutes) % cycle_time

            pos = self._resolve_position(
                train_time, route_time, turnaround,
                stations, cum_times, cycle_time, train_idx
            )
            if pos:
                pos['train_id']  = train_idx + 1
                pos['line_id']   = line['id']
                pos['line_name'] = line['name']
                pos['line_color']= line['color']
                results.append(pos)

        return results

    # ──────────────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────────────

    def _cumulative_times(
        self,
        stations: List[Dict],
        intervals: Dict[tuple, float]
    ) -> List[float]:
        cum = [0.0]
        for i in range(len(stations) - 1):
            fid = stations[i]['id']
            tid = stations[i+1]['id']
            t   = intervals.get((fid, tid), intervals.get((tid, fid), 2.5))
            cum.append(cum[-1] + t)
        return cum

    def _resolve_position(
        self,
        train_time: float,
        route_time: float,
        turnaround: float,
        stations: List[Dict],
        cum_times: List[float],
        cycle_time: float,
        train_idx: int,
    ) -> Optional[Dict]:
        """Map train_time within cycle to a physical GPS position."""

        phase_up_end          = route_time
        phase_turn1_end       = route_time + turnaround
        phase_down_end        = route_time + turnaround + route_time
        # phase_turn2_end    = cycle_time

        # ── Phase 1: UP direction ─────────────────────────────────────────
        if train_time < phase_up_end:
            elapsed = train_time
            return self._position_along_route(
                elapsed, stations, cum_times, direction='UP'
            )

        # ── Phase 2: Turnaround at LAST station ───────────────────────────
        elif train_time < phase_turn1_end:
            s = stations[-1]
            remaining = phase_turn1_end - train_time
            return {
                'direction':    'UP',
                'status':       'TURNAROUND',
                'from_station': s['name'],
                'to_station':   s['name'],
                'progress':     0.0,
                'lat':          s['latitude'],
                'lng':          s['longitude'],
                'next_station': stations[-2]['name'] if len(stations) > 1 else s['name'],
                'eta_minutes':  round(remaining, 1),
            }

        # ── Phase 3: DOWN direction ───────────────────────────────────────
        elif train_time < phase_down_end:
            elapsed = train_time - phase_turn1_end
            return self._position_along_route(
                elapsed, list(reversed(stations)),
                list(reversed([route_time - t for t in cum_times])),
                direction='DOWN'
            )

        # ── Phase 4: Turnaround at FIRST station ──────────────────────────
        else:
            s = stations[0]
            remaining = cycle_time - train_time
            return {
                'direction':    'DOWN',
                'status':       'TURNAROUND',
                'from_station': s['name'],
                'to_station':   s['name'],
                'progress':     0.0,
                'lat':          s['latitude'],
                'lng':          s['longitude'],
                'next_station': stations[1]['name'] if len(stations) > 1 else s['name'],
                'eta_minutes':  round(remaining, 1),
            }

    def _position_along_route(
        self,
        elapsed: float,
        stations: List[Dict],
        cum_times: List[float],
        direction: str,
    ) -> Dict:
        """Find which segment the train is on and interpolate GPS."""
        n = len(stations)
        # Clamp
        elapsed = max(0.0, min(elapsed, cum_times[-1]))

        # Binary-search for segment
        seg_idx = 0
        for i in range(n - 1):
            if cum_times[i] <= elapsed <= cum_times[i+1]:
                seg_idx = i
                break
            elif elapsed > cum_times[i+1]:
                seg_idx = i + 1

        seg_idx = min(seg_idx, n - 2)
        s1 = stations[seg_idx]
        s2 = stations[seg_idx + 1]

        seg_duration = cum_times[seg_idx + 1] - cum_times[seg_idx]
        if seg_duration > 0:
            progress = (elapsed - cum_times[seg_idx]) / seg_duration
        else:
            progress = 0.0
        progress = max(0.0, min(1.0, progress))

        lat, lng = _interpolate(
            s1['latitude'], s1['longitude'],
            s2['latitude'], s2['longitude'],
            progress
        )

        # ETA to next station
        time_in_seg = elapsed - cum_times[seg_idx]
        eta = seg_duration - time_in_seg

        return {
            'direction':    direction,
            'status':       'RUNNING',
            'from_station': s1['name'],
            'to_station':   s2['name'],
            'progress':     round(progress, 4),
            'lat':          round(lat, 6),
            'lng':          round(lng, 6),
            'next_station': s2['name'],
            'eta_minutes':  round(max(0.0, eta), 1),
        }


# Singleton
engine = SimulationEngine()
