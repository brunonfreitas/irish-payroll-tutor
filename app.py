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


def extract_section_items(chapters, section_names):
    items = []

    for chapter in chapters:
        lines = chapter.splitlines()
        inside = False

        for line in lines:
            line = line.strip()

            if any(name.lower() in line.lower() for name in section_names):
                inside = True
                continue

            if inside and line.startswith("## "):
                inside = False

            if inside and line.startswith("-"):
                items.append(line.replace("-", "", 1).strip())

    return items


def extract_quizzes(chapters):
    quizzes = []

    for chapter in chapters:
        lines = chapter.splitlines()
        inside = False
        current = None

        for line in lines:
            line = line.strip()

            if "quiz questions" in line.lower():
                inside = True
                continue

            if inside and line.startswith("## "):
                inside = False

            if not inside:
                continue

            if line.startswith("Q:"):
                if current:
                    quizzes.append(current)

                current = {
                    "question": line[2:].strip(),
                    "options": [],
                    "correct": ""
                }

            elif current and line.startswith(("A:", "B:", "C:", "D:")):
                current["options"].append({
                    "letter": line[0],
                    "text": line[2:].strip()
                })

            elif current and line.startswith("Correct:"):
                current["correct"] = line.split(":")[1].strip().upper()

        if current:
            quizzes.append(current)

    return [
        q for q in quizzes
        if len(q["options"]) == 4 and q["correct"] in ["A", "B", "C", "D"]
    ]


@app.route("/")
def home():
    chapters = load_chapters()

    morning_tips = extract_section_items(chapters, ["morning tips"])
    evening_reviews = extract_section_items(chapters, ["evening reviews"])
    quizzes = extract_quizzes(chapters)

    return render_template(
        "index.html",
        morning_tip=random.choice(morning_tips) if morning_tips else None,
        evening_review=random.choice(evening_reviews) if evening_reviews else None,
        quizzes=quizzes
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)