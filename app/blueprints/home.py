from flask import Blueprint


home = Blueprint(
    'home',
    __name__,
    template_folder='views',
    )


@home.route('/')
def index():
    return 'Meu primeiro run'
