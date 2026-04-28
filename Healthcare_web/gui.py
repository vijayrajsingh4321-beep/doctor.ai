#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from chatbot import extract_symptoms, predict_disease, cols, description_list, precautionDictionary

def send():
    user_input = entry.get()
    chat_box.insert(tk.END, "You: " + user_input + "\n")

    symptoms = extract_symptoms(user_input, cols)

    if not symptoms:
        chat_box.insert(tk.END, "Bot: Please describe valid symptoms.\n\n")
    else:
        chat_box.insert(tk.END, "Bot: Analyzing symptoms...\n")

        disease, confidence = predict_disease(symptoms)

        chat_box.insert(tk.END, f"Bot: You may have {disease} ({confidence}% confidence)\n")

        if disease in description_list:
            chat_box.insert(tk.END, f"About: {description_list[disease]}\n")

        if disease in precautionDictionary:
            chat_box.insert(tk.END, "Precautions:\n")
            for p in precautionDictionary[disease]:
                chat_box.insert(tk.END, f"- {p}\n")

        chat_box.insert(tk.END, "\n")

    entry.delete(0, tk.END)

# ------------------ UI ------------------
root = tk.Tk()
root.title("Healthcare Chatbot")
root.geometry("600x500")

chat_box = tk.Text(root, bg="black", fg="white", font=("Arial", 12))
chat_box.pack(pady=10)

scroll = tk.Scrollbar(root)
chat_box.config(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

entry = tk.Entry(root, width=50)
entry.pack(side=tk.LEFT, padx=10)

entry.bind("<Return>", lambda event: send())

send_btn = tk.Button(root, text="Send", command=send, bg="green", fg="white")
send_btn.pack(side=tk.LEFT)

root.mainloop()


# In[4]:





# In[ ]:




