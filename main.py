import argparse
import datetime
import glob
import logging
import os.path
import shutil

from PyPDF2 import PdfReader

from extractors.traderepublic import ExtractorTradeRepublic

DEBUG = True
DEPOT_PATHS = [("Trade Republic", "Trade Republic")]

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

    start_time = datetime.datetime.now()
    processed_pdfs = 0

    for pdf_path in pdfs:
        processed_pdfs += 1
        logger.info(f"File:  {os.path.basename(pdf_path)}")
        depot, holding = get_information(pdf_path)

        if not DEBUG:
            target_path = check_and_create_paths(target_directory, depot, holding)
            target_path = os.path.join(target_path, os.path.basename(pdf_path))
            shutil.copy2(pdf_path, target_path)

    end_time = datetime.datetime.now()
    process_time = (end_time - start_time).total_seconds()
    logger.info(f"Time in sec: {process_time}")
    logger.info(f"Processed PDFs: {processed_pdfs}")


def check_and_create_paths(target_path: str, depot: str, holding: str):
    full_path = os.path.join(target_path, depot, holding)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path


def get_depot(pdf_text: str) -> str:
    for search_word, directory_name in DEPOT_PATHS:
        if search_word in pdf_text:
            return directory_name


def get_holding(pdf_text: str, depot: str) -> str:
    pdf_list = pdf_text.split("\n")
    if depot == "Trade Republic":
        return ExtractorTradeRepublic().get_holding_name(pdf_list)


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
