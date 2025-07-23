from PyQt6.QtWidgets import QApplication
from reverso_anki.view.reverso_app import ReversoApp
from reverso_anki.controller.reverso_controller import ReversoController
import sys

def main():
    app = QApplication(sys.argv)
    controller = ReversoController()
    window = ReversoApp(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
