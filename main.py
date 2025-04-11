from PyQt6 import uic,QtWidgets
import sqlite3

def listar_costureiros():
    try:
        
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor() 
        cursor.execute('SELECT * FROM Costureiro')
        dados_lidos = cursor.fetchall()
        tela_cadastro.tabelaCostureiro.setRowCount(len(dados_lidos))
        tela_cadastro.tabelaCostureiro.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0,4):
                tela_cadastro.tabelaCostureiro.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 
        banco.close()


    except sqlite3.Error  as erro:
        print(f'Erro exibir dados: {erro}')

def salvar_dados():
    nome = tela_cadastro.txtNome.text()
    telefone = tela_cadastro.txtTelefone.text()
    endereco = tela_cadastro.txtEndereco.text()
    endereco = tela_cadastro.txtEndereco.text()
    listar_costureiros()

    try:
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Costureiro (NomeCostureiro text,TelefoneCostureiro text,Endereco text)')
        cursor.execute("INSERT INTO COSTUREIRO (NomeCostureiro ,TelefoneCostureiro ,Endereco)VALUES (?,?,?)",(nome,telefone,endereco))
        banco.commit()
        banco.close()
        print('Dados salvos com sucesso!')

    except sqlite3.Error  as erro:
        print(f'Erro ao inserir os dados: {erro}')




app = QtWidgets.QApplication([])
tela_cadastro=uic.loadUi("OficinaDeCostura.ui")
tela_cadastro.pushButton.clicked.connect(salvar_dados)
listar_costureiros()
tela_cadastro.show()
app.exec()
# def salvar_dados():
#     nome = txtEndereco.text()