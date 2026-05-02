from flask import Flask, render_template
import os

app = Flask(__name__)

def load_chapters():
    folder = "study_notes"
    chapters = []

    for file in os.listdir(folder):
        if file.endswith(".md"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                chapters.append(f.read())

    return chapters

@app.route("/")
def home():
    chapters = load_chapters()
    return render_template("index.html", chapters=chapters)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)