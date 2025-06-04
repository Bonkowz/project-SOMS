import tkinter as tk
from tkinter import ttk, messagebox

class OrganizationGUI:
    def __init__(self, root, db, utils):
        self.root = root
        self.db = db
        self.utils = utils
        self.org_window = tk.Toplevel(self.root)
        self.org_window.title("Organization Management")
        self.org_window.geometry("1200x600")
        self.org_window.configure(bg="#f0f4f7")
        self._create_organization_gui()
        self.load_organizations()

    def _create_organization_gui(self):
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

    def search_organization(self):
        org_id = self.org_search_entry.get().strip() # Changed from combo to entry
        if not org_id:
            self.load_organizations()
            return

        for item in self.org_tree.get_children():
            self.org_tree.delete(item)

        query = '''
            SELECT organization_id, organization_name, organization_type,
                   no_of_members, total_paid_fees, total_unpaid_fees
            FROM organization
            WHERE organization_id = %s
        '''
        rows = self.db.execute_query(query, (org_id,), fetch_type="all")
        if rows:
            for row in rows:
                self.org_tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Not Found", "Organization not found.")

    def load_organizations(self):
        for item in self.org_tree.get_children():
            self.org_tree.delete(item)

        query = '''
            SELECT organization_id, organization_name, organization_type,
                   no_of_members, total_paid_fees, total_unpaid_fees
            FROM organization
        '''
        rows = self.db.execute_query(query, fetch_type="all")
        if rows:
            for row in rows:
                self.org_tree.insert('', 'end', values=row)