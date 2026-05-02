from flask import Flask, render_template
import os
import random

app = Flask(__name__)

STUDY_FOLDER = "study_notes"

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

def extract_morning_tips(chapters):
    tips = []

    for chapter in chapters:
        lines = chapter.splitlines()
        inside_section = False

        for line in lines:
            line = line.strip()

            if line.startswith("## Morning Tips"):
                inside_section = True
                continue

            if inside_section and line.startswith("## "):
                inside_section = False

            if inside_section and line.startswith("-"):
                tip = line.replace("-", "", 1).strip()
                if tip:
                    tips.append(tip)

    return tips

@app.route("/")
def home():
    chapters = load_chapters()
    morning_tips = extract_morning_tips(chapters)

    morning_tip = random.choice(morning_tips) if morning_tips else None

    return render_template(
        "index.html",
        morning_tip=morning_tip
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)