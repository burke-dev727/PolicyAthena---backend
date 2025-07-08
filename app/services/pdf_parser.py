import os
from typing import List, Union, Tuple
import pdfplumber
from app.models.plan_model import PageBlock

def parse_pdf_to_blocks(
    file_path: str,
    save_text: bool = True,
    return_text_path: bool = False
) -> Union[List[PageBlock], Tuple[List[PageBlock], str]]:

    blocks: List[PageBlock] = []
    all_text: List[str] = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                blocks.append(PageBlock(page_num=i + 1, content=text))
                all_text.append(text)

    txt_path = ""
    if save_text and all_text:
        out_dir = os.path.join("data", "extracted_text")
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
        txt_path = os.path.join(out_dir, filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n\n--- PAGE BREAK ---\n\n".join(all_text))

    if return_text_path:
        return blocks, txt_path
    else:
        return blocks
