from flask import Flask, render_template
import json
import random

app = Flask(__name__)

@app.route("/")
def home():
    with open("questions.json") as file:
        questions = json.load(file)

    random.shuffle(questions)
    return render_template("index.html", questions=questions[:5])

if __name__ == "__main__":
    app.run(debug=True)