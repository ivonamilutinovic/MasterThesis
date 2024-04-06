import csv
import os

from io import BytesIO

from PyPDF2 import PdfReader

from src.backend.utils.log import get_logger

LOGGER = get_logger(__name__)


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


def remove_file(file_to_delete: str) -> None:
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        LOGGER.debug(f"File {file_to_delete} has been successfully deleted.")
    else:
        LOGGER.debug(f"File {file_to_delete} does not exist.")
