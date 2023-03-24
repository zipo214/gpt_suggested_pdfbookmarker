import os
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz


# Define the PDF and TOC classes
class Chapter:
    def __init__(self, title, page):
        self.title = title
        self.page = page


class TOC:
    def __init__(self, chapters):
        self.chapters = chapters

    def __iter__(self):
        return iter(self.chapters)


# Define the UI elements
class FileChooser:
    def __init__(self):
        self.file_path = None

    def choose_file(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Choose a PDF file"
        )


class ChapterList:
    def __init__(self, chapters):
        self.chapters = chapters
        self.selected_chapters = []

    def select_chapter(self, index):
        self.selected_chapters.append(self.chapters[index])

    def deselect_chapter(self, index):
        self.selected_chapters.remove(self.chapters[index])


class HelpSection:
    def __init__(self, content):
        self.content = content

    def display(self):
        messagebox.showinfo("Help", self.content)


# Define the PDF bookmarking functions
def read_pdf(pdf_path, password=None):
    with fitz.open(pdf_path, password=password) as doc:
        return doc.page_count


def read_toc(pdf_path, password=None):
    with fitz.open(pdf_path, password=password) as doc:
        toc = []
        for toc_item in doc.get_toc():
            toc.append(Chapter(toc_item[1], toc_item[0]))
        return TOC(toc)


def create_bookmarks(pdf_path, toc, selected_chapters, custom_titles):
    bookmarks = []
    for i, chapter in enumerate(toc):
        if chapter in selected_chapters:
            if i < len(custom_titles):
                title = custom_titles[i]
            else:
                title = chapter.title
            bookmark = (title, chapter.page)
            bookmarks.append(bookmark)
    return bookmarks


def write_bookmarks(pdf_path, bookmarks):
    with fitz.open(pdf_path) as doc:
        for i in range(doc.page_count):
            if i == bookmarks[0][1] - 1:
                toc_dest = doc.add_destination(
                    bookmarks[0][0], fitz.Rect(0, 0, 0, 0), i
                )
                bookmarks.pop(0)
                if not bookmarks:
                    break
        doc.save(pdf_path, garbage=4)


