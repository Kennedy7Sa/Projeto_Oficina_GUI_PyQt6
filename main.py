from PyQt6 import uic,QtWidgets
from PySide6.QtWidgets import QMessageBox
import sqlite3
import icons_rc

#importante não esqueça de baixar a lib do pyside6 e converter os icones 
#com o comando pyside6-rcc nome_do_arquivo.qrc -o icons_rc.py
 

#parte de cadastro de costureiros 

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

    try:
        if nome and telefone and endereco: #validando campos 
            banco = sqlite3.connect('bd_oficina.db')
            cursor = banco.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS Costureiro (NomeCostureiro text,TelefoneCostureiro text,Endereco text)')
            cursor.execute("INSERT INTO COSTUREIRO (NomeCostureiro ,TelefoneCostureiro ,Endereco)VALUES (?,?,?)",(nome,telefone,endereco))
            banco.commit()
            banco.close()
            print('Dados salvos com sucesso!')
            listar_costureiros()
        else:
            print('Preencha todos os campos ')
    except sqlite3.Error  as erro:
        print(f'Erro ao inserir os dados: {erro}')

def excluir_costureiro():
    linha = tela_cadastro.tabelaCostureiro.currentRow()  # linha selecionada

    if linha == -1:
        print("Nenhuma linha selecionada.")
        return

    # Pegando o ID da linha (coluna 0, assumindo que ID seja a primeira coluna)
    id_item = tela_cadastro.tabelaCostureiro.item(linha, 0)

    if id_item is None:
        print("ID não encontrado.")
        return

    id = id_item.text()

    try:
        resposta = QMessageBox.question(
        None,
        "Confirmar Exclusão",
        "Tem certeza que deseja excluir este item?",
        QMessageBox.Yes | QMessageBox.No
    )
        if resposta == QMessageBox.Yes:
            banco = sqlite3.connect('bd_oficina.db')
            cursor = banco.cursor()
            cursor.execute("DELETE FROM Costureiro WHERE idCostureiro=?", (id,))
            banco.commit()
            banco.close()

            print(f"Registro com ID {id} excluído com sucesso!")

            listar_costureiros()  # Atualiza a tabela na interface
        else:
            print('Exclusão cancelada ')

    except sqlite3.Error as erro:
        print(f"Erro ao excluir o registro: {erro}")


def preencher_campos():
    linha = tela_cadastro.tabelaCostureiro.currentRow()

    if linha != -1:
        tela_cadastro.txtNome.setText(tela_cadastro.tabelaCostureiro.item(linha, 1).text())
        tela_cadastro.txtTelefone.setText(tela_cadastro.tabelaCostureiro.item(linha, 2).text())
        tela_cadastro.txtEndereco.setText(tela_cadastro.tabelaCostureiro.item(linha, 3).text())

def editar_dados():
    linha = tela_cadastro.tabelaCostureiro.currentRow()

    if linha == -1:
        print("Nenhuma linha selecionada para edição.")
        return

    id_item = tela_cadastro.tabelaCostureiro.item(linha, 0)
    if id_item is None:
        print("ID não encontrado.")
        return

    id = id_item.text()
    nome = tela_cadastro.txtNome.text()
    telefone = tela_cadastro.txtTelefone.text()
    endereco = tela_cadastro.txtEndereco.text()

    try:
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor()
        cursor.execute("""
            UPDATE Costureiro
            SET NomeCostureiro=?, TelefoneCostureiro=?, Endereco=?
            WHERE idCostureiro=?
        """, (nome, telefone, endereco, id))
        banco.commit()
        banco.close()

        print(f"Registro com ID {id} atualizado com sucesso!")
        listar_costureiros()

    except sqlite3.Error as erro:
        print(f"Erro ao editar o registro: {erro}")


#********Cadastro de produção 
def preencher_combo_box_costureiro(tela):
    banco = sqlite3.connect('bd_oficina.db')
    cursor = banco.cursor() 

    cursor.execute("SELECT idCostureiro, NomeCostureiro FROM Costureiro")
    nomes = cursor.fetchall()

    tela.Cmb_selecionar_costureiro.clear()

    for id_costureiro, nome in nomes:
        # Exibe o nome, mas guarda o id (útil para salvar depois)
        tela.Cmb_selecionar_costureiro.addItem(nome, id_costureiro)

    banco.close()


def preencher_combo_box_peca(tela):
    banco = sqlite3.connect('bd_oficina.db')
    cursor = banco.cursor() 

    cursor.execute("SELECT idPeca, NomePeca FROM Pecas")
    nomes = cursor.fetchall()

    tela.Cmb_selecionar_peca.clear()

    for id_peca, nome_peca in nomes:
        # Exibe o nome, mas guarda o id (útil para salvar depois)
        tela.Cmb_selecionar_peca.addItem(nome_peca, id_peca)

    banco.close()

def ao_mudar_aba(index):#função para acaptar a mudança de aba
    if index == 1:  # índice da tab_2
        preencher_combo_box_costureiro(tela_cadastro)
        preencher_combo_box_peca(tela_cadastro)
        listar_producao()

