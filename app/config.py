"""    
CSRF_ENABLED = habilita o uso de criptografia em sessões do Flask
SECRET = Será usada em alguns momentos para criar chaves e valores criptografados
TEMPLATE_FOLDER = Caminho do local em que os arquivos de template do projeto ficarão    
ROOT_DIR = Caminho do local em que a raiz do projeto se encontra  
APP = Constante que receberá a propiedade do app 
TESTING Constante que habilitao ambiente de teste no Flask
DEBUG = Do mesmo jeito que TESTING, esta constante habilita os debugs dque o python exibe no console de execução    
IP_HOST =  Constante que informa o IP da maquina em que estamos rodando o projeto
PORT_HOST = Define a porta da aplicação
URL_MAIN  = Une a o IP com a PORT_HOST para gerar o endereço principal da sua aplicação ex: http://localhost:8000
app_config = Possue três subclasses que determina qual tipo de ambiente usaremos
app_active = Receberá um dos três valores: development , testing e production . Esse valor será atribuído através de uma variável de ambiente, ou seja, poderemos trocá-lo dinamicamente. Usamos a função
"""

import os
import random
import string


class Config(object):
    CSRF_ENABLED = True
    SECRET = 'ysb_92=qe#djf8%ng+a*#4rt#5%3*4k5%i2bck*gn@w3@f&-&'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'template')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = NotImplemented


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 5000
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s' % (IP_HOST, PORT_HOST)


app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'Production': ProductionConfig()
}

app_active = os.getenv('FLASK_ENV')
