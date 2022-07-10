from flask import Flask, render_template, request, url_for, flash, redirect, session
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from sqlalchemy import ForeignKey

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config['SECRET_KEY'] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Aluno(db.Model):
    _tablename_ = 'aluno'
    ra = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(60), nullable=False)
    nascimento = db.Column(db.Integer)
    num_ser = db.Column(db.String(15))
    turma = db.Column(db.String(10))
    sexo = db.Column(db.String(10))
    situacao = db.Column(db.String(10))
    nome_mae = db.Column(db.String(60))
    profissao_mae = db.Column(db.String(40))
    localtrab_mae = db.Column(db.String(40))
    nasc_mae = db.Column(db.Integer)
    fone_mae = db.Column(db.Integer)
    nome_pai = db.Column(db.String(60))
    profissao_pai = db.Column(db.String(40))
    localtrab_pai = db.Column(db.String(40))
    nasc_pai = db.Column(db.Integer)
    fone_pai = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login')
def login():
    return render_template('login.html')


# ROTAS RELATIVAS A AUTENTICAÇÃO ===========================================#

# ROTA PARA AUTENTICAÇÃO NA ÁREA LOGADA
@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'master' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + 'logou com sucesso!')
        return redirect('/menu_area_logada.html')
    else:
        flash('Não logado. Tente novamente!')
        return redirect('/')

#ROTA PARA LOGOUT
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/')

# ROTA DIRETA PARA O MENU ÁREA LOGADA
@app.route('/menu_area_logada.html')
def menu_area_logada():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Login Obrigatório!')
        return redirect('/')
    return render_template('menu_area_logada.html', titulo='Menu Área Logada')

# FUNÇÃO GET ALUNO
def get_aluno(Aluno, ra):
    aluno = Aluno.query.filter_by(ra=ra).first()
    if aluno is None:
        abort(484)
    return aluno


@app.route('/pesquisar_aluno')
def pesquisar_aluno():
    lista_alunos = Aluno.query.all()
    return render_template('/pesquisar_aluno.html', alunos=lista_alunos)


@app.route('/cadastrar_aluno', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome_aluno = request.form['nome_aluno']
        nascimento = request.form['nascimento']
        num_ser = request.form['num_ser']
        turma = request.form['turma']
        sexo = request.form['sexo']
        situacao = request.form['situacao']
        nome_mae = request.form['nome_mae']
        profissao_mae = request.form['profissao_mae']
        localtrab_mae = request.form['localtrab_mae']
        nasc_mae = request.form['nasc_mae']
        fone_mae = request.form['fone_mae']
        nome_pai = request.form['nome_pai']
        profissao_pai = request.form['profissao_pai']
        localtrab_pai = request.form['localtrab_pai']
        nasc_pai = request.form['nasc_pai']
        fone_pai = request.form['fone_pai']

        if not nome_aluno or not nascimento:
            flash('O Nome e nascimento são Obrigatórios!')
        else:
            aluno = Aluno(nome_aluno=nome_aluno, nascimento=nascimento, num_ser=num_ser, turma=turma, sexo=sexo,
                          situacao=situacao, nome_mae=nome_mae, profissao_mae=profissao_mae,
                          localtrab_mae=localtrab_mae, nasc_mae=nasc_mae, fone_mae=fone_mae, nome_pai=nome_pai,
                          profissao_pai=profissao_pai, localtrab_pai=localtrab_pai, nasc_pai=nasc_pai,
                          fone_pai=fone_pai)
            db.session.add(aluno)
            db.session.commit()
            return redirect(url_for('pesquisar_aluno'))
    return render_template('/cadastrar_aluno.html')


# ROTA PARA A PAGINA DE CONSULTA ALUNO
@app.route('/<int:ra>')
def detalhe_aluno(ra):
    detalhe = get_aluno(Aluno, ra)
    return render_template('/consultar_aluno.html', detalhe_aluno=detalhe)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(post.title))
    return redirect(url_for('index'))

@app.route('/lista_presença')
def lista_presença():
    lista_alunos = Aluno.query.all()
    return render_template('/lista_presença.html', alunos=lista_alunos)

app.run(debug=True)