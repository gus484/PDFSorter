from abc import abstractmethod


class Extractor:
    def __init__(self):
        pass

    def find_sections(self):
        pass

    @staticmethod
    def find_section_name(pdf_content: list[str], section_name: str) -> int:
        i = 0
        for line in pdf_content:
            if line.startswith(section_name):
                return i
            i += 1
        return -1

    @abstractmethod
    def get_holding_name(self, pdf_content: list[str]) -> str:
        pass
