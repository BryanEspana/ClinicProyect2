from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import DevelopmentConfig, config
from werkzeug.security import check_password_hash
from sqlalchemy.sql import text
from models import db, Usuario, Paciente, Medico, Enfermedad, UtencilioMed, Lugar, Usuario, Inventario, Historial
import subprocess
import sys

def install_package(package):
    """Instala un paquete utilizando pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_module(package):
    """Verifica si un módulo está instalado y, en caso contrario, lo instala"""
    try:
        __import__(package)
    except ImportError:
        print(f"{package} no está instalado. Instalando ahora...")
        install_package(package)

check_module('flask')
check_module('config')
check_module('werkzeug.security')
check_module('sqlalchemy.sql')



# Commit para backend
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
id_usuarioActual = 0
id_lugarActual = 0

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
            global id_lugarActual
            id_usuarioActual = result[0]  # asignar el valor de la consulta a la variable global
            id_lugarActual = db.session.execute(text("SELECT id_lugar FROM medico WHERE id_medico = :id"), {'id': id_usuarioActual}).fetchone()[0]
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
@app.route('/medicamentos', methods=['GET', 'POST'])
def medicamentos():
    global id_lugarActual
    global id_usuarioActual
    query = text("""SELECT h.id_historial, l.nombre AS establecimiento, p.nombre AS paciente, m.nombre AS medico,e.nombre AS enfermedad, h.herencia, h.tratamiento, h.evolucion, h.estado, h.comentario FROM historial h JOIN lugar L ON h.id_lugar = l.id_lugar JOIN paciente p ON h.id_paciente = p.id_paciente JOIN medico m ON h.id_medico = m.id_medico JOIN enfermedad e ON h.id_enfermedad = e.id_enfermedad WHERE h.id_lugar = :id_lugar;""")
    result = db.session.execute(query, {'id_lugar': id_lugarActual})
    columns = result.keys()
    result = result.fetchall()

    if request.method == 'POST':
        paciente = request.form['paciente']
        nombrePaciente = request.form['nombrePaciente']
        medico = request.form['medico']
        enfermedad = request.form['enfermedad']
        herencia = request.form['herencia']
        tratamiento = request.form['tratamiento']
        evolucion = request.form['evolucion']
        estado = request.form['estado']
        comentario = request.form['comentario']
        id_historial = request.form['id_historial']
        id_paciente = db.session.execute(text("""SELECT id_paciente FROM paciente WHERE nombre = :paciente"""), {'paciente': nombrePaciente}).fetchone()[0]
        if paciente == "" and medico == "" and enfermedad == "" and herencia == "" and tratamiento == "" and evolucion == "" and estado == "" and comentario == "":
            query = text("DELETE FROM historial WHERE id_paciente = :id_paciente")
            db.session.execute(query, {'id_paciente': id_paciente})
            db.session.commit()
            return render_template('medicamentos/medicamento.html', historial=result, columns=columns)
        else:
            id_medico = db.session.execute(text("""SELECT id_medico FROM medico WHERE nombre = :medico"""), {'medico': medico}).fetchone()[0]
            id_enfermedad = db.session.execute(text("""SELECT id_enfermedad FROM enfermedad WHERE nombre = :enfermedad"""), {'enfermedad': enfermedad}).fetchone()[0]
            query = text("""UPDATE historial SET id_paciente = :id_paciente, id_medico = :id_medico, id_enfermedad = :id_enfermedad, herencia = :herencia, tratamiento = :tratamiento, evolucion = :evolucion, estado = :estado, comentario = :comentario WHERE id_historial = :id_historial""")
            db.session.execute(query, {'id_paciente': id_paciente, 'id_medico': id_medico, 'id_enfermedad': id_enfermedad, 'herencia': herencia, 'tratamiento': tratamiento, 'evolucion': evolucion, 'estado': estado, 'comentario': comentario, 'id_historial': id_historial})
            id_bitacora = db.session.execute(text("""SELECT id_cambio FROM bitacora ORDER BY id_cambio DESC LIMIT 1""")).fetchone()[0]
            db.session.execute(text("UPDATE bitacora SET usuario = :id_usuario WHERE id_cambio = :id_bitacora"), {'id_usuario': id_usuarioActual, 'id_bitacora': id_bitacora})
            db.session.commit()
            return render_template('medicamentos/medicamento.html', historial=result, columns=columns)

        return render_template('medicamentos/medicamento.html', historial=result, columns=columns)
    return render_template('medicamentos/medicamento.html', historial=result, columns=columns)

#-----------------------------------------Establecimientos-----------------------------------------
@app.route('/establecimiento', methods=['GET', 'POST'])
def establecimientos():
    global id_lugarActual

    query1 = text("""SELECT u.id_medico, u.usuario, u.password FROM usuario u JOIN medico m ON u.id_medico = m.id_medico WHERE m.id_lugar = :id_lugar;""")
    query2 = text("""SELECT * FROM medico WHERE id_lugar = :id_lugar;""")
    query3 = text("""SELECT l.nombre AS  lugar, u.nombre, i.cantidad, i.expiracion FROM inventario i JOIN utencilio_med u ON i.id_utencilio = u.id_utencilio JOIN lugar l ON l.id_lugar = i.id_lugar  WHERE i.id_lugar = :id_lugar;""")
    query4 = text("""SELECT u.nombre, i.cantidad, (i.expiracion - current_date) AS dias_habiles FROM inventario i JOIN utencilio_med u ON u.id_utencilio = i.id_utencilio WHERE i.cantidad<= (0.15*u.cant_optima) AND i.id_lugar = :id_lugar;""")
    result1 = db.session.execute(query1, {'id_lugar': id_lugarActual})
    result2 = db.session.execute(query2, {'id_lugar': id_lugarActual})
    result3 = db.session.execute(query3, {'id_lugar': id_lugarActual})
    result4 = db.session.execute(query4, {'id_lugar': id_lugarActual})

    ColumnUsuarios = result1.keys()
    ColumnMedicos = result2.keys()
    ColumnInventario = result3.keys()
    ColumnInventarioAlerta = result4.keys()

    result1 = result1.fetchall()
    result2 = result2.fetchall()
    result3 = result3.fetchall()
    result4 = result4.fetchall()

    if request.method == 'POST':
        if request.form['identificador'] == 'usuario':
            id_usuario = request.form['id']
            usuario = request.form['usuario']
            password = request.form['password']
            queryUpdate = text("""UPDATE usuario SET id_medico = :id_usuario, usuario = :usuario, password = :password WHERE id_medico = :id_usuario""")
            db.session.execute(queryUpdate, {'id_usuario': id_usuario, 'usuario': usuario, 'password': password})
            db.session.commit()
            return render_template('establecimiento/establecimiento.html', usuarios=result1, personal=result2, inventario=result3, alerta=result4, ColumnUsuarios=ColumnUsuarios, ColumnMedicos=ColumnMedicos, ColumnInventario=ColumnInventario, ColumnInventarioAlerta=ColumnInventarioAlerta)
        elif request.form['identificador'] == 'personal':
            id_usuario = request.form['idmedico']
            usuario = request.form['nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            numero_colegiado = request.form['numcolegiado']
            especialidad = request.form['especialidad']
            id_lugar = request.form['lugar']
            queryUpdate = text("""UPDATE medico SET id_medico = :id_usuario, nombre = :usuario, direccion = :direccion, telefono = :telefono, numcolegiado = :numcolegiado, especialidad = :especialidad, id_lugar = :id_lugar WHERE id_medico = :id_usuario""")
            db.session.execute(queryUpdate, {'id_usuario': id_usuario, 'usuario': usuario, 'direccion': direccion, 'telefono': telefono, 'numcolegiado': numero_colegiado, 'especialidad': especialidad, 'id_lugar': id_lugar})
            db.session.commit()
            return render_template('establecimiento/establecimiento.html', usuarios=result1, personal=result2, inventario=result3, alerta=result4, ColumnUsuarios=ColumnUsuarios, ColumnMedicos=ColumnMedicos, ColumnInventario=ColumnInventario, ColumnInventarioAlerta=ColumnInventarioAlerta)
       

    return render_template('establecimiento/establecimiento.html', usuarios=result1, personal=result2, inventario=result3, alerta=result4, ColumnUsuarios=ColumnUsuarios, ColumnMedicos=ColumnMedicos, ColumnInventario=ColumnInventario, ColumnInventarioAlerta=ColumnInventarioAlerta)

#---------------------Agregar a inventario---------------------
@app.route('/agregarInventario', methods=['GET', 'POST'])
def agregarInventario():
    global id_lugarActual
    query = text("""SELECT * FROM utencilio_med;""")
    result = db.session.execute(query).fetchall()
    query1 = text("SELECT * FROM lugar")
    result1 = db.session.execute(query1).fetchall()

    if request.method == 'POST':
        global id_lugarActual
        id_utencilio = request.form['utencilio']
        cantidad = request.form['cantidad']
        expiracion = request.form['expiracion']
        idInv = db.session.execute(text("SELECT id_inventario FROM inventario ORDER BY id_inventario DESC LIMIT 1;")).fetchone()[0] + 1
        query = text("""INSERT INTO inventario VALUES (:id_inventario, :id_lugar, :id_utencilio, :cantidad, :expiracion);""")
        db.session.execute(query, {'id_inventario':idInv,'id_utencilio': id_utencilio, 'id_lugar': id_lugarActual, 'cantidad': cantidad, 'expiracion': expiracion})
        db.session.commit()
        return render_template('establecimiento/agregarInv.html',utencilios=result, lugares=result1)
    
    return render_template('establecimiento/agregarInv.html',utencilios=result, lugares=result1)


#-----------------------------------------dashboard-----------------------------------------
@app.route('/dashboard/dashboard')
def dashboard():
    
    return render_template('dashboard/dashboard.html')

#-----------------------------------------Inventario-----------------------------------------
@app.route('/inventario')
def estadisticas():
    global id_lugarActual
    #Enfermedades mortales
    enfermedades = text("""SELECT e.nombre AS Enfermedad, count(h.id_enfermedad) AS Muertes FROM historial h JOIN enfermedad e ON e.id_enfermedad = h.id_enfermedad WHERE h.estado LIKE 'Muerto%' GROUP BY e.nombre ORDER BY Muertes DESC;""")
    resultEnfermedades = db.session.execute(enfermedades).fetchall()
    #Medicos Populares
    medicos = text("""SELECT * FROM lugar;
                    SELECT m.nombre AS medico, count(h.id_medico) AS visita
                    FROM historial h
                    JOIN medico m ON h.id_medico = m.id_medico
                    GROUP BY medico
                    ORDER BY  visita DESC
                    LIMIT 10;""")
    resultMedicos = db.session.execute(medicos).fetchall()
    #pacientes mas visitados
    visitas = text("""SELECT COUNT(h.id_paciente) AS cuenta, p.nombre, p.telefono, p.direccion 
                      FROM historial h 
                      JOIN paciente p ON h.id_paciente = p.id_paciente 
                      WHERE h.id_lugar = :id_lugar 
                      GROUP BY p.id_paciente 
                      ORDER BY cuenta desc 
                      LIMIT 5;""")
    resultVisitas = db.session.execute(visitas, {'id_lugar': id_lugarActual}).fetchall()
    print(resultVisitas)
    #Reporte de inventario
    reporte = text("""SELECT u.nombre, i.cantidad FROM inventario i JOIN utencilio_med u ON i.id_utencilio = u.id_utencilio WHERE i.cantidad<10 AND i.id_lugar = :id_lugar;""")
    resultReporte = db.session.execute(reporte, {'id_lugar': id_lugarActual}).fetchall()
    #Establecimientos populares

    #Todos
    pop = text("""SELECT lugar.nombre AS lugar, COUNT(*) AS cantidad_pacientes FROM lugar JOIN historial ON lugar.id_lugar = historial.id_lugar GROUP BY lugar.id_lugar ORDER BY cantidad_pacientes DESC LIMIT 3""")
    resultPop = db.session.execute(pop).fetchall()
    # Hospitales
    hosp = text("""SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes FROM lugar JOIN historial ON lugar.id_lugar = historial.id_lugar WHERE lugar.nombre LIKE '%Hospital%' GROUP BY lugar.nombre ORDER BY cantidad_pacientes DESC LIMIT 3;""")
    resultHosp = db.session.execute(hosp).fetchall()
    # Clinicas
    clinic = text("""SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes FROM lugar JOIN historial ON lugar.id_lugar = historial.id_lugar WHERE lugar.nombre LIKE '%Clinica%' GROUP BY lugar.nombre ORDER BY cantidad_pacientes DESC LIMIT 3;""")
    resultClinic = db.session.execute(clinic).fetchall()
    # Centros Medicos
    Centro = text("""SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes FROM lugar JOIN historial ON lugar.id_lugar = historial.id_lugar WHERE lugar.nombre LIKE '%Centro Medico%' GROUP BY lugar.nombre ORDER BY cantidad_pacientes DESC LIMIT 3;""")
    resultCentro = db.session.execute(Centro).fetchall()
    return render_template('inventario/inventario.html', enfermedades = resultEnfermedades, medicos = resultMedicos, pacientes = resultVisitas, inventario = resultReporte, total = resultPop, hospitales = resultHosp, clinicas = resultClinic, centros = resultCentro)
 

#-----------------------------------------Agregar a Historial----------------------------------------
@app.route('/AgregarAHistorial', methods=['GET', 'POST'])
def AddHistorial():
    establecimientos = text("""SELECT * FROM lugar;""")
    resultEstablecimientos = db.session.execute(establecimientos).fetchall()
    pacientes = text("""SELECT * FROM paciente;""")
    resultPacientes = db.session.execute(pacientes).fetchall()
    enferm = text("""SELECT * FROM enfermedad;""")
    resultEnferm = db.session.execute(enferm).fetchall()
    medico = text("""SELECT * FROM medico;""")
    resultMedico = db.session.execute(medico).fetchall()
    if request.method == 'POST':
        newPaciente = request.form['paciente']
        newMedico = request.form['medico']
        newEnfermedad = request.form['enfermedad']
        newLugar = request.form['lugar']
        newHerencia = request.form['herencia']
        newTratamiento = request.form['tratamiento']
        newEvolucion = request.form['evolucion']
        newEstado = request.form['estado']
        newComentario = request.form['comentario']
        idHistorial = db.session.execute(text("SELECT id_historial FROM historial ORDER BY id_historial DESC LIMIT 1;")).fetchone()[0] + 1
        query = text("""
                        INSERT INTO historial 
                        VALUES (:id_historial,current_date,:herencia,:tratamiento,:evolucion,:estado,:comentario,:id_lugar,:id_paciente,:id_medico,:id_enfermedad);
        """)
        
        db.session.execute(query, {'id_historial': idHistorial, 'herencia': newHerencia, 'tratamiento': newTratamiento, 'evolucion': newEvolucion, 'estado': newEstado, 'comentario':newComentario,'id_lugar': newLugar, 'id_paciente': newPaciente, 'id_medico': newMedico, 'id_enfermedad': newEnfermedad})
        db.session.commit()
        return render_template('medicamentos/AddHistorial.html', lugares = resultEstablecimientos, pacientes = resultPacientes, enfermedades = resultEnferm, medicos=resultMedico)

    return render_template('medicamentos/AddHistorial.html', lugares = resultEstablecimientos, pacientes = resultPacientes, enfermedades = resultEnferm, medicos=resultMedico)

#-----------------------------------------Agregar a Paciente----------------------------------------
@app.route('/AgregarPaciente', methods=['GET', 'POST'])
def AddPaciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        masa = request.form['masa']
        altura = request.form['altura']
        adiccion = request.form['adicciones']
        telefono = request.form['tel']
        direccion = request.form['direccion']
        idPaciente = db.session.execute(text("SELECT id_paciente FROM paciente ORDER BY id_paciente DESC LIMIT 1;")).fetchone()[0] + 1
        query = text("""INSERT INTO paciente VALUES (:id_paciente, :nombre, :masa, :altura, :adicciones, :telefono, :direccion);""")
        db.session.execute(query, {'id_paciente':idPaciente,'nombre': nombre, 'masa': masa, 'altura': altura, 'adicciones': adiccion, 'telefono': telefono, 'direccion': direccion})
        db.session.commit()
        return render_template('pacientes/AddPaciente.html')
    return render_template('pacientes/AddPaciente.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()