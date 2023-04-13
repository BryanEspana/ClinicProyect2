from flask_login import UserMixin
from flask_Mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

db = MySQL()

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255))

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    numero_colegiado = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    hospital = db.relationship('Hospital', backref=db.backref('medicos', lazy=True))

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    masa_corporal = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    adicciones = db.Column(db.String(255))
    enfermedades_hereditarias = db.Column(db.String(255))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    hospital = db.relationship('Hospital', backref=db.backref('pacientes', lazy=True))

class Diagnostico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    enfermedad = db.Column(db.String(255), nullable=False)
    tratamiento = db.Column(db.String(255), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    resultado = db.Column(db.String(255))

    paciente = db.relationship('Paciente', backref=db.backref('diagnosticos', lazy=True))
    medico = db.relationship('Medico', backref=db.backref('diagnosticos', lazy=True))

class Transladomedico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    hospital_origen_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    hospital_destino_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)

    medico = db.relationship('Medico', backref=db.backref('traslados', lazy=True))
    hospital_origen = db.relationship('Hospital', foreign_keys=[hospital_origen_id], backref=db.backref('traslados_salientes', lazy=True))
    hospital_destino = db.relationship('Hospital', foreign_keys=[hospital_destino_id], backref=db.backref('traslados_entrantes', lazy=True))


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<Usuario {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Bitacora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    accion = db.Column(db.String(255), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('bitacoras', lazy=True))

class Especialidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

class Medico_Especialidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)

    medico = db.relationship('Medico', backref=db.backref('medico_especialidades', lazy=True))
    especialidad = db.relationship('Especialidad', backref=db.backref('medico_especialidades', lazy=True))

class Medicamentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer)
    fecha_vencimiento = db.Column(db.Date)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    hospital = db.relationship("Hospital", backref="medicamentos")
