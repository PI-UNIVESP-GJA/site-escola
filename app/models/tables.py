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

class Alunos(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key = True)
    numero = db.Column(db.Integer)
    nome = db.Column(db.String, unique=True)
    classe = db.Column(db.String)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    professor = db.relationship('User', foreign_keys=professor_id)
    materia = db.Column(db.String)
    nota = db.Column(db.String)
    qtd_aulas = db.Column(db.String)
    qtd_faltas = db.Column(db.String)



    def __init__(self, numero, nome, classe, professor_id, materia, nota, qtd_aulas, qtd_faltas):
        self.numero = numero
        self.nome = nome
        self.classe = classe
        self.professor_id = professor_id
        self.materia = materia
        self.nota = nota
        self.qtd_aulas = qtd_aulas
        self.qtd_faltas = qtd_faltas

    def __repr__(self):
        return "<Aluno %r>" % self.nome
