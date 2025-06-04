import tkinter as tk
from auth_gui import AuthGUI
from dashboard_gui import DashboardGUI
from database import DB_CONFIG, Database
from utils import Utils

class SOMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Organization Management System")
        self.root.geometry("1000x700")
        self.db = Database(DB_CONFIG)
        self.utils = Utils()

        self.selected_org_id = None # To store the currently selected organization ID

        self.auth_gui = AuthGUI(root, self.db, self.show_dashboard, self.utils)
        self.dashboard_gui = DashboardGUI(root, self.db, self.set_selected_org_id, self.get_selected_org_id, self.utils)
        self.auth_gui.create_sign_in()

    def show_dashboard(self):
        self.dashboard_gui.create_dashboard()

    def set_selected_org_id(self, org_id):
        self.selected_org_id = org_id

    def get_selected_org_id(self):
        return self.selected_org_id

if __name__ == "__main__":
    root = tk.Tk()
    app = SOMSApp(root)
    root.mainloop()