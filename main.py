from flask import Flask, request, jsonify, render_template
import json
import datetime

app = Flask(__name__)


# Route for caretaker data
@app.route('/api/save-caretaker-data', methods=['POST'])
def save_caretaker_data():
    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data received'}), 400

        # Extract caretaker info
        caretaker = data.get('caretaker', {})
        patients = data.get('patients', [])
        summary = data.get('summary', {})

        print("=== CARETAKER DATA RECEIVED ===")
        print(f"Caretaker Name: {caretaker.get('name')}")
        print(f"Total Patients: {summary.get('totalPatients')}")
        print(f"Total Medicines: {summary.get('totalMedicines')}")

        # Process each patient
        for patient in patients:
            print(f"\nPatient: {patient.get('name')}")
            print(f"Medicines: {len(patient.get('medicines', []))}")

            # Process each medicine
            for medicine in patient.get('medicines', []):
                print(f"  - {medicine.get('name')}: {medicine.get('pillsPerDay')} pills/day")
                for slot in medicine.get('schedule', []):
                    print(f"    * {slot.get('displayName')}")

        # Here you can save to database, send emails, etc.
        # save_to_database(data)
        # send_reminder_emails(data)
        # setup_notifications(data)

        return jsonify({
            'success': True,
            'message': 'Caretaker and patient data saved successfully!',
            'patients_count': len(patients),
            'total_medicines': summary.get('totalMedicines')
        })

    except Exception as e:
        print(f"Error processing caretaker data: {str(e)}")
        return jsonify({'error': 'Failed to process data'}), 500


# Route for patient schedule data
@app.route('/api/save-patient-schedule', methods=['POST'])
def save_patient_schedule():
    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data received'}), 400

        # Extract patient info
        patient = data.get('patient', {})
        schedule = data.get('medicineSchedule', {})
        summary = data.get('summary', {})

        print("=== PATIENT SCHEDULE DATA RECEIVED ===")
        print(f"Patient Name: {patient.get('name')}")
        print(f"Phone: {patient.get('phone')}")
        print(f"Total Medicines: {schedule.get('totalMedicines')}")

        # Process medicines
        for medicine in schedule.get('medicines', []):
            print(f"\nMedicine: {medicine.get('name')}")
            print(f"Type: {medicine.get('type')}")
            print(f"Doses per day: {medicine.get('dosesPerDay')}")
            print("Schedule:")
            for slot in medicine.get('schedule', []):
                print(f"  - {slot.get('displayName')}")

        # Here you can:
        # save_patient_schedule_to_db(data)
        # setup_medicine_reminders(data)
        # send_confirmation_sms(patient.get('phone'))

        return jsonify({
            'success': True,
            'message': f'Schedule saved for {patient.get("name")}!',
            'medicines_count': schedule.get('totalMedicines')
        })

    except Exception as e:
        print(f"Error processing patient schedule: {str(e)}")
        return jsonify({'error': 'Failed to process schedule'}), 500

@app.route("/")
def home():
    return render_template(
        "index.html",
        year=datetime.date.today().year,
    )


@app.route("/patient")
def patient():
    return render_template(
        "patient.html"
    )


@app.route("/caretaker")
def caretaker():
    return render_template(
        "caretaker.html"
    )


if __name__ == "__main__":
    app.run(debug=True)
