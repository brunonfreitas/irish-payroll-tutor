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

def extract_quizzes(chapters):
    quizzes = []

    for chapter in chapters:
        lines = chapter.splitlines()

        current_quiz = None

        for line in lines:
            line = line.strip()

            if line.startswith("Q:"):
                if current_quiz:
                    quizzes.append(current_quiz)

                current_quiz = {
                    "question": line.replace("Q:", "").strip(),
                    "options": [],
                    "correct": ""
                }

            elif current_quiz and line.startswith("A:"):
                current_quiz["options"].append({
                    "letter": "A",
                    "text": line.replace("A:", "").strip()
                })

            elif current_quiz and line.startswith("B:"):
                current_quiz["options"].append({
                    "letter": "B",
                    "text": line.replace("B:", "").strip()
                })

            elif current_quiz and line.startswith("C:"):
                current_quiz["options"].append({
                    "letter": "C",
                    "text": line.replace("C:", "").strip()
                })

            elif current_quiz and line.startswith("D:"):
                current_quiz["options"].append({
                    "letter": "D",
                    "text": line.replace("D:", "").strip()
                })

            elif current_quiz and line.startswith("Correct:"):
                current_quiz["correct"] = line.replace("Correct:", "").strip().upper()

        if current_quiz:
            quizzes.append(current_quiz)

    clean_quizzes = []

    for quiz in quizzes:
        if quiz["question"] and len(quiz["options"]) == 4 and quiz["correct"] in ["A", "B", "C", "D"]:
            clean_quizzes.append(quiz)

    return clean_quizzes

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
    quizzes = extract_quizzes(chapters)

    return render_template(
        "index.html",
        chapters=chapters,
        progress=progress,
        quizzes=quizzes
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)