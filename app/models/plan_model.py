from typing import List
from pydantic import BaseModel
from typing import List, Optional

class PageBlock(BaseModel):
    page_num: int
    content: str

class PlanData(BaseModel):
    name: str
    text_blocks: List[PageBlock]
    extracted_text_path: Optional[str] = None