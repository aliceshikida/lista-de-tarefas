from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(200))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def realizar_login():
    # Pegando do formulário os nomes corretos
    nome_usuario = request.form['username']
    senha = request.form['password']  # se quiser validar, pode usar depois

    # Para agora, só aceita qualquer login que informe nome e senha (sem validação)
    if nome_usuario and senha:
        session['usuario'] = nome_usuario
        return redirect(url_for('listar_tarefas'))
    else:
        return "Usuário ou senha inválidos", 403

@app.route('/tarefas')
def listar_tarefas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tarefas = Tarefa.query.all()
    return render_template('tarefas.html', tarefas=tarefas, usuario=session['usuario'])

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    nova_tarefa = Tarefa(
        titulo=request.form['titulo'],
        descricao=request.form['descricao']
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for('listar_tarefas'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if request.method == 'POST':
        tarefa.titulo = request.form['titulo']
        tarefa.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('listar_tarefas'))
    return render_template('editar.html', tarefa=tarefa)

@app.route('/apagar/<int:id>')
def apagar_tarefa(id):
    tarefa = Tarefa.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('listar_tarefas'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
