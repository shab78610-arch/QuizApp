import tkinter as tk
from tkinter import messagebox
import json
import random

class QuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x400")

        self.score = 0
        self.q_index = 0

        with open("questions.json", "r") as file:
            self.questions = json.load(file)

        random.shuffle(self.questions)

        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()

        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(root, text="", variable=self.var, value="")
            btn.pack(anchor="w")
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        if self.q_index < len(self.questions):
            q = self.questions[self.q_index]
            self.question_label.config(text=q["question"])
            self.var.set(None)

            for i, option in enumerate(q["options"]):
                self.option_buttons[i].config(text=option, value=option[0])
        else:
            messagebox.showinfo("Result", f"Final Score: {self.score}")
            self.root.quit()

    def next_question(self):
        selected = self.var.get()
        correct = self.questions[self.q_index]["answer"]

        if selected == correct:
            self.score += 1

        self.q_index += 1
        self.load_question()

root = tk.Tk()
app = QuizGUI(root)
root.mainloop()