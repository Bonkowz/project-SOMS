import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from members_gui import MembersGUI
from fees_gui import FeesGUI
from organization_gui import OrganizationGUI

class DashboardGUI:
    def __init__(self, root, db, set_selected_org_id_callback, get_selected_org_id_callback, utils):
        self.root = root
        self.db = db
        self.set_selected_org_id = set_selected_org_id_callback
        self.get_selected_org_id = get_selected_org_id_callback
        self.utils = utils
        self.organizations_map = {} # To store org_name: org_id mapping

    def create_dashboard(self):
        self.utils.clear_widgets(self.root)
        self.root.configure(bg="#f0f4f7")

        tk.Label(self.root, text="Organization Dashboard", font=("Helvetica", 24, "bold"),
                bg="#f0f4f7", fg="#2a2f45").pack(pady=20)

        search_frame = tk.Frame(self.root, bg="#f0f4f7")
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Select Organization:", font=("Helvetica", 12),
                bg="#f0f4f7").pack(side=tk.LEFT)

        self.organizations_map = self.db.fetch_organizations_for_combo()
        organizations = list(self.organizations_map.keys())
        self.org_search_combo = ttk.Combobox(search_frame, font=("Helvetica", 12), width=30, state="readonly")
        self.org_search_combo['values'] = organizations
        self.org_search_combo.pack(side=tk.LEFT, padx=5)
        self.org_search_combo.bind('<<ComboboxSelected>>', lambda e: self.display_selected_organization())

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

        action_frame = tk.Frame(self.root, bg="#f0f4f7")
        action_frame.pack(pady=15)
        
        btn1 = tk.Button(action_frame, text="Membership Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_membership_management)
        btn1.pack(side=tk.LEFT, padx=10)
        self.utils.add_hover_effect(btn1, "#4caf50", "#45a049")

        btn2 = tk.Button(action_frame, text="Fees Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_fees_management)
        btn2.pack(side=tk.LEFT, padx=10)
        self.utils.add_hover_effect(btn2, "#4caf50", "#45a049")

        btn3 = tk.Button(action_frame, text="Organization Management", width=25, font=("Helvetica", 10, "bold"),
                        bg="#4caf50", fg="white", relief="flat", command=self.open_organization_management)
        btn3.pack(side=tk.LEFT, padx=10)
        self.utils.add_hover_effect(btn3, "#4caf50", "#45a049")

        self.report_frame = tk.LabelFrame(self.root, text="Generate Reports", font=("Helvetica", 12, "bold"),
                                        bg="#ffffff", padx=10, pady=10)
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.report_dropdown = ttk.Combobox(self.report_frame, width=90, state="readonly", font=("Helvetica", 10))
        self.report_dropdown['values'] = [
            "1. Members by Role, Status, Gender, Degree, etc.",
            "2. Members with Unpaid Fees (Semester + SY)",
            "3. Member's Unpaid Fees (All Orgs)",
            "4. Executive Committee Members (By Year)",
            "5. Presidents Per Year (Reverse Chronological)",
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
        self.utils.add_hover_effect(gen_report_btn, "#2196f3", "#1976d2")
        
        self.report_output = ttk.Treeview(self.report_frame, height=15, show="headings")
        self.report_output.pack(fill="both", expand=True, pady=5)

        y_scrollbar = ttk.Scrollbar(self.report_frame, orient="vertical", command=self.report_output.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(self.report_frame, orient="horizontal", command=self.report_output.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        self.report_output.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    def display_selected_organization(self):
        org_name = self.org_search_combo.get()
        org_id = self.organizations_map.get(org_name)
        self.set_selected_org_id(org_id)

        result = self.db.get_organization_info(org_name)
        if result:
            org_id, name, org_type, members = result
            self.org_labels["Name"].config(text=f"Name: {name}")
            self.org_labels["Type"].config(text=f"Type: {org_type}")
            self.org_labels["Members"].config(text=f"Members: {members}")
            self.org_labels["ID"].config(text=f"ID: {org_id}")
        else:
            messagebox.showinfo("Not Found", "Organization not found.")

    def generate_report(self):
        index = self.report_dropdown.current()
        org_id = self.get_selected_org_id()

        if org_id is None and index not in [2]:  # Query 3 doesn't use org_id
            messagebox.showerror("Error", "Please select an organization first.")
            return

        if index == -1:
            messagebox.showerror("Error", "Please select a report first.")
            return

        query = ""
        params = []
        
        if index == 0:
            query = '''
                SELECT m.student_id, m.member_name, s.committee_role, s.membership_status, m.gender, m.degree_program,
                    s.batch_year_of_membership, s.committee
                FROM member_serves s
                INNER JOIN member m ON m.student_id = s.student_id
                WHERE s.organization_id = %s
            '''
            params = (org_id,)

        elif index == 1:
            school_year = simpledialog.askstring("Input", "Enter School Year (e.g., 2023):")
            semester = simpledialog.askstring("Input", "Enter Semester (e.g., 1):")
            if not school_year or not semester: return
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
            params = (org_id, school_year, semester)

        elif index == 2:
            student_id = simpledialog.askstring("Input", "Enter Student ID:")
            if not student_id: return
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
            params = (student_id,)

        elif index == 3:
            school_year = simpledialog.askstring("Input", "Enter School Year:")
            if not school_year: return
            query = '''
                SELECT m.member_name, s.committee_role, s.school_year
                FROM member_serves s
                INNER JOIN member m ON s.student_id = m.student_id
                WHERE s.committee_role != 'Member'
                AND s.organization_id = %s
                AND s.school_year = %s
            '''
            params = (org_id, school_year)

        elif index == 4:
            query = '''
                SELECT m.member_name, s.committee_role, s.school_year
                FROM member_serves s
                INNER JOIN member m ON s.student_id = m.student_id
                WHERE s.committee_role = 'President'
                AND s.organization_id = %s
                ORDER BY s.school_year DESC
            '''
            params = (org_id,)

        elif index == 5:
            school_year = simpledialog.askstring("Input", "Enter School Year:")
            semester = simpledialog.askstring("Input", "Enter Semester:")
            if not school_year or not semester: return
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
            params = (org_id, school_year, semester)

        elif index == 6:
            query = '''
                SELECT
                    COUNT(CASE WHEN membership_status = 'Active' THEN 1 END)/COUNT(*) AS '%Active',
                    COUNT(CASE WHEN membership_status = 'Inactive' THEN 1 END)/COUNT(*) AS '%Inactive'
                FROM member_serves ms
                LEFT JOIN organization org ON ms.organization_id = org.organization_id
                WHERE ms.organization_id = %s
            '''
            params = (org_id,)

        elif index == 7:
            query = '''
                SELECT member_name, enrollment_status, graduation_date
                FROM member m
                LEFT JOIN member_serves ms ON m.student_id = ms.student_id
                WHERE organization_id = %s
                AND enrollment_status = 'Graduated'
                AND graduation_date >= DATE_SUB(CURRENT_DATE(), INTERVAL (20 * 6) MONTH)
            '''
            params = (org_id,)

        elif index == 8:
            date = simpledialog.askstring("Input", "Enter the date in the format (YYYY-MM-DD):")
            if not date: return
            query = '''
                SELECT SUM(amount) AS "Total Amount", payment_status
                FROM fee f
                LEFT JOIN organization o ON f.organization_id = o.organization_id
                WHERE f.organization_id = %s
                AND due_date > DATE(%s)
                AND COALESCE(pay_date > DATE(%s), 1)
                GROUP BY f.payment_status
            '''
            params = (org_id, date, date)

        elif index == 9:
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
            params = (org_id, org_id)
        else:
            messagebox.showerror("Error", "Report not yet implemented.")
            return

        conn = self.db.connect()
        if conn is None: return

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            for item in self.report_output.get_children():
                self.report_output.delete(item)

            self.report_output['columns'] = columns
            for col in columns:
                self.report_output.heading(col, text=col.replace('_', ' ').title())
                self.report_output.column(col, width=100)

            if not rows:
                messagebox.showinfo("Report", "No results found.")
            else:
                for row in rows:
                    self.report_output.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()

    def open_membership_management(self):
        MembersGUI(self.root, self.db, self.get_selected_org_id(), self.utils)

    def open_fees_management(self):
        FeesGUI(self.root, self.db, self.utils)

    def open_organization_management(self):
        OrganizationGUI(self.root, self.db, self.utils)