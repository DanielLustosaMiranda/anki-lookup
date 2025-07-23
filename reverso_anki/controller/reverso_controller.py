# src/controllers/reverso_controller.py
from reverso_anki.services.reverso_service import ReversoScraperService
from reverso_anki.models.exemple_manager import ExemploManager
from reverso_anki.services.anki_deck_manager import AnkiDeckManager
import os

class ReversoController:
    def __init__(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
        os.makedirs(root_dir, exist_ok=True)

        self.scraper = ReversoScraperService()
        self.exemplo_manager = ExemploManager(root_dir)
        self.exemplos = []

    def buscar_exemplos(self, palavra, source, target):
        data = self.scraper.get_context(palavra, source, target)
        if not data or 'examples' not in data:
            return []

        self.exemplo_manager.salvar_exemplos(data)
        self.exemplos = self.exemplo_manager.carregar_exemplos()
        return self.exemplos

    def salvar_csv(self, ids):
        selecionados = self.exemplo_manager.filtrar_por_ids(self.exemplos, ids)
        self.exemplo_manager.salvar_csv(selecionados)

    def listar_decks(self):
        try:
            import urllib.request, json
            req = {
                "action": "deckNames",
                "version": 6
            }
            data = json.dumps(req).encode("utf-8")
            response = urllib.request.urlopen(
                urllib.request.Request("http://localhost:8765", data=data)
            )
            decks = json.load(response)["result"]
            return decks
        except Exception as e:
            print("Erro ao listar decks:", e)
            return []

    def enviar_para_anki(self, ids, deck_name):
        selecionados = self.exemplo_manager.filtrar_por_ids(self.exemplos, ids)
        if not selecionados:
            return False

        manager = AnkiDeckManager(deck_name)
        cards = [{'Front': ex['source'], 'Back': ex['target']} for ex in selecionados]
        return manager.add_cards(cards)

    def limpar_sessao(self):
        self.exemplo_manager.apagar_sessao()
