import pymupdf
from pathlib import Path
from elsai_agent_hub.utils.text_utils import TextUtils

class ReadPdf:
    def pdf_reader(self, pdf_path: str = None, page_no: int = None) -> str:
        """Extract text from the PDF file

        Args:
            pdf_path (str): PDF file path. Defaults to None.
            page_no (int, optional): Specific page number to extract. Defaults to None.

        Raises:
            ValueError: if PDF file path is empty
            FileNotFoundError: if file path not found in the location.
            ValueError: if page number not a integer type

        Returns:
            str: Extracted text from PDF
        """
        if not pdf_path:
            raise ValueError("A file path must be provided to read a PDF")
        
        file_path = Path(pdf_path)
        if not file_path.exists():
            file_error = fr"The file {str(pdf_path)} does not exist in the given path."
            raise FileNotFoundError(file_error)
        
        if page_no and not isinstance(page_no, int):
            raise ValueError("Page number must be a valid integer")
        
        doc = pymupdf.open(pdf_path)

        text = ""
        for page in doc:
            if page_no and page.number == page_no:
                #Extracts text if page number given
                page_text = page.get_text()
                page_text = TextUtils().text_preprocess(page_text)
                return page_text    
            text = page.get_text()
            text = text + " " + text
        text = TextUtils().text_preprocess(text)
        return text