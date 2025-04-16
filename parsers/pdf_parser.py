import fitz
import logging
import re

logger = logging.getLogger(__name__)

class PDFParser:
    @staticmethod
    def scrape_acknowledgments(file_path):
        logger.info(f"Parsing acknowledgments for {file_path}")
        try:
            doc = fitz.open(file_path)
            full_text = [page.get_text("blocks") for page in doc]
            for page_blocks in full_text:
                for block in page_blocks:
                    text = block[4]
                    if re.search(r"acknowledg(e)?ments?", text, re.IGNORECASE):
                        idx = page_blocks.index(block)
                        body_blocks = page_blocks[idx + 1: idx + 4]
                        body = "\n".join(b[4].strip() for b in body_blocks)
                        return f"{text.strip()}\n{body.strip()}"
            return "Acknowledgements not found"
        except Exception as e:
            logger.exception("Failed to parse acknowledgements")
            return "Error reading PDF"

