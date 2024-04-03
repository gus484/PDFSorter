from extractors.extractor import Extractor


class ExtractorIng(Extractor):
    def get_holding_name(self, pdf_content: list[str]) -> str:
        line_nbr = Extractor.find_section_name(pdf_content, "Wertpapierbezeichnung")
        return pdf_content[line_nbr].removeprefix("Wertpapierbezeichnung ")

    def __init__(self):
        super().__init__()