# Define the main UI
class MainWindow:
    def __init__(self):
        self.file_chooser = FileChooser()
        self.chapter_list = None
        self.help_section = HelpSection(
            "To use this application, select a PDF file and its table of contents.\n"
            "You can then select which chapters to bookmark and specify custom bookmark titles"
        )

    def run(self):
        # Choose the PDF file
        self.file_chooser.choose_file()
        if not self.file_chooser.file_path:
            return

        # Get the PDF password (if any)
        password = None
        if fitz.has_pdf_load_pdftotext():
            with open(self.file_chooser.file_path, "rb") as f:
                if fitz.PDFximage().extract_text(f, password="") is None:
                    password = messagebox.askstring(
                        "Password Required",
                        "Enter the password for this PDF file (if any):",
                        show="

# Define the main UI
class MainWindow:
    def __init__(self):
        # Initialize the file chooser
        self.file_chooser = FileChooser()

        # Initialize the TOC selector
        self.toc_selector = None
        self.custom_titles_entry = None

        # Initialize the chapter list
        self.chapter_list = None

        # Initialize the help section
        self.help_section = HelpSection(
            "To use this application, select a PDF file and its table of contents.\n"
            "You can then select which chapters to bookmark and specify custom bookmark titles."
            "Welcome to PDF Bookmarker!"

            "This application allows you to create bookmarks in a PDF file based on a table of contents file."

            "To use this application, follow these steps:"

            "1. Click on the ""Choose PDF file"" button and select the PDF file that you want to add bookmarks to."

            "2. Click on the ""Choose TOC file"" button and select the table of contents file for the PDF file. The table of contents file should be in the form of bookmarks, with each bookmark representing a chapter or section in the PDF file."

            "3. Select the chapters that you want to add bookmarks to. You can select all chapters by clicking on the ""Select All"" option in the Edit menu, or select individual chapters by clicking on them in the chapter list."

            "4. If you want to customize the bookmark titles, enter the custom titles in the ""Custom titles"" section. Each title should be on a separate line."

            "5. Click on the ""Create bookmarks"" button to create the bookmarks in the PDF file."

            "6. The bookmarks should now be visible in the PDF file. You can test them by clicking on them in the bookmark pane."

            "If you have any questions or encounter any issues, please consult the documentation or contact customer support."

        )

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("PDF Bookmarker")

        # Add a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add a File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open PDF", command=self.choose_pdf_file)
        self.file_menu.add_command(label="Open TOC", command=self.choose_toc_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_application)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add a Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Select All", command=self.select_all_chapters)
        self.edit_menu.add_command(label="Deselect All", command=self.deselect_all_chapters)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Add a Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Add a Choose PDF button
        self.choose_pdf_button = tk.Button(
            self.root,
            text="Choose PDF file",
            command=self.choose_pdf_file,
            font=("Arial", 14)
        )
        self.choose_pdf_button.pack(pady=10)

        # Add a Choose TOC button
        self.choose_toc_button = tk.Button(
            self.root,
            text="Choose TOC file",
            command=self.choose_toc_file,
            font=("Arial", 14)
        )
        self.choose_toc_button.pack(pady=10)

        # Add a Select Chapters section
        self.select_chapters_label = tk.Label(
            self.root,
            text="Select chapters:",
            font=("Arial", 16)
        )
        self.select_chapters_label.pack()

        self.chapter_listbox = tk.Listbox(
            self.root,
            selectmode=tk.MULTIPLE,
            font=("Arial", 14)
        )
        self.chapter_listbox.pack()

        # Add a Custom Titles section
        self.custom_titles_label = tk.Label(
            self.root,
            text="Custom titles:",
            font=("Arial", 16)
        )
        self.custom_titles_label.pack()

        self.custom_titles_entry = tk.Entry(
            self.root,
            font=("Arial", 14)
        )
        self.custom_titles_entry.pack()

        # Add a Create Bookmarks button
        self.create_bookmarks_button = tk.Button(
            self.root,
            text="Create bookmarks",
            command=self.create_bookmarks,
            font=("Arial", 14)
        )
        self.create_bookmarks_button.pack(pady=10)

    def choose_pdf_file(self):
        self.file_chooser.choose_file()
        if self.file_chooser
                if not self.file_chooser.file_path:
            return

        # Get the PDF password (if any)
        password = None
        if fitz.has_pdf_load_pdftotext():
            with open(self.file_chooser.file_path, "rb") as f:
                if fitz.PDFximage().extract_text(f, password="") is None:
                    password = messagebox.askstring(
                        "Password Required",
                        "Enter the password for this PDF file (if any):",
                        show="*"
                    )

        # Read the PDF and TOC
        try:
            pdf_pages = read_pdf(self.file_chooser.file_path, password)
            toc = read_toc(self.toc_selector.file_path, password)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to read PDF or TOC: {e}"
            )
            return

        # Get the selected chapters and custom titles
        selected_chapters = self.chapter_list.selected_chapters
        custom_titles = self.custom_titles_entry.get().split(",")

        # Create the bookmarks
        bookmarks = create_bookmarks(
            self.file_chooser.file_path,
            toc,
            selected_chapters,
            custom_titles
        )

        # Write the bookmarks to the PDF
        try:
            write_bookmarks(self.file_chooser.file_path, bookmarks)
            messagebox.showinfo(
                "Success",
                "Bookmarks created successfully!"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to create bookmarks: {e}"
            )

    def run(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("PDF Bookmarker")

        # Add a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add a File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open PDF", command=self.choose_pdf_file)
        self.file_menu.add_command(label="Open TOC", command=self.choose_toc_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_application)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add a Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Select All", command=self.select_all_chapters)
        self.edit_menu.add_command(label="Deselect All", command=self.deselect_all_chapters)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Add a Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Add a Choose PDF button
        self.choose_pdf_button = tk.Button(
            self.root,
            text="Choose PDF file",
            command=self.choose_pdf_file,
            font=("Arial", 14)
        )
        self.choose_pdf_button.pack(pady=10)

        # Add a Choose TOC button
        self.choose_toc_button = tk.Button(
            self.root,
            text="Choose TOC file",
            command=self.choose_toc_file,
            font=("Arial", 14)
        )
        self.choose_toc_button.pack(pady=10)

        # Add a Select Chapters section
        self.select_chapters_label = tk.Label(
            self.root,
            text="Select
    def choose_toc_file(self):
        self.file_chooser.choose_file()
        if self.file_chooser.file_path:
            toc = read_toc(self.file_chooser.file_path, password=self.password)
            self.toc_selector = TOCSelector(self.root, toc)
            self.chapter_list = ChapterList(toc)
            self.custom_titles_entry.delete(0, tk.END)
            for i in range(len(toc)):
                self.chapter_listbox.insert(tk.END, toc.chapters[i].title)

    def select_all_chapters(self):
        self.selected_chapters = []
        for i in range(len(self.chapter_list.chapters)):
            self.chapter_listbox.select_set(i)
            self.chapter_list.select_chapter(i)
        self.selected_chapters = self.chapter_list.selected_chapters

    def deselect_all_chapters(self):
        self.selected_chapters = []
        for i in range(len(self.chapter_list.chapters)):
            self.chapter_listbox.select_clear(i)
            self.chapter_list.deselect_chapter(i)
        self.selected_chapters = self.chapter_list.selected_chapters

    def show_help(self):
        self.help_section.display()

    def create_bookmarks(self):
        if not self.file_chooser.file_path:
            messagebox.showerror("Error", "Please choose a PDF file.")
            return

        if not self.toc_selector:
            messagebox.showerror("Error", "Please choose a table of contents file.")
            return

        custom_titles = self.custom_titles_entry.get().splitlines()
        bookmarks = create_bookmarks(
            self.file_chooser.file_path,
            self.chapter_list.chapters,
            self.selected_chapters,
            custom_titles
        )

        write_bookmarks(self.file_chooser.file_path, bookmarks)

        messagebox.showinfo("Success", "Bookmarks created successfully.")

    def exit_application(self):
        self.root.destroy()

    def run(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("PDF Bookmarker")

        # Add a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add a File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open PDF", command=self.choose_pdf_file)
        self.file_menu.add_command(label="Open TOC", command=self.choose_toc_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_application)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add a Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Select All", command=self.select_all_chapters)
        self.edit_menu.add_command(label="Deselect All", command=self.deselect_all_chapters)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Add a Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Add a Choose PDF button
        self.choose_pdf_button = tk.Button(
            self.root,
            text="Choose PDF file",
            command=self.choose_pdf_file,
            font=("Arial", 14)
        )
        self.choose_pdf_button.pack(pady=10)

        # Add a Choose TOC button
        self.choose_toc_button = tk.Button(
            self.root,
            text="Choose TOC file",
            command=self.choose_toc_file,
            font=("Arial", 14)
        )
        self.choose_toc_button.pack(pady=10)

        # Add a Password Entry section
            self.password_label = tk.Label(
                self.root,
                text="Password:",
                font=("Arial", 16)
            )
            self.password_label.pack()

            self.password_entry = tk.Entry(
                self.root,
                show="*",
                font=("Arial", 14)
            )
            self.password_entry.pack()

            # Add a Select Chapters section
            self.select_chapters_label = tk.Label(
                self.root,
                text="Select chapters:",
                font=("Arial", 16)
            )
            self.select_chapters_label.pack()

            self.chapter_listbox = tk.Listbox(
                self.root,
                selectmode=tk.MULTIPLE,
                font=("Arial", 14)
            )
            self.chapter_listbox.pack()

        # Add a Custom Titles section
        self.custom_titles_label = tk.Label(
        self.root,
        text="Custom titles:",
        font=("Arial", 16)
        )
        self.custom_titles_label.pack()

        self.custom_titles_entry = tk.Entry(
        self.root,
        font=("Arial", 14)
        )
        self.custom_titles_entry.pack()

        # Add a Create Bookmarks button
        self.create_bookmarks_button = tk.Button(
        self.root,
        text="Create bookmarks",
        command=self.create_bookmarks,
        font=("Arial", 14)
        )
        self.create_bookmarks_button.pack(pady=10)

        # Run the main loop
        self.root.mainloop()
        
        #Define the entry point for the application
        if name == "main":
        app= MainWindow()
        app.run()
        
