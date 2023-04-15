from flask import Flask, render_template
from config import config

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('auth/main.html')

@app.route('/auth/login')
def login():
    return render_template('auth/login.html')

@app.route('/auth/register')
def register():
    return render_template('auth/register.html')

@app.route('/inicio')
def inicio():
    return render_template('dashboard/dashboard.html')

@app.route('/pacientes')
def paciente():
    return render_template('pacientes/paciente.html')

@app.route('/medicamentos')
def medicamentos():
    return render_template('medicamentos/medicamento.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()