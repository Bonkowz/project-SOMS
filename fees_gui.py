import tkinter as tk
from tkinter import ttk, messagebox

class FeesGUI:
    def __init__(self, root, db, utils):
        self.root = root
        self.db = db
        self.utils = utils
        self.fee_window = tk.Toplevel(self.root)
        self.fee_window.title("Fees Management")
        self.fee_window.geometry("1200x600")
        self.fee_window.configure(bg="#f0f4f7")
        self._create_fees_gui()
        self.load_fees()

    def _create_fees_gui(self):
        tk.Label(self.fee_window, text="Fees Management",
                font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#2a2f45").pack(pady=20)

        search_frame = tk.Frame(self.fee_window, bg="#f0f4f7")
        search_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(search_frame, text="Search Fee ID:",
                font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)

        self.fee_search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        self.fee_search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_frame, text="Search", font=("Helvetica", 10, "bold"),
                             bg="#4a90e2", fg="white", relief="flat",
                             command=self.search_fee)
        search_btn.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(search_frame, text="Add Fee", font=("Helvetica", 10, "bold"),
                          bg="#4caf50", fg="white", relief="flat",
                          command=self.add_fee)
        add_btn.pack(side=tk.RIGHT, padx=5)

        delete_frame = tk.Frame(self.fee_window, bg="#f0f4f7")
        delete_frame.pack(pady=5, padx=10, fill="x")
        tk.Label(delete_frame, text="Delete Fee ID:", font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)
        self.fee_delete_entry = tk.Entry(delete_frame, font=("Helvetica", 12), width=30)
        self.fee_delete_entry.pack(side=tk.LEFT, padx=5)
        delete_btn = tk.Button(delete_frame, text="Delete Fee", font=("Helvetica", 10, "bold"),
                              bg="#e53935", fg="white", relief="flat", command=self.delete_fee)
        delete_btn.pack(side=tk.LEFT, padx=5)

        self.approve_entry = tk.Entry(delete_frame, font=("Helvetica", 12), width=30)
        self.approve_entry.pack(side=tk.RIGHT, padx=5)

        approve_btn = tk.Button(delete_frame, text="Approve", font=("Helvetica", 10, "bold"),
                                bg="#ffeb3b", fg="#333333", relief="flat", command=self.approve_fee)
        approve_btn.pack(side=tk.RIGHT, padx=5)

        columns = ("Fee ID", "Student ID", "Organization ID", "Amount", "Due Date", "Payment Status",
                  "Pay Date", "School Year", "Semester")
        column_widths = {
            "Fee ID": 80,
            "Student ID": 100,
            "Organization ID": 100,
            "Amount": 80,
            "Due Date": 100,
            "Payment Status": 100,
            "Pay Date": 100,
            "School Year": 80,
            "Semester": 80
        }

        self.fee_tree = ttk.Treeview(self.fee_window, columns=columns, show="headings", height=15)

        for col in columns:
            self.fee_tree.heading(col, text=col)
            self.fee_tree.column(col, width=column_widths[col])

        y_scrollbar = ttk.Scrollbar(self.fee_window, orient="vertical",
                                  command=self.fee_tree.yview)
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(self.fee_window, orient="horizontal",
                                  command=self.fee_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        self.fee_tree.configure(yscrollcommand=y_scrollbar.set,
                              xscrollcommand=x_scrollbar.set)

        self.fee_tree.pack(pady=10, padx=10, fill="both", expand=True)

    def search_fee(self):
        fee_id = self.fee_search_entry.get().strip()
        if not fee_id:
            self.load_fees()
            return

        for item in self.fee_tree.get_children():
            self.fee_tree.delete(item)
        query = '''
            SELECT fee_id, student_id, organization_id, amount, due_date, payment_status,
                   pay_date, school_year, semester
            FROM fee
            WHERE fee_id = %s
        '''
        row = self.db.execute_query(query, (fee_id,), fetch_type="one")
        if row:
            self.fee_tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Not Found", "Fee not found.")

    def load_fees(self):
        for item in self.fee_tree.get_children():
            self.fee_tree.delete(item)
        query = '''
            SELECT fee_id, student_id, organization_id, amount, due_date, payment_status,
                   pay_date, school_year, semester
            FROM fee
        '''
        rows = self.db.execute_query(query, fetch_type="all")
        if rows:
            for row in rows:
                self.fee_tree.insert('', 'end', values=row)

    def add_fee(self):
        popup = tk.Toplevel(self.fee_window)
        popup.title("Add Fee")
        popup.geometry("500x500")
        popup.grab_set()

        fields = [
            ("Amount", "amount"),
            ("Payment Status", "payment_status"),
            ("Due Date (YYYY-MM-DD)", "due_date"),
            ("Pay Date (YYYY-MM-DD or blank)", "pay_date"),
            ("School Year", "school_year"),
            ("Semester", "semester"),
            ("Organization ID", "organization_id"),
            ("Student ID", "student_id"),
        ]
        entries = {}
        for idx, (label, key) in enumerate(fields):
            tk.Label(popup, text=label, font=("Helvetica", 11)).grid(row=idx, column=0, sticky="e", padx=10, pady=8)
            entry = tk.Entry(popup, font=("Helvetica", 11), width=30)
            entry.grid(row=idx, column=1, padx=10, pady=8)
            entries[key] = entry

        def on_submit():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            # Get the next fee_id
            get_next_fee_id_query = "SELECT COALESCE(MAX(fee_id), 0) + 1 FROM fee"
            next_fee_id_result = self.db.execute_query(get_next_fee_id_query, fetch_type="one")
            next_fee_id = next_fee_id_result[0] if next_fee_id_result else 1

            insert_fee_query = '''
                INSERT INTO fee (
                    fee_id, amount, payment_status, due_date, pay_date,
                    school_year, semester, organization_id, student_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            insert_fee_params = (
                next_fee_id,
                data["amount"],
                data["payment_status"],
                data["due_date"],
                data["pay_date"] if data["pay_date"] else None,
                data["school_year"],
                data["semester"],
                data["organization_id"],
                data["student_id"]
            )
            try:
                self.db.execute_query(insert_fee_query, insert_fee_params)
                messagebox.showinfo("Info", "Added fee successfully!")
                popup.destroy()
                self.load_fees()
            except Exception as err:
                messagebox.showerror("Database Error", str(err))

        submit_btn = tk.Button(popup, text="Submit", font=("Helvetica", 11, "bold"), bg="#4caf50", fg="white", command=on_submit)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def delete_fee(self):
        fee_id = self.fee_delete_entry.get().strip()
        if not fee_id:
            messagebox.showwarning("Input Error", "Please enter a Fee ID to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete fee with Fee ID: {fee_id}?")
        if not confirm:
            return
        query = "DELETE FROM fee WHERE fee_id = %s"
        result = self.db.execute_query(query, (fee_id,))
        if result is not None:
            if self.db.execute_query("SELECT ROW_COUNT()", fetch_type="one")[0] > 0:
                messagebox.showinfo("Success", "Fee deleted successfully.")
                self.load_fees()
            else:
                messagebox.showinfo("Not Found", "Fee ID not found.")

    def approve_fee(self):
        fee_id = self.approve_entry.get().strip()
        if not fee_id:
            messagebox.showwarning("Input Error", "Please enter a Fee ID to approve.")
            return
        query = '''
            UPDATE fee
            SET payment_status = 'Paid', pay_date = CURRENT_DATE()
            WHERE fee_id = %s;
        '''
        result = self.db.execute_query(query, (fee_id,))
        if result is not None:
            if self.db.execute_query("SELECT ROW_COUNT()", fetch_type="one")[0] > 0:
                messagebox.showinfo("Success", "Fee approved successfully.")
                self.load_fees()
            else:
                messagebox.showinfo("Not Found", "Fee ID not found.")