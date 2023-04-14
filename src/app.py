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

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()