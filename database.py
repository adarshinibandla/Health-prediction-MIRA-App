import sqlite3

conn = sqlite3.connect("health_data.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- TABLE ----------------
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


# ---------------- CREATE ----------------
def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    cursor.execute("""
    INSERT INTO patients (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()


# ---------------- READ ----------------
def view_patients():
    cursor.execute("SELECT * FROM patients")
    return cursor.fetchall()


# ---------------- UPDATE ----------------
def update_patient(patient_id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    cursor.execute("""
    UPDATE patients
    SET name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
    WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id))
    conn.commit()


# ---------------- DELETE ----------------
def delete_patient(patient_id):
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()


# ---------------- RESET IDS ----------------
def reset_ids():
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='patients'")
    conn.commit()