from flask import Blueprint, render_template, request, redirect
from flask_login import login_user
from controller.user import UserController


login = Blueprint(
    'login',
    __name__,
    template_folder='views',
    )


@login.route('/login/')
def login():
    return render_template(
        'login.html',
        data={
            'status': 200,
            'msg': None,
            'type': None
            })

@login.route('/login/', methods=['POST'])
def login_post():
    user = UserController()

    email = request.form['email']
    password = request.form['password']

    result = user.login(email, password)

    if result:
        if result.role == 4:
            return render_template(
                'login.html',
                data={
                    'status': 401,
                    'msg': 'Seu usuário não tem permissão\
                            para acessar o admin',
                    'type': 2
                    })
        else:
            login_user(result)
            return redirect('/admin')
    else:
        return render_template(
            'login.html',
            data={
                'status': 401,
                'msg': 'Dados de usuário incorretos',
                'type': 1
                })
