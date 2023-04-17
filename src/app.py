from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import DevelopmentConfig, config
from werkzeug.security import check_password_hash
from sqlalchemy.sql import text
from models import db, Usuario, Paciente, Medico, Enfermedad, UtencilioMed, Lugar, Usuario, Inventario, Historial

# Commit para backend
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
id_usuarioActual = 0
id_pacienteActual = 0

with app.app_context():
    db.create_all()


#-----------------------------------------Register/Crear usuario-----------------------------------------
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']
        confirmacion = request.form['passwordConfirm']
        establecimiento = request.form['lugares']
        numero = request.form['numero']
        colegiado = request.form['colegiado']
        direccion = request.form['direccion']
        especialidad = request.form['especialidad']
        id = db.session.execute(text("SELECT id_medico FROM medico ORDER BY id_medico DESC LIMIT 1")).fetchone()[0] + 1

        if password != confirmacion:
            flash('La contraseña y la confirmación no coinciden')
            return redirect(url_for('index'))
        else:
            queryMed = text("INSERT INTO medico VALUES (:id, :nombre, :direccion, :telefono, :num_colegiado, :especialidad, :id_lugar)")
            queryUser = text("INSERT INTO usuario VALUES (:id, :usuario, :password)")
            db.session.execute(queryMed, {'id': id, 'nombre': usuario, 'direccion': direccion, 'telefono': numero, 'num_colegiado': colegiado, 'especialidad': especialidad, 'id_lugar': establecimiento})
            db.session.execute(queryUser, {'id': id, 'usuario': usuario, 'password': password})
            db.session.commit()

    return render_template('auth/main.html')

@app.route('/auth/register')
def register():
    query = text("SELECT * FROM lugar")
    result = db.session.execute(query).fetchall()
    return render_template('auth/register.html', lugares=result)


#-----------------------------------------LogOut/Login-----------------------------------------------------------------------
@app.route('/logout')
def logout():
    global id_usuarioActual
    id_usuarioActual = 0
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

#-----------------------------------------Pacientes-----------------------------------------------------------------------------------
@app.route('/pacientes')
def paciente():
    query = text("""SELECt * FROM paciente""")
    result = db.session.execute(query)
    columns = result.keys()
    result = result.fetchall()

    queryInfoEsp = text("""SELECT p.id_paciente, p.nombre, p.masacorporal,p.altura,p.adicciones,p.telefono,p.direccion,
                                h.herencia, e.nombre, h.tratamiento, m.nombre
                            FROM historial h
                            JOIN paciente p ON h.id_paciente = p.id_paciente
                            JOIN medico m ON h.id_medico = m.id_medico
                            JOIN enfermedad e ON h.id_enfermedad = e.id_enfermedad""")
    resultInfoEsp = db.session.execute(queryInfoEsp)
    pacientes = []
    paciente = {
        'id_paciente': 0, 
        'nombre': "", 
        'masacorporal': 0,
        'altura': 0,
        'adicciones': "",
        'telefono' : "",
        'direccion' : "",
        'herencia': [],
        'Enfermedades': [], 
        'tratamiento' : [],
        'medico' : []
    }
    for row in resultInfoEsp:
        if row[0] != paciente['id_paciente']:
            # si la fila corresponde a un nuevo paciente, se agrega el paciente anterior a la lista
            pacientes.append(paciente)
            # se crea un nuevo diccionario para el nuevo paciente
            paciente = {
                'id_paciente': row[0], 
                'nombre': row[1], 
                'masacorporal': row[2],
                'altura': row[3],
                'adicciones': row[4],
                'telefono' : row[5],
                'direccion' : row[6],
                'herencia': [],
                'Enfermedades': [], 
                'tratamiento' : [],
                'medico' : []
            }
        # se agregan los valores de herencia y tratamiento a las listas correspondientes en el diccionario
        paciente['herencia'].append(row[7])
        paciente['Enfermedades'].append(row[8])
        paciente['tratamiento'].append(row[9])
        paciente['medico'].append(row[10])
        # se agrega el último paciente a la lista
        pacientes.append(paciente)

    return render_template('pacientes/paciente.html', pacientes=result, columns=columns, pacientesInfo=pacientes)



@app.route('/informacionPaciente', methods=['POST'])
def infoPaciente():
    id_paciente = request.form['id_paciente']
    query = text("""SELECT nombre, masacorporal, altura, adicciones, telefono, direccion FROM paciente WHERE id_paciente = :id_paciente""")
    query2 = text("""SELECT h.herencia, h.tratamiento, e.nombre AS Enfermedades, m.nombre AS Medico FROM historial h JOIN enfermedad e ON h.id_enfermedad = e.id_enfermedad JOIN medico m ON h.id_medico = m.id_medico WHERE id_paciente = :id_paciente""")
    result1 = db.session.execute(query, {'id_paciente': id_paciente}).fetchone()
    result2 = db.session.execute(query2, {'id_paciente': id_paciente}).fetchall()
    herencia = []
    tratamiento = []
    enfermedad = []
    medico = []

    for i in range(len(result2)):
        herencia.append(result2[i][0])
        tratamiento.append(result2[i][1])
        enfermedad.append(result2[i][2])
        medico.append(result2[i][3])

    return render_template('pacientes/paciente-individual.html', id_paciente=id_paciente, paciente=result1, herencia=herencia, tratamiento=tratamiento, enfermedad=enfermedad, medico=medico)
#-----------------------------------------Medicamentos-----------------------------------------
@app.route('/medicamentos')
def medicamentos():
    return render_template('medicamentos/medicamento.html')

#-----------------------------------------Establecimientos-----------------------------------------
@app.route('/establecimiento')
def establecimientos():
    query1 = text("""SELECT * FROM usuario""")
    query2 = text("""SELECT * FROM medico""")
    query3 = text("""SELECT * FROM paciente""")
    return render_template('establecimiento/establecimiento.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()