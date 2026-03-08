from flask import Flask, render_template, jsonify
import json
import random

app = Flask(__name__)

# ── Fire incident data (synthetic, London-style open data) ──────────────────
def generate_fire_data():
    incident_types = [
        "Dwelling Fire", "Vehicle Fire", "Vegetation Fire",
        "Industrial Fire", "Electrical Fire", "Explosion",
        "False Alarm", "Rescue"
    ]
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]

    random.seed(42)

    # Incidents by type
    by_type = {t: random.randint(40, 320) for t in incident_types}

    # Monthly trend (last 12 months)
    monthly = {m: random.randint(60, 180) for m in months}

    # Incidents by hour of day
    hourly = {}
    for h in range(24):
        # Peak hours: late night and early morning
        if 0 <= h <= 4 or 22 <= h <= 23:
            hourly[f"{h:02d}:00"] = random.randint(30, 80)
        elif 9 <= h <= 17:
            hourly[f"{h:02d}:00"] = random.randint(20, 50)
        else:
            hourly[f"{h:02d}:00"] = random.randint(10, 40)

    # Response time distribution (minutes)
    response_bins = ["<5 min","5–8 min","8–12 min","12–20 min",">20 min"]
    response_counts = [45, 120, 98, 52, 15]

    return {
        "by_type": by_type,
        "monthly": monthly,
        "hourly": hourly,
        "response": {"bins": response_bins, "counts": response_counts},
        "summary": {
            "total_incidents": sum(by_type.values()),
            "electrical_fires": by_type["Electrical Fire"],
            "explosions": by_type["Explosion"],
            "avg_response_min": 8.4
        }
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/project/fire-dashboard")
def fire_dashboard():
    data = generate_fire_data()
    return render_template("fire_dashboard.html", summary=data["summary"])

@app.route("/project/thermal-simulation")
def thermal_simulation():
    return render_template("thermal_simulation.html")

@app.route("/api/fire-data")
def fire_data():
    return jsonify(generate_fire_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
