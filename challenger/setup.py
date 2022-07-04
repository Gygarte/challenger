import json
import os
from pathlib import Path
data = {"DOC":"Rezultate teste stationaritate.xlsx", "DATABASE": "input.xlsx", "OUTPUT": "output.xlsx"}
with open(os.path.join(Path(__file__).resolve(True).parent, "basic_setup.json"), "w") as file:
    json.dump(data, file, indent=4)

