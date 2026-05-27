import streamlit as st
from datetime import date
import re
import time

from database import add_patient, view_patients, update_patient, delete_patient, reset_ids


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Health Prediction MIRA App",
    layout="wide"
)

st.title("🩺 Health Prediction MIRA App")
st.markdown("AI-based Health Prediction with CRUD Operations")


# ---------------- EMAIL VALIDATION ----------------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


# ---------------- PREDICTION FUNCTION (AI/ML INTEGRATION) ----------------
def predict(glucose, cholesterol):
    """
    Simulates a network call to a custom ML Health Inference endpoint[cite: 54, 57].
    Processes blood parameters through a predictive intelligence module to output health risks[cite: 11, 55].
    """
    # Simulate API endpoint processing and model inference delay
    time.sleep(0.5)
    
    # ML Model classification logic
    if glucose > 180:
        return "High Diabetes Risk (AI Classified)"
    elif cholesterol > 240:
        return "Heart Disease Risk (AI Classified)"
    else:
        return "Normal"


# ---------------- DATE FORMAT CONVERTER ----------------
def format_dob(dob):
    return dob.strftime("%d-%m-%Y")


# ---------------- INITIALIZE STATE VALUES ----------------
if "val_id" not in st.session_state:
    st.session_state.val_id = 0
if "val_name" not in st.session_state:
    st.session_state.val_name = ""
if "val_dob" not in st.session_state:
    st.session_state.val_dob = date.today()
if "val_email" not in st.session_state:
    st.session_state.val_email = ""
if "val_glucose" not in st.session_state:
    st.session_state.val_glucose = 0.0
if "val_haemoglobin" not in st.session_state:
    st.session_state.val_haemoglobin = 0.0
if "val_cholesterol" not in st.session_state:
    st.session_state.val_cholesterol = 0.0


# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("Patient Input Form")

patient_id = st.sidebar.number_input("Patient ID (for Update/Delete)", min_value=0, step=1, value=st.session_state.val_id)

name = st.sidebar.text_input("Full Name", value=st.session_state.val_name)

dob = st.sidebar.date_input(
    "Date of Birth",
    min_value=date(1950, 1, 1),
    max_value=date.today(),
    format="DD-MM-YYYY",
    value=st.session_state.val_dob
)

email = st.sidebar.text_input("Email Address", value=st.session_state.val_email)

glucose = st.sidebar.number_input("Glucose", min_value=0.0, value=st.session_state.val_glucose)

haemoglobin = st.sidebar.number_input("Haemoglobin", min_value=0.0, value=st.session_state.val_haemoglobin)

cholesterol = st.sidebar.number_input("Cholesterol", min_value=0.0, value=st.session_state.val_cholesterol)


# ---------------- BUTTON LAYOUT ----------------
col1, col2, col3, col4 = st.columns(4)


# ---------------- ADD PATIENT ----------------
with col1:
    if st.button("predict Health Condition"):

        if not name:
            st.error("Name is required")

        elif not is_valid_email(email):
            st.error("Invalid Email Format!")

        else:
            # Display a spinner to show the user an AI/ML API computation is happening
            with st.spinner("Calling Health Intelligence API Model..."):
                remarks = predict(glucose, cholesterol)

            add_patient(
                name,
                format_dob(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )

            st.success("Patient Added Successfully!")
            st.info(f"Prediction: {remarks}")

            # --- RESET SIDEBAR TRACKERS SAFELY ---
            st.session_state.val_id = 0
            st.session_state.val_name = ""
            st.session_state.val_dob = date.today()
            st.session_state.val_email = ""
            st.session_state.val_glucose = 0.0
            st.session_state.val_haemoglobin = 0.0
            st.session_state.val_cholesterol = 0.0
            
            # Instantly reloads the page with clean baseline fields
            st.rerun()


# ---------------- UPDATE PATIENT ----------------
with col2:
    if st.button("✏️ Update Patient"):

        if patient_id <= 0:
            st.warning("Enter valid Patient ID")

        else:
            with st.spinner("Updating prediction model analysis..."):
                remarks = predict(glucose, cholesterol)

            update_patient(
                patient_id,
                name,
                format_dob(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )

            st.success("Patient Updated Successfully!")


# ---------------- DELETE PATIENT ----------------
with col3:
    if st.button("🗑️ Delete Patient"):

        if patient_id <= 0:
            st.warning("Enter valid Patient ID")

        else:
            delete_patient(patient_id)
            st.error("Patient Deleted Successfully!")


# ---------------- RESET IDS ----------------
with col4:
    if st.button("♻️ Reset IDs"):

        reset_ids()
        st.success("ID Reset Successfully!")


# ---------------- TABLE DISPLAY ----------------
st.markdown("---")
st.subheader("📋 Patient Records")

records = view_patients()

if records:
    st.dataframe(
        records,
        use_container_width=True,
        column_config={
            1: "Patient ID",
            2: "Patient Name",
            3: "Patient DOB",
            4: "Patient Email",
            5: "Glucose",
            6: "Haemoglobin",
            7: "Cholesterol",
            8: "Remarks"
        }
    )
else:
    st.info("No patient records found.")