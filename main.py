import argparse
import glob
import logging
import os.path
import shutil

from PyPDF2 import PdfReader

from extractors.ing import ExtractorIng
from extractors.traderepublic import ExtractorTradeRepublic

DEBUG = True
DEPOT_PATHS = [("Trade Republic", "Trade Republic", ExtractorTradeRepublic), ("ING-DiBa", "Ing", ExtractorIng)]

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=logging.DEBUG)


def get_pdfs_from_path(src_path: str, file_type: str) -> list:
    if not os.path.isdir(src_path):
        logger.warning("Source path not exists")
        return []
    return glob.glob(f"{src_path}/{file_type}")


def move_pdfs(target_directory: str, pdfs: list):
    if not os.path.isdir(target_directory):
        logger.warning("Target path not exists")
        return

    for pdf_path in pdfs:
        logger.info(f"File:  {os.path.basename(pdf_path)}")
        depot, holding = get_information(pdf_path)

        if not depot or not holding:
            continue

        if not DEBUG:
            target_path = check_and_create_paths(target_directory, depot, holding)
            target_path = os.path.join(target_path, os.path.basename(pdf_path))
            shutil.copy2(pdf_path, target_path)


def check_and_create_paths(target_path: str, depot: str, holding: str):
    full_path = os.path.join(target_path, depot, holding)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def get_depot(pdf_text: str) -> str:
    for search_word, directory_name, _ in DEPOT_PATHS:
        if search_word in pdf_text:
            return directory_name
    return None


def get_holding(pdf_text: str, depot: str) -> str:
    pdf_list = pdf_text.split("\n")
    for _, depot_name, extractor in DEPOT_PATHS:
        if depot == depot_name:
            return extractor().get_holding_name(pdf_list)


def get_information(pdf_path: str):
    pdf_text = extract_information(pdf_path)
    depot = get_depot(pdf_text)
    holding = get_holding(pdf_text, depot)
    logger.info(f"Depot: {depot} / Holding: {holding}")
    return depot, holding


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        pdf_text = pdf.pages[0].extract_text()

    return pdf_text


def main():
    parser = argparse.ArgumentParser(description="Sort and copy")
    parser.add_argument("src_path", type=str)
    parser.add_argument("target_path", type=str)

    args = parser.parse_args()
    src_path = args.src_path
    target_path = args.target_path

    pdfs = get_pdfs_from_path(src_path, "*.pdf")
    move_pdfs(target_path, pdfs)


if __name__ == '__main__':
    main()
