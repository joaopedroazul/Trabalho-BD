Projeto de Banco de Dados UnB

 etapas para rodar o projeto 

-Verifique se tem python instalado na sua máquina
  
- Abra o terminal no diretorio do programa e crie uma venv. (Ex Windows: python -m venv venv)

- Instale o Flask:
    'pip install flask'
    'pip install psycopg2'
    'pip install secrets'
    'pip install flask_session'

- Vá até o arquivo create.py altere as configurações do postgres
    conn = psycopg2.connect(database="postgres", user="postgres",
    password="postgres123",
    host="localhost", port="5432")

- No terminal rode o comando
    'python connection.py'



  

