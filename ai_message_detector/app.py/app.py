import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample data for training the model
messages = [
    ('Hello, I hope you are well.', 'real'),
    ('Congratulations! You have won a prize. Click here to claim your money.', 'fraud'),
    ('Please make sure to update your account information.', 'fraud'),
    ('Your account has been successfully updated.', 'real'),
]

# Prepare the dataset
texts, labels = zip(*messages)
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(texts, labels)

def classify_message(message):
    prediction = model.predict([message])[0]
    return prediction

def analyze_message():
    message = message_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Warning", "Please enter a message.")
        return

    if "http://" in message or "https://" in message:
        links = re.findall(r'(https?://\S+)', message)
        links_list.delete(1.0, tk.END)
        for link in links:
            links_list.insert(tk.END, link + "\n")
        links_list.bind("<Button-1>", lambda e: links_list.event_generate("<Control-c>"))
    else:
        links_list.delete(1.0, tk.END)

    result = classify_message(message)
    if result == 'real':
        background_label.config(image=real_img)
    elif result == 'fraud':
        background_label.config(image=fraud_img)
    else:
        background_label.config(image=default_img)

# Set up the main application window
root = tk.Tk()
root.title("Message Analyzer")

# Load images
real_img = PhotoImage(file="real.png")
fraud_img = PhotoImage(file="fraud.png")
default_img = PhotoImage(file="default.png")

# Create a background label
background_label = tk.Label(root)
background_label.pack(fill='both', expand=True)

# Overlay the other widgets on top of the background
message_label = tk.Label(root, text="Enter your message:", bg="white")
message_label.pack(pady=10)

message_entry = tk.Text(root, height=10, width=50)
message_entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze", command=analyze_message)
analyze_button.pack(pady=10)

links_label = tk.Label(root, text="Links found in the message:", bg="white")
links_label.pack(pady=10)

links_list = tk.Text(root, height=10, width=50)
links_list.pack(pady=10)

# Start with the default image
background_label.config(image=default_img)

# Start the Tkinter event loop
root.mainloop()