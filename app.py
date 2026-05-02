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

            if any(line.startswith(section) for section in section_names):
                inside = True
                continue

            if inside and line.startswith("## "):
                inside = False

            if inside and line.startswith("-"):
                item = line.replace("-", "", 1).strip()
                if item:
                    items.append(item)

    return items


def extract_quizzes(chapters):
    quizzes = []

    for chapter in chapters:
        lines = chapter.splitlines()
        inside_quiz = False
        current = None

        for line in lines:
            line = line.strip()

            if line.startswith("## App Quiz Questions") or line.startswith("## Quiz Questions"):
                inside_quiz = True
                continue

            if inside_quiz and line.startswith("## "):
                inside_quiz = False

            if not inside_quiz:
                continue

            if line.startswith("Q:"):
                if current:
                    quizzes.append(current)

                current = {
                    "question": line.replace("Q:", "", 1).strip(),
                    "options": [],
                    "correct": ""
                }

            elif current and line.startswith("A:"):
                current["options"].append({"letter": "A", "text": line.replace("A:", "", 1).strip()})

            elif current and line.startswith("B:"):
                current["options"].append({"letter": "B", "text": line.replace("B:", "", 1).strip()})

            elif current and line.startswith("C:"):
                current["options"].append({"letter": "C", "text": line.replace("C:", "", 1).strip()})

            elif current and line.startswith("D:"):
                current["options"].append({"letter": "D", "text": line.replace("D:", "", 1).strip()})

            elif current and line.startswith("Correct:"):
                current["correct"] = line.replace("Correct:", "", 1).strip().upper()

        if current:
            quizzes.append(current)

    valid_quizzes = []

    for quiz in quizzes:
        if quiz["question"] and len(quiz["options"]) == 4 and quiz["correct"] in ["A", "B", "C", "D"]:
            valid_quizzes.append(quiz)

    return valid_quizzes


@app.route("/")
def home():
    chapters = load_chapters()

    morning_tips = extract_section_items(chapters, ["## Morning Tips"])
    evening_reviews = extract_section_items(chapters, ["## Evening Reviews"])
    quizzes = extract_quizzes(chapters)

    morning_tip = random.choice(morning_tips) if morning_tips else None
    evening_review = random.choice(evening_reviews) if evening_reviews else None

    return render_template(
        "index.html",
        morning_tip=morning_tip,
        evening_review=evening_review,
        quizzes=quizzes
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)