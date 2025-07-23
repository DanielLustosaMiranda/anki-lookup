from aqt import mw
from aqt.utils import showInfo
from .controller.reverso_controller import ReversoController
from .view.reverso_app import ReversoApp

def main():
    controller = ReversoController()
    app = ReversoApp(mw, controller)
    # Exemplo simples, se quiser pode fazer algo mais complexo, como mostrar janela etc
    showInfo("Addon Reverso iniciado!")
