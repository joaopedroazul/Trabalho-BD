import psycopg2


def connenction():
    conn = psycopg2.connect(database="postgres", user="postgres",
    password="postgres123",
    host="localhost", port="5432")
    return conn

def create_DB():
    conn = connenction()
    cur = conn.cursor()

    cur = conn.cursor()

    # criando o schema e as tabelas do banco de dados
    cur.execute('''CREATE SCHEMA IF NOT EXISTS "BD";''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Aluno (matricula serial PRIMARY KEY, nome varchar(100),senha varchar(100), curso varchar(100),email varchar(100),  is_admin boolean) ''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Departamento (departamento_id serial PRIMARY KEY, nome varchar(100)) ''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Professor (matricula serial PRIMARY KEY, nome varchar(100), 
	 fk_departamento_id integer REFERENCES "BD".Departamento (departamento_id)) ''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Disciplina (disciplina_id serial PRIMARY KEY, nome varchar(100),
                 fk_departamento_id integer REFERENCES "BD".Departamento (departamento_id)) ''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Turma (turma_id serial PRIMARY KEY, nome varchar(100),
                 fk_professor_id integer REFERENCES "BD".Professor (matricula),
				 fk_disciplina_id integer REFERENCES "BD".Disciplina (disciplina_id))''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Avaliacao (avaliacao_id serial PRIMARY KEY, nota integer, 
                mensagem varchar(500), fk_professor_id integer REFERENCES "BD".Professor (matricula),
				fk_disciplina_id integer REFERENCES "BD".Disciplina (disciplina_id),
                fk_aluno_id integer REFERENCES "BD".aluno (matricula)) ''')
    conn.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS "BD".Denuncia (denuncia_id serial PRIMARY KEY,  fk_avaliacao_id integer REFERENCES "BD".Avaliacao (avaliacao_id)) ''')

    # commit the changes
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()

