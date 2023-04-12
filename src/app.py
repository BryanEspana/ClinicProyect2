from flask import Flask, render_template
from config import config
from models import db
from models import Hospital, Medico, Paciente, Diagnostico, Transladomedico, Medicamentos, Usuario, Bitacora, Especialidad, Medico_Especialidad


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    db.init_app(app)
    register_routes(app)

    return app

def register_routes(app):
    from models import Hospital, Medico, Paciente, Diagnostico, Transladomedico, Medicamentos, Usuario, Bitacora, Especialidad, Medico_Especialidad

    @app.route('/')
    def index():
        return render_template('auth/main.html')

    @app.route('/auth/login')
    def login():
        return render_template('auth/login.html')

    @app.route('/test_db')
    def test_db():
        hospitals = Hospital.query.all()
        hospital_names = [hospital.nombre for hospital in hospitals]
        if hospital_names:
            return f"Conexión exitosa a la base de datos y se encontraron {len(hospital_names)} hospitales: {', '.join(hospital_names)}"
        else:
            return "No se encontraron hospitales en la base de datos"



app = create_app()

if __name__ == '__main__':
    app.run()