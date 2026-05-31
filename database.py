import sqlite3

def get_connection():
    return sqlite3.connect("health_data.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO patients
    (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()

def view_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()
    conn.close()
    return records

def update_patient(patient_id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE patients
    SET name=?, dob=?, email=?, glucose=?,
        haemoglobin=?, cholesterol=?, remarks=?
    WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()

def clear_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='patients'")
    conn.commit()
    conn.close()

def email_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE email=?", (email,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def patient_exists(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE id=?", (patient_id,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

init_db()