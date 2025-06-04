import tkinter as tk
from tkinter import ttk, messagebox

class MembersGUI:
    def __init__(self, root, db, selected_org_id, utils):
        self.root = root
        self.db = db
        self.selected_org_id = selected_org_id
        self.utils = utils
        self.member_window = tk.Toplevel(self.root)
        self.member_window.title("Membership Management")
        self.member_window.geometry("1400x600")
        self.member_window.configure(bg="#f0f4f7")
        self._create_member_gui()
        self.load_members()

    def _create_member_gui(self):
        tk.Label(self.member_window, text="Membership Management",
                font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#2a2f45").pack(pady=20)

        search_frame = tk.Frame(self.member_window, bg="#f0f4f7")
        search_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(search_frame, text="Search Student ID:",
                font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)

        self.member_search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        self.member_search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_frame, text="Search", font=("Helvetica", 10, "bold"),
                             bg="#4a90e2", fg="white", relief="flat",
                             command=self.search_member)
        search_btn.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(search_frame, text="Add member", font=("Helvetica", 10, "bold"),
                          bg="#4caf50", fg="white", relief="flat",
                          command=self.add_member)
        add_btn.pack(side=tk.RIGHT, padx=5)

        delete_frame = tk.Frame(self.member_window, bg="#f0f4f7")
        delete_frame.pack(pady=5, padx=10, fill="x")
        tk.Label(delete_frame, text="Delete Student ID:", font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)
        self.member_delete_entry = tk.Entry(delete_frame, font=("Helvetica", 12), width=30)
        self.member_delete_entry.pack(side=tk.LEFT, padx=5)
        delete_btn = tk.Button(delete_frame, text="Delete member", font=("Helvetica", 10, "bold"),
                              bg="#e53935", fg="white", relief="flat", command=self.delete_member)
        delete_btn.pack(side=tk.LEFT, padx=5)

        columns = ("Id", "Name", "Email", "Gender", "Enrollment Status", "Graduation Date", "Degree Program", "Unpaid Fees",
                   "Organization ID", "Membership Batch", "Membership Status", "Committee Role", "Committee")
        column_widths = {
            "Id": 80,
            "Name": 150,
            "Email": 150,
            "Gender": 60,
            "Enrollment Status": 80,
            "Graduation Date": 100,
            "Degree Program": 100,
            "Unpaid Fees": 80,
            "Organization ID": 80,
            "Membership Batch": 100,
            "Membership Status": 80,
            "Committee Role": 80,
            "Committee": 80
        }

        self.member_tree = ttk.Treeview(self.member_window, columns=columns, show="headings", height=15)

        for col in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=column_widths[col])

        y_scrollbar = ttk.Scrollbar(self.member_window, orient="vertical",
                                  command=self.member_tree.yview)
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(self.member_window, orient="horizontal",
                                  command=self.member_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        self.member_tree.configure(yscrollcommand=y_scrollbar.set,
                                 xscrollcommand=x_scrollbar.set)

        self.member_tree.pack(pady=10, padx=10, fill="both", expand=True)

    def search_member(self):
        student_id = self.member_search_entry.get().strip()
        if not student_id:
            self.load_members()
            return

        for item in self.member_tree.get_children():
            self.member_tree.delete(item)

        query = '''
            SELECT m.student_id, m.member_name, m.email_address, m.gender, m.enrollment_status,
                   m.graduation_date, m.degree_program, m.member_total_unpaid_fees, ms.organization_id,
                   ms.batch_year_of_membership, ms.membership_status, ms.committee_role, ms.committee
            FROM member m LEFT JOIN member_serves ms ON m.student_id = ms.student_id
            WHERE m.student_id = %s
        '''
        row = self.db.execute_query(query, (student_id,), fetch_type="one")
        if row:
            self.member_tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Not Found", "Student not found.")

    def load_members(self):
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)

        query = '''
            SELECT m.student_id, m.member_name, m.email_address, m.gender, m.enrollment_status,
                   m.graduation_date, m.degree_program, m.member_total_unpaid_fees, ms.organization_id,
                   ms.batch_year_of_membership, ms.membership_status, ms.committee_role, ms.committee
            FROM member m LEFT JOIN member_serves ms ON m.student_id = ms.student_id
        '''
        rows = self.db.execute_query(query, fetch_type="all")
        if rows:
            for row in rows:
                self.member_tree.insert('', 'end', values=row)

    def add_member(self):
        popup = tk.Toplevel(self.member_window)
        popup.title("Add Member")
        popup.geometry("500x600")
        popup.grab_set()

        fields = [
            ("Member Name", "member_name"),
            ("Email Address", "email_address"),
            ("Gender", "gender"),
            ("Enrollment Status", "enrollment_status"),
            ("Batch Year of Enrollment", "batch_year_of_enrollment"),
            ("Graduation Date (YYYY-MM-DD)", "graduation_date"),
            ("Degree Program", "degree_program"),
            ("Organization ID (for serves)", "organization_id_serves"),
            ("Org School Year (for serves)", "org_school_year"),
            ("Semester (for serves)", "semester"),
            ("Batch Year of Membership (for serves)", "batch_year_of_membership"),
            ("Membership Status (for serves)", "membership_status"),
            ("Committee Role (for serves)", "committee_role"),
            ("Committee (for serves)", "committee"),
        ]
        entries = {}
        for idx, (label, key) in enumerate(fields):
            tk.Label(popup, text=label, font=("Helvetica", 11)).grid(row=idx, column=0, sticky="e", padx=10, pady=8)
            entry = tk.Entry(popup, font=("Helvetica", 11), width=30)
            entry.grid(row=idx, column=1, padx=10, pady=8)
            entries[key] = entry

        def on_submit():
            data = {key: entry.get().strip() for key, entry in entries.items()}

            next_student_id = self.db.get_next_student_id()

            member_query = '''
              INSERT INTO member (
                student_id, gender, enrollment_status, email_address, member_name,
                batch_year_of_enrollment, degree_program, member_total_unpaid_fees, graduation_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 0, %s);
            '''
            member_params = (
                next_student_id,
                data["gender"],
                data["enrollment_status"],
                data["email_address"],
                data["member_name"],
                data["batch_year_of_enrollment"],
                data["degree_program"],
                data["graduation_date"] if data["graduation_date"] else None,
            )

            serves_query = '''
                INSERT INTO member_serves (
                    school_year, membership_status, batch_year_of_membership, semester,
                    committee_role, committee, organization_id, student_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            serves_params = (
                data["org_school_year"],
                data["membership_status"],
                data["batch_year_of_membership"],
                data["semester"],
                data["committee_role"] if data["committee_role"] else None,
                data["committee"],
                data["organization_id_serves"],
                next_student_id
            )

            try:
                # Insert into member table
                self.db.execute_query(member_query, member_params)

                # Insert into member_serves table
                self.db.execute_query(serves_query, serves_params)

                # Update member count in organization
                self.db.execute_query("UPDATE organization SET no_of_members = no_of_members + 1 WHERE organization_id = %s;",
                                      (data["organization_id_serves"],))

                messagebox.showinfo("Success", "Member added successfully!")
                popup.destroy()
                self.load_members()
            except Exception as err:
                messagebox.showerror("Error adding member", str(err))


        submit_btn = tk.Button(popup, text="Submit", font=("Helvetica", 11, "bold"), bg="#4caf50", fg="white", command=on_submit)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def delete_member(self):
        student_id = self.member_delete_entry.get().strip()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member with Student ID: {student_id}?")
        if not confirm:
            return

        try:
            # Get organization_id associated with the student before deletion to decrement member count
            org_id_query = "SELECT organization_id FROM member_serves WHERE student_id = %s"
            org_id_result = self.db.execute_query(org_id_query, (student_id,), fetch_type="one")
            
            delete_member_query = "DELETE FROM member WHERE student_id = %s"
            result = self.db.execute_query(delete_member_query, (student_id,))

            if result is not None: # Check if query executed without database error
                if self.db.execute_query("SELECT ROW_COUNT()", fetch_type="one")[0] > 0: # Check if any row was affected
                    messagebox.showinfo("Success", "Member deleted successfully.")
                    if org_id_result:
                        organization_id = org_id_result[0]
                        self.db.execute_query("UPDATE organization SET no_of_members = no_of_members - 1 WHERE organization_id = %s;", (organization_id,))
                    self.load_members()
                else:
                    messagebox.showinfo("Not Found", "Student ID not found.")
            
        except Exception as err:
            messagebox.showerror("Error deleting member", str(err))