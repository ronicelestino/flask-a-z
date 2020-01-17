# -*- coding: utf-8 -*-
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template, Response, json
from config import app_config, app_active
from admin.admin import start_views
from controller.user import UserController
from controller.product import ProductController
config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(config.APP)
    start_views(app, db)
    Bootstrap(app)
    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Origin', '*')
        response.headers.add('Access-Controll-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Controll-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return render_template('login.html', message="Essa é uma mensagemque veio da rota")

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']
        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={
                'status': 401,
                'msg': 'Dados de usuário incorreto',
                'type': None
            })

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui entrara a tela de recuperação de senha'

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form['email'])
        if result:
            return render_template('recovery.html', data={
                'status': 200,
                'msg': 'Erro ao enviar e-mail de recuperação'
            })


    @app.route('/products/', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    def get_products(limit=None):
        header = {}

        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(
                json.dumps(response, ensure_ascii=False),
                mimetype='application/json'), response['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    def get_product(product_id):
        header = {}

        product = ProductController()
        response = product.get_product_by_id(product_id=product_id)

        return Response(
            json.dumps(response, ensure_ascii=False),
            mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    def get_user_profile(user_id):
        header = {}

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header

    return app
