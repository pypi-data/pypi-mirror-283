import tkinter
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Canvas
import sv_ttk
import threading
import os
import subprocess
import json
from pdf_crawler.report_generator import ReportGenerator
from pdf_crawler.selenium_crawler import SeleniumCrawler
#from report_generator import ReportGenerator
#from selenium_crawler import SeleniumCrawler

class UI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.path_mapping = {}
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_ui()
        sv_ttk.set_theme("dark")
        self.center_window(self.root)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        self.root.title("Volume II Generator")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        tabControl = ttk.Notebook(self.root)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        tabControl.add(tab1, text="Crawler + Report Generator")
        tabControl.add(tab2, text="Report Generator")
        tabControl.add(tab3, text="Downloaded Reports")

        self.crawler_and_pdf_generator_tab(tab1)
        self.pdf_generator_tab(tab2)
        self.downloaded_reports_tab(tab3)

        tabControl.pack(fill=tkinter.BOTH, expand=True)

    def crawler_and_pdf_generator_tab(self, tab):
        content_frame = ttk.Frame(tab)
        content_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.create_buttons(tab)

        self.create_console(tab, content_frame)

        text_box = ttk.Entry(content_frame)
        text_box.grid(column=0, row=2, padx=(10, 5), pady=(5, 10), ipady=5, sticky="ew")

        self.crawler_submit_button = ttk.Button(content_frame, text="Submit Link", width=15, command=lambda: self.validate_and_submit_link(tab, text_box.get()))
        self.crawler_submit_button.grid(column=1, row=2, padx=(10, 0), pady=(5, 10), ipady=5, sticky="e")

        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_rowconfigure(2, weight=0)

    def validate_and_submit_link(self, tab, link):
        if link.startswith("http://committees.parliament.uk") or link.startswith("https://committees.parliament.uk"):

            self.crawler_submit_button.config(state=tkinter.DISABLED)
            thread = threading.Thread(target=self.run_crawler_and_pdf_generator, args=(tab, link))
            thread.start()
        else:
            messagebox.showerror("Invalid Link", "Please enter a valid URL")

    def run_crawler_and_pdf_generator(self, tab, link):
        try:
                s_crawler = SeleniumCrawler(link, tab.console_text)
                s_crawler.crawl()
        finally:
            self.crawler_submit_button.config(state=tkinter.NORMAL)

    def pdf_generator_tab(self, tab):
        content_frame = ttk.Frame(tab)
        content_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.create_buttons(tab)

        self.create_console(tab, content_frame)

        ttk.Label(content_frame, text="Select folder containing Witness Evidence:").grid(column=0, row=1, padx=10, pady=(10, 5), sticky="w")
        ttk.Label(content_frame, text="Select folder containing Published Written Evidence:").grid(column=0, row=2, padx=10, pady=(10, 5), sticky="w")
        ttk.Label(content_frame, text="Select folder containing the full report:").grid(column=0, row=3, padx=10, pady=(10, 5), sticky="w")

        self.folder_path_witness = tkinter.StringVar(value="Browse...")
        browse_button_witness = ttk.Button(content_frame, textvariable=self.folder_path_witness, command=lambda: self.browse_folder(self.folder_path_witness, 'folder_path_witness'))
        browse_button_witness.grid(column=1, row=1, padx=(10, 5), pady=(10, 5), sticky="w")

        self.folder_path_published = tkinter.StringVar(value="Browse...")
        browse_button_published = ttk.Button(content_frame, textvariable=self.folder_path_published, command=lambda: self.browse_folder(self.folder_path_published, 'folder_path_published'))
        browse_button_published.grid(column=1, row=2, padx=(10, 5), pady=(10, 5), sticky="w")

        self.folder_path_report = tkinter.StringVar(value="Browse...")
        browse_button_report = ttk.Button(content_frame, textvariable=self.folder_path_report, command=lambda: self.browse_file(self.folder_path_report, 'folder_path_report'))
        browse_button_report.grid(column=1, row=3, padx=(10, 5), pady=(10, 5), sticky="w")

        self.report_submit_button = ttk.Button(content_frame, text="Submit", command=lambda: self.submit_folders(tab), width=20)
        self.report_submit_button.grid(column=1, row=4, columnspan=3, padx=(10, 5), pady=(5, 10), sticky="w")

        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_rowconfigure(3, weight=0)
        content_frame.grid_rowconfigure(4, weight=0)

    def truncate_path(self, path, max_length=28):
        if len(path) > max_length:
            return '...' + path[-max_length:]
        return path

    def browse_folder(self, folder_path_var, folder_key):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            truncated_path = self.truncate_path(folder_selected)
            folder_path_var.set(truncated_path)
            self.path_mapping[folder_key] = folder_selected

    def browse_file(self, file_path_var, file_key):
        file_selected = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_selected:
            truncated_path = self.truncate_path(file_selected)
            file_path_var.set(truncated_path)
            self.path_mapping[file_key] = file_selected

    def submit_folders(self, tab):
        witness_evidence_folder = self.path_mapping.get('folder_path_witness', '')
        published_evidence_folder = self.path_mapping.get('folder_path_published', '')
        report_pdf = self.path_mapping.get('folder_path_report', '')

        if (witness_evidence_folder and published_evidence_folder and report_pdf):
            self.report_submit_button.config(state=tkinter.DISABLED)
            thread = threading.Thread(target=self.run_pdf_processor, args=(report_pdf, published_evidence_folder, witness_evidence_folder, tab))
            thread.start()
        else:
            messagebox.showerror("Error", "Please select all required folders and report file")
            return

    def run_pdf_processor(self, report_pdf, published_evidence_folder, witness_evidence_folder, tab):
        try:
            report_generator = ReportGenerator(report_pdf, published_evidence_folder, witness_evidence_folder, tab.console_text)
            report_generator.create_report()
            messagebox.showinfo("Success", "PDF Processing Completed Successfully")
        finally:
            self.report_submit_button.config(state=tkinter.NORMAL)

    def create_console(self, tab, frame):
        console_text = scrolledtext.ScrolledText(frame, wrap=tkinter.WORD)
        console_text.grid(column=0, row=0, columnspan=3, padx=(10, 0), pady=(10, 5), sticky="nsew")
        console_text.configure(state='disabled')
        tab.console_text = console_text

    def create_buttons(self, tab):
        button_frame = ttk.Frame(tab)
        button_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        button1 = ttk.Button(button_frame, text="File Explorer", width=20, command=self.open_file_explorer)
        button1.pack(pady=10, padx=10, ipady=10)

    def open_file_explorer(self):
        current_dir = os.getcwd()
        if os.name == 'nt':
            subprocess.Popen(f'explorer "{current_dir}"')
        elif os.name == 'posix':
            subprocess.Popen(['open', current_dir])

    def downloaded_reports_tab(self, tab):
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill=tkinter.X, padx=10, pady=10)

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tkinter.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

        self.search_entry.bind("<Return>", lambda event: self.refresh_downloaded_reports())

        self.refresh_reports_button = ttk.Button(search_frame, text="Refresh", command=self.refresh_downloaded_reports)
        self.refresh_reports_button.pack(side=tkinter.LEFT, padx=(5, 0))

        canvas = Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_downloaded_reports()

    def refresh_downloaded_reports(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        search_query = self.search_entry.get().lower()

        json_file_path = os.path.join(self.current_dir, 'data', 'downloaded_reports.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                for link, description in data.items():
                    if search_query in description.lower():
                        frame = ttk.Frame(self.scrollable_frame)
                        frame.pack(fill=tkinter.X, padx=10, pady=5)
                        label = ttk.Label(frame, text=description, anchor="w")

                        label.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

                        label.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=(0, 10))

                        delete_button = ttk.Button(frame, text="Delete", command=lambda l=link: self.delete_link(l))
                        delete_button.pack(side=tkinter.RIGHT)

    def delete_link(self, link):
        json_file_path = os.path.join(self.current_dir, 'data', 'downloaded_reports.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            if link in data:
                del data[link]
                with open(json_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                self.refresh_downloaded_reports()
                messagebox.showinfo("Success", "Link deleted successfully.")
            else:
                messagebox.showerror("Error", "Link not found.")

    def log_message(self, tab, message):
        tab.log_text.configure(state='normal')
        tab.log_text.insert(tkinter.END, message + "\n")
        tab.log_text.configure(state='disabled')
        tab.log_text.see(tkinter.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.run()
