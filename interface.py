from PyQt6 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

# Variável global para armazenar o ID do produto
numero_id = 0

# Conexão com o banco de dados MySQL
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="38439KFDsnf@",
    database="cadastro_produtos"
)

def editar_dados():
    # Função para editar os dados de um produto
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()  # Obtém a linha selecionada na tabela

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")  # Seleciona todos os IDs dos produtos
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]  # Obtém o ID do produto selecionado
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))  # Seleciona todos os dados do produto pelo ID
    produto = cursor.fetchall()
    tela_editar.show()  # Exibe a tela de edição

    numero_id = valor_id  # Armazena o ID do produto na variável global

    # Preenche os campos de edição com os dados do produto
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))

def salvar_dados_editados():
    # Função para salvar os dados editados de um produto
    global numero_id
    # Obtém os valores digitados nos campos de edição
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    # Atualiza os dados no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo, descricao, preco, categoria, numero_id))
    banco.commit()
    # Fecha as janelas de edição e atualização
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()  # Atualiza a tabela de produtos

def excluir_dados():
    # Função para excluir um produto
    linha = segunda_tela.tableWidget.currentRow()  # Obtém a linha selecionada na tabela
    segunda_tela.tableWidget.removeRow(linha)  # Remove a linha da tabela
    print(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")  # Seleciona todos os IDs dos produtos
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]  # Obtém o ID do produto selecionado
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))  # Exclui o produto pelo ID
    banco.commit()

def gerar_pdf():
    # Função para gerar um PDF com os dados dos produtos
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"  # Seleciona todos os dados dos produtos
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)


    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CÓDIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "PREÇO")
    pdf.drawString(410,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        # Incrementa a posição vertical para cada linha de dados
        y = y + 50
        # Desenha os dados do produto no PDF em diferentes posições horizontais
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    # Salva o PDF
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")

def funcao_principal():
    # Função principal para capturar dados do formulário e inserir no banco de dados
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = ""

    # Verifica qual categoria foi selecionada no formulário
    if formulario.radioButton.isChecked():
        print("Categoria Informatica foi selecionado")
        categoria = "Informatica"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Alimentos foi selecionado")
        categoria = "Alimentos"
    else:
        print("Categoria Eletrônico foi selecionado")
        categoria = "Eletrônicos"

    # Exibe os dados capturados no console
    print("Código", linha1)
    print("Descrição", linha2)
    print("Preço", linha3)

    # Insere os dados no banco de dados
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()

    # Limpa os campos do formulário
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    # Função para exibir a segunda tela com a lista de produtos
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    # Configura a tabela da segunda tela com o número de linhas e colunas
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    # Preenche a tabela com os dados dos produtos
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

# Configurações iniciais do aplicativo
app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
segunda_tela = uic.loadUi("listar_dados.ui")
tela_editar = uic.loadUi("menu_editar.ui")

# Conecta os botões às suas respectivas funções
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)

# Exibe o formulário inicial
formulario.show()
app.exec()