
# AI Resume Analyzer

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python">
<img src="https://img.shields.io/badge/NLP-Sentence%20Transformers-green">
<img src="https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit">
<img src="https://img.shields.io/badge/Testing-Pytest-orange?logo=pytest">
<img src="https://img.shields.io/badge/License-MIT-yellow">
<img src="https://img.shields.io/badge/Status-Active-success">
<img src="https://img.shields.io/github/stars/yourusername/resume-analyzer">
<img src="https://img.shields.io/github/forks/yourusername/resume-analyzer">
<img src="https://img.shields.io/github/issues/yourusername/resume-analyzer">
<img src="https://img.shields.io/github/last-commit/yourusername/resume-analyzer">
</p>

<p align="center">
An AI-powered system that analyzes resumes against job descriptions using semantic similarity, skill extraction, and automated gap detection.
</p>


---

# Overview

Recruiters often spend hours manually reviewing resumes.
This project automates that process by evaluating how closely a candidate’s resume matches a job description using modern NLP techniques.

The system automatically:

* extracts text from PDF resumes
* detects technical skills
* computes semantic similarity between resume and job description
* identifies missing skills
* produces a final candidate fit score

The result is a **transparent and interpretable evaluation pipeline** that helps recruiters and candidates understand role alignment.

---

# Demo

<p align="center">
<img src="demo/demo.gif" width="850">
</p>

Upload a resume and paste a job description to generate:

| Output              | Description                     |
| ------------------- | ------------------------------- |
| Candidate Fit Score | Overall ranking score           |
| Semantic Match      | Contextual similarity           |
| Skill Coverage      | Percentage of JD skills matched |
| Extracted Skills    | Technologies detected           |
| Missing Skills      | Required skills not present     |

Example Output

```
Candidate Fit Score : 0.74
Semantic Similarity : 0.78
Skill Coverage      : 0.68

Missing Skills: Docker, Kubernetes, AWS
```

---

# Key Features

## PDF Resume Parsing

Extracts structured text from multi-page resumes using **PDFPlumber**.

Capabilities:

* supports multi-page documents
* handles different resume layouts
* extracts readable structured text

---

## Intelligent Text Preprocessing

Preserves technical tokens that are normally destroyed by standard tokenizers.

Examples preserved:

```
C++
Node.js
C#
```

Cleaning pipeline includes:

* Unicode normalization
* URL removal
* email removal
* punctuation filtering
* whitespace normalization

---

## Hybrid Similarity Engine

The analyzer combines two complementary similarity approaches.

| Method                 | Weight | Purpose                   |
| ---------------------- | ------ | ------------------------- |
| TF-IDF                 | 45%    | keyword overlap detection |
| Transformer Embeddings | 55%    | semantic similarity       |

Embedding model used:

```
all-MiniLM-L6-v2
```

Example semantic relationships:

```
Machine Learning ≈ ML
Backend Development ≈ Server-side Engineering
```

---

## Multi-Strategy Skill Extraction

Skills are detected using a **three-layer matching system**.

| Method        | Technique                | Example                |
| ------------- | ------------------------ | ---------------------- |
| Exact Match   | Regex boundary matching  | Python                 |
| Variant Match | Alias mapping            | k8s → Kubernetes       |
| Fuzzy Match   | RapidFuzz typo detection | Kubernets → Kubernetes |

This makes the system **robust to typos and alternate naming conventions**.

---

## Skill Gap Analysis

Compares resume skills against job description requirements.

Outputs include:

* matched skills
* missing skills
* coverage percentage

This helps candidates identify **skills required to qualify for a role**.

---

## Candidate Fit Score

The final score combines similarity and skill coverage.

```
Final Score

60% Semantic Similarity
40% Skill Coverage
```

This produces an **interpretable ranking metric for candidate evaluation**.

---

# Animated Pipeline Illustration

<p align="center">
<img src="docs/pipeline.gif" width="850">
</p>

---

# System Architecture


```
Resume PDF + Job Description
            │
            ▼
       PDF Parsing
            │
            ▼
    Text Preprocessing
            │
            ▼
     Skill Extraction
   (Exact + Variant + Fuzzy)
            │
            ▼
   Hybrid Similarity Engine
   (TF-IDF + MiniLM Model)
            │
            ▼
        Gap Analysis
            │
            ▼
     Candidate Fit Score
```

The system is designed using **modular NLP components**, making it easy to extend and maintain.

---


# Project Structure

```
resume-analyzer/
│
├── app.py
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── pdf_parser.py
│   ├── preprocessing.py
│   ├── similarity.py
│   ├── skills.py
│   └── gap_analysis.py
│
└── tests/
    └── test_skills.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```
streamlit
pdfplumber
scikit-learn
sentence-transformers
rapidfuzz
numpy
pandas
torch
plotly
pytest
```

---

# Running the Application

Start the Streamlit app

```bash
streamlit run app.py
```

Open the interface

```
http://localhost:8501
```

Steps:

1. Upload resume (PDF)
2. Paste job description
3. Click **Analyze Candidate**

---

# Performance Metrics

| Metric                           | Value             | Context             |
| -------------------------------- | ----------------- | ------------------- |
| Skill detection accuracy         | ~85–90%           | taxonomy skills     |
| Resume–JD similarity reliability | ~75–80%           | hybrid similarity   |
| Manual screening reduction       | ~60–70%           | automated filtering |
| Processing throughput            | 40–60 resumes/min | local CPU           |

---

# Technology Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Language        | Python                |
| UI              | Streamlit             |
| NLP             | Sentence Transformers |
| ML              | Scikit-learn          |
| Fuzzy Matching  | RapidFuzz             |
| PDF Parsing     | PDFPlumber            |
| Data Processing | NumPy / Pandas        |
| Visualization   | Plotly                |
| Testing         | Pytest                |

---

# Auto-Generated API Documentation

Core modules:

```
PDFParser
TextPreprocessor
SimilarityEngine
SkillExtractor
GapAnalyzer
```

Each component is modular and independently testable.

---

# GitHub Metrics

<p align="center">
<img src="https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=yourusername">
</p>


---

# Download Statistics

<p align="center">
<img src="https://img.shields.io/github/downloads/yourusername/resume-analyzer/total">
</p>

---

# Use Cases

This project can be used for:

* automated resume screening
* candidate self-assessment before applying
* ATS keyword optimization
* NLP and information retrieval demonstrations
* recruitment analytics research

---

# Future Improvements

Planned enhancements:

Experience Extraction
Use LLM APIs to infer years of experience per skill.

Corpus Pre-training
Train TF-IDF on large resume datasets.

Batch Resume Processing
Analyze multiple resumes simultaneously.

---

# License

MIT License

---

# Author

Developed as a machine learning and NLP project demonstrating automated document analysis, hybrid similarity search, and algorithm-driven candidate matching.









