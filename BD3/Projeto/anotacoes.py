import mysql.connector
import datetime

# Funções de Consulta no banco
def insere_valores(titulo_assunto, corpo_texto, data_anotada):
    sql = 'INSERT INTO anotação (titulo_assunto, corpo_texto, data_anotada) VALUES (%s,%s,%s)'
    valores = (titulo_assunto,corpo_texto,data_anotada)
    meu_cursor.execute(sql,valores)
    meu_bd.commit()
    return meu_cursor.lastrowid # Retorna o id da consulta

def listar_todos():
    meu_cursor.execute('select id, titulo_assunto from anotação')
    resultados = meu_cursor.fetchall()
    return resultados

def listar_id(id):
    sql = 'select * from anotação where id={}'.format(id)
    meu_cursor.execute(sql)
    resultados = meu_cursor.fetchall()
    return resultados

def exclui_valores(id):
    sql = 'DELETE FROM anotação WHERE id={}'.format(id)
    meu_cursor.execute(sql)
    meu_bd.commit()


# Função para o tratamento de Dados na consulta
def print_anotacao(id):
    resultados = listar_id(id)
    id = resultados[0][0]
    assunto = resultados[0][1]
    data = resultados[0][2]
    anotacao = resultados[0][3]
    # Cabecalho
    print('\t\t', end='')
    print(('='*21) + 'ANOTAÇÃO' + ('='*22))
    if id >= 10:
        print('\t\t|ID:', id,(' '*42)+'|')
    else:
        print('\t\t|ID:', id,(' '*43)+'|')
    print('\t\t|Assunto: '+assunto+(40-len(assunto))*' '+'|')
    print('\t\t|Data:', data, ' '*32+'|')

    # Anotação
    cont = 0
    anotacao_completa = []
    diferenca = 300 - (len(anotacao)) #Descobre a quantidade de espaços em branco necessário
    anotacao_completa += anotacao
    anotacao_completa += ' ' * diferenca
    linha = '='*52
    print('\t\t'+linha)
    for i in anotacao_completa:
        if cont == 0:
            print('\t\t|', end='')
        if cont < 50:
            print(i, end='')
        else:
            print('|')
            print('\t\t|{}'.format(i), end='')
            cont = 0
        cont += 1
    print('|')
    print('\t\t'+linha)


# Funções para as opções do Usuário
def mostrar_anotacoes():
    lista = listar_todos()
    print('\n\t ID    Assunto')
    print('\t==============================')
    for i in lista:
        print('\t',end='')
        print(i[0],' - ', i[1])
    print()

def inserir_anotacao(titulo, anotacao):
    id = insere_valores(titulo, anotacao, datetime.date.today())
    print_anotacao(id)
    print('\t\tA anotação foi inserida com sucesso!')

def excluir_anotacao(id):
    exclui_valores(id)
    print('\t\tA anotação de ID: {}, foi excluida com sucesso!'.format(id))


# Execução
try:
    meu_bd = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='1212',
                                     database='anotacoes')
    meu_cursor = meu_bd.cursor()

    while True:
        print('Menu de opções: ')
        print('[0] - Sair'
              '\n[1] - Inserir anotação'
              '\n[2] - Excluir anotação'
              '\n[3] - Consultar anotação'
              '\n[4] - Mostrar anotações')
        opcao = input('Escolha uma opção → ')

        if opcao == '0':
            break
        elif opcao == '1':
            titulo = input('\tAssunto: ')
            anotacao = input('\tAnotação: ')
            inserir_anotacao(titulo[:25], anotacao[:300])
        elif opcao == '2':
            id = int(input('\tID da anotação: '))
            excluir_anotacao(id)
        elif opcao == '3':
            id = int(input('\tID da anotação: '))
            print_anotacao(id)
        elif opcao == '4':
            mostrar_anotacoes()
        else:
            print('\tErro! - Opção inválida')
except ValueError:
    print('ERRO! - O valor digitado é inválido')
except IndexError:
    print('ERRO! - Possivelmente o ID digitado não existe')
except:
    print('ERRO! - Algo Inesperado ocorreu')
    raise



