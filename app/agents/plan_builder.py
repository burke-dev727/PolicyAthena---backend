import os
from app.services.pdf_parser import parse_pdf_to_blocks
from app.services.storage import save_plan, load_plan
from app.models.plan_model import PlanData

class PlanBuilderAgent:
    def parse_and_save(self, file_path: str, plan_name: str):
        blocks, extracted_text_path = parse_pdf_to_blocks(file_path, return_text_path=True)
        plan_data = PlanData(name=plan_name, text_blocks=blocks, extracted_text_path=extracted_text_path)
        save_plan(plan_data)
        return plan_data

    def get_plan(self, plan_name: str) -> PlanData:
        return load_plan(plan_name)