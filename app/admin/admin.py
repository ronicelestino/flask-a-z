# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from model.role import Role
from model.user import User
from model.category import Category
from model.product import Product


def start_views(app, db):
    admin = Admin(app, name='Meu Estoque', template_mode='bootstrap3')

    admin.add_view(ModelView(Role, db.session, "Funções", category="Usuários"))
    admin.add_view(ModelView(User, db.session, "Usuário", category="Usuários"))
    admin.add_view(ModelView(Category, db.session, "Categorias", category="Produtos"))
    admin.add_view(ModelView(Product, db.session, "Produtos", category="Produtos"))