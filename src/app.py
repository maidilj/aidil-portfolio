from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ── Real SCDF fire statistics data (2021–2025) ───────────────────────────────
RAW_DATA = [
    {"year": 2021, "total": 1844, "residential": 1010, "non_res": 415, "non_bldg": 419, "pmd": 32, "pab": 23, "pma": 8,  "vehicle": 155, "vegetation": 179, "injuries": 193, "fatalities": 4},
    {"year": 2022, "total": 1799, "residential": 935,  "non_res": 434, "non_bldg": 430, "pmd": 14, "pab": 21, "pma": 7,  "vehicle": 204, "vegetation": 106, "injuries": 171, "fatalities": 6},
    {"year": 2023, "total": 1954, "residential": 970,  "non_res": 404, "non_bldg": 580, "pmd": 18, "pab": 32, "pma": 5,  "vehicle": 215, "vegetation": 133, "injuries": 81,  "fatalities": 3},
    {"year": 2024, "total": 1990, "residential": 968,  "non_res": 415, "non_bldg": 607, "pmd": 25, "pab": 31, "pma": 11, "vehicle": 220, "vegetation": 180, "injuries": 80,  "fatalities": 5},
    {"year": 2025, "total": 2050, "residential": 1051, "non_res": 471, "non_bldg": 528, "pmd": 31, "pab": 12, "pma": 6,  "vehicle": 193, "vegetation": 109, "injuries": 94,  "fatalities": 6},
]

def get_fire_data():
    years = [d["year"] for d in RAW_DATA]

    # Chart A — total fires overview 2021–2025
    overview = {
        "years": years,
        "total":       [d["total"]       for d in RAW_DATA],
        "residential": [d["residential"] for d in RAW_DATA],
        "non_res":     [d["non_res"]     for d in RAW_DATA],
        "non_bldg":    [d["non_bldg"]    for d in RAW_DATA],
        "injuries":    [d["injuries"]    for d in RAW_DATA],
        "fatalities":  [d["fatalities"]  for d in RAW_DATA],
    }

    # Chart B — breakdown by year for pie chart
    # Non-Bldg is broken into vehicle + vegetation + other (remainder)
    breakdown_by_year = {}
    for d in RAW_DATA:
        non_bldg_other = d["non_bldg"] - d["vehicle"] - d["vegetation"]
        breakdown_by_year[d["year"]] = {
            "labels": ["Residential", "Non-Residential", "Vehicle", "Vegetation", "Other Non-Building"],
            "values": [
                d["residential"],
                d["non_res"],
                d["vehicle"],
                d["vegetation"],
                max(non_bldg_other, 0)
            ]
        }

    # Chart C — AMD fires (PAB + PMD + PMA) 2021–2025
    amd = {
        "years": years,
        "pmd": [d["pmd"] for d in RAW_DATA],
        "pab": [d["pab"] for d in RAW_DATA],
        "pma": [d["pma"] for d in RAW_DATA],
        "total_amd": [d["pmd"] + d["pab"] + d["pma"] for d in RAW_DATA],
    }

    # Summary cards — latest year (2025)
    latest = RAW_DATA[-1]
    prev   = RAW_DATA[-2]
    summary = {
        "total":          latest["total"],
        "total_change":   latest["total"] - prev["total"],
        "total_amd":      latest["pmd"] + latest["pab"] + latest["pma"],
        "amd_change":     (latest["pmd"] + latest["pab"] + latest["pma"]) - (prev["pmd"] + prev["pab"] + prev["pma"]),
        "injuries":       latest["injuries"],
        "fatalities":     latest["fatalities"],
        "latest_year":    latest["year"],
    }

    return {
        "overview": overview,
        "breakdown_by_year": breakdown_by_year,
        "amd": amd,
        "summary": summary,
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/project/fire-dashboard")
def fire_dashboard():
    data = get_fire_data()
    return render_template("fire_dashboard.html", summary=data["summary"])

@app.route("/project/thermal-simulation")
def thermal_simulation():
    return render_template("thermal_simulation.html")

@app.route("/api/fire-data")
def fire_data():
    return jsonify(get_fire_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)