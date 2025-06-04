import tkinter as tk
from tkinter import messagebox

class AuthGUI:
    def __init__(self, root, db, on_login_success, utils):
        self.root = root
        self.db = db
        self.on_login_success = on_login_success
        self.utils = utils

    def create_sign_in(self):
        self.utils.clear_widgets(self.root)
        self.root.configure(bg="#f0f4f7")

        tk.Label(self.root, text="Sign In", font=("Helvetica", 24, "bold"),
                bg="#f0f4f7", fg="#2a2f45").pack(pady=40)

        form_frame = tk.Frame(self.root, bg="#f0f4f7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Username:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Password:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 12), show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_btn = tk.Button(self.root, text="Login", font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white",
                            relief="flat", command=self.authenticate_user)
        login_btn.pack(pady=20)
        self.utils.add_hover_effect(login_btn, "#4caf50", "#45a049")

    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        query = '''
                    SELECT * FROM users WHERE username = %s AND password = %s
                '''
        result = self.db.execute_query(query, (username, password), fetch_type="one")

        if result:
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")