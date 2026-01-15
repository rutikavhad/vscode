from in_state.engine import LocationEngine

engine = LocationEngine()

print("States:", engine.get_states())
engine.select_state("Maharashtra")

print("Districts:", engine.get_districts())
engine.select_district("Pune")

print("Tehsils:", engine.get_tehsils())
engine.select_tehsil("Mulshi")

print("Villages:", engine.get_villages())
engine.select_village("Adgaon")

print("\n✅ FINAL SELECTION COMPLETED")



engine = LocationEngine()

print(engine.validate(
    "Maharashtra", "Pune", "Mulshi", "Adgaon"
))  # True

print(engine.validate(
    "Maharashtra", "Pune", "Mulshi", "WrongVillage"
))  # False


from in_state.engine import LocationEngine

engine = LocationEngine()

engine.select_state("Maharashtra")
engine.select_district("Pune")
engine.select_tehsil("Mulshi")

print(engine.get_villages())
print(engine.validate("Maharashtra", "Pune", "Mulshi", "Adgaon"))
print(engine.validate("Maharashtra", "Pune", "Mulshi", "WrongVillage"))
