import pandas as pd
from elsai_agent_hub.tools import ReadPdf
from elsai_agent_hub.tools import WebScrap

class Utils:

    def extract_text(self, pdf_file_path: str = None, url: str = None, urls: list = [], text: str = None) -> str:
        """Extracts the text from source

        Args:
            pdf_file_path (str, optional): Path to a PDF file to be analyzed. Defaults to None.
            urls (list, optional): A list of URLs whose content is to be analyzed. Defaults to an empty list.
            text (str, optional): Text to be analyzed. Defaults to None.

        Returns:
            str : Extracted text
        """
        prompt_text = ""
        if pdf_file_path:
             temp_text = ReadPdf().pdf_reader(pdf_file_path)
             prompt_text += temp_text
        if url:
             temp_text = WebScrap().read_url(url)
             prompt_text = prompt_text + " " + temp_text
        if urls:
             temp_text = WebScrap().read_url(urls=urls)
             prompt_text = prompt_text + " " + temp_text
        if text:
             prompt_text = prompt_text + " " + text
        return prompt_text
    
    def read_csv(self, csv_file_path: str):
         df = pd.read_csv(csv_file_path)
         return df