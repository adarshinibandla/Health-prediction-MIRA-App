# Health Prediction MIRA App 🩺

An AI-driven medical analysis and patient records management platform built using Python and Streamlit, featuring robust data validation layers and a localized SQLite architecture.

## Features
- **MIRA Health Risk Engine**: Classifies risk indicators for diabetes and heart conditions based on patient biometric inputs.
- **Full CRUD Support**: Complete pipeline for adding, reading, updating, and removing entries securely.
- **Automated Input Stripping**: Robust data protection that strips accidental spaces copied from data tables.
- **Advanced Validation Mechanics**:
  - Global domain protection matching complex extensions like `.com.au`.
  - Date validation enforcing chronological rules and highlighting anomaly edge-cases.
  - Unique identification schema flags to prevent duplicate record processing.

## Tech Stack
- **Frontend**: Streamlit (v1.31+)
- **Database Layer**: SQLite3
- **Regex Engine**: Native Python `re`

## Local Installation & Initialization

1. Install project dependencies:
   pip install -r requirements.txt
2. Spin up the localized runtime workspace environment:
   streamlit run app.py
## Author
Developed for Gokul Infocare Assignment 