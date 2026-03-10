import json
import random
import time
from database import create_table, insert_score, get_top_scores


class Question:
    def __init__(self, question, options, answer, difficulty):
        self.question = question
        self.options = options
        self.answer = answer
        self.difficulty = difficulty

    def display(self):
        print("\n" + self.question)
        for option in self.options:
            print(option)


class Quiz:
    def __init__(self, difficulty):
        self.questions = []
        self.score = 0
        self.difficulty = difficulty

    def load_questions(self):
        with open("questions.json", "r") as file:
            data = json.load(file)

        filtered = [q for q in data if q["difficulty"] == self.difficulty]

        if not filtered:
            print("No questions found for this difficulty.")
            return False

        random.shuffle(filtered)

        for q in filtered:
            self.questions.append(
                Question(q["question"], q["options"], q["answer"], q["difficulty"])
            )

        return True

    def start(self):
        print("\n🎯 Quiz Started!")
        print("You have 10 seconds per question.")

        for question in self.questions:
            question.display()

            start_time = time.time()
            answer = input("Your answer (A/B/C/D): ").upper()
            end_time = time.time()

            if end_time - start_time > 10:
                print("⏰ Time's up!")
                continue

            if answer == question.answer:
                print("✅ Correct!")
                self.score += 1
            else:
                print(f"❌ Wrong! Correct answer: {question.answer}")

        self.show_result()

    def show_result(self):
        total = len(self.questions)
        percentage = (self.score / total) * 100

        if percentage >= 90:
            grade = "A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "D"

        print("\n🏁 Quiz Finished!")
        print(f"Score: {self.score}/{total}")
        print(f"Percentage: {percentage:.2f}%")
        print(f"Grade: {grade}")

        name = input("Enter your name: ")
        insert_score(name, self.difficulty, self.score, percentage)
        print("💾 Score saved to database!")


def show_leaderboard():
    scores = get_top_scores()

    print("\n🏆 Leaderboard (Top 5)")
    print("---------------------------------")

    if not scores:
        print("No scores yet.")
        return

    for i, (name, difficulty, score, percentage) in enumerate(scores, 1):
        print(f"{i}. {name} | {difficulty} | {score} | {percentage:.2f}%")


def main():
    create_table()

    while True:
        print("\n===== QUIZ APPLICATION =====")
        print("1. Start Quiz")
        print("2. View Leaderboard")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            difficulty = input("Choose difficulty (easy/medium/hard): ").lower()

            quiz = Quiz(difficulty)
            if quiz.load_questions():
                quiz.start()

        elif choice == "2":
            show_leaderboard()

        elif choice == "3":
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()