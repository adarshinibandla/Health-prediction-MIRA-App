import streamlit as st
import re
import time
from datetime import date

from database import (
    add_patient,
    view_patients,
    update_patient,
    delete_patient,
    clear_all_records,
    email_exists,
    patient_exists
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Health Prediction MIRA App",
    layout="wide"
)

st.title("🩺 Health Prediction MIRA App")
st.markdown("AI-based Health Prediction Platform with Advanced Data Validation Analytics.")

# ---------------- DATA VALIDATION ENGINES ----------------
def is_valid_email(email):
    cleaned_email = email.strip()
    # Validates standard and multi-tier domains (like .com.au) while catching syntax mistakes
    pattern = r'^[\w\.-]+@[\w\.-]+\.[\w\.]+$'
    return bool(re.fullmatch(pattern, cleaned_email))

# ---------------- MIRA MODEL CORE ENGINE ----------------
def predict_health_risk(glucose, cholesterol):
    time.sleep(0.3)  # Simulates model network parsing latency
    if glucose > 180:
        return "High Diabetes Risk (MIRA Classified)"
    elif cholesterol > 240:
        return "Heart Disease Risk (MIRA Classified)"
    else:
        return "Normal"

# ---------------- SIDEBAR INTERFACE ----------------
st.sidebar.header("Patient Entry Form")

patient_id = st.sidebar.number_input("Patient ID (For Update/Delete Actions)", min_value=0, step=1, value=0)
name = st.sidebar.text_input("Full Name")

# --- DATE PICKER WIDGET ---
# Set max_value to 2035 to safely allow Test #8 (19.10.2030) to be selected natively
dob_calendar = st.sidebar.date_input(
    "Date of Birth",
    value=date(1990, 1, 1),
    min_value=date(1930, 1, 1),
    max_value=date(2035, 12, 31),
    format="DD-MM-YYYY"  # Forces user interface display as dd-mm-yyyy
)

email = st.sidebar.text_input("Email Address")

st.sidebar.markdown("### Clinical Bio-markers")
glucose = st.sidebar.number_input("Glucose Level", min_value=0.0, step=1.0)
haemoglobin = st.sidebar.number_input("Haemoglobin Level", min_value=0.0, step=0.1)
cholesterol = st.sidebar.number_input("Cholesterol Level", min_value=0.0, step=1.0)

# Format into clean standard string layout for database storage
normalized_dob = dob_calendar.strftime("%d-%m-%Y")

# ---------------- CONTROLLER ACTION ROW ----------------
col1, col2, col3, col4 = st.columns(4)

# --- ACTION: CREATE ---
with col1:
    if st.button("➕ Predict & Create Record", width="stretch"):
        # Dynamically checks the year based on what is currently chosen inside the calendar picker
        is_future_date = dob_calendar.year > 2026
        cleaned_email = email.strip()
        cleaned_name = name.strip()
        
        # Array list to collect multiple data entry faults simultaneously
        validation_errors = []
        
        # 1. Base Structure Required Fields
        if not cleaned_name:
            validation_errors.append("Full Name is required.")
        if not cleaned_email:
            validation_errors.append("Email field cannot be empty.")
            
        # 2. Dynamic Multi-Error Scanner (Tracks exact selected variables in real-time)
        if cleaned_email and not is_valid_email(cleaned_email):
            validation_errors.append(f"Email Syntax Violation: '{cleaned_email}' is missing standard structures.")
            
        if is_future_date:
            validation_errors.append(f"Chronological Timeline Anomaly: Birth year '{dob_calendar.year}' cannot exist in the future.")
            
        if cleaned_email and is_valid_email(cleaned_email) and email_exists(cleaned_email):
            validation_errors.append(f"Database Conflict: Email '{cleaned_email}' unique-key constraint violation.")

        # --- EVALUATING TARGET VALIDATION STATUS ---
        if validation_errors:
            # Displays all collected errors in a clear list box layout
            st.error("🚨 Submission Denied: Multiple Validation Failures Found!")
            for err in validation_errors:
                st.markdown(f"- {err}")
        else:
            with st.spinner("Executing MIRA Classifier Inference..."):
                remarks = predict_health_risk(glucose, cholesterol)
            
            add_patient(cleaned_name, normalized_dob, cleaned_email, glucose, haemoglobin, cholesterol, remarks)
            st.success(f"Record successfully initialized for {cleaned_name}!")
            st.rerun()

# --- ACTION: UPDATE ---
with col2:
    if st.button("🔄 Update Existing Record", width="stretch"):
        cleaned_email = email.strip()
        cleaned_name = name.strip()
        
        if patient_id <= 0:
            st.warning("Action Required: Provide a valid target Patient ID.")
        elif not patient_exists(patient_id):
            st.error(f"Database Error: Reference ID #{patient_id} cannot be found.")
        elif not is_valid_email(cleaned_email):
            st.error("Validation Failure: Cannot overwrite record with an invalid email address.")
        else:
            remarks = predict_health_risk(glucose, cholesterol)
            if dob_calendar.year > 2026:
                remarks += " | System Log: Warning: Future registration timeline detected."
                
            update_patient(patient_id, cleaned_name, normalized_dob, cleaned_email, glucose, haemoglobin, cholesterol, remarks)
            st.success(f"Record #{patient_id} updated successfully.")
            st.rerun()

# --- ACTION: DELETE ---
with col3:
    if st.button("❌ Remove Record", width="stretch"):
        if patient_id <= 0:
            st.warning("Action Required: Provide a valid target Patient ID.")
        elif not patient_exists(patient_id):
            st.error(f"Database Error: Reference ID #{patient_id} cannot be found.")
        else:
            delete_patient(patient_id)
            st.success(f"Patient Record #{patient_id} permanently erased.")
            st.rerun()

# --- ACTION: PURGE SYSTEM ---
with col4:
    if st.button("🚨 Clear All (Task Prep)", width="stretch"):
        clear_all_records()
        st.success("Database purged. Ready for clean evaluation runtime.")
        st.rerun()

# ---------------- LIVE VIEW REPOSITORY (READ) ----------------
st.markdown("---")
st.subheader("📋 Active Patient System Records")

raw_records = view_patients()

if raw_records:
    ui_display_list = []
    for row in raw_records:
        ui_display_list.append({
            "Patient ID": row[0],
            "Full Name": row[1],
            "Date of Birth": row[2],
            "Email": row[3],
            "Glucose": row[4],
            "Haemoglobin": row[5],
            "Cholesterol": row[6],
            "AI Diagnosis Remarks": row[7]
        })
    st.dataframe(ui_display_list, width="stretch")
else:
    st.info("System Empty: No records currently initialized in the database cluster.")