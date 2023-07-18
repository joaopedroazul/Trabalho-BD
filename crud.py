from flask import Flask, request
import json
import base64
import psycopg2
from create import create_aluno

def connenction():
    conn = psycopg2.connect(database="postgres", user="postgres",
    password="postgres123",
    host="localhost", port="5432")
    return conn

def index_aluno(tabela):
    if tabela.upper == 'ALUNO':
        # Connect to the database
        conn = connenction() 

        # create a cursor
        cur = conn.cursor()

        # Select all products from the table
        cur.execute('''SELECT * FROM "BD".Aluno''')

        # Fetch the data
        data = cur.fetchall()

        array = []
        for x in data:
            if x[3] != None:
                array.append([x[0],x[1],x[2], base64.b64encode(x[3]).decode('ascii')])
            else:
                array.append([x[0],x[1],x[2],'None'])	

        # close the cursor and connection
        cur.close()
        conn.close()
        return json.dumps(array)


def create(tabela):
    if tabela.upper == 'ALUNO':
        create_aluno()


def update():
	conn = psycopg2.connect(database="postgres", user="postgres",
	password="postgres123",
	host="localhost", port="5432")
	cur = conn.cursor()

	cur = conn.cursor()

	# Get the data from the form
	nome = request.form['nome']
	codigo = request.form['codigo']
	disciplina_id = request.form['disciplina_id']

	# Update the data in the table
	cur.execute(
		'''UPDATE "BD".disciplina SET nome=%s,\
		codigo=%s WHERE disciplina_id=%s''', (nome, codigo, disciplina_id))

	# commit the changes
	conn.commit()
	return json.dumps(['Sucesso'])


def delete():
	conn = psycopg2.connect(database="postgres", user="postgres",
	password="postgres123",
	host="localhost", port="5432")
	cur = conn.cursor()

	# Get the data from the form
	disciplina_id = request.form['disciplina_id']

	# Delete the data from the table
	cur.execute('''DELETE FROM "BD".disciplina  WHERE disciplina_id=%s''', (disciplina_id,))

	# commit the changes
	conn.commit()

	# close the cursor and connection
	cur.close()
	conn.close()

	return json.dumps(['Sucesso'])
