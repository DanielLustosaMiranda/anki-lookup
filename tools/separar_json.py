import json
import os
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

base_dir = os.path.join(root_dir, 'data')

input_path = os.path.join(base_dir, 'output.json')

# Leitura do arquivo JSON principal
with open(input_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

translations = data.get('translations', [])
examples = data.get('examples', [])

translations_path = os.path.join(base_dir, 'translation.json')
examples_path = os.path.join(base_dir, 'examples.json')

with open(translations_path, 'w', encoding='utf-8') as f_trans:
    json.dump(translations, f_trans, ensure_ascii=False, indent=2)

with open(examples_path, 'w', encoding='utf-8') as f_ex:
    json.dump(examples, f_ex, ensure_ascii=False, indent=2)

print("✅ Arquivos 'translation.json' e 'examples.json' foram criados na pasta 'data/' com sucesso.")
