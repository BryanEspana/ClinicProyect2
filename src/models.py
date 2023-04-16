from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Paciente(db.Model):
    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    masa_corporal = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    adicciones = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.Text, nullable=False)


class Medico(db.Model):
    id_medico = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    num_colegiado = db.Column(db.String(15), nullable=False)
    especialidad = db.Column(db.String(40), nullable=False)
    id_lugar = db.Column(db.Integer, db.ForeignKey('lugar.id_lugar'), nullable=False)


class Enfermedad(db.Model):
    id_enfermedad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15), nullable=False)


class UtencilioMed(db.Model):
    id_utencilio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    cant_optima = db.Column(db.Integer, nullable=False)


class Lugar(db.Model):
    id_lugar = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    localizacion = db.Column(db.Text, nullable=False)


class Usuario(db.Model):
    id_medico = db.Column(db.Integer, db.ForeignKey('medico.id_medico'), primary_key=True)
    usuario = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable=False)


class Inventario(db.Model):
    id_inventario = db.Column(db.Integer, primary_key=True)
    id_lugar = db.Column(db.Integer, db.ForeignKey('lugar.id_lugar'), nullable=False)
    id_utencilio = db.Column(db.Integer, db.ForeignKey('utencilio_med.id_utencilio'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    expiracion = db.Column(db.Date, nullable=False)


class Historial(db.Model):
    id_historial = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    herencia = db.Column(db.Text, nullable=False)
    tratamiento = db.Column(db.Text, nullable=False)
    evolucion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    id_lugar = db.Column(db.Integer, db.ForeignKey('lugar.id_lugar'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_paciente'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medico.id_medico'), nullable=False)
    id_enfermedad = db.Column(db.Integer, db.ForeignKey('enfermedad.id_enfermedad'), nullable=False)

