import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'gift',
    'password': 'useruser',
    'database': 'soms'
}

# TODO: update todal unpaid when adding fee
# TODO: update cound when adding member

class SOMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Organization Management System")
        self.root.geometry("1000x700")
        self.create_sign_in()
        #####
        self.organizations = {} # Dictionary to store org_name: org_id mapping

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
        self.root.configure(bg="#f0f4f7") # Light background

        tk.Label(self.root, text="Organization Dashboard", font=("Helvetica", 24, "bold"),
                bg="#f0f4f7", fg="#2a2f45").pack(pady=20) # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f4f7")
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Select Organization:", font=("Helvetica", 12),
                bg="#f0f4f7").pack(side=tk.LEFT)
        
        organizations = self.fetch_organizations()
        self.org_search_combo = ttk.Combobox(search_frame, font=("Helvetica", 12), width=30, state="readonly")
        self.org_search_combo['values'] = organizations
        self.org_search_combo.pack(side=tk.LEFT, padx=5)
        
        # combobox selection to automatically search
        self.org_search_combo.bind('<<ComboboxSelected>>', lambda e: self.get_organizations())

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

        btn3 = tk.Button(action_frame, text="Organization Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_organization_management)
        btn3.pack(side=tk.LEFT, padx=10)
        self.add_hover_effect(btn3, "#4caf50", "#45a049")

        # Report section
        self.report_frame = tk.LabelFrame(self.root, text="Generate Reports", font=("Helvetica", 12, "bold"),
                                        bg="#ffffff", padx=10, pady=10)
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.report_dropdown = ttk.Combobox(self.report_frame, width=90, state="readonly", font=("Helvetica", 10))
        self.report_dropdown['values'] = [
            "1. Members by Role, Status, Gender, Degree, etc.",
            "2. Members with Unpaid Fees (Semester + SY)",
            "3. Member's Unpaid Fees (All Orgs)",
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
        self.add_hover_effect(gen_report_btn, "#2196f3", "#1976d2") 
        self.report_output = ttk.Treeview(self.report_frame, height=15, show="headings")
        self.report_output.pack(fill="both", expand=True, pady=5)
        
        # scrollbars
        y_scrollbar = ttk.Scrollbar(self.report_frame, orient="vertical", command=self.report_output.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(self.report_frame, orient="horizontal", command=self.report_output.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        self.report_output.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    def add_hover_effect(self, widget, bg_normal, bg_hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))

    def get_organizations(self):
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
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def generate_report(self):
        index = self.report_dropdown.current()
        org_id = getattr(self, "selected_org_id", None)

        if org_id is None and index not in [2]: # Query 3 doesn't use org_id
            messagebox.showerror("Error", "Please select an organization first.")
            return

        if index not in [0,1,2,3,4,5,6,7,8,9]: 
            messagebox.showerror("Error", "Please select a report first.")
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
                    SELECT
                        f.amount,
                        f.due_date,
                        f.payment_status,
                        f.school_year,
                        f.semester
                    FROM fee f
                    LEFT JOIN member_serves s ON f.student_id = s.student_id
                    LEFT JOIN organization o ON s.organization_id = o.organization_id
                    WHERE f.payment_status = 'Not Paid'
                    AND f.student_id = %s;
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
                date = simpledialog.askstring("Input", "Enter the date in the format (YYYY-MM-DD):")
                query = '''
                    SELECT SUM(amount) AS "Total Amount", payment_status
                    FROM fee f
                    LEFT JOIN organization o ON f.organization_id = o.organization_id
                    WHERE f.organization_id = %s
                    AND due_date > DATE(%s)
                    AND COALESCE(pay_date > DATE(%s), 1)
                    GROUP BY f.payment_status
                '''
                cursor.execute(query, (org_id,date,date))

            elif index == 9:
                # Query 10
                query = '''
                SELECT
                    m.member_name AS Member,
                    SUM(f.amount) AS "Total Amount"
                FROM
                    fee f
                LEFT JOIN
                    member m ON f.student_id = m.student_id
                WHERE
                    f.organization_id = %s
                GROUP BY
                    m.member_name, f.student_id
                HAVING
                    SUM(f.amount) = (
                        SELECT MAX(TotalAmount)
                        FROM (
                            SELECT SUM(amount) AS TotalAmount
                            FROM fee
                            WHERE organization_id = %s AND payment_status = 'Not Paid'
                            GROUP BY student_id
                        ) AS SubQueryMax
                    );
                '''
                cursor.execute(query, (org_id,org_id))

            else:
                self.report_output.delete("1.0", tk.END)
                self.report_output.insert(tk.END, "Report not yet implemented.")
                return 
            
            # Shows stuff in a grid view
            # Get column names from cursor description
            columns = [desc[0] for desc in cursor.description]
            self.report_output['columns'] = columns
            for col in columns:
                self.report_output.heading(col, text=col.replace('_', ' ').title())
                self.report_output.column(col, width=100)
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
    
    # NOTE: members
    def open_membership_management(self):   
        self.member_window = tk.Toplevel(self.root)
        self.member_window.title("Membership Management")
        self.member_window.geometry("1400x600")
        self.member_window.configure(bg="#f0f4f7")

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

        # edit_btn = tk.Button(delete_frame, text="Edit member", font=("Helvetica", 10, "bold"),
        #                     bg="#ffeb3b", fg="#333333", relief="flat", command=self.add_member)
        # edit_btn.pack(side=tk.RIGHT, padx=5)
        
        columns = ("Id", "Name", "Email", "Gender", "Status", "Grad date", "Program", "Unpaid fees", "Org Id", "Membership Batch", "Status", "Role", "Committee")
        column_widths = {
            "Id": 80,           
            "Name": 150,        
            "Email": 150,       
            "Gender": 60,       
            "Enrollment": 80,       
            "Grad date": 100,   
            "Program": 100,     
            "Unpaid fees": 80,
            "Org Id": 80,
            "Membership Batch": 100,
            "Status": 80,
            "Role": 80,
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

        self.load_members()    
    
    def search_member(self):
        student_id = self.member_search_entry.get().strip()
        if not student_id:
            self.load_members()
            return
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.member_tree.get_children():
                self.member_tree.delete(item)                  
            
            query = '''
                SELECT m.student_id, m.member_name, m.email_address, m.gender, m.enrollment_status,
                       m.graduation_date, m.degree_program, m.member_total_unpaid_fees, ms.organization_id,
                       ms.batch_year_of_membership, ms.membership_status, ms.committee_role, ms.committee 
                FROM member m LEFT JOIN member_serves ms ON m.student_id = ms.student_id
                WHERE m.student_id = %s
            '''
            cursor.execute(query, (student_id,))
            
            row = cursor.fetchone()
            if row:
                self.member_tree.insert('', 'end', values=row)
            else:
                messagebox.showinfo("Not Found", "Student not found.")
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def load_members(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.member_tree.get_children():
                self.member_tree.delete(item)                
            query = '''
                SELECT m.student_id, m.member_name, m.email_address, m.gender, m.enrollment_status,
                       m.graduation_date, m.degree_program, m.member_total_unpaid_fees, ms.organization_id,
                       ms.batch_year_of_membership, ms.membership_status, ms.committee_role, ms.committee 
                FROM member m LEFT JOIN member_serves ms ON m.student_id = ms.student_id
            '''
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.member_tree.insert('', 'end', values=row)
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    
    def add_member(self):
        popup = tk.Toplevel(self.member_window)
        popup.title("Add Member")
        popup.geometry("500x600")
        popup.grab_set()

        fields = [
            ("Member Name", "member_name"), # NOTE: done
            ("Email Address", "email_address"), # NOTE: done
            ("Gender", "gender"), # NOTE: done
            ("Enrollment Status", "enrollment_status"), # NOTE: done
            ("Batch", "batch_year_of_enrollment"), # NOTE: done
            ("Graduation Date (YYYY-MM-DD)", "graduation_date"), # NOTE: done
            ("Degree Program", "degree_program"), # NOTE: done
            ("Organization ID", "organization_id"),
            ("Org School Year", "org_school_year"),
            ("Semester", "semester"),   
            ("Batch Year of Membership", "batch_year_of_membership"),
            ("Membership Status", "membership_status"),
            ("Committee Role", "committee_role"),
            ("Committee", "committee"),
        ]
        entries = {}
        for idx, (label, key) in enumerate(fields):
            tk.Label(popup, text=label, font=("Helvetica", 11)).grid(row=idx, column=0, sticky="e", padx=10, pady=8)
            entry = tk.Entry(popup, font=("Helvetica", 11), width=30)
            entry.grid(row=idx, column=1, padx=10, pady=8)
            entries[key] = entry

        def on_submit():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(MAX(student_id), 0) + 1 FROM member")
            next_student_id = cursor.fetchone()[0]
            query = '''
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
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                0,
                %s
            );
            '''
            params = (
                next_student_id,
                data["gender"],
                data["enrollment_status"],
                data["email_address"],
                data["member_name"],
                data["batch_year_of_enrollment"],
                data["degree_program"],
                data["graduation_date"] if data["graduation_date"] else None,
            )
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                messagebox.showinfo("Info", "Added fee successfully!")
                popup.destroy()
                conn.close()
                self.load_fees()    
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            query = '''
                INSERT INTO member_serves (
                    school_year,
                    membership_status,
                    batch_year_of_membership,
                    semester,
                    committee_role,
                    committee,
                    organization_id,
                    student_id
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s, 
                    %s
                );
            '''
            params = (
                data["org_school_year"],
                data["membership_status"],
                data["batch_year_of_membership"],
                data["semester"],
                data["committee_role"] if data["committee_role"] else None,
                data["committee"],
                data["organization_id"],
                data["student_id"] 
            )
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute(query, params)
                cursor.execute("UPDATE organization SET no_of_members = no_of_members + 1 WHERE organization_id = %s;", (data["organization_id"],))
                conn.commit()
                messagebox.showinfo("Info", "Added fee successfully!")
                popup.destroy()
                conn.close()
                self.load_fees()    
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

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
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "DELETE FROM member WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Member deleted successfully.")
                self.load_members() 
            else:
                messagebox.showinfo("Not Found", "Student ID not found.")
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    # NOTE: fee
    def open_fees_management(self):
        self.fee_window = tk.Toplevel(self.root)
        self.fee_window.title("Fees Management")
        self.fee_window.geometry("1200x600")
        self.fee_window.configure(bg="#f0f4f7")

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

        self.load_fees()

    def search_fee(self):
        fee_id = self.fee_search_entry.get().strip()
        if not fee_id:
            self.load_fees()
            return
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.fee_tree.get_children():
                self.fee_tree.delete(item)
            query = '''
                SELECT fee_id, student_id, organization_id, amount, due_date, payment_status, 
                       pay_date, school_year, semester
                FROM fee
                WHERE fee_id = %s
            '''
            cursor.execute(query, (fee_id,))
            
            row = cursor.fetchone()
            if row:
                self.fee_tree.insert('', 'end', values=row)
            else:
                messagebox.showinfo("Not Found", "Fee not found.")
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def load_fees(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.fee_tree.get_children():
                self.fee_tree.delete(item)
            query = '''
                SELECT fee_id, student_id, organization_id, amount, due_date, payment_status, 
                       pay_date, school_year, semester
                FROM fee
            '''
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.fee_tree.insert('', 'end', values=row)
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

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
            query = '''
                INSERT INTO fee (
                    (SELECT COALESCE(MAX(fee_id), 0) + 1 FROM fee),
                    amount,
                    payment_status,
                    due_date,
                    pay_date,
                    school_year,
                    semester,
                    organization_id,
                    student_id
                ) VALUES (
                    1, %s, %s, %s, %s, %s, %s, %s, %s
                );
            '''
            params = (
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
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                messagebox.showinfo("Info", "Added fee successfully!")
                popup.destroy()
                conn.close()
                self.load_fees()    
            except mysql.connector.Error as err:
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
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "DELETE FROM fee WHERE fee_id = %s"
            cursor.execute(query, (fee_id,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Fee deleted successfully.")
                self.load_fees()
            else:
                messagebox.showinfo("Not Found", "Fee ID not found.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    
    def approve_fee(self):
        fee_id = self.approve_entry.get().strip()
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = '''
                UPDATE fee
                SET
                    payment_status = 'Paid',
                    pay_date = CURRENT_DATE()
                WHERE
                    fee_id = %s;
            '''
            cursor.execute(query, (fee_id,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Fee approved successfully.")
                self.load_fees()
            else:
                messagebox.showinfo("Not Found", "Fee ID not found.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    

    # NOTE: orgs
    def open_organization_management(self):
        self.org_window = tk.Toplevel(self.root)
        self.org_window.title("Organization Management")
        self.org_window.geometry("1200x600")
        self.org_window.configure(bg="#f0f4f7")

        tk.Label(self.org_window, text="Organization Management", 
                font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#2a2f45").pack(pady=20)

        search_frame = tk.Frame(self.org_window, bg="#f0f4f7")
        search_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(search_frame, text="Search Organization ID:", 
                font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)
        
        self.org_search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        self.org_search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=("Helvetica", 10, "bold"),
                             bg="#4a90e2", fg="white", relief="flat",
                             command=self.search_organization)
        search_btn.pack(side=tk.LEFT, padx=5)

        # add_btn = tk.Button(search_frame, text="Add Organization", font=("Helvetica", 10, "bold"),
        #                   bg="#4caf50", fg="white", relief="flat",
        #                   command=self.add_organization)        
        # add_btn.pack(side=tk.RIGHT, padx=5)

        # delete_frame = tk.Frame(self.org_window, bg="#f0f4f7")
        # delete_frame.pack(pady=5, padx=10, fill="x")
        # tk.Label(delete_frame, text="Delete Organization ID:", font=("Helvetica", 12), bg="#f0f4f7").pack(side=tk.LEFT)
        # self.org_delete_entry = tk.Entry(delete_frame, font=("Helvetica", 12), width=30)
        # self.org_delete_entry.pack(side=tk.LEFT, padx=5)
        # delete_btn = tk.Button(delete_frame, text="Delete Organization", font=("Helvetica", 10, "bold"),
        #                       bg="#e53935", fg="white", relief="flat", command=self.delete_organization)
        # delete_btn.pack(side=tk.LEFT, padx=5)

        columns = ("Organization ID", "Organization Name", "Organization Type", "No. of Members", "Total Paid Fees", "Total Unpaid Fees")
        column_widths = {
            "Organization ID": 100,
            "Organization Name": 200,
            "Organization Type": 100,
            "No. of Members": 100,
            "Total Paid Fees": 120,
            "Total Unpaid Fees": 120
        }
        
        self.org_tree = ttk.Treeview(self.org_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.org_tree.heading(col, text=col)
            self.org_tree.column(col, width=column_widths[col])

        y_scrollbar = ttk.Scrollbar(self.org_window, orient="vertical", 
                                  command=self.org_tree.yview)
        y_scrollbar.pack(side="right", fill="y")
        
        x_scrollbar = ttk.Scrollbar(self.org_window, orient="horizontal", 
                                  command=self.org_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        
        self.org_tree.configure(yscrollcommand=y_scrollbar.set, 
                              xscrollcommand=x_scrollbar.set)
        
        self.org_tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.load_organizations()    
    
    def search_organization(self):
        org_id = self.org_search_combo.get().strip()
        if not org_id:
            self.load_organizations()
            return
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.org_tree.get_children():
                self.org_tree.delete(item)            
                
            query = '''
                SELECT organization_id, organization_name, organization_type, 
                       no_of_members, total_paid_fees, total_unpaid_fees
                FROM organization
                WHERE organization_id = %s
            '''
            cursor.execute(query, (org_id,))
            
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    self.org_tree.insert('', 'end', values=row)
            else:
                messagebox.showinfo("Not Found", "Organization not found.")
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def load_organizations(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for item in self.org_tree.get_children():
                self.org_tree.delete(item)            
                
            query = '''
                SELECT organization_id, organization_name, organization_type, 
                       no_of_members, total_paid_fees, total_unpaid_fees
                FROM organization
            '''
            cursor.execute(query)
            
            for row in cursor.fetchall():
                self.org_tree.insert('', 'end', values=row)
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def add_organization(self):
        pass

    def delete_organization(self):
        org_id = self.org_delete_entry.get().strip()
        if not org_id:
            messagebox.showwarning("Input Error", "Please enter an Organization ID to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete organization with ID: {org_id}?")
        if not confirm:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "DELETE FROM organization WHERE organization_id = %s"
            cursor.execute(query, (org_id,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Organization deleted successfully.")
                self.load_organizations()
            else:
                messagebox.showinfo("Not Found", "Organization ID not found.")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

if __name__ == "__main__":
    root = tk.Tk()
    app = SOMSApp(root)
    root.mainloop()
