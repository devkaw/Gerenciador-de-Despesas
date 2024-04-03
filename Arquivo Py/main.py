import sqlite3


# Criando nossa conexão, cursor e banco de dados
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY,
    categoria TEXT NOT NULL,
    nome TEXT NOT NULL,
    valor REAL NOT NULL
)
''')

inserir_informacoes = """
INSERT INTO despesas (id, categoria, nome, valor) VALUES (?, ?, ?, ?)
"""


# O nosso print de instruções e nossas funções para o funcionamento do programa 
print('Bem vindos ao Gerenciador de Despesas! Nele, você pode adicionar despesas, remover despesas e ver as despesas que já foram adicionadas. Todas as suas alterações serão salvas em um banco de dados! Isso quer dizer que quando você fechar o programa, suas alterações continuarão lá!')
def verificar_id_existente(id):
    cursor.execute("SELECT id FROM despesas WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    return resultado is not None

def filtro_categoria(categoria):
    cursor.execute("SELECT * FROM despesas WHERE categoria = ?", (categoria,))
    filter = cursor.fetchall()
    return filter

def filtro_id(id):
    cursor.execute("SELECT * FROM despesas WHERE id = ?", (id,))
    filterr = cursor.fetchone()
    return filterr

def busca_despesas():
    cursor.execute("SELECT * FROM despesas")
    busquinha = cursor.fetchall()
    return busquinha

def calcular_soma_despesas():
    cursor.execute("SELECT SUM(valor) FROM despesas")
    soma = cursor.fetchone()[0]
    return soma

continuacao = 'y'


# O nosso loop e as opções que podem ser escolhidas
while continuacao.lower() == 'y':
    print('''
1) Adicionar despesa
2) Remover despesa da lista de despesas
3) Ver despesas
4) Ver despesas filtrando algo
5) Ver somatória dos valores de todas as despesas
''')
    print("=" * 50)
    
    opcao = int(input('Digite a opção desejada: '))


# Todo o código para caso o usuário escolher a 1º opção
    if opcao == 1:
        id = int(input('Digite o ID que deseja dar para a sua despesa (ele precisa ter no máximo 3 caracteres): '))
        if verificar_id_existente(id):
            print('ERROR: Esse ID já esta registrado no banco de dados. Se preferir, visualize os IDs já existentes para escolher um não existente.')
            print("=" * 50)
            continue
        categoria = input('Digite a categoria que deseja dar para a sua despesa: ')
        nome = input('Digite o nome que deseja dar para a sua despesa: ')
        valor = float(input('Digite o valor da despesa: ').replace(',','.'))
        cursor.execute(inserir_informacoes, (id, categoria, nome, valor))
        conexao.commit()
        print('Despesa adicionada no banco de dados com sucesso!')
        print("=" * 50)


# Todo o código para caso o usuário escolher a 2º opção
    elif opcao == 2:
        busca = busca_despesas()
        if busca:
            print('Lista de despesas: ')
            for despesa in busca:
                print("ID:", despesa[0])
                print("Categoria:", despesa[1])
                print("Nome:", despesa[2])
                print("Valor:", despesa[3])
                print("-" * 30)
                
        else:
            print("Não há nenhuma despesa adicionada.")
            print("=" * 50)
            continue
        print("=" * 50)
        remover = int(input('Digite o ID da despesa que deseja remover: '))
        if not verificar_id_existente(remover):
            print('ERROR: Esse ID não está registrado no banco de dados. Se preferir, visualize os IDs já existentes para escolher um não existente.')
            print("=" * 50)
            continue
        cursor.execute("DELETE FROM despesas WHERE id = ?", (remover,))
        conexao.commit()
        print('Despesa removida do banco de dados com sucesso!')
        print("=" * 50)


# Todo o código para caso o usuário escolher a 3º opção
    elif opcao == 3:
        busca = busca_despesas()
        if busca:
            print('Lista de despesas: ')
            for despesa in busca:
                print("ID:", despesa[0])
                print("Categoria:", despesa[1])
                print("Nome:", despesa[2])
                print("Valor:", despesa[3])
                print("-" * 30)
        print("=" * 50)



# Todo o código para caso o usuário escolher a 4º opção
    elif opcao == 4:
        print('''
1) Filtrar por ID
2) Filtrar por categoria
''')
        filtro = int(input('Digite a opção desejada: '))
        if filtro == 1:
            id_desejado = int(input('Digite o ID que deseja filtrar: '))
            id_filtrado = filtro_id(id_desejado)
            print("=" * 50)
            if id_filtrado:
                print("Despesa encontrada:")
                print("ID:", id_filtrado[0])
                print("Categoria:", id_filtrado[1])
                print("Nome:", id_filtrado[2])
                print("Valor:", id_filtrado[3])
            else:
                print('Nenhuma despesa encontrada com o ID informado.')
            print('=' * 50)

        if filtro == 2:
            categoria_desejada = input('Digite a categoria que deseja filtrar: ')
            categoria_filtrada = filtro_categoria(categoria_desejada)
            print("=" * 50)
            if categoria_filtrada:
                print(f'Despesas encontradas na categoria {categoria_desejada}:')
                for despesinha in categoria_filtrada:
                    print("Despesa encontrada:")
                    print("ID:", despesinha[0])
                    print("Categoria:", despesinha[1])
                    print("Nome:", despesinha[2])
                    print("Valor:", despesinha[3])
                    print("-" * 30)
                    
            else:
                print(f'Nenhuma despesa encontrada na categoria {categoria_desejada}.') 
            print("=" * 50)  


# Todo o código para caso o usuário escolher a 5º opção    
    elif opcao == 5:
        soma_despesas = calcular_soma_despesas()
        print(f'A soma dos valores de todas as despesas é de: R${soma_despesas:.2f}.')
        print("=" * 50)


# Pergunta de continuação
    continuacao = input('Você deseja continuar o programa? Digite Y para sim e N para não: ')


# Caso o usuário não apertar y
print('Obrigado por usar meu programa!')
input('Pressione qualquer tecla para fechar: ')
conexao.close()

