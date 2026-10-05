from quiz_generator import QuizGenerator


def ask_choice(prompt, choices):
    """Show choices and return a valid selection."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            number = int(answer)
            if 1 <= number <= len(choices):
                return choices[number - 1]
        print(f"Please enter a number from 1 to {len(choices)}.")


def main():
    try:
        quiz_app = QuizGenerator()
        print("\n==============================================")
        print("  MECHANIZED FARMING & SEED PRODUCTION QUIZ")
        print("==============================================")
        learner = input("Enter your name: ").strip()
        while not learner:
            learner = input("Name cannot be empty. Enter your name: ").strip()

        categories = ["All"] + quiz_app.categories()
        print("\nChoose a topic:")
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")
        category = ask_choice("Topic number: ", categories)

        difficulties = ["All", "Easy", "Medium", "Hard"]
        print("\nChoose difficulty:")
        for i, level in enumerate(difficulties, start=1):
            print(f"{i}. {level}")
        difficulty = ask_choice("Difficulty number: ", difficulties)

        while True:
            raw = input(f"\nHow many questions? (1-{len(quiz_app.questions)}): ").strip()
            try:
                number = int(raw)
                if number > 0:
                    break
            except ValueError:
                pass
            print("Enter a whole number greater than zero.")

        quiz = quiz_app.generate_quiz(number, category, difficulty)
        answers = []
        print(f"\nStarting quiz: {len(quiz)} questions. Read each question carefully.")
        for index, question in enumerate(quiz, start=1):
            print(f"\nQ{index}. [{question['category']} | {question['difficulty']} | {question['points']} point(s)]")
            print(question["question"])
            options = question["options"][:]
            # Shuffle displayed choices without changing the correct answer text.
            import random
            random.shuffle(options)
            for option_index, option in enumerate(options, start=1):
                print(f"  {option_index}. {option}")
            selected = ask_choice("Your answer number: ", options)
            answers.append(selected)

        result = quiz_app.calculate_score(quiz, answers)
        print("\n---------------- QUIZ RESULT ----------------")
        print(f"Learner: {learner}")
        print(f"Correct answers: {result['correct_count']} / {result['question_count']}")
        print(f"Points: {result['points_earned']} / {result['points_possible']}")
        print(f"Percentage: {result['percentage']}%")
        print("\nReview:")
        for index, (question, detail) in enumerate(zip(quiz, result["details"]), start=1):
            status = "Correct" if detail["is_correct"] else "Incorrect"
            print(f"\n{index}. {status}")
            print(f"Correct answer: {question['answer']}")
            print(f"Explanation: {question['explanation']}")

        quiz_app.save_score(learner, category, difficulty, result)
        print("\nYour result has been saved in quiz_scores.json.")
        print("\nRecent score history:")
        for record in quiz_app.get_score_history()[-5:]:
            print(f"- {record['learner']}: {record['percentage']}% "
                  f"({record['correct_count']}/{record['question_count']})")
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"\nUnable to run quiz: {error}")


if __name__ == "__main__":
    main()
from quiz_generator import QuizGenerator


def ask_choice(prompt, choices):
    """Show choices and return a valid selection."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            number = int(answer)
            if 1 <= number <= len(choices):
                return choices[number - 1]
        print(f"Please enter a number from 1 to {len(choices)}.")


def main():
    try:
        quiz_app = QuizGenerator()
        print("\n==============================================")
        print("  MECHANIZED FARMING & SEED PRODUCTION QUIZ")
        print("==============================================")
        learner = input("Enter your name: ").strip()
        while not learner:
            learner = input("Name cannot be empty. Enter your name: ").strip()

        categories = ["All"] + quiz_app.categories()
        print("\nChoose a topic:")
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")
        category = ask_choice("Topic number: ", categories)

        difficulties = ["All", "Easy", "Medium", "Hard"]
        print("\nChoose difficulty:")
        for i, level in enumerate(difficulties, start=1):
            print(f"{i}. {level}")
        difficulty = ask_choice("Difficulty number: ", difficulties)

        while True:
            raw = input(f"\nHow many questions? (1-{len(quiz_app.questions)}): ").strip()
            try:
                number = int(raw)
                if number > 0:
                    break
            except ValueError:
                pass
            print("Enter a whole number greater than zero.")

        quiz = quiz_app.generate_quiz(number, category, difficulty)
        answers = []
        print(f"\nStarting quiz: {len(quiz)} questions. Read each question carefully.")
        for index, question in enumerate(quiz, start=1):
            print(f"\nQ{index}. [{question['category']} | {question['difficulty']} | {question['points']} point(s)]")
            print(question["question"])
            options = question["options"][:]
            # Shuffle displayed choices without changing the correct answer text.
            import random
            random.shuffle(options)
            for option_index, option in enumerate(options, start=1):
                print(f"  {option_index}. {option}")
            selected = ask_choice("Your answer number: ", options)
            answers.append(selected)

        result = quiz_app.calculate_score(quiz, answers)
        print("\n---------------- QUIZ RESULT ----------------")
        print(f"Learner: {learner}")
        print(f"Correct answers: {result['correct_count']} / {result['question_count']}")
        print(f"Points: {result['points_earned']} / {result['points_possible']}")
        print(f"Percentage: {result['percentage']}%")
        print("\nReview:")
        for index, (question, detail) in enumerate(zip(quiz, result["details"]), start=1):
            status = "Correct" if detail["is_correct"] else "Incorrect"
            print(f"\n{index}. {status}")
            print(f"Correct answer: {question['answer']}")
            print(f"Explanation: {question['explanation']}")
        quiz_app.save_score(learner, category, difficulty, result)
        print("\nYour result has been saved in quiz_scores.json.")
        print("\nRecent score history:")
        for record in quiz_app.get_score_history()[-5:]:
            print(f"- {record['learner']}: {record['percentage']}% "
                  f"({record['correct_count']}/{record['question_count']})")
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"\nUnable to run quiz: {error}")


if __name__ == "__main__":
    main()
