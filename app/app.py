# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template
from config import app_config, app_active
from admin.admin import start_views
from controller.user import UserController
config = app_config[app_active]
from flask_sqlalchemy import SQLAlchemy

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(config.APP)
    start_views(app, db)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return 'Aqui entrara a tela de login'

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']
        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorreto', 'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui entrara a tela de recuperação de senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form['email'])
        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'Erro ao enviar e-mail de recuperação'})

    @app.route('/profile/<int:id>/action/<action>/')
    def profile(id, action):
        if action == 'action1':
            return 'Ação action1 usuário de ID %d' % id
        elif action == 'action2':
            return 'Ação action2 usuário de ID %d' % id
        elif action == 'action3':
            return 'Ação action3 usuário de ID %d' % id

    @app.route('/profile/', methods=['POST'])
    def create_profile():
        username = request.form['username']
        password = request.form['password']

        return 'Essa rota possui um método POST e criará um usuário com os dados de usuário %s e senha %s' % (username, password)

    @app.route('/profile/<int:id>/', methods=['PUT'])
    def edital_total_profile(id):
        username = request.form['username']
        password = request.form['password']

        return 'Essa rota possui um método PUT e editará o nome do usuário para %s e a senha para %s' % (username, password)

    return app
