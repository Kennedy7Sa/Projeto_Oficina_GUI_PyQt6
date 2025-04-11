from PyQt6 import uic,QtWidgets
import sqlite3

def salvar_dados():
    nome = tela_cadastro.txtNome.text()
    telefone = tela_cadastro.txtTelefone.text()
    endereco = tela_cadastro.txtEndereco.text()
    endereco = tela_cadastro.txtEndereco.text()

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

tela_cadastro.show()
app.exec()
# def salvar_dados():
#     nome = txtEndereco.text()