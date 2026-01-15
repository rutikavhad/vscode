from in_state.data.state import STATES
from in_state.data.district import DISTRICTS
from in_state.data.tehsil import TEHSILS
from in_state.data.state_village import get_villages_by_state_tehsil


class LocationEngine:
    def __init__(self):
        self.state_id = None
        self.district_id = None
        self.tehsil_id = None

    # ---------- helpers ----------
    def _find_key_by_name(self, data: dict, name: str):
        for k, v in data.items():
            if v.lower() == name.lower():
                return k
        return None

    # ---------- state ----------
    def get_states(self):
        return list(STATES.values())

    def select_state(self, state_name):
        state_id = self._find_key_by_name(STATES, state_name)
        if not state_id:
            raise ValueError("Invalid state name")

        self.state_id = state_id
        self.district_id = None
        self.tehsil_id = None
        return state_name

    # ---------- district ----------
    def get_districts(self):
        if not self.state_id:
            raise ValueError("Select state first")

        return list(DISTRICTS.get(self.state_id, {}).values())

    def select_district(self, district_name):
        if not self.state_id:
            raise ValueError("Select state first")

        district_id = self._find_key_by_name(
            DISTRICTS.get(self.state_id, {}), district_name
        )
        if not district_id:
            raise ValueError("Invalid district name")

        self.district_id = district_id
        self.tehsil_id = None
        return district_name

    # ---------- tehsil ----------
    def get_tehsils(self):
        if not self.district_id:
            raise ValueError("Select district first")

        return list(TEHSILS.get(self.district_id, {}).values())

    def select_tehsil(self, tehsil_name):
        if not self.district_id:
            raise ValueError("Select district first")

        tehsil_id = self._find_key_by_name(
            TEHSILS.get(self.district_id, {}), tehsil_name
        )
        if not tehsil_id:
            raise ValueError("Invalid tehsil name")

        self.tehsil_id = tehsil_id
        return tehsil_name

    # ---------- village ----------
    def get_villages(self):
        if not self.tehsil_id:
            raise ValueError("Select tehsil first")

        villages = get_villages_by_state_tehsil(
            self.state_id, self.tehsil_id
        )
        return list(villages.values())

    def select_village(self, village_name):
        if not self.tehsil_id:
            raise ValueError("Select tehsil first")

        villages = get_villages_by_state_tehsil(
            self.state_id, self.tehsil_id
        )

        village_id = self._find_key_by_name(villages, village_name)
        if not village_id:
            raise ValueError("Invalid village name")

        return village_name

    # ---------- VALIDATION ----------
    def validate(self, state, district, tehsil, village) -> bool:
        # ---- STATE ----
        state_id = self._find_key_by_name(STATES, state)
        if not state_id:
            return False

        # ---- DISTRICT ----
        districts = DISTRICTS.get(state_id, {})
        district_id = self._find_key_by_name(districts, district)
        if not district_id:
            return False

        # ---- TEHSIL ----
        tehsils = TEHSILS.get(district_id, {})
        tehsil_id = self._find_key_by_name(tehsils, tehsil)
        if not tehsil_id:
            return False

        # ---- VILLAGE ----
        villages = get_villages_by_state_tehsil(state_id, tehsil_id)
        village_id = self._find_key_by_name(villages, village)
        if not village_id:
            return False

        return True
