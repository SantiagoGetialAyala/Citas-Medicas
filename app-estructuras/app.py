from flask import Flask, render_template, request, redirect
from collections import deque

app = Flask(__name__)

# Clase que gestiona la EPS
class EPS:
    def __init__(self):
        self.appointments = []  # Lista para almacenar citas
        self.appointment_history = deque()  # Cola para historial de citas
        self.patients_appointments = {}  # Diccionario para rastrear las citas de cada paciente
        self.doctors = ["Dr. Pérez", "Dra. García", "Dr. López"]  # Lista de doctores disponibles
        self.available_times = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

    def schedule_appointment(self, patient, date, time, doctor, document, document_type):
        # Verificar si el paciente ya tiene una cita
        if patient in self.patients_appointments:
            return "El paciente ya tiene una cita agendada."

        appointment = {
            'patient': patient,
            'date': date,
            'time': time,
            'doctor': doctor,
            'document': document,
            'document_type': document_type
        }
        self.appointments.append(appointment)  # Añadir la cita a la lista
        self.appointment_history.append(appointment)  # Añadir la cita al historial (cola)
        self.patients_appointments[patient] = appointment  # Asociar la cita con el paciente

    def cancel_appointment(self, index):
        appointment = self.appointments.pop(index)  # Eliminar de la lista de citas
        self.appointment_history.remove(appointment)  # Eliminar del historial (cola)
        self.patients_appointments.pop(appointment['patient'], None)  # Eliminar la cita del paciente

# Instancia de EPS
eps = EPS()

@app.route('/')
def index():
    return render_template('index.html', doctors=eps.doctors, available_times=eps.available_times, appointments=eps.appointments, appointment_history=list(eps.appointment_history))

@app.route('/schedule', methods=['POST'])
def schedule():
    patient = request.form['patient']
    date = request.form['date']
    time = request.form['time']
    doctor = request.form['doctor']
    document = request.form['document']
    document_type = request.form['document_type']

    # Agendar cita usando la clase EPS
    message = eps.schedule_appointment(patient, date, time, doctor, document, document_type)
    if message:
        return message  # Si hay un error, devolver el mensaje

    return redirect('/')

@app.route('/cancel/<int:index>', methods=['POST'])
def cancel(index):
    # Cancelar cita usando la clase EPS
    eps.cancel_appointment(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
