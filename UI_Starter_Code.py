import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FinPayApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("FinPay - Transaction Manager")
        self.geometry("800x600")

        # Configure a consistent style
        style = ttk.Style(self)
        style.theme_use('clam')

        # Container to hold all the screens (frames)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to keep track of the frames
        self.frames = {}

        # Initialize all three screens
        for F in (WelcomeScreen, UploadScreen, DashboardScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all pages in the same location; the one on top will be visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the first screen
        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
        """Brings the specified frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Center content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        lbl_title = ttk.Label(self, text="Welcome to FinPay", font=("Helvetica", 24, "bold"))
        lbl_title.grid(row=1, column=0, pady=10)

        lbl_subtitle = ttk.Label(self, text="Internal Finance Department Portal", font=("Helvetica", 14))
        lbl_subtitle.grid(row=2, column=0, pady=10)

        btn_start = ttk.Button(self, text="Get Started", command=lambda: controller.show_frame("UploadScreen"))
        btn_start.grid(row=3, column=0, sticky="n", pady=20)


class UploadScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Center content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        lbl_header = ttk.Label(self, text="Load Transaction Data", font=("Helvetica", 18, "bold"))
        lbl_header.grid(row=0, column=0, pady=20, sticky="s")

        # Upload Box Area
        upload_frame = ttk.LabelFrame(self, text="File Upload", padding=40)
        upload_frame.grid(row=1, column=0, pady=20)

        lbl_info = ttk.Label(upload_frame, text="Browse to select a file.\nSupported formats: .csv, .json only.")
        lbl_info.pack(pady=10)

        self.lbl_filename = ttk.Label(upload_frame, text="No file selected", foreground="gray")
        self.lbl_filename.pack(pady=5)

        btn_browse = ttk.Button(upload_frame, text="Browse File", command=self.browse_file)
        btn_browse.pack(pady=10)

        # Navigation
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=20)

        btn_back = ttk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("WelcomeScreen"))
        btn_back.grid(row=0, column=0, padx=10)

        # In a real app, this should only enable after a file is selected
        self.btn_load = ttk.Button(btn_frame, text="Load Data",
                                   command=lambda: controller.show_frame("DashboardScreen"))
        self.btn_load.grid(row=0, column=1, padx=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Transaction File",
            filetypes=(("CSV Files", "*.csv"), ("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        if filename:
            self.lbl_filename.config(text=filename.split("/")[-1])  # Show just the file name


class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Top Bar (Filters)
        filter_frame = ttk.Frame(self, padding=10)
        filter_frame.pack(side="top", fill="x")

        ttk.Label(filter_frame, text="Filter by:").pack(side="left", padx=5)

        # Date Filter
        ttk.Label(filter_frame, text="Date:").pack(side="left", padx=5)
        self.cb_date = ttk.Combobox(filter_frame, values=["All", "2026-10-19", "2026-10-18"], state="readonly",
                                    width=12)
        self.cb_date.current(0)
        self.cb_date.pack(side="left", padx=5)

        # Type Filter
        ttk.Label(filter_frame, text="Type:").pack(side="left", padx=5)
        self.cb_type = ttk.Combobox(filter_frame, values=["All", "Credit", "Debit"], state="readonly", width=10)
        self.cb_type.current(0)
        self.cb_type.pack(side="left", padx=5)

        ttk.Button(filter_frame, text="Apply Filters").pack(side="left", padx=15)
        ttk.Button(filter_frame, text="Clear Filters").pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Back to Upload", command=lambda: controller.show_frame("UploadScreen")).pack(
            side="right", padx=5)

        # Main Content Area (Treeview)
        columns = ("City", "Date", "Time", "Type", "Amount")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        # Define headings and column widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Add scrollbar to Treeview
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bottom Bar
        bottom_frame = ttk.Frame(self, padding=10)
        bottom_frame.pack(side="bottom", fill="x")

        ttk.Label(bottom_frame, text="Total Records Loaded: 3").pack(side="left")
        ttk.Button(bottom_frame, text="Export CSV").pack(side="right")

        # Insert dummy data for students to see
        self.insert_dummy_data()

    def insert_dummy_data(self):
        dummy_data = [
            ("Karachi", "2026-10-19", "10:30 AM", "Credit", "+ Rs. 50,000"),
            ("Lahore", "2026-10-19", "11:15 AM", "Debit", "- Rs. 12,000"),
            ("Islamabad", "2026-10-18", "04:45 PM", "Credit", "+ Rs. 8,500")
        ]
        for row in dummy_data:
            self.tree.insert("", tk.END, values=row)


if __name__ == "__main__":
    app = FinPayApp()
    app.mainloop()