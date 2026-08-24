from flask import Flask, render_template, request, redirect, url_for

from storage import add_data_to_file, load_data

app = Flask(__name__)

MOODS = [
    ("angry", "Vihane"),
    ("scared", "Hirmul"),
    ("sad", "Kurb"),
    ("anxious", "Ärevil"),
    ("calm", "Rahulik"),
    ("rested", "Puhanud"),
    ("happy", "Rõõmus"),
    ("excited", "Elevil"),
]

MOOD_SCORES = {
    "angry": 1,
    "scared": 2,
    "sad": 3,
    "anxious": 4,
    "calm": 5,
    "rested": 6,
    "happy": 7,
    "excited": 8,
}

MOOD_LABELS = ["", "Vihane", "Hirmunud", "Kurb", "Närviline", "Rahulik", "Puhanud", "Rõõmus", "Elevil"]

REASONS = [
    "Mind kiusati",
    "Tüli",
    "Halb ilm",
    "Liikusin",
    "Halb uni",
    "Olen üksi",
    "Sain tehtud",
    "Sain tagasisidet",
    "Olen enesekindel",
    "Saavutus",
    "Koos sõpradega",
    "Puhkasin hästi",
    "Väsimus",
    "Öeldi halvasti",
]


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _day_averages():
    data = load_data()
    days = []
    for day, values in data.items():
        moods = [MOOD_SCORES[m] for m in values.get("mood", []) if m in MOOD_SCORES]
        tempos = [float(t) for t in values.get("tempo", []) if _is_number(t)]
        fuels = [float(f) for f in values.get("fuel", []) if _is_number(f)]

        avg_mood = sum(moods) / len(moods) if moods else 0
        # Scale 0-100 sliders down to the same 1-8 range moods use.
        avg_tempo = (sum(tempos) / len(tempos) / 100 * 8) if tempos else 0
        avg_fuel = (sum(fuels) / len(fuels) / 100 * 8) if fuels else 0

        days.append(
            {
                "day": day,
                "mood": round(avg_mood, 2),
                "tempo": round(avg_tempo, 2),
                "fuel": round(avg_fuel, 2),
            }
        )
    return days


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        add_data_to_file("mood", request.form.get("mood", ""))
        return redirect(url_for("feelings"))
    return render_template("mood.html", moods=MOODS)


@app.route("/feelings", methods=["GET", "POST"])
def feelings():
    if request.method == "POST":
        reason = request.form.get("reason") or request.form.get("custom_reason") or "Ma ei tea"
        add_data_to_file("reason", reason)
        return redirect(url_for("tempo"))
    return render_template("feelings.html", reasons=REASONS)


@app.route("/tempo", methods=["GET", "POST"])
def tempo():
    if request.method == "POST":
        add_data_to_file("tempo", request.form.get("tempo", "0"))
        return redirect(url_for("fuel"))
    return render_template("tempo.html")


@app.route("/fuel", methods=["GET", "POST"])
def fuel():
    if request.method == "POST":
        add_data_to_file("fuel", request.form.get("fuel", "0"))
        return redirect(url_for("results"))
    return render_template("fuel.html")


@app.route("/results")
def results():
    return render_template("results.html", days=_day_averages())


@app.route("/statistics/mood")
def mood_statistics():
    return render_template("mood_stats.html", days=_day_averages(), labels=MOOD_LABELS)


def _day_tempo_fuel():
    data = load_data()
    days = []
    for day, values in data.items():
        tempos = [float(t) for t in values.get("tempo", []) if _is_number(t)]
        fuels = [float(f) for f in values.get("fuel", []) if _is_number(f)]

        days.append(
            {
                "day": day,
                "tempo": round(sum(tempos) / len(tempos), 1) if tempos else 0,
                "fuel": round(sum(fuels) / len(fuels), 1) if fuels else 0,
            }
        )
    return days


@app.route("/statistics/tempo")
def tempo_statistics():
    days = _day_tempo_fuel()
    latest = days[-1] if days else None
    avg_tempo = round(sum(d["tempo"] for d in days) / len(days), 1) if days else 0
    avg_fuel = round(sum(d["fuel"] for d in days) / len(days), 1) if days else 0
    return render_template(
        "tempo_stats.html",
        days=days,
        latest=latest,
        avg_tempo=avg_tempo,
        avg_fuel=avg_fuel,
    )


if __name__ == "__main__":
    app.run(debug=True)
