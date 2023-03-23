import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox


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
def read_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        return reader.getNumPages()

def read_toc(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        toc_page = reader.getOutline()[0].page
        toc_reader = PyPDF2.PdfFileReader(f)
        toc_reader.decrypt('')
        toc_reader.setPageMode('/UseOutlines')
        toc_reader.setPageLayout('/SinglePage')
        toc_reader.setPageMode('/UseOutlines')
        toc_reader.setPage(toc_page - 1)
        toc = []
        for line in toc_reader.outlines:
            toc.append(Chapter(line.title, line.dest[0].objid + 1))
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
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        writer = PyPDF2.PdfFileWriter()
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))
            if i == bookmarks[0][1] - 1:
                toc = writer.addBookmark(
                    bookmarks[0][0],
                    bookmarks[0][1] - 1,
                )
                bookmarks.pop(0)
                if not bookmarks:
                    break
        with open(pdf_path, 'wb') as f:
            writer.write(f)

# Define the main UI
class MainWindow:
    def __init__(self):
        self.file_chooser = FileChooser()
        self.chapter_list = None
        self.help_section = HelpSection(
            "To use this application, select a PDF file and its table of contents.\n"
            "You can then select which chapters to bookmark and specify custom bookmark titles