def salvar_producao():
    qtd_entregue = tela_cadastro.txt_qtd_entregue.text()
    data_entrega = tela_cadastro.txt_data_entrega.text()
    
    # Pegando os dados armazenados (idCostureiro e idPeca)
    id_costureiro = tela_cadastro.Cmb_selecionar_costureiro.currentData()
    id_peca = tela_cadastro.Cmb_selecionar_peca.currentData()
    
    # Verificando qual radio button está marcado
    if tela_cadastro.rdb_pago.isChecked():
        status = "PAGO"
    elif tela_cadastro.rdb_em_eberto.isChecked():
        status = "EM ABERTO"
    else:
        status = None

    if not (qtd_entregue and data_entrega and id_costureiro and id_peca and status):
        print("Preencha todos os campos corretamente.")
        return

    try:
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Producao (
                idProducao INTEGER PRIMARY KEY AUTOINCREMENT,
                idCostureiro INTEGER,
                idPeca INTEGER,
                QuantidadeEntregue INTEGER,
                DataEntrega TEXT,
                Status TEXT
            )
        ''')

        cursor.execute('''
            INSERT INTO Producao (idCostureiro, idPeca, Quantidade_entregue, Data_Entregue, Status)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_costureiro, id_peca, qtd_entregue, data_entrega, status))

        banco.commit()
        banco.close()
        print("Produção salva com sucesso!")

    except sqlite3.Error as erro:
        print(f"Erro ao salvar produção: {erro}")


def listar_producao():
    try:
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor()

        consulta = """
            SELECT 
                Producao.idProducao,
                Producao.data_entregue, 
                Costureiro.NomeCostureiro, 
                Pecas.NomePeca, 
                Producao.quantidade_entregue,
                Producao.status
            FROM Producao
            JOIN Costureiro ON Producao.idCostureiro = Costureiro.idCostureiro
            JOIN Pecas ON Producao.idPeca = Pecas.idPeca
        """

        cursor.execute(consulta)
        dados_lidos = cursor.fetchall()

        tela_cadastro.tabela_producao.setRowCount(len(dados_lidos))
        tela_cadastro.tabela_producao.setColumnCount(6)
       

        for i in range(len(dados_lidos)):
            for j in range(6):
                tela_cadastro.tabela_producao.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

        banco.close()

    except sqlite3.Error as erro:
        print(f"Erro ao listar produção: {erro}")

def preencher_campos_producao():
    linha = tela_cadastro.tabela_producao.currentRow()
    if linha == -1:
        return

    # Pegando os dados diretamente da tabela
    data_entrega = tela_cadastro.tabela_producao.item(linha, 1).text()
    nome_costureiro = tela_cadastro.tabela_producao.item(linha, 2).text()
    nome_peca = tela_cadastro.tabela_producao.item(linha, 3).text()
    qtd = tela_cadastro.tabela_producao.item(linha, 4).text()
    status = tela_cadastro.tabela_producao.item(linha, 5).text()

    tela_cadastro.txt_data_entrega.setText(data_entrega)
    tela_cadastro.txt_qtd_entregue.setText(qtd)

    # Selecionar o costureiro e a peça correta no ComboBox
    index_costureiro = tela_cadastro.Cmb_selecionar_costureiro.findText(nome_costureiro)
    tela_cadastro.Cmb_selecionar_costureiro.setCurrentIndex(index_costureiro)

    index_peca = tela_cadastro.Cmb_selecionar_peca.findText(nome_peca)
    tela_cadastro.Cmb_selecionar_peca.setCurrentIndex(index_peca)

    # Setar o radio button correto
    if status == "PAGO":
        tela_cadastro.rdb_pago.setChecked(True)
    elif status == "EM ABERTO":
        tela_cadastro.rdb_em_eberto.setChecked(True)

def editar_producao():
    linha = tela_cadastro.tabela_producao.currentRow()
    if linha == -1:
        print("Selecione uma linha para editar.")
        return

    # Pegando o ID da produção (assumindo que você adicionou a coluna oculta 5 com ID)
    id_item = tela_cadastro.tabela_producao.item(linha, 0)
    if not id_item:
        print("ID da produção não encontrado.")
        return
    id_producao = id_item.text()

    qtd_entregue = tela_cadastro.txt_qtd_entregue.text()
    data_entrega = tela_cadastro.txt_data_entrega.text()
    id_costureiro = tela_cadastro.Cmb_selecionar_costureiro.currentData()
    id_peca = tela_cadastro.Cmb_selecionar_peca.currentData()

    if tela_cadastro.rdb_pago.isChecked():
        status = "PAGO"
    elif tela_cadastro.rdb_em_eberto.isChecked():
        status = "EM ABERTO"
    else:
        status = None

    if not (qtd_entregue and data_entrega and id_costureiro and id_peca and status):
        print("Preencha todos os campos corretamente.")
        return

    try:
        banco = sqlite3.connect('bd_oficina.db')
        cursor = banco.cursor()

        cursor.execute("""
            UPDATE Producao
            SET idCostureiro=?, idPeca=?, Quantidade_entregue=?, Data_Entregue=?, Status=?
            WHERE idProducao=?
        """, (id_costureiro, id_peca, qtd_entregue, data_entrega, status, id_producao))

        banco.commit()
        banco.close()
        print("Produção atualizada com sucesso!")
        listar_producao()

    except sqlite3.Error as erro:
        print(f"Erro ao atualizar produção: {erro}")






app = QtWidgets.QApplication([])
tela_cadastro=uic.loadUi("OficinaDeCostura.ui")
tela_cadastro.pushButton.clicked.connect(salvar_dados)
tela_cadastro.btn_salvar_producao.clicked.connect(salvar_producao)
tela_cadastro.btnExcluir.clicked.connect(excluir_costureiro)
tela_cadastro.tabelaCostureiro.cellClicked.connect(preencher_campos)
tela_cadastro.btnEditar.clicked.connect(editar_dados)
tela_cadastro.tabela_producao.cellClicked.connect(preencher_campos_producao)
tela_cadastro.btn_editar_producao.clicked.connect(editar_producao)


# Conectando a troca de abas
tela_cadastro.tabWidget.currentChanged.connect(ao_mudar_aba)



listar_costureiros()

tela_cadastro.tabWidget.setCurrentIndex(0)  # <- Força iniciar na primeira aba
tela_cadastro.show()
app.exec()
