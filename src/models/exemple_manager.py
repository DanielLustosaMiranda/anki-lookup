# src/models/exemplo_manager.py
import os
import json
import csv

class ExemploManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def salvar_exemplos(self, data):
        output_path = os.path.join(self.data_dir, 'output.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.separar_json()

    def separar_json(self):
        input_path = os.path.join(self.data_dir, 'output.json')
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Erro ao ler output.json: {e}")
            return

        translations = data.get('translations', [])
        examples = data.get('examples', [])

        with open(os.path.join(self.data_dir, 'translation.json'), 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        with open(os.path.join(self.data_dir, 'examples.json'), 'w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)

    def carregar_exemplos(self):
        path = os.path.join(self.data_dir, 'examples.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def filtrar_por_ids(self, exemplos, ids):
        return [ex for ex in exemplos if ex['id'] in ids]

    def salvar_csv(self, exemplos_filtrados):
        path = os.path.join(self.data_dir, 'exemplos_filtrados.csv')
        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows([(ex['source'], ex['target']) for ex in exemplos_filtrados])
