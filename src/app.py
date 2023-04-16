from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import DevelopmentConfig, config
from werkzeug.security import check_password_hash
from sqlalchemy.sql import text
from models import db, Usuario, Paciente, Medico, Enfermedad, UtencilioMed, Lugar, Usuario, Inventario, Historial


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
id_usuarioActual = 0

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('auth/main.html')

@app.route('/logout')
def logout():
    # Elimina la información del usuario de la sesión
    session.pop('user_id', None)
    # Redirecciona al usuario a la página de inicio de sesión
    return redirect(url_for('login'))


@app.route('/auth/login')
def login():
    return render_template('auth/login.html')

@app.route('/dashboard/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/auth/register')
def register():
    return render_template('auth/register.html')
@app.route('/inicio', methods=('GET', 'POST'))
def inicio():
    if request.method == 'POST':
        # obtiene los datos del formulario
        usuario = request.form['username']
        password = request.form['password']

        # ejecuta la consulta SQL en bruto
        query = text("SELECT id_medico ,usuario, password FROM usuario WHERE usuario = :usuario AND password = :password")
        result = db.session.execute(query, {'usuario': usuario, 'password': password}).fetchone()

        if result is None:
            # si el usuario no existe o la contraseña no es válida, redirecciona al inicio de sesión
            flash('Nombre de usuario o contraseña inválidos')
            return redirect(url_for('login'))
        else:
            # si la autenticación es exitosa, inicia sesión y redirecciona al dashboard
            global id_usuarioActual
            id_usuarioActual = result[0]  # asignar el valor de la consulta a la variable global
            return render_template('dashboard/dashboard.html')

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