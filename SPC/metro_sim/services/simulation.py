from __future__ import annotations
import time
import math
from typing import List, Dict, Any, Optional


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _now_minutes(speed_multiplier: float = 1.0, time_offset: float = 0.0) -> float:
    real_minutes = time.time() / 60.0
    return real_minutes * speed_multiplier + time_offset


def _interpolate(lat1, lng1, lat2, lng2, progress):
    lat = lat1 + (lat2 - lat1) * progress
    lng = lng1 + (lng2 - lng1) * progress
    return lat, lng


# ─────────────────────────────────────────────────────────────
# Simulation Engine
# ─────────────────────────────────────────────────────────────

class SimulationEngine:

    def compute_positions(
        self,
        line: Dict,
        stations: List[Dict],
        intervals: Dict[tuple, float],
        config: Dict,
        speed_multiplier: float = 1.0,
        time_offset: float = 0.0,
    ) -> List[Dict[str, Any]]:

        freq       = config['frequency_minutes']
        turnaround = config['turnaround_minutes']
        dwell      = config.get('dwell_time_min', 2)   # ⭐ NEW

        # Build timeline WITH stops
        timeline = self._build_timeline(stations, intervals, dwell)

        route_time = timeline[-1][1]
        cycle_time = route_time + turnaround + route_time + turnaround

        now = _now_minutes(speed_multiplier, time_offset)
        n_trains = max(1, math.ceil(cycle_time / freq))

        results = []

        for train_idx in range(n_trains):
            offset = train_idx * freq
            train_time = (now - offset) % cycle_time

            pos = self._resolve_position(
                train_time, route_time, turnaround,
                stations, timeline, cycle_time
            )

            if pos:
                pos['train_id']  = train_idx + 1
                pos['line_id']   = line['id']
                pos['line_name'] = line['name']
                pos['line_color']= line['color']
                results.append(pos)

        return results


    # ─────────────────────────────────────────────────────────

    def _build_timeline(self, stations, intervals, dwell):
        """
        Build timeline including travel + stop at each station
        """
        timeline = [(stations[0], 0.0)]
        current_time = 0.0

        for i in range(len(stations) - 1):
            s1 = stations[i]
            s2 = stations[i+1]

            fid = s1['id']
            tid = s2['id']

            travel = intervals.get((fid, tid), intervals.get((tid, fid), 2.5))

            # travel
            current_time += travel
            timeline.append((s2, current_time))

            # stop
            current_time += dwell
            timeline.append((s2, current_time))

        return timeline


    # ─────────────────────────────────────────────────────────

    def _resolve_position(
        self,
        train_time,
        route_time,
        turnaround,
        stations,
        timeline,
        cycle_time,
    ):

        phase_up_end = route_time
        phase_turn1_end = route_time + turnaround
        phase_down_end = route_time + turnaround + route_time

        # ── UP ─────────────────────────────────────────
        if train_time < phase_up_end:
            return self._position_from_timeline(train_time, timeline, 'UP')

        # ── TURNAROUND END ─────────────────────────
        elif train_time < phase_turn1_end:
            s = stations[-1]
            return self._station_stop(s, 'UP')

        # ── DOWN ─────────────────────────────────────────
        elif train_time < phase_down_end:
            down_time = train_time - phase_turn1_end
            reversed_timeline = self._reverse_timeline(timeline)
            return self._position_from_timeline(down_time, reversed_timeline, 'DOWN')

        # ── TURNAROUND START ─────────────────────────
        else:
            s = stations[0]
            return self._station_stop(s, 'DOWN')


    # ─────────────────────────────────────────────────────────

    def _reverse_timeline(self, timeline):
        total = timeline[-1][1]
        return [(s, total - t) for (s, t) in reversed(timeline)]


    # ─────────────────────────────────────────────────────────

    def _position_from_timeline(self, elapsed, timeline, direction):

        for i in range(len(timeline) - 1):
            s1, t1 = timeline[i]
            s2, t2 = timeline[i + 1]

            if t1 <= elapsed <= t2:

                # STOP phase (same station)
                if s1['id'] == s2['id']:
                    return self._station_stop(s1, direction)

                # MOVING phase
                segment_time = t2 - t1
                progress = (elapsed - t1) / segment_time if segment_time > 0 else 0

                lat, lng = _interpolate(
                    s1['latitude'], s1['longitude'],
                    s2['latitude'], s2['longitude'],
                    progress
                )

                return {
                    'direction': direction,
                    'status': 'RUNNING',
                    'from_station': s1['name'],
                    'to_station': s2['name'],
                    'progress': round(progress, 4),
                    'lat': round(lat, 6),
                    'lng': round(lng, 6),
                    'next_station': s2['name'],
                    'eta_minutes': round(t2 - elapsed, 1)
                }

        # fallback
        s = timeline[-1][0]
        return self._station_stop(s, direction)


    # ─────────────────────────────────────────────────────────

    def _station_stop(self, station, direction):
        return {
            'direction': direction,
            'status': 'STOPPED',
            'from_station': station['name'],
            'to_station': station['name'],
            'progress': 0.0,
            'lat': station['latitude'],
            'lng': station['longitude'],
            'next_station': station['name'],
            'eta_minutes': 0
        }


# singleton
engine = SimulationEngine()