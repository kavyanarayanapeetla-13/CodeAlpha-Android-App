
import tkinter as tk
from tkinter import ttk, messagebox
import random

# Vocabulary database
LESSONS = {
    "Spanish": [
        {"word": "Hola", "meaning": "Hello"},
        {"word": "Gracias", "meaning": "Thank you"},
        {"word": "Agua", "meaning": "Water"},
        {"word": "Amigo", "meaning": "Friend"},
        {"word": "Casa", "meaning": "House"},
        {"word": "Perro", "meaning": "Dog"},
        {"word": "Libro", "meaning": "Book"},
    ],
    "French": [
        {"word": "Bonjour", "meaning": "Hello"},
        {"word": "Merci", "meaning": "Thank you"},
        {"word": "Eau", "meaning": "Water"},
        {"word": "Ami", "meaning": "Friend"},
        {"word": "Maison", "meaning": "House"},
        {"word": "Chien", "meaning": "Dog"},
        {"word": "Livre", "meaning": "Book"},
    ],
    "Hindi": [
        {"word": "Namaste", "meaning": "Hello"},
        {"word": "Dhanyavaad", "meaning": "Thank you"},
        {"word": "Paani", "meaning": "Water"},
        {"word": "Dost", "meaning": "Friend"},
        {"word": "Ghar", "meaning": "House"},
        {"word": "Kutta", "meaning": "Dog"},
        {"word": "Kitaab", "meaning": "Book"},
    ],
}

class LanguageLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LinguaLearn - Language Practice")
        self.root.geometry("600x500")
        self.root.configure(bg="#f2f5ff")

        self.language = tk.StringVar(value="Spanish")
        self.score = 0
        self.total = 0
        self.current = None
        self.questions = []

        title = tk.Label(
            root, text="🌍 LinguaLearn",
            font=("Arial", 25, "bold"),
            bg="#f2f5ff", fg="#304ffe"
        )
        title.pack(pady=15)

        tk.Label(
            root, text="Choose a language to learn",
            font=("Arial", 12), bg="#f2f5ff"
        ).pack()

        self.language_box = ttk.Combobox(
            root, textvariable=self.language,
            values=list(LESSONS.keys()),
            state="readonly", font=("Arial", 12)
        )
        self.language_box.pack(pady=8)
        self.language_box.bind(
            "<<ComboboxSelected>>", self.reset
        )

        self.word_label = tk.Label(
            root, text="Welcome! Start a vocabulary quiz.",
            font=("Arial", 19, "bold"),
            bg="#f2f5ff", wraplength=500
        )
        self.word_label.pack(pady=25)

        self.options_frame = tk.Frame(root, bg="#f2f5ff")
        self.options_frame.pack(pady=5)

        self.feedback = tk.Label(
            root, text="", font=("Arial", 12),
            bg="#f2f5ff", wraplength=500
        )
        self.feedback.pack(pady=12)

        self.score_label = tk.Label(
            root, text="Score: 0 / 0",
            font=("Arial", 12, "bold"), bg="#f2f5ff"
        )
        self.score_label.pack(pady=5)

        self.next_button = tk.Button(
            root, text="Start Learning",
            command=self.next_question,
            bg="#304ffe", fg="white",
            font=("Arial", 12, "bold"),
            padx=20, pady=10
        )
        self.next_button.pack(pady=15)

        self.lesson_button = tk.Button(
            root, text="View Vocabulary",
            command=self.show_vocabulary,
            font=("Arial", 11)
        )
        self.lesson_button.pack()

    def reset(self, event=None):
        self.score = 0
        self.total = 0
        self.feedback.config(text="")
        self.score_label.config(text="Score: 0 / 0")
        self.next_button.config(text="Start Learning")
        self.next_question()

    def next_question(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.feedback.config(text="")
        vocabulary = LESSONS[self.language.get()]
        self.current = random.choice(vocabulary)

        self.word_label.config(
            text=f"What does '{self.current['word']}' mean?"
        )

        wrong_answers = [
            item["meaning"] for item in vocabulary
            if item["meaning"] != self.current["meaning"]
        ]
        choices = random.sample(wrong_answers, 3)
        choices.append(self.current["meaning"])
        random.shuffle(choices)

        for choice in choices:
            tk.Button(
                self.options_frame,
                text=choice,
                width=25,
                font=("Arial", 12),
                command=lambda answer=choice: self.check_answer(answer),
                bg="white", pady=5
            ).pack(pady=4)

        self.next_button.config(text="Next Question")

    def check_answer(self, answer):
        if self.current is None:
            return

        correct = self.current["meaning"]
        self.total += 1

        if answer == correct:
            self.score += 1
            self.feedback.config(
                text="Correct! Great job!",
                fg="green"
            )
        else:
            self.feedback.config(
                text=f"Not quite. The answer is: {correct}",
                fg="red"
            )

        self.score_label.config(
            text=f"Score: {self.score} / {self.total}"
        )

        # Prevent scoring the same question more than once.
        for widget in self.options_frame.winfo_children():
            widget.config(state="disabled")

        self.current = None

    def show_vocabulary(self):
        language = self.language.get()
        words = LESSONS[language]

        window = tk.Toplevel(self.root)
        window.title(f"{language} Vocabulary")
        window.geometry("350x350")

        tk.Label(
            window, text=f"{language} Word List",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        for item in words:
            tk.Label(
                window,
                text=f"{item['word']}  —  {item['meaning']}",
                font=("Arial", 12)
            ).pack(anchor="w", padx=20, pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageLearningApp(root)
    root.mainloop()
