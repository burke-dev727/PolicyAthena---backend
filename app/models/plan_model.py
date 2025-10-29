from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class PageBlock(BaseModel):
    page_num: int
    content: str

class PlanData(BaseModel):
    name: str
    text_blocks: List[PageBlock]
    extracted_text_path: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None  # AI-extracted structured plan data
