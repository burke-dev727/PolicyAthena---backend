import re

def extract_plan_fields(text: str):
    """
    Given full text (from extracted PDF), parse out fields of interest.
    Returns a dict.
    """
    fields = {}

    # Plan name (grab from first page title)
    m = re.search(r"Coverage for: [^\|]+\| Plan Type: ([A-Z]+)", text)
    fields["plan_type"] = m.group(1) if m else None

    m = re.search(r"^: ([^\n]+)\nCoverage for:", text, re.MULTILINE)
    fields["plan_name"] = m.group(1).strip() if m else None

    # Coverage period
    m = re.search(r"Coverage Period: ([\d/–\-]+)", text)
    fields["coverage_period"] = m.group(1) if m else None

    # Deductible
    m = re.search(r"overall.*deductible[^\$]*\$(\d{1,3}(?:,\d{3})*) Individual/\$(\d{1,3}(?:,\d{3})*) Family", text, re.IGNORECASE)
    fields["deductible_individual"] = m.group(1) if m else None
    fields["deductible_family"] = m.group(2) if m else None

    # Out-of-pocket
    m = re.search(r"out[- ]of[- ]pocket.*?\$(\d{1,3}(?:,\d{3})*) Individual/\$(\d{1,3}(?:,\d{3})*) Family", text, re.IGNORECASE)
    fields["oop_max_individual"] = m.group(1) if m else None
    fields["oop_max_family"] = m.group(2) if m else None

    # Primary care visit
    m = re.search(r"Primary care visit to treat an[^\n]+\$([\d/]+)[^0-9]*visit", text)
    fields["primary_care_visit"] = m.group(1) if m else None

    # Specialist visit
    m = re.search(r"Specialist visit[^\n]+\$([\d/]+)[^0-9]*visit", text)
    fields["specialist_visit"] = m.group(1) if m else None

    # ER, urgent care, etc. (examples)
    m = re.search(r"Emergency room care[^\n]+([\d%/]+)[^0-9]", text)
    fields["emergency_room"] = m.group(1) if m else None

    m = re.search(r"Urgent care[^\n]+\$([\d/]+)[^0-9]*visit", text)
    fields["urgent_care"] = m.group(1) if m else None

    # Drug copays (generic, brand)
    m = re.search(r"Generic drugs[^\n]+\$([\d/]+)", text)
    fields["generic_drug"] = m.group(1) if m else None

    m = re.search(r"Brand drugs.*Preferred[^\n]+\$([\d/]+)", text)
    fields["brand_drug_preferred"] = m.group(1) if m else None

    return fields
