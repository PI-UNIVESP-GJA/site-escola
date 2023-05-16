from app import db


class User(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    senha = db.Column(db.String)
    tipo = db.Column(db.Integer)

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    
    def get_id(self):
        return str(self.id)
    

    def __init__(self, nome, email, senha, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def __repr__(self):
        return "<Professor %r>" % self.nome