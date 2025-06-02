import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'gift',
    'password': 'useruser',
    'database': 'soms'
}


class SOMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Organization Management System")
        self.root.geometry("1000x700")
        self.create_sign_in()
        self.organizations = {}  # Dictionary to store org_name: org_id mapping

    def fetch_organizations(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT organization_id, organization_name FROM organization ORDER BY organization_name"
            cursor.execute(query)
            results = cursor.fetchall()
            self.organizations = {org_name: org_id for org_id, org_name in results}
            conn.close()
            return list(self.organizations.keys())
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return []

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_sign_in(self):
        self.clear_root()
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
        self.add_hover_effect(login_btn, "#4caf50", "#45a049")

    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        try:
            print("Connecting with:", DB_CONFIG)
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                self.create_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


    def create_dashboard(self):
        self.clear_root()
        self.root.configure(bg="#f0f4f7")  # Light background

        tk.Label(self.root, text="Organization Dashboard", font=("Helvetica", 24, "bold"),
                bg="#f0f4f7", fg="#2a2f45").pack(pady=20)        # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f4f7")
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Select Organization:", font=("Helvetica", 12),
                bg="#f0f4f7").pack(side=tk.LEFT)
        
        # Create and populate the Combobox
        organizations = self.fetch_organizations()
        self.org_search_combo = ttk.Combobox(search_frame, font=("Helvetica", 12), width=30, state="readonly")
        self.org_search_combo['values'] = organizations
        self.org_search_combo.pack(side=tk.LEFT, padx=5)
        
        # Bind the combobox selection to automatically search
        self.org_search_combo.bind('<<ComboboxSelected>>', lambda e: self.search_organization())

        # Organization info frame
        self.org_info_frame = tk.LabelFrame(self.root, text="Organization Info", font=("Helvetica", 12, "bold"),
                                            bg="#ffffff", padx=10, pady=10)
        self.org_info_frame.pack(fill="x", padx=10, pady=10)

        self.org_labels = {
            "Name": tk.Label(self.org_info_frame, text="Name: ", font=("Helvetica", 11), bg="#ffffff"),
            "Type": tk.Label(self.org_info_frame, text="Type: ", font=("Helvetica", 11), bg="#ffffff"),
            "Members": tk.Label(self.org_info_frame, text="Members: ", font=("Helvetica", 11), bg="#ffffff"),
            "ID": tk.Label(self.org_info_frame, text="ID: ", font=("Helvetica", 11), bg="#ffffff")
        }
        for label in self.org_labels.values():
            label.pack(anchor="w", pady=2)

        # Action buttons
        action_frame = tk.Frame(self.root, bg="#f0f4f7")
        action_frame.pack(pady=15)

        btn1 = tk.Button(action_frame, text="Membership Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_membership_management)
        btn1.pack(side=tk.LEFT, padx=10)
        self.add_hover_effect(btn1, "#4caf50", "#45a049")

        btn2 = tk.Button(action_frame, text="Fees Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_fees_management)
        btn2.pack(side=tk.LEFT, padx=10)
        self.add_hover_effect(btn2, "#4caf50", "#45a049")

        btn3 = tk.Button(action_frame, text="Other Reports", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_reports)
        btn3.pack(side=tk.LEFT, padx=10)
        self.add_hover_effect(btn3, "#4caf50", "#45a049")

        # Report section
        self.report_frame = tk.LabelFrame(self.root, text="Other Reports", font=("Helvetica", 12, "bold"),
                                        bg="#ffffff", padx=10, pady=10)
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.report_dropdown = ttk.Combobox(self.report_frame, width=90, state="readonly", font=("Helvetica", 10))
        self.report_dropdown['values'] = [
            "1. Members by Role, Status, Gender, Degree, etc.",
            "2. Members with Unpaid Fees (Semester + SY)",
            "3. Member’s Unpaid Fees (All Orgs)",
            "4. Executive Committee Members (By Year)",
            "5. Presidents Per Year (Reverse Chrono)",
            "6. Late Payments in a Semester",
            "7. % Active vs Inactive Members",
            "8. Alumni Members as of Date",
            "9. Total Paid vs Unpaid Fees (As of Date)",
            "10. Member with Highest Debt"
        ]
        self.report_dropdown.pack(pady=5)

        gen_report_btn = tk.Button(self.report_frame, text="Generate Report", font=("Helvetica", 10, "bold"),
                                bg="#2196f3", fg="white", relief="flat", command=self.generate_report)
        gen_report_btn.pack(pady=5)
        self.add_hover_effect(gen_report_btn, "#2196f3", "#1976d2")        # Create Treeview for tabular data display
        self.report_output = ttk.Treeview(self.report_frame, height=15, show="headings")
        self.report_output.pack(fill="both", expand=True, pady=5)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.report_frame, orient="vertical", command=self.report_output.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(self.report_frame, orient="horizontal", command=self.report_output.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        self.report_output.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    def add_hover_effect(self, widget, bg_normal, bg_hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))

    def search_organization(self):
        org_name = self.org_search_combo.get()
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT organization_id, organization_name, organization_type, no_of_members FROM organization WHERE organization_name LIKE %s"
            cursor.execute(query, ('%' + org_name + '%',))
            result = cursor.fetchone()
            if result:
                org_id, name, org_type, members = result
                self.org_labels["Name"].config(text=f"Name: {name}")
                self.org_labels["Type"].config(text=f"Type: {org_type}")
                self.org_labels["Members"].config(text=f"Members: {members}")
                self.org_labels["ID"].config(text=f"ID: {org_id}")
                self.selected_org_id = org_id
            else:
                messagebox.showinfo("Not Found", "Organization not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def generate_report(self):
        index = self.report_dropdown.current()
        org_id = getattr(self, "selected_org_id", None)

        if org_id is None and index not in [2]:  # Query 3 doesn't use org_id
            messagebox.showerror("Error", "Please select an organization first.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            if index == 0:
                # Query 1
                query = '''
                    SELECT m.student_id, m.member_name, s.committee_role, s.membership_status, m.gender, m.degree_program,
                        s.batch_year_of_membership, s.committee
                    FROM member_serves s
                    INNER JOIN member m ON m.student_id = s.student_id
                    WHERE s.organization_id = %s
                '''
                cursor.execute(query, (org_id,))

            elif index == 1:
                # Query 2
                school_year = simpledialog.askstring("Input", "Enter School Year (e.g., 2023):")
                semester = simpledialog.askstring("Input", "Enter Semester (e.g., 1):")
                query = '''
                    SELECT m.member_name, f.amount, f.payment_status, s.batch_year_of_membership,
                        s.semester, s.school_year
                    FROM member m
                    INNER JOIN member_serves s ON m.student_id = s.student_id
                    INNER JOIN fee f ON m.student_id = f.student_id
                    WHERE f.payment_status = 'Not Paid'
                    AND s.organization_id = %s
                    AND f.school_year = %s
                    AND f.semester = %s
                '''
                cursor.execute(query, (org_id, school_year, semester))

            elif index == 2:
                # Query 3
                student_id = simpledialog.askstring("Input", "Enter Student ID:")
                if not student_id:
                    return
                query = '''
                    SELECT o.organization_name, f.amount, f.due_date, f.payment_status,
                        f.school_year, f.semester
                    FROM fee f
                    INNER JOIN member_serves s ON f.student_id = s.student_id
                    INNER JOIN organization o ON s.organization_id = o.organization_id
                    WHERE f.payment_status = 'Not Paid'
                    AND f.student_id = %s
                '''
                cursor.execute(query, (student_id,))

            elif index == 3:
                # Query 4
                school_year = simpledialog.askstring("Input", "Enter School Year:")
                query = '''
                    SELECT m.member_name, s.committee_role, s.school_year
                    FROM member_serves s
                    INNER JOIN member m ON s.student_id = m.student_id
                    WHERE s.committee_role != 'Member'
                    AND s.organization_id = %s
                    AND s.school_year = %s
                '''
                cursor.execute(query, (org_id, school_year))

            elif index == 4:
                # Query 5
                query = '''
                    SELECT m.member_name, s.committee_role, s.school_year
                    FROM member_serves s
                    INNER JOIN member m ON s.student_id = m.student_id
                    WHERE s.committee_role = 'President'
                    AND s.organization_id = %s
                    ORDER BY s.school_year DESC
                '''
                cursor.execute(query, (org_id,))

            elif index == 5:
                # Query 6
                school_year = simpledialog.askstring("Input", "Enter School Year:")
                semester = simpledialog.askstring("Input", "Enter Semester:")
                query = '''
                    SELECT member_name, payment_status, due_date, pay_date
                    FROM fee f
                    LEFT JOIN member m ON f.student_id = m.student_id
                    WHERE organization_id = %s
                    AND school_year = %s
                    AND semester = %s
                    AND payment_status = 'Paid'
                    AND pay_date > due_date
                '''
                cursor.execute(query, (org_id, school_year, semester))

            elif index == 6:
                # Query 7
                query = '''
                    SELECT 
                        COUNT(CASE WHEN membership_status = 'Active' THEN 1 END)/COUNT(*) AS '%Active',
                        COUNT(CASE WHEN membership_status = 'Inactive' THEN 1 END)/COUNT(*) AS '%Inactive'
                    FROM member_serves ms
                    LEFT JOIN organization org ON ms.organization_id = org.organization_id
                    WHERE ms.organization_id = %s
                '''
                cursor.execute(query, (org_id,))

            elif index == 7:
                # Query 8
                query = '''
                    SELECT member_name, enrollment_status, graduation_date
                    FROM member m
                    LEFT JOIN member_serves ms ON m.student_id = ms.student_id
                    WHERE organization_id = %s
                    AND enrollment_status = 'Graduated'
                    AND graduation_date >= DATE_SUB(CURRENT_DATE(), INTERVAL (20 * 6) MONTH)
                '''
                cursor.execute(query, (org_id,))

            elif index == 8:
                # Query 9
                query = '''
                    SELECT SUM(amount) AS "Total Amount", payment_status
                    FROM fee f
                    LEFT JOIN organization o ON f.organization_id = o.organization_id
                    WHERE f.organization_id = %s
                    AND due_date < DATE("2024-01-01")
                    AND COALESCE(pay_date < DATE("2024-01-01"), 1)
                    GROUP BY f.payment_status
                '''
                cursor.execute(query, (org_id,))

            elif index == 9:
                # Query 10
                query = '''
                    SELECT MAX(Amount) AS "Total Amount", Member FROM (
                        SELECT SUM(amount) AS Amount, member_name AS Member
                        FROM fee f
                        LEFT JOIN member m ON f.student_id = m.student_id
                        WHERE f.organization_id = %s
                        GROUP BY f.student_id
                    ) q
                '''
                cursor.execute(query, (org_id,))

            else:
                self.report_output.delete("1.0", tk.END)
                self.report_output.insert(tk.END, "Report not yet implemented.")
                return            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            
            # Configure treeview columns
            self.report_output['columns'] = columns
            for col in columns:
                self.report_output.heading(col, text=col.replace('_', ' ').title())
                self.report_output.column(col, width=100)  # Adjust width as needed
            
            # Fetch and insert data
            rows = cursor.fetchall()
            
            # Clear previous data
            for item in self.report_output.get_children():
                self.report_output.delete(item)
                
            if not rows:
                messagebox.showinfo("Report", "No results found.")
            else:
                for row in rows:
                    self.report_output.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def open_membership_management(self):
        self.clear_root()
        self.root.configure(bg="#f0f4f7")

        tk.Label(self.root, text="Membership Management", font=("Helvetica", 20, "bold"), bg="#f0f4f7").pack(pady=10)

        control_frame = tk.Frame(self.root, bg="#f0f4f7")
        control_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(control_frame, text="Search Student (Name/ID):", bg="#f0f4f7").pack(side=tk.LEFT)
        search_entry = tk.Entry(control_frame)
        search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Search", bg="#4a90e2", fg="white", command=lambda: self.search_member(search_entry.get())).pack(side=tk.LEFT)

        add_btn = tk.Button(control_frame, text="Add member", font=("Helvetica", 14, "bold"), bg="#4caf50", fg="white", command=self.open_add_member_modal)
        add_btn.pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        xscroll = tk.Scrollbar(table_frame, orient="horizontal")
        yscroll = tk.Scrollbar(table_frame, orient="vertical")
        self.members_tree = ttk.Treeview(
            table_frame,
            columns=("id", "name", "gender", "status", "program", "unpaid_fees", "grad_date",
                    "school_year", "membership_status", "batch", "semester", "committee", "role"),
            show="headings",
            xscrollcommand=xscroll.set,
            yscrollcommand=yscroll.set
        )
        xscroll.config(command=self.members_tree.xview)
        yscroll.config(command=self.members_tree.yview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.members_tree.pack(fill="both", expand=True)

        for col in self.members_tree["columns"]:
            self.members_tree.heading(col, text=col.replace("_", " ").capitalize())
            self.members_tree.column(col, anchor="center", width=100, minwidth=100, stretch=True)

        self.populate_members()

    def open_add_member_modal(self):
        modal = tk.Toplevel(self.root)
        modal.title("Member Attributes")
        modal.geometry("420x650")
        modal.grab_set()

        canvas = tk.Canvas(modal)
        frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(modal, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=frame, anchor='nw')

        fields = {
            "student_id": "Student ID",
            "gender": "Gender",
            "enrollment_status": "Enrollment Status",
            "email_address": "Email Address",
            "member_name": "Full Name",
            "batch_year_of_enrollment": "Batch Year of Enrollment",
            "degree_program": "Degree Program",
            "member_total_unpaid_fees": "Total Unpaid Fees",
            "graduation_date": "Graduation Date (YYYY-MM-DD)"
        }

        entries = {}
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry

        def open_member_serves_modal(student_id, organization_id):
            serves_modal = tk.Toplevel(self.root)
            serves_modal.title("Membership Relations")
            serves_modal.geometry("400x400")
            serves_modal.grab_set()

            serves_fields = {
                "school_year": "School Year",
                "membership_status": "Membership Status",
                "batch_year_of_membership": "Batch Year of Membership",
                "semester": "Semester",
                "committee_role": "Committee Role",
                "committee": "Committee"
            }

            serves_entries = {}
            for i, (key, label) in enumerate(serves_fields.items()):
                tk.Label(serves_modal, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
                entry = tk.Entry(serves_modal, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                serves_entries[key] = entry

            def submit_serves():
                sdata = {key: entry.get().strip() for key, entry in serves_entries.items() if key in serves_fields}
                if not sdata.get("school_year") or not sdata.get("membership_status"):
                    messagebox.showwarning("Input Error", "School year and membership status are required.", parent=serves_modal)
                    return

                try:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cursor = conn.cursor()
                    insert_query = '''
                        INSERT INTO member_serves (
                            school_year, membership_status, batch_year_of_membership, semester,
                            committee_role, committee, organization_id, student_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(insert_query, (
                        sdata.get("school_year"), sdata.get("membership_status"), sdata.get("batch_year_of_membership"),
                        sdata.get("semester"), sdata.get("committee_role"), sdata.get("committee"),
                        organization_id, student_id
                    ))
                    
                    # Update member count
                    cursor.execute('''
                        UPDATE organization 
                        SET no_of_members = no_of_members + 1 
                        WHERE organization_id = %s
                    ''', (organization_id,))

                    conn.commit()
                    conn.close()

                    sql_line = f"""
    INSERT INTO member_serves (
        school_year, membership_status, batch_year_of_membership, semester,
        committee_role, committee, organization_id, student_id
    ) VALUES (
        {sdata.get('school_year')}, '{sdata.get('membership_status')}', {sdata.get('batch_year_of_membership')},
        '{sdata.get('semester')}', '{sdata.get('committee_role')}', '{sdata.get('committee')}',
        {organization_id}, {student_id}
    );

    UPDATE organization 
    SET no_of_members = no_of_members + 1 
    WHERE organization_id = {organization_id};
    """
                    with open("soms_db.sql", "a") as f:
                        f.write(sql_line)

                    messagebox.showinfo("Success", "Membership relation added successfully.", parent=serves_modal)
                    serves_modal.destroy()
                    self.open_membership_management()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", str(err), parent=serves_modal)

            submit_btn = tk.Button(serves_modal, text="Submit", bg="#4caf50", fg="white", command=submit_serves)
            submit_btn.grid(row=len(serves_fields), column=0, columnspan=2, pady=20)

        def submit_member():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            required_keys = ["student_id", "gender", "enrollment_status", "email_address", "member_name", "batch_year_of_enrollment", "degree_program"]
            if not all(data.get(k) for k in required_keys):
                messagebox.showwarning("Input Error", "All required fields must be filled out.", parent=modal)
                return

            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                insert_query = '''
                    INSERT INTO member (
                        student_id, gender, enrollment_status, email_address,
                        member_name, batch_year_of_enrollment, degree_program,
                        member_total_unpaid_fees, graduation_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (
                    data.get("student_id"), data.get("gender"), data.get("enrollment_status"), data.get("email_address"),
                    data.get("member_name"), data.get("batch_year_of_enrollment"), data.get("degree_program"),
                    data.get("member_total_unpaid_fees"), data.get("graduation_date")
                ))
                conn.commit()
                conn.close()

                sql_line = f"""
    INSERT INTO member (
        student_id,
        gender,
        enrollment_status,
        email_address,
        member_name,
        batch_year_of_enrollment,
        degree_program,
        member_total_unpaid_fees,
        graduation_date
    ) VALUES (
        {data.get('student_id')},
        '{data.get('gender')}',
        '{data.get('enrollment_status')}',
        '{data.get('email_address')}',
        '{data.get('member_name')}',
        {data.get('batch_year_of_enrollment')},
        '{data.get('degree_program')}',
        {data.get('member_total_unpaid_fees')},
        '{data.get('graduation_date')}'
    );
    """
                with open("soms_db.sql", "a") as f:
                    f.write(sql_line)

                modal.destroy()
                open_member_serves_modal(data.get("student_id"), self.selected_org_id)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err), parent=modal)

        submit_btn = tk.Button(frame, text="Submit", bg="#4caf50", fg="white", command=submit_member)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)


   


    def populate_members(self):
        self.members_tree.delete(*self.members_tree.get_children())
        org_id = getattr(self, "selected_org_id", None)
        if not org_id:
            messagebox.showwarning("Missing Organization", "No organization selected.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = '''
                SELECT m.student_id, m.member_name, m.gender, m.enrollment_status, m.degree_program,
                    m.member_total_unpaid_fees, m.graduation_date,
                    s.school_year, s.membership_status, s.batch_year_of_membership, s.semester, s.committee, s.committee_role
                FROM member m
                JOIN member_serves s ON m.student_id = s.student_id
                WHERE s.organization_id = %s
            '''
            cursor.execute(query, (org_id,))
            for row in cursor.fetchall():
                self.members_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))



    def update_member(self, student_id):
        print(f"Update logic for student_id={student_id}")



    def delete_member(self, student_id):
        print(f"Delete logic for student_id={student_id}")



    def search_member(self, keyword):
        print(f"Search for member with keyword: {keyword}")



    def open_fees_management(self):
        messagebox.showinfo("Coming Soon", "Fees Management module will be implemented next.")

    def open_reports(self):
        pass  # already shown in main screen

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SOMSApp(root)
    root.mainloop()
