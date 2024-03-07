import csv
import os
from contextlib import suppress
from io import BytesIO

from PyPDF2 import PdfReader


def create_subfolders_to(filename: str):
    """
        Creating (sub)folders to provided filename (path) argument.

        Check if filename argument has actual file name in itself (if filename has any extension in itself, then passed
        filename argument has actual file name in itself) ---> create all folders that are above that actual file
        name in provided path.
        Otherwise, filename argument is actually (sub)folders structure that needs to be created if it doesn't exist.
    """

    with suppress(FileNotFoundError):
        if not os.path.splitext(filename)[1]:
            os.makedirs(os.path.normpath(filename), exist_ok=True)
        else:
            os.makedirs(os.path.dirname(os.path.normpath(filename)), exist_ok=True)


def pdf_to_csv(pdf_content: bytes, csv_file: str) -> None:
    # Wrapping the pdf_content bytes object in BytesIO to make it seekable
    pdf_stream = BytesIO(pdf_content)

    # Opening the PDF file
    pdf_reader = PdfReader(pdf_stream)

    # Creating a CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Reading each page of the PDF and writing to CSV
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Splitting the text into lines
            lines = text.split('\n')

            # Writing each line to CSV
            for line in lines:
                writer.writerow([line])
