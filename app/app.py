# -*- coding: utf-8 -*-
from flask_login import LoginManager, login_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template, Response, json, abort
from config import app_config, app_active
from admin.admin import start_views
from functools import wraps
from controller.user import UserController
from controller.product import ProductController
config = app_config[app_active]


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    login_manager = LoginManager()
    login_manager.init_app(app)
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

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])
            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso')

        return verify_token

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return render_template('login.html', data={
            'status': 200,
            'msg': None,
            'type': None
            })
    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            if result.role == 4:
                return render_template('login.html', data={'status': 401, 'msg': 'Seu usuário não tem permissão para acessar o admin', 'type':2})
            else:
                login_user(result)
                return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': 1})

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
    @auth_token_required
    def get_products(limit=None):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
        }

        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(
                json.dumps(response, ensure_ascii=False),
                mimetype='application/json'), response['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    @auth_token_required
    def get_product(product_id):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
        }

        product = ProductController()
        response = product.get_product_by_id(product_id=product_id)

        return Response(
            json.dumps(response, ensure_ascii=False),
            mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
    def get_user_profile(user_id):
        header = {
            'access_token': request.headers['access_token'],
            'token_type': 'JWT'
            }
        user = UserController()
        response = user.get_user_by_id(user_id=user_id)
        return Response(json.dumps(
            response, ensure_ascii=False),
            mimetype='application/json'), response['status'], header

    @app.route('/login_api/', methods=['POST'])
    def login_api():
        header = {}
        user = UserController()
        email = request.json['email']
        password = request.json['password']
        result = user.login(email, password)
        code = 401
        response = {"message": "Usuário não autorizado", "result": []}
        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }
                header = {
                    "access_token": user.generate_auth_token(result),
                    "token_type": "JWT"
                }
                code = 200
                response["message"] = "Login realizado com sucesso"
                response["result"] = result
        return Response(json.dumps(
            response, ensure_ascii=False),
             mimetype='application/json'), code, header

    @app.route('/logout')
    def logout_send():
        logout_user()
        return render_template('login.html', data={
            'status': 200,
            'msg': 'Usuário deslogado',
            'type': 3
        })

    @login_manager.user_loader
    def loader_user(user_id):
        user = UserController()
        return user.get_admin_login(user_id)

    return app
