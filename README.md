# ClinicProyect2

Instalar Python y configurar ruta PATH

Instalaciones necesarias para el pip: (pip install nombre)
- flask
- flask-login
- flask-WTF
- virtualenv
- psycopg2
- psycopg2-binary 
- Flask-SQLAlchemy


Para correr el proyecto solamente se debe de ejecutar el archivo
app.py desde la terminal y colocar el link generado en google



-------------------------------------PARA LA BASE DE DATOS------------------------------

Si no tienes la base de datos creala apartir de estas tablas y con el into values que contiene se puede verificar si si funciono la conexión
CREATE TABLE Hospital (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255)
);

CREATE TABLE Especialidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Medico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    numero_colegiado VARCHAR(255),
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES Hospital(id)
);

CREATE TABLE Medico_Especialidad (
    medico_id INTEGER,
    especialidad_id INTEGER,
    PRIMARY KEY (medico_id, especialidad_id),
    FOREIGN KEY (medico_id) REFERENCES Medico(id),
    FOREIGN KEY (especialidad_id) REFERENCES Especialidad(id)
);

CREATE TABLE Paciente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    masa_corporal DECIMAL,
    altura DECIMAL,
    peso DECIMAL,
    adicciones TEXT,
    enfermedades_hereditarias TEXT,
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES Hospital(id)
);

CREATE TABLE Diagnostico (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER,
    medico_id INTEGER,
    enfermedad VARCHAR(255),
    tratamiento VARCHAR(255),
    fecha_hora TIMESTAMP,
    resultado VARCHAR(255),
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id),
    FOREIGN KEY (medico_id) REFERENCES Medico(id)
);

CREATE TABLE Transladomedico (
    id SERIAL PRIMARY KEY,
    medico_id INTEGER,
    hospital_origen_id INTEGER,
    hospital_destino_id INTEGER,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (medico_id) REFERENCES Medico(id),
    FOREIGN KEY (hospital_origen_id) REFERENCES Hospital(id),
    FOREIGN KEY (hospital_destino_id) REFERENCES Hospital(id)
);

CREATE TABLE Medicamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cantidad INTEGER,
    fecha_vencimiento DATE,
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES Hospital(id)
);

CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(255),
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES Hospital(id)
);

CREATE TABLE Bitacora (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    accion VARCHAR(255),
    fecha_hora TIMESTAMP,
    descripcion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);


/*--------------- Llenar tablas ---------------------*/

INSERT INTO Hospital (nombre, direccion) VALUES 
    ('Hospital San Juan', 'Calle 1, Zona 5'),
    ('Hospital Central', 'Avenida 2, Zona 10'),
    ('Hospital del Sur', 'Calle 5, Zona 1'),
    ('Hospital Infantil', 'Avenida 7, Zona 12'),
    ('Hospital de la Mujer', 'Calle 8, Zona 15');







