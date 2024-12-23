import subprocess
import tempfile
from os import chdir, path
import pkg_resources
import pathlib
import tkinter as tk
from tkinter import filedialog

class DocPipe(object):
    """a class to do document conversions"""

    def pdf(self, markdown_file, bibliography, output_name, output_directory):
        """Make PDF file using markdown and the included latex template
        
        Args:
            markdown_file: the file that has your written material.
            bibliography: the bibtex formatted file for biblography.
            output_name: the name prefix for the outputted file
            output_directory: the directory where the pdf is saved
        """
        full_md_path = pathlib.Path(markdown_file).resolve()
        full_bib_path = pathlib.Path(bibliography).resolve()
        if not output_directory:
            output_directory = selectSaveLocation()
        out_dir_path = pathlib.Path(output_directory).resolve()
            
        with tempfile.TemporaryDirectory() as temp_dir:
            chdir(temp_dir)
            style_path = path.join(temp_dir, 'style.sty')
            with pkg_resources.resource_stream(__name__, 'style.sty') as f:
                with open(style_path, 'w') as f2:
                    f2.write(f.read().decode('utf-8'))
            copy(full_md_path, temp_dir)
            copy(full_bib_path, temp_dir)
            _generate_pdf(markdown_file, bibliography, output_name)
            filename = output_name + ".pdf"
            saveLocation = out_dir_path
            copy(filename, saveLocation)

    def pdf_help(self):
        """Get Help for PDF files"""
        msg = """Make PDF file using markdown and the included latex template
        
        Args:
            markdown_file: the file that has your written material.
            bibliography: the bibtex formatted file for biblography.
            output_name: the name prefix for the outputted file
            output_directory: the directory where the pdf is saved
        
        Notes:
            The markdown file should use \citet or \citep for  embedded citations
        """

def copy(srcFile, dest):
    subprocess.run(["cp",srcFile, dest], check=True)

def _generate_pdf(markdown_file, bibtex_file, output_filename):
    """
    Generates PDF files from Markdown text, BibTeX, and CSL files using pandoc and latex packages.

    Args:
        markdown_text (str): The Markdown text content.
        bibtex_file (str): Path to the BibTeX file.
        output_filename (str): Base filename for the output files (without extension).
    """

    try:
        subprocess.run([
            "pandoc",
            "-o", f"{output_filename}.tex", 
            markdown_file,
            "--include-in-header", "style.sty",
            "--bibliography", bibtex_file, 
            "--natbib",
        ], check=True)

        subprocess.run([
            "pdflatex", f"{output_filename}.tex"
        ], check=True)

        subprocess.run([
            "bibtex", output_filename
        ], check=True)

        subprocess.run([
            "pdflatex", f"{output_filename}.tex"
        ], check=True)

        subprocess.run([
            "pdflatex", f"{output_filename}.tex"
        ], check=True)

    except Exception as e:
        print(f"Error generating documents: {e}")

def selectSaveLocation() -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory()
    if folder_path:
        return folder_path
    else:
        return path.expanduser("~/Downloads")



