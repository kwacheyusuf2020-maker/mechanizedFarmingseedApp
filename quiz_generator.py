import json
import random
from datetime import datetime
from pathlib import Path


class QuizGenerator:
    """Loads farming questions, creates quizzes, scores answers, and saves progress."""

    def __init__(self, question_file="questions.json", score_file="quiz_scores.json"):
        self.folder = Path(__file__).resolve().parent
        self.question_file = self.folder / question_file
        self.score_file = self.folder / score_file
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with self.question_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise FileNotFoundError(f"Question bank not found: {self.question_file}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in question bank: {error}") from error

        if not isinstance(data, list) or not data:
            raise ValueError("Question bank must be a non-empty JSON list.")

        seen_ids = set()
        required = {"id", "category", "difficulty", "question", "options",
                    "answer", "explanation", "points", "tags"}

        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"Question {index} must be a JSON object.")
            missing = required - item.keys()
            if missing:
                raise ValueError(f"Question {index} is missing: {', '.join(sorted(missing))}")
            if item["id"] in seen_ids:
                raise ValueError(f"Duplicate question ID: {item['id']}")
            seen_ids.add(item["id"])
            if not isinstance(item["options"], list) or len(item["options"]) < 2:
                raise ValueError(f"Question {item['id']} needs at least two options.")
            if len(set(item["options"])) != len(item["options"]):
                raise ValueError(f"Question {item['id']} has duplicate options.")
            if item["answer"] not in item["options"]:
             raise ValueError(f"Correct answer for {item['id']} is not among its options.")
            if item["difficulty"] not in {"Easy", "Medium", "Hard"}:
              raise ValueError(f"Question {item['id']} has an unsupported difficulty.")
            if not isinstance(item["points"], int) or item["points"] < 1:
                raise ValueError(f"Question {item['id']} must have positive integer points.")
            if not isinstance(item["tags"], list):
                raise ValueError(f"Tags for {item['id']} must be a list.")
        return data

    def categories(self):
        return sorted({q["category"] for q in self.questions})

    def generate_quiz(self, number=10, category="All", difficulty="All"):
        if number < 1:
            raise ValueError("Number of questions must be at least 1.")
        available = [
            q for q in self.questions
            if (category == "All" or q["category"] == category)
            and (difficulty == "All" or q["difficulty"] == difficulty)
        ]
        if not available:
            raise ValueError("No questions match the selected category and difficulty.")
        return random.sample(available, min(number, len(available)))

    @staticmethod
    def calculate_score(quiz, user_answers):
        correct = 0
        points_earned = 0
        points_possible = sum(q["points"] for q in quiz)
        details = []
        for question, selected in zip(quiz, user_answers):
            is_correct = selected == question["answer"]
            if is_correct:
                correct += 1
                points_earned += question["points"]
            details.append({
                "question_id": question["id"],
                "selected": selected,
                "correct_answer": question["answer"],
                "is_correct": is_correct,
                "points_earned": question["points"] if is_correct else 0,
                "points_possible": question["points"]
            })
        percentage = round((points_earned / points_possible) * 100, 2) if points_possible else 0
        return {
            "correct_count": correct,
            "question_count": len(quiz),
            "points_earned": points_earned,
            "points_possible": points_possible,
            "percentage": percentage,
            "details": details
        }

    def save_score(self, learner, category, difficulty, result):
        records = self.get_score_history()
        record = {
            "learner": learner.strip(),
            "category": category,
            "difficulty": difficulty,
            "correct_count": result["correct_count"],
            "question_count": result["question_count"],
            "points_earned": result["points_earned"],
            "points_possible": result["points_possible"],
            "percentage": result["percentage"],
            "completed_at": datetime.now().astimezone().isoformat(timespec="seconds")
        }
        records.append(record)
        with self.score_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)
        return record

    def get_score_history(self):
        if not self.score_file.exists():
            return []
        try:
            with self.score_file.open("r", encoding="utf-8") as file:
                records = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Score history JSON is damaged: {error}") from error
        if not isinstance(records, list):
            raise ValueError("Score history must contain a JSON list.")
        return records
