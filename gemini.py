import tkinter as tk
import requests

API_URL = "http://127.0.0.1:8000/chat/"

def send_message():
    user_msg = entry.get()

    response = requests.post(API_URL, json={"message": user_msg})
    data = response.json()

    chat_box.insert(tk.END, "You: " + user_msg + "\n\n")
    chat_box.insert(tk.END, "Gemini: " + data["reply"] + "\n\n")

    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Gemini")

chat_box = tk.Text(root, height=20, width=100)
chat_box.pack()

input_frame =tk.Frame(root)
input_frame.pack(pady=10)

entry = tk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, padx=10)

send_btn = tk.Button(input_frame, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

root.mainloop()
