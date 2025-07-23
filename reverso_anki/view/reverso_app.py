from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QGridLayout,
    QHBoxLayout, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt

from reverso_anki.enums.languages import SupportedLanguages

class ReversoApp(QWidget):
    def __init__(self, controller):
        super().__init__()   # inicializa QMainWindow
        self.controller = controller
        self.exemplos = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Anki Lookup")
        self.resize(750, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Linha 0: Idiomas
        idioma_layout = QHBoxLayout()
        idioma_layout.addWidget(QLabel("De:"))
        self.source_lang = QComboBox()
        self.source_lang.addItems(SupportedLanguages)
        self.source_lang.setCurrentText("english")
        idioma_layout.addWidget(self.source_lang)
        idioma_layout.addSpacing(20)

        idioma_layout.addWidget(QLabel("Para:"))
        self.target_lang = QComboBox()
        self.target_lang.addItems(SupportedLanguages)
        self.target_lang.setCurrentText("portuguese")
        idioma_layout.addWidget(self.target_lang)
        main_layout.addLayout(idioma_layout)

        # Linha 1: Palavra
        palavra_layout = QHBoxLayout()
        palavra_layout.addWidget(QLabel("Palavra:"))
        self.palavra_entry = QLineEdit()
        palavra_layout.addWidget(self.palavra_entry)
        self.buscar_btn = QPushButton("Buscar exemplos")
        self.buscar_btn.clicked.connect(self.on_buscar)
        palavra_layout.addWidget(self.buscar_btn)
        main_layout.addLayout(palavra_layout)

        # Linha 2: Resultados
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        main_layout.addWidget(self.resultado_text)

        # Linha 3: IDs + Salvar
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("IDs (ex: 0,2,4):"))
        self.ids_entry = QLineEdit()
        id_layout.addWidget(self.ids_entry)
        self.salvar_btn = QPushButton("💾 Salvar CSV")
        self.salvar_btn.clicked.connect(self.on_salvar_csv)
        id_layout.addWidget(self.salvar_btn)
        main_layout.addLayout(id_layout)

        # Linha 4: Anki
        anki_layout = QHBoxLayout()
        anki_layout.addWidget(QLabel("Deck:"))
        self.deck_menu = QComboBox()
        self.deck_menu.addItem("Carregando...")
        anki_layout.addWidget(self.deck_menu)
        self.anki_btn = QPushButton("📥 Enviar para Anki")
        self.anki_btn.clicked.connect(self.on_enviar_anki)
        anki_layout.addWidget(self.anki_btn)
        main_layout.addLayout(anki_layout)

        # Linha 5: Limpar sessão
        self.limpar_btn = QPushButton("🧹 Limpar sessão")
        self.limpar_btn.clicked.connect(self.on_limpar_sessao)
        main_layout.addWidget(self.limpar_btn)

        # Linha 6: Status
        self.status_label = QLabel("Pronto.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Carrega decks
        self.listar_decks()

    def set_status(self, msg: str):
        self.status_label.setText(msg)
        QApplication.processEvents()

    def listar_decks(self):
        self.set_status("Carregando decks...")
        decks = self.controller.listar_decks()
        if decks:
            self.deck_menu.clear()
            self.deck_menu.addItems(decks)
            self.set_status("Decks carregados.")
        else:
            self.deck_menu.clear()
            self.deck_menu.addItem("Nenhum deck encontrado")
            self.set_status("Erro ao carregar decks.")

    def on_buscar(self):
        palavra = self.palavra_entry.text().strip()
        source = self.source_lang.currentText()
        target = self.target_lang.currentText()

        if not palavra:
            QMessageBox.warning(self, "Aviso", "Digite uma palavra.")
            return

        self.set_status("🔍 Buscando exemplos...")
        self.resultado_text.clear()

        exemplos = self.controller.buscar_exemplos(palavra, source, target)

        if not exemplos:
            self.set_status("⚠️ Nenhum exemplo encontrado.")
            QMessageBox.information(self, "Sem resultados", "Nenhum exemplo encontrado.")
            return

        self.exemplos = exemplos
        for ex in exemplos:
            self.resultado_text.append(f"[{ex['id']}] Source: {ex['source']}")
            self.resultado_text.append(f"          Target: {ex['target']}")
            self.resultado_text.append("-" * 40)

        self.set_status("✅ Pronto.")

    def on_salvar_csv(self):
        entrada = self.ids_entry.text().strip()
        if not entrada:
            QMessageBox.warning(self, "Aviso", "Digite os IDs a salvar.")
            return

        try:
            ids = [int(i.strip()) for i in entrada.split(",")]
        except ValueError:
            QMessageBox.warning(self, "Aviso", "IDs inválidos.")
            return

        self.controller.salvar_csv(ids)
        QMessageBox.information(self, "Salvo", f"Exemplos com IDs {ids} salvos em CSV.")
        self.set_status("✅ Exemplos salvos.")

    def on_enviar_anki(self):
        entrada = self.ids_entry.text().strip()
        if not entrada:
            QMessageBox.warning(self, "Aviso", "Digite os IDs a enviar.")
            return

        try:
            ids = [int(i.strip()) for i in entrada.split(",")]
        except ValueError:
            QMessageBox.warning(self, "Aviso", "IDs inválidos.")
            return

        deck = self.deck_menu.currentText()
        sucesso = self.controller.enviar_para_anki(ids, deck)

        if sucesso:
            QMessageBox.information(self, "Sucesso", f"Exemplos com IDs {ids} enviados para o Anki no deck '{deck}'.")
            self.set_status("✅ Cartões enviados para o Anki.")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao enviar para o Anki.")
            self.set_status("❌ Erro ao enviar cartões para o Anki.")

    def on_limpar_sessao(self):
        reply = QMessageBox.question(
            self, "Confirmar", "Tem certeza que deseja apagar todos os arquivos da sessão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.limpar_sessao()
            QMessageBox.information(self, "Sessão limpa", "Todos os arquivos foram apagados.")
            self.set_status("🧹 Sessão limpa.")
