from flask import Flask, render_template, request, redirect, url_for,flash,session
from flask_session import Session
import psycopg2
import secrets
import json
import base64
from create import create_DB,connenction
secret = secrets.token_urlsafe(32)



app = Flask(__name__,template_folder='template')
app.secret_key = secret
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# cria o banco de dados e as tabelas 
create_DB()


# Rotas para Usuário
@app.route('/')
def index():  # put application's code here
	return render_template('index.html')


# Rotas para Usuário
@app.route('/indexlogado')
def indexlogado():  # put application's code here
    data_bd = index_aluno()
    if session['logged_in'] == True:
    	return render_template('indexlogado.html',data=data_bd)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		response = auth(request)
		if response:
			flash('Login realizado com sucesso!', 'success')
			return redirect(url_for('indexlogado'))
		else:
			flash('Credenciais incorretas. Tente novamente.', 'error')
	return render_template('login.html')


def auth(request):
    email = request.form.get('email')
    senha = request.form.get('senha')

    response = verificar_usuario(email, senha)

    if response:
        # Credenciais corretas, armazena as informações do usuário na sessão
        session['logged_in'] = True
        session['user_id'] = response[0]
        session['user_email'] = response[1]
        return True
    else:
        # Credenciais incorretas
        return False   

def verificar_usuario(email, senha):
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	cur.execute(
		'''SELECT matricula,email FROM "BD".aluno WHERE email = %s AND senha = %s''',
		(email, senha))

	result = cur.fetchone()
	# close the cursor and connection
	cur.close()
	conn.close()

	# Verifica se as credenciais estão corretas e retorna True ou False
	return result

    

@app.route('/logout')
def logout():
    # Lógica para fazer o logout do usuário
    session.clear()  # Limpa a sessão
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('login'))



@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        criarUsuario =  create_aluno()
        if criarUsuario :
            print('Estudante cadastrado com sucesso!', 200)
            return render_template('login.html')
        else:
            return render_template('user/cadastro.html')
    return render_template('cadastro.html')




@app.route('/aluno/index')
def index_aluno():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select * from "BD".aluno
''')

	# Fetch the data
	data = cur.fetchall()


	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return data

@app.route('/aluno/create', methods=['POST'])
def create_aluno():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nome = request.form['nome']
	email = request.form['email']
	matricula = request.form['matricula']
	curso = request.form['curso']
	password = request.form['senha']
	is_admin = False
	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".Aluno (matricula, nome,senha,curso,email,is_admin) \
		VALUES (%s, %s, %s, %s, %s, %s)''',
		( matricula, nome, password, curso,email ,is_admin))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return render_template('login.html')

@app.route('/aluno/update', methods=['PUT'])
def update_aluno():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	email = request.form['email']
	matricula = request.form['matricula']


	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".aluno SET email=%s WHERE  matricula=%s''', (email,  matricula))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/aluno/delete', methods=['DELETE'])
def delete_aluno():
	conn = connenction

	# Get the data from the form
	matricula = request.form['matricula']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".aluno  WHERE matricula=%s''', (matricula,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])

# Departamento 
@app.route('/departamento/index')
def index_depto():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select departamento_id,nome from "BD".departamento
''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/departamento/create', methods=['POST'])
def create_depto():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nome = request.form['nome']
	departamento_id = request.form['departamento_id']

	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".departamento (departamento_id, nome) \
		VALUES ( %s, %s)''',
		( departamento_id, nome))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/departamento/update', methods=['PUT'])
def update_depto():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	departamento_id = request.form['id']
	nome = request.form['nome']


	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".departamento SET nome=%s WHERE  departamento_id=%s''', (nome,departamento_id,))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/departamento/delete', methods=['DELETE'])
def delete_depto():
	conn = connenction

	# Get the data from the form
	departamento_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".departamento  WHERE departamento_id=%s''', (departamento_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])

# Professor 
@app.route('/professor/index')
def index_prof():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select professor_id,nome,matricula,fk_departamento_id from "BD".professor
''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/professor/create', methods=['POST'])
def create_prof():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nome = request.form['nome']
	professor_id = request.form['id']
	matricula = request.form['matricula']
	fk_departamento_id = request.form['fk_id']

	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".professor (professor_id,nome,matricula,fk_departamento_id) \
		VALUES ( %s, %s,%s, %s)''',
		( professor_id, nome, matricula, fk_departamento_id,))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/professor/update', methods=['PUT'])
def update_prof():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	professor_id = request.form['id']
	nome = request.form['nome']

	
	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".professor SET nome=%s WHERE  professor_id=%s''', (nome,professor_id,))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/professor/delete', methods=['DELETE'])
def delete_prof():
	conn = connenction

	# Get the data from the form
	professor_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".professor  WHERE professor_id=%s''', (professor_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])

