# Resume Analyzer

A Python application that compares a resume with a job description to measure relevance and identify skill gaps.

The tool extracts text from a resume PDF, preprocesses both the resume and job description, computes text similarity, matches technical skills, and highlights missing or weak areas.

## Features

- PDF resume text extraction  
- Text preprocessing and normalization  
- TF-IDF based similarity scoring  
- Skill extraction using keyword and variant matching  
- Skill gap analysis with priority levels  
- Category-wise coverage analysis  
- Simple Streamlit web interface  

## Project Structure

resume-analyzer/
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── pdf_parser.py
│   ├── preprocessing.py
│   ├── similarity.py
│   ├── skills.py
│   └── gap_analysis.py
├── app.py
├── requirements.txt
└── README.md

## Installation

1. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate

markdown
Copy code

2. Install dependencies
pip install -r requirements.txt

shell
Copy code

## Usage

Run the application:
streamlit run app.py

css
Copy code

Upload a resume PDF and paste a job description to view similarity scores, matched skills, missing skills, and recommendations.

## Notes

- Clean object-oriented design  
- No external APIs used  
- Runs entirely locally  
- Intended for educational and personal use  
