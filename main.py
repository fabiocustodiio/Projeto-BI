import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTreeWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import mysql.connector
from datetime import datetime

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.setWindowTitle("PULSEWEBM - SISTEMA DE GERENCIAMENTO")
        self.setWindowIcon(QIcon("icon.ico"))
        self.login_button.clicked.connect(self.check_login)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Teste20ser24",  # Substitua 'your_password' pela sua senha correta
                database="cadastro_produto"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()

            if result:
                self.main_window = MainWindow()
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Erro', 'Usuário ou senha incorretos.')
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f"Erro ao conectar ao banco de dados: {err}")
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f"Erro inesperado: {e}")

class Cadastro(QDialog):
    def __init__(self, main_window):
        super(Cadastro, self).__init__()
        loadUi("cadastro.ui", self)
        self.setWindowTitle("PULSEWEBM - SISTEMA DE GERENCIAMENTO")
        self.setWindowIcon(QIcon("icon.ico"))

        # Configurações iniciais
        self.data_input.setText(datetime.now().strftime('%Y-%m-%d'))
        self.id_input.setReadOnly(True)  # Campo ID não editável

        self.cadastrar_button.clicked.connect(self.cadastrar_produto)
        self.cancelar_button.clicked.connect(self.close)
        self.deletar_button.clicked.connect(self.deletar_produto)

        # Referência à MainWindow para atualizar a lista de produtos
        self.main_window = main_window

    def cadastrar_produto(self):
        descricao = self.produto_input.text()
        numero_serie = self.serie_input.text()
        data_cadastro = datetime.now().strftime('%Y-%m-%d')

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Teste20ser24",  # Substitua 'your_password' pela sua senha correta
                database="cadastro_produto"
            )
            cursor = db.cursor()
            cursor.execute("INSERT INTO produtos (descricao, numero_serie, data_cadastro) VALUES (%s, %s, %s)", (descricao, numero_serie, data_cadastro))
            db.commit()
            QMessageBox.information(self, 'Sucesso', 'Produto cadastrado com sucesso!')
            self.id_input.setText(str(cursor.lastrowid))  # Atualiza o ID com o último ID inserido
            self.main_window.load_produtos()  # Atualiza a lista de produtos
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f"Erro ao conectar ao banco de dados: {err}")
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f"Erro inesperado: {e}")

    def deletar_produto(self):
        numero_serie = self.numero_serie_deletar.text()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Teste20ser24",  # Substitua 'your_password' pela sua senha correta
                database="cadastro_produto"
            )
            cursor = db.cursor()
            cursor.execute("DELETE FROM produtos WHERE numero_serie=%s", (numero_serie,))
            db.commit()
            QMessageBox.information(self, 'Sucesso', 'Produto deletado com sucesso!')
            self.main_window.load_produtos()  # Atualiza a lista de produtos
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f"Erro ao conectar ao banco de dados: {err}")
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f"Erro inesperado: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("PULSEWEBM - SISTEMA DE GERENCIAMENTO")
        self.setWindowIcon(QIcon("icon.ico"))
        self.cadastro_button.clicked.connect(self.abrir_cadastro)
        self.verificar_button.clicked.connect(self.verificar_serie)
        self.sobre_button.clicked.connect(self.sobre)
        self.sair_button.clicked.connect(self.close)
        self.load_produtos()

    def abrir_cadastro(self):
        cadastro_dialog = Cadastro(self)  # Passa a referência da MainWindow
        cadastro_dialog.exec_()

    def verificar_serie(self):
        numero_serie = self.serie_input.text()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Teste20ser24",  # Substitua 'your_password' pela sua senha correta
                database="cadastro_produto"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM produtos WHERE numero_serie=%s", (numero_serie,))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, 'Verificado', 'Número de série encontrado.')
            else:
                QMessageBox.warning(self, 'Não encontrado', 'Número de série não encontrado.')
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f"Erro ao conectar ao banco de dados: {err}")
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f"Erro inesperado: {e}")

    def load_produtos(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Teste20ser24",  # Substitua 'your_password' pela sua senha correta
                database="cadastro_produto"
            )
            cursor = db.cursor()
            cursor.execute("SELECT id, descricao, numero_serie, data_cadastro FROM produtos")
            results = cursor.fetchall()

            self.treeWidget.clear()
            self.treeWidget.setHeaderLabels(['ID', 'Produto', 'N/Serie', 'Data Cadastro'])

            for row in results:
                id = str(row[0])
                descricao = row[1]
                numero_serie = row[2]
                data_cadastro = row[3].strftime('%Y-%m-%d')  # Convertendo datetime para string
                item = QTreeWidgetItem([id, descricao, numero_serie, data_cadastro])
                self.treeWidget.addTopLevelItem(item)
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Erro', f"Erro ao conectar ao banco de dados: {err}")
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f"Erro inesperado: {e}")

    def sobre(self):
        QMessageBox.information(self, 'Sobre', 'Sistema de Cadastro de Produtos\nDesenvolvido por Fabio Custodio\n 	PulseWebM')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    login = Login()
    login.show()
    sys.exit(app.exec_())
