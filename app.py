from flask import Flask, render_template
import os

app = Flask(__name__)

STUDY_FOLDER = "study_notes"

PAYROLL_AREAS = [
    "PAYE",
    "PRSI",
    "USC",
    "Revenue",
    "Payroll Processing",
    "Deadlines",
    "Reporting",
    "Tax Credits",
    "BIK",
    "Pension",
    "Emergency Tax",
    "Gross to Net"
]

def load_chapters():
    chapters = []

    if not os.path.exists(STUDY_FOLDER):
        return chapters

    for file in os.listdir(STUDY_FOLDER):
        if file.endswith(".md"):
            path = os.path.join(STUDY_FOLDER, file)

            with open(path, "r", encoding="utf-8") as f:
                chapters.append(f.read())

    return chapters

def calculate_progress(chapters):
    progress = {}

    for area in PAYROLL_AREAS:
        count = 0

        for chapter in chapters:
            if area.lower() in chapter.lower():
                count += 1

        percentage = min(count * 25, 100)

        if percentage < 40:
            level = "weak"
        elif percentage < 65:
            level = "medium"
        elif percentage < 85:
            level = "good"
        else:
            level = "excellent"

        progress[area] = {
            "percentage": percentage,
            "level": level
        }

    return progress

@app.route("/")
def home():
    chapters = load_chapters()
    progress = calculate_progress(chapters)

    return render_template(
        "index.html",
        chapters=chapters,
        progress=progress
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)