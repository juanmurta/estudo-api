import sqlite3

with sqlite3.connect('artistas.db') as conexao:
    # criar a conexão com o banco
    sql = conexao.cursor()
    # comando para criar tabela
    sql.execute('create table banda(nome text, estilo text, membro integer);')
    # inserindo dados
    sql.execute('insert into banda(nome, estilo, membro) values ("Banda 1", "Rock", 3)')
    nome = input('Digite o nome da banda: ')
    estilo = input('Digite o estilo da banda: ')
    quantidade_integrantes = int(input('Digite a quantidade de integrantes: '))
    #
    sql.execute('insert into banda values(?, ?, ?)', [nome, estilo, quantidade_integrantes])
    # # salvando alterações no banco
    conexao.commit()

    # exibir dados no console
    bandas = sql.execute('select * from banda;')
    for banda in bandas:
        print(banda)
