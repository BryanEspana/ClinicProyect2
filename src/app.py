from flask import Flask, render_template
from config import config
from flask import request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import db, Usuario, Paciente, Medico, Enfermedad, UtencilioMed, Lugar, Usuario, Inventario, Historial


app=Flask(__name__)
db.init_app(app)

@app.route('/')
def index():
    return render_template('auth/main.html')

@app.route('/auth/login')
def login():
    return render_template('auth/login.html')


@app.route('/auth/register')
def register():
    return render_template('auth/register.html')

@app.route('/inicio', methods=('GET', 'POST'))
def inicio():
    if request.method == 'POST':
        # obtiene los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # busca el usuario en la base de datos
        user = Usuario.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            # si el usuario no existe o la contraseña no es válida, redirecciona al inicio de sesión
            flash('Nombre de usuario o contraseña inválidos')
            return redirect(url_for('inicio_sesion'))
        else:
            # si la autenticación es exitosa, inicia sesión y redirecciona al dashboard
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('dashboard/dashboard.html')

@app.route('/pacientes')
def paciente():
    return render_template('pacientes/paciente.html')

@app.route('/medicamentos')
def medicamentos():
    return render_template('medicamentos/medicamento.html')

@app.route('/establecimiento')
def establecimientos():
    return render_template('establecimiento/establecimiento.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()