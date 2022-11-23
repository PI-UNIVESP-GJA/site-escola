from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db, login_manager
from app.models.tables import User, Alunos
from app.models.forms import FormLogin, FormCadastro, FormCadastroAluno, FormAtualizaAluno, FormConsultaAluno
from sqlalchemy import asc, and_

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
    error = None
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.tipo != 1:
            error = "Usuário não é professor"
        else:
            if user and user.senha == form.senha.data:
                login_user(user)
                return redirect(url_for("sistema"))
            else:
                error = "Credenciais incorretas!"
    return render_template('login.html', form = form, error=error)   

@app.route('/login2coord/', methods=["GET", "POST"])
def login2coord():
    error = None
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.tipo != 2:
            error = "Usuário não é coordenador"
        else:
            if user and user.senha == form.senha.data:
                login_user(user)
                return redirect(url_for("coordenacao"))
            else:
                error = "Credenciais incorretas!"
    return render_template('login2coord.html', form = form, error=error) 

@app.route('/login3aluno/', methods=["GET", "POST"])
def login3aluno():
    error = None
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.tipo != 3:
            error = "Usuário não é aluno"
        else:    
            if user and user.senha == form.senha.data:
                login_user(user)
                return redirect(url_for("sistema_aluno"))
            else:
                error = "Credenciais incorretas!"
    return render_template('login3aluno.html', form = form, error=error)     
    
@app.route('/sistema/<info>')
@app.route('/sistema/', defaults={'info':None}, methods=["GET", "POST"])
def sistema(info): 
    if current_user.is_anonymous == True:
        return render_template('index.html')
    else:
        alunos = Alunos.query.filter_by(professor_id=current_user.id).order_by(asc(Alunos.numero))
        return render_template('sistema.html', alunos = alunos)

@app.route('/sistema_aluno/<info>')
@app.route('/sistema_aluno/', defaults={'info':None}, methods=["GET", "POST"])
def sistema_aluno(info): 
    if current_user.is_anonymous == True:
        return render_template('index.html')
    else:
        alunos = Alunos.query.filter_by(nome=current_user.nome)
        return render_template('sistema_aluno.html', alunos = alunos)

@app.route('/consulta/<info>')
@app.route('/consulta/', defaults={'info':None}, methods=["GET", "POST"])
def consulta(info):
    if current_user.is_anonymous == True:
        return render_template('index.html')
    else: 
        form = FormAtualizaAluno()
        if form.validate_on_submit():
            alunos = Alunos.query.filter_by(professor_id=current_user.id).order_by(asc(Alunos.numero))
            form2 = FormConsultaAluno()
            for aluno in alunos:
                if(form2.numero.data != ""):
                    alunosNumero = Alunos.query.filter(and_(Alunos.professor_id == current_user.id, Alunos.numero == form2.numero.data)).all()
                    return render_template('consulta.html', alunos = alunosNumero, form = form2)
                elif(aluno.nome != ""):
                    alunosNome = Alunos.query.filter(and_(Alunos.professor_id == current_user.id, Alunos.nome == form2.nome.data)).all()
                    return render_template('consulta.html', alunos = alunosNome, form = form2)
    return render_template('consulta.html', form = form)

@app.route('/coordenacao/<info>')
@app.route('/coordenacao/', defaults={'info':None}, methods=["GET", "POST"])
def coordenacao(info):
    professores = User.query.filter_by(tipo=1).order_by(asc(User.id))
    return render_template('coordenacao.html', professores = professores)

@app.route('/delete/<int:aluno_id>', methods=["GET", "POST"])
def delete(aluno_id):
    if current_user.is_anonymous == True:
       return render_template('index.html')
    else:
        aluno_d = Alunos.query.filter_by(id=aluno_id).first()
        db.session.delete(aluno_d)
        db.session.commit()
        return redirect(url_for("sistema", aluno_id = aluno_id))

@app.route('/delete2/<int:professor_id>', methods=["GET", "POST"])
def delete2(professor_id):
        professor_d = User.query.filter_by(id=professor_id).first()
        db.session.delete(professor_d)
        db.session.commit()
        return redirect(url_for("coordenacao", professor_id = professor_id))

@app.route('/grafico/<int:professor_id>', methods=["GET", "POST"])
def grafico(professor_id):
    alunos = Alunos.query.filter_by(professor_id=professor_id).order_by(asc(Alunos.numero))
    url_grafico = "https://quickchart.io/chart?c={type:'line',data:{labels:["
    for aluno in alunos:
        url_grafico = url_grafico + "'" + aluno.nome + "',"
    url_grafico = url_grafico.rstrip(url_grafico[-1])    
    url_grafico = url_grafico + "],datasets:[{label:'Notas',data:["
    for aluno in alunos:
        url_grafico = url_grafico + aluno.nota + ","
    url_grafico = url_grafico.rstrip(url_grafico[-1])    
    url_grafico = url_grafico + "],fill:false,borderColor:'green'},{label:'Faltas',data:["
    for aluno in alunos:
        url_grafico = url_grafico + aluno.qtd_faltas + ","
    url_grafico = url_grafico.rstrip(url_grafico[-1])
    url_grafico = url_grafico + "],fill:false,borderColor:'blue'}]}}"
    return render_template('grafico.html', alunos = alunos, url_grafico=url_grafico)

@app.route('/update/<info>')
@app.route('/update/<int:aluno_id>', defaults={'info':None}, methods=["GET", "POST"])
def update(aluno_id, info):
    if current_user.is_anonymous == True:
        return render_template('index.html')
    else:
        form = FormCadastroAluno()
        aluno_e = Alunos.query.filter_by(id=aluno_id).first()

        form.numero.data = aluno_e.numero 
        form.nome.data = aluno_e.nome 
        form.classe.data = aluno_e.classe 
        form.materia.data = aluno_e.materia 
        form.nota.data = aluno_e.nota 
        form.aulas.data = aluno_e.qtd_aulas 
        form.faltas.data = aluno_e.qtd_faltas 
        form.bimestre.data = aluno_e.bimestre
        
        if form.validate_on_submit():
            form2 = FormAtualizaAluno()
            aluno_e.numero = str(form2.numero.data)
            aluno_e.nome = str(form2.nome.data)
            aluno_e.classe = str(form2.classe.data)
            aluno_e.materia = str(form2.materia.data)
            aluno_e.nota = str(form2.nota.data ) 
            aluno_e.qtd_aulas = str(form2.aulas.data)
            aluno_e.qtd_faltas = str(form2.faltas.data)
            aluno_e.bimestre = str(form2.bimestre.data)
            db.session.add(aluno_e)
            db.session.commit()
            return redirect(url_for("sistema", form = form2))
        return render_template('cadastro_aluno.html', form = form)  


@app.route('/cadastro/<int:tipo>', methods=["GET", "POST"])
def cadastro(tipo):
    form = FormCadastro()
    error = None
    if form.validate_on_submit():
        if form.senha.data == form.confirmar_senha.data:
            i = User(form.nome.data, form.email.data, form.senha.data, tipo)
            db.session.add(i)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            error = "Insira a mesma senha nos dois campos"
    return render_template('cadastro.html', form = form, error=error, tipo=tipo)


@app.route('/cadastro_aluno/<info>')
@app.route('/cadastro_aluno/', defaults={'info':None}, methods=["GET", "POST"])
def cadastro_aluno(info):
    if current_user.is_anonymous == True:
        return render_template('index.html')
    else:
        form = FormCadastroAluno()
        if form.validate_on_submit():
            i = Alunos(form.numero.data, form.nome.data, form.classe.data, current_user.id , form.materia.data, form.nota.data, form.aulas.data, form.faltas.data, form.bimestre.data)
            db.session.add(i)
            db.session.commit()
            form.numero.data = "" 
            form.nome.data = "" 
            form.classe.data = "" 
            form.materia.data = ""  
            form.nota.data = ""  
            form.aulas.data = ""  
            form.faltas.data = ""
            form.bimestre.data = ""  
        return render_template('cadastro_aluno.html', form = form)


@app.route('/logout/')
def logout():
    logout_user()
    error = "Sessão encerrada com sucesso"
    return render_template('index.html', error=error)