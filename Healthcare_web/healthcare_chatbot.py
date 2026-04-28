#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ===================== LOAD DATA =====================
training = pd.read_csv("Training.csv")

# Clean column names
training.columns = training.columns.str.strip().str.lower().str.replace(" ", "_")

# Separate features and labels
X = training.drop("prognosis", axis=1)
y = training["prognosis"]

# Encode disease labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
model = RandomForestClassifier()
model.fit(X, y_encoded)

symptom_list = X.columns.tolist()

# ===================== FUNCTION =====================
from difflib import get_close_matches

def predict_disease(user_input):
    user_input = user_input.lower().replace(" ", "_").split(",")
    user_input = [sym.strip() for sym in user_input]

    if len(user_input) < 3:
        return " Please enter at least 3 symptoms separated by commas.\nExample: fever, headache, fatigue"

    input_vector = np.zeros(len(symptom_list))
    matched_symptoms = []
    suggestions = []

    for symptom in user_input:
        if symptom in symptom_list:
            index = symptom_list.index(symptom)
            input_vector[index] = 1
            matched_symptoms.append(symptom)
        else:
            # Find closest match
            close_match = get_close_matches(symptom, symptom_list, n=1, cutoff=0.6)
            if close_match:
                index = symptom_list.index(close_match[0])
                input_vector[index] = 1
                matched_symptoms.append(close_match[0])
                suggestions.append(f"{symptom} → {close_match[0]}")

    if len(matched_symptoms) == 0:
        return " No valid symptoms found. Try using terms like:\n" + ", ".join(symptom_list[:10])

    input_vector = pd.DataFrame([input_vector], columns=symptom_list)

    probs = model.predict_proba(input_vector)[0]
    top_indices = probs.argsort()[-3:][::-1]

    result = " Analysis Result:\n\n"

    if suggestions:
        result += " Auto-corrected symptoms:\n"
        result += "\n".join(suggestions) + "\n\n"

    for i in top_indices:
        disease = le.inverse_transform([i])[0]
        confidence = probs[i] * 100

        if confidence > 50:
            result += f"✅ Likely: {disease} ({confidence:.2f}%)\n"
        elif confidence > 30:
            result += f" Possible: {disease} ({confidence:.2f}%)\n"

    if "Likely" not in result and "Possible" not in result:
        return " Prediction not reliable. Please consult a doctor."

    result += "\n Advice:\n- Stay hydrated\n- Get proper rest\n- Consult a doctor if symptoms persist"

    return result


# ===================== UI =====================
def send_message():
    user_text = entry.get()
    chat_box.insert(tk.END, "You: " + user_text + "\n")

    response = predict_disease(user_text)
    chat_box.insert(tk.END, "Bot: " + response + "\n\n")

    entry.delete(0, tk.END)


root = tk.Tk()
root.title("Healthcare Assistant Chatbot")
root.geometry("600x500")
root.configure(bg="#1e1e1e")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 11))
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_message, bg="green", fg="white")
send_button.pack(pady=5)

# Disclaimer
chat_box.insert(tk.END,
" DISCLAIMER:\nThis chatbot is for educational purposes only.\nIt does NOT provide medical diagnosis.\n\n")

root.mainloop()


# In[ ]:


get_ipython().system('jupyter nbconvert --to script "healthcare_chatbot.ipynb"')


# In[ ]:




