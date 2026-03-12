SECTION_HEADERS = [
    "experience",
    "projects",
    "education",
    "skills",
    "technical skills"
]


def split_sections(text: str):

    sections = {"general": []}
    current = "general"

    for line in text.split("\n"):

        clean = line.strip().lower()

        if clean in SECTION_HEADERS:
            current = clean
            sections[current] = []
        else:
            sections[current].append(line)

    return {k: " ".join(v) for k, v in sections.items()}
