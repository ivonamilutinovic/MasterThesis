import os

import tabula

from train_wiser.backend.utils.log import get_logger

LOGGER = get_logger(__name__)


def pdf_to_csv(pdf_path: str, csv_path: str) -> None:
    return tabula.convert_into(pdf_path, csv_path, pages='all', output_format='csv', silent=True)


def remove_file(file_to_delete: str) -> None:
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        LOGGER.debug(f"File {file_to_delete} has been successfully deleted.")
    else:
        LOGGER.debug(f"File {file_to_delete} does not exist.")
