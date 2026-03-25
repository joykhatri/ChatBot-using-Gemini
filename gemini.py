import tkinter as tk
import requests

API_URL = "http://127.0.0.1:8000/chat/"

access_token = None
refresh_token = None

def hide_all():
    login_frame.pack_forget()
    register_frame.pack_forget()
    chat_frame.pack_forget()

def show_login():
    hide_all()
    login_frame.pack()

def show_register():
    hide_all()
    register_frame.pack()

def show_chat_screen():
    hide_all()
    chat_frame.pack()


def login():
    global access_token, refresh_token

    data = {
        "email": login_email.get(),
        "password": login_password.get()
    }

    result = requests.post("http://127.0.0.1:8000/api/login/", json=data).json()

    if result.get("status"):
        access_token = result["data"]["tokens"]["access"]
        refresh_token = result["data"]["tokens"]["refresh"]

        show_chat_screen()
    else:
        login_status.config(text=result.get("message"))

def register():
    data = {
        "name": reg_name.get(),
        "email": reg_email.get(),
        "password": reg_password.get()
    }

    result = requests.post("http://127.0.0.1:8000/api/register/", json=data).json()
    reg_status.config(text=result.get("message"))

def send_message():
    global access_token
    user_msg = entry.get()

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(API_URL, json={"message": user_msg}, headers=headers)
    data = response.json()

    chat_box.insert(tk.END, "You: " + user_msg + "\n\n")
    chat_box.insert(tk.END, "Gemini: " + data["reply"] + "\n\n")

    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Gemini")
root.geometry("800x400")
root.resizable(False, False)

login_frame = tk.Frame(root)
tk.Label(login_frame, text="Login", font=("Arial", 16)).pack()

tk.Label(login_frame, text="Email").pack()
login_email = tk.Entry(login_frame)
login_email.pack()

tk.Label(login_frame, text="Password").pack()
login_password = tk.Entry(login_frame, show="*")
login_password.pack()

tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Go to Register", command=show_register).pack()

login_status = tk.Label(login_frame, text="")
login_status.pack()



register_frame = tk.Frame(root)
tk.Label(register_frame, text="Register", font=("Arial", 16)).pack()

tk.Label(register_frame, text="Name").pack()
reg_name = tk.Entry(register_frame)
reg_name.pack()

tk.Label(register_frame, text="Email").pack()
reg_email = tk.Entry(register_frame)
reg_email.pack()

tk.Label(register_frame, text="Password").pack()
reg_password = tk.Entry(register_frame, show="*")
reg_password.pack()

tk.Button(register_frame, text="Register", command=register).pack()
tk.Button(register_frame, text="Go to Login", command=show_login).pack()

reg_status = tk.Label(register_frame, text="")
reg_status.pack()


chat_frame = tk.Frame(root)
# tk.Label(chat_frame, text="Gemini", font=("Arial", 16)).pack()

chat_box = tk.Text(chat_frame, height=20, width=100)
chat_box.pack()

input_frame =tk.Frame(chat_frame)
input_frame.pack(pady=10)

entry = tk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, padx=10)

send_btn = tk.Button(input_frame, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

show_login()
root.mainloop()
