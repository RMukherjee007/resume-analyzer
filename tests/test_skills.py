from core.skills import SkillExtractor

def test_exact_match_with_symbols():
    extractor = SkillExtractor()
    matches = extractor.extract_skills("I have 5 years of C++ experience.")
    extracted_names = [m.skill.name for m in matches]
    assert "c++" in extracted_names

def test_variant_match():
    extractor = SkillExtractor()
    matches = extractor.extract_skills("Deployed apps on Amazon Web Services.")
    extracted_names = [m.skill.name for m in matches]
    assert "aws" in extracted_names

def test_fuzzy_match_typos():
    extractor = SkillExtractor()
    matches = extractor.extract_skills("Orchestration using Kubernets in prod.")
    extracted_names = [m.skill.name for m in matches]
    assert "kubernetes" in extracted_names