# Disciplina 
@app.route('/disciplina/index')
def index_disciplina():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select disciplina_id,nome,codigo,fk_departamento_id from "BD".disciplina
''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/disciplina/create', methods=['POST'])
def create_disciplina():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nome = request.form['nome']
	disciplina_id = request.form['id']
	codigo = request.form['codigo']
	fk_departamento_id = request.form['fk_id']

	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".disciplina (disciplina_id,nome,codigo,fk_departamento_id) \
		VALUES ( %s, %s,%s, %s)''',
		( disciplina_id, nome, codigo, fk_departamento_id,))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/disciplina/update', methods=['PUT'])
def update_disciplina():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	disciplina_id = request.form['id']
	nome = request.form['nome']

	
	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".disciplina SET nome=%s WHERE  disciplina_id=%s''', (nome,disciplina_id,))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/disciplina/delete', methods=['DELETE'])
def delete_disciplina():
	conn = connenction

	# Get the data from the form
	disciplina_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".disciplina  WHERE disciplina_id=%s''', (disciplina_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])

# Turma 
@app.route('/turma/index')
def index_turma():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select turma_id,nome,fk_professor_id,fk_disciplina_id from "BD".turma''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/turma/create', methods=['POST'])
def create_turma():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nome = request.form['nome']
	turma_id = request.form['id']
	fk_professor_id = request.form['fk_pro_id']
	fk_disciplina_id = request.form['fk_dis_id']

	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".turma (turma_id,nome,fk_professor_id,fk_disciplina_id) \
		VALUES ( %s, %s,%s, %s)''',
		( turma_id,nome,fk_professor_id,fk_disciplina_id))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/turma/update', methods=['PUT'])
def update_turma():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	turma_id = request.form['id']
	nome = request.form['nome']


	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".turma SET nome=%s WHERE  turma_id=%s''', (nome,turma_id,))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/turma/delete', methods=['DELETE'])
def delete_turma():
	conn = connenction

	# Get the data from the form
	turma_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".turma WHERE turma_id=%s''', (turma_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])

# Avaliação
@app.route('/avaliacao/index')
def index_avaliacao():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id from "BD".avaliacao''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/avaliacao/create', methods=['POST'])
def create_avaliacao():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	nota = request.form['nota']
	avaliacao_id = request.form['id']
	mensagem = request.form['mensagem']
	fk_professor_id = request.form['fk_pro_id']
	fk_disciplina_id = request.form['fk_dis_id']

		# avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id from "BD".avaliacao
	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".avaliacao (avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id) \
		VALUES ( %s, %s, %s, %s, %s)''',
		( avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/avaliacao/update', methods=['PUT'])
def update_avaliacao():
	conn = connenction

	cur = conn.cursor()

	
	nota = request.form['nota']
	avaliacao_id = request.form['id']

		# avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id from "BD".avaliacao
	# Get the data from the form


	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".avaliacao SET nota=%s WHERE  avaliacao_id=%s''', (nota,avaliacao_id,))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])

@app.route('/avaliacao/delete', methods=['DELETE'])
def delete_avaliacao():
	conn = connenction

	# Get the data from the form
	avaliacao_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".avaliacao WHERE avaliacao_id=%s''', (avaliacao_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])


# Denuncia
@app.route('/denuncia/index')
def index_denuncia():
	# Connect to the database
	conn = connenction

	# create a cursor
	cur = conn.cursor()

	# Select all products from the table
	cur.execute('''select denuncia_id,fk_avaliacao_id from "BD".denuncia''')

	# Fetch the data
	data = cur.fetchall()

	# close the cursor and connection
	cur.close()
	conn.close()
	print(data)
	return json.dumps(data)

@app.route('/denuncia/create', methods=['POST'])
def create_denuncia():
	conn = connenction

	cur = conn.cursor()

	# Get the data from the form
	
	denuncia_id = request.form['id']
	fk_avaliacao_id = request.form['fk_id']
		# avaliacao_id,nota,mensagem,fk_professor_id,fk_disciplina_id from "BD".avaliacao
	# Insert the data into the table
	cur.execute(
		'''INSERT INTO "BD".denuncia (denuncia_id,fk_avaliacao_id) \
		VALUES ( %s, %s, %s, %s, %s)''',
		( denuncia_id,fk_avaliacao_id))

	# commit the changes
	conn.commit()
	# close the cursor and connection
	cur.close()
	conn.close()
	return json.dumps(['Sucesso'])

@app.route('/denuncia/delete', methods=['DELETE'])
def delete_denuncia():
	conn = connenction

	# Get the data from the form
	denuncia_id = request.form['id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".denuncia WHERE denuncia_id=%s''', (denuncia_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])




if __name__ == '__main__':
	app.run(debug=True)
