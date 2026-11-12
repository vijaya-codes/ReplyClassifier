
import re
import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime


def contains_term(text, term):
    pattern = r"\b" + re.escape(term) + r"\b"
    return re.search(pattern, text) is not None


def classify_reply(message):
    if not message or not message.strip():
        return {
            "category": "Neutral",
            "priority": "NORMAL",
            "follow_up_required": False
        }

    text = message.lower().strip()


    urgent_words = [
        "urgent", "asap", "immediately", "deadline", "emergency"
    ]

    positive_words = [
    "thank you", "thanks", "great", "excellent",
    "happy", "agree", "approved", "yes", "appreciate",
    "like", "love", "enjoy", "satisfied", "pleased"
]


    negative_words = [
        "unhappy", "disappointed", "complaint", "problem",
        "issue", "not satisfied", "reject", "angry", "poor",
        "not happy", "not pleased", "not good", "not impressed",
        "not interested", "never again", "bad experience",
        "waste of time", "terrible", "awful"
    ]
    

    follow_up_words = [
        "please confirm",
        "get back to me",
        "follow up",
        "waiting",
        "remind",
        "update me",
        "let me know",
        "call me back",
        "contact me",
        "reply soon",
        "keep me updated",
        "send me an update"
    
    ]

  
    negated_positive_phrases = [
        "not happy",
        "not pleased",
        "not good",
        "not impressed",
        "don't like",
        "do not like"
    
    ]

    urgent = any(contains_term(text, w) for w in urgent_words)
    negative = any(contains_term(text, w) for w in negative_words)

    positive = (
        any(contains_term(text, w) for w in positive_words)
        and not any(
            contains_term(text, phrase)
            for phrase in negated_positive_phrases
        )
    )

    follow_up = any(contains_term(text, w) for w in follow_up_words)

    if positive and negative:
        category = "Mixed"
    elif negative:
        category = "Negative"
    elif positive:
        category = "Positive"
    else:
        category = "Neutral"

    if urgent:
        priority = "URGENT"
    elif negative or follow_up:
        priority = "HIGH"
    else:
        priority = "NORMAL"

    return {
        "category": category,
        "priority": priority,
        "follow_up_required": follow_up
    }


CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "classified_replies.csv"
)


def save_to_csv(message, result):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date and Time",
                "Message",
                "Category",
                "Priority",
                "Follow-up Required"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message,
            result["category"],
            result["priority"],
            result["follow_up_required"]
        ])


def classify_button():
    message = input_box.get("1.0", tk.END).strip()

    if not message:
        messagebox.showwarning(
            "No message",
            "Please enter a reply first."
        )
        return

    result = classify_reply(message)

    try:
        save_to_csv(message, result)
    except OSError as error:
        messagebox.showerror(
            "Save error",
            f"Could not save the result:\n{error}"
        )
        return

    category_label.config(
        text=result["category"],
        fg={
            "Positive": "#16803c",
            "Negative": "#dc2626",
            "Mixed": "#b7791f",
            "Neutral": "#475569"
        }[result["category"]]
    )

    priority_label.config(text=result["priority"])

    follow_up_label.config(
        text="Yes" if result["follow_up_required"] else "No"
    )

    save_label.config(
        text="Saved to classified_replies.csv",
        fg="#16803c"
    )


def clear_button():
    input_box.delete("1.0", tk.END)
    category_label.config(text="—", fg="#475569")
    priority_label.config(text="—")
    follow_up_label.config(text="—")
    save_label.config(text="")


window = tk.Tk()
window.title("Reply Classifier")
window.geometry("650x570")
window.configure(bg="#f1f5f9")
window.resizable(False, False)

header = tk.Frame(window, bg="#172554", height=90)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="REPLY CLASSIFIER",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#172554"
).pack(pady=(18, 2))

tk.Label(
    header,
    text="Analyse and prioritise incoming replies",
    font=("Arial", 10),
    fg="#cbd5e1",
    bg="#172554"
).pack()

main_frame = tk.Frame(window, bg="#f1f5f9", padx=25, pady=20)
main_frame.pack(fill="both", expand=True)

tk.Label(
    main_frame,
    text="Enter a reply",
    font=("Arial", 12, "bold"),
    bg="#f1f5f9",
    fg="#172554"
).pack(anchor="w")

input_box = tk.Text(
    main_frame,
    height=5,
    font=("Arial", 11),
    wrap="word",
    relief="solid",
    bd=1
)
input_box.pack(fill="x", pady=(8, 15))

button_frame = tk.Frame(main_frame, bg="#f1f5f9")
button_frame.pack(fill="x", pady=(0, 18))

tk.Button(
    button_frame,
    text="CLASSIFY REPLY",
    command=classify_button,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
).pack(side="left")

tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_button,
    bg="#e2e8f0",
    fg="#334155",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
).pack(side="left", padx=10)

result_frame = tk.Frame(
    main_frame,
    bg="white",
    padx=20,
    pady=18,
    relief="solid",
    bd=1
)
result_frame.pack(fill="x")

tk.Label(
    result_frame,
    text="CLASSIFICATION RESULTS",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#172554"
).pack(anchor="w", pady=(0, 12))

def result_row(label_text):
    row = tk.Frame(result_frame, bg="white")
    row.pack(fill="x", pady=5)

    tk.Label(
        row,
        text=label_text,
        font=("Arial", 10),
        bg="white",
        fg="#64748b",
        width=20,
        anchor="w"
    ).pack(side="left")

    value = tk.Label(
        row,
        text="—",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#475569"
    )
    value.pack(side="left")

    return value


category_label = result_row("Category")
priority_label = result_row("Priority")
follow_up_label = result_row("Follow-up required")

save_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 9),
    bg="#f1f5f9"
)
save_label.pack(anchor="w", pady=(10, 0))

tk.Label(
    window,
    text="Reply Classifier | Version 2.1",
    font=("Arial", 9),
    fg="#64748b",
    bg="#f1f5f9"
).pack(pady=10)

window.mainloop()
