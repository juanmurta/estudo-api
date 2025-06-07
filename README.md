# API de Blog - Estudo de API REST com Flask

## Descrição do Projeto
Este projeto é uma API REST para um sistema de blog, desenvolvida com Flask e SQLAlchemy. A API permite gerenciar autores e postagens, com autenticação JWT para proteger os endpoints.

## Tecnologias Utilizadas
- Python
- Flask
- SQLAlchemy
- JWT (JSON Web Tokens)
- SQLite

## Estrutura do Banco de Dados
O projeto utiliza SQLite como banco de dados, com duas tabelas principais:
- **Autor**: Armazena informações dos autores (id, nome, email, senha, admin)
- **Postagem**: Armazena as postagens do blog (id, título, id do autor)

## Configuração e Instalação
1. Clone o repositório
2. Instale as dependências:
   ```
   pip install flask flask-sqlalchemy pyjwt requests
   ```
3. Inicialize o banco de dados:
   ```
   python estrutura_banco.py
   ```
4. Execute a aplicação:
   ```
   python app.py
   ```

## Autenticação
A API utiliza autenticação JWT (JSON Web Tokens). Para acessar os endpoints protegidos:
1. Faça login através do endpoint `/login` com credenciais básicas (username e password)
2. Utilize o token retornado no header `x-access-token` para as requisições subsequentes

Exemplo de autenticação (usando o script `autorizacao_request.py`):
```python
from requests.auth import HTTPBasicAuth
import requests

# Obter token
resultado = requests.get('http://localhost:5000/login', auth=('juan', '123456'))
token = resultado.json()['token']

# Usar token para acessar endpoint protegido
resultado_autores = requests.get('http://localhost:5000/autores', 
                                headers={'x-access-token': token})
print(resultado_autores.json())
```

## Endpoints da API

### Autenticação
- **POST /login**: Autentica um usuário e retorna um token JWT

### Postagens
- **GET /**: Lista todas as postagens
- **GET /postagem/{id}**: Obtém uma postagem específica pelo ID
- **POST /postagem**: Cria uma nova postagem
- **PUT /postagem/{id}**: Atualiza uma postagem existente
- **DELETE /postagem/{id}**: Exclui uma postagem

### Autores
- **GET /autores**: Lista todos os autores
- **GET /autores/{id}**: Obtém um autor específico pelo ID
- **POST /autores**: Cria um novo autor
- **PUT /autores/{id}**: Atualiza um autor existente
- **DELETE /autores/{id}**: Exclui um autor

## Observações
- Todos os endpoints (exceto `/login`) requerem autenticação via token JWT
- O token JWT expira após 30 minutos
- Por padrão, um usuário administrador é criado durante a inicialização do banco de dados:
  - Nome: juan
  - Senha: 123456
