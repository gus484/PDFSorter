from extractors.extractor import Extractor


class ExtractorTradeRepublic(Extractor):
    def get_holding_name(self, pdf_content: list[str]) -> str:
        line_nbr = Extractor.find_section_name(pdf_content, "POSITION ANZAHL")
        return pdf_content[line_nbr+1]

    def __init__(self):
        super().__init__()
