def extract_quizzes(chapters):
    quizzes = []

    for chapter in chapters:
        lines = chapter.splitlines()
        current = None
        inside_quiz = False

        for line in lines:
            line = line.strip()

            # Detect ANY quiz section (mais flexível)
            if "quiz questions" in line.lower():
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
                    "question": line[2:].strip(),
                    "options": [],
                    "correct": ""
                }

            elif current and line.startswith(("A:", "B:", "C:", "D:")):
                letter = line[0]
                text = line[2:].strip()
                current["options"].append({
                    "letter": letter,
                    "text": text
                })

            elif current and line.startswith("Correct:"):
                current["correct"] = line.split(":")[1].strip().upper()

        if current:
            quizzes.append(current)

    # só quizzes válidos
    return [
        q for q in quizzes
        if len(q["options"]) == 4 and q["correct"] in ["A", "B", "C", "D"]
    ]