import json
import os

def separar_json():
    # Caminho da raiz do projeto
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Caminho da pasta 'data'
    base_dir = os.path.join(root_dir, 'data')

    # Caminho do arquivo de entrada
    input_path = os.path.join(base_dir, 'output.json')

    # Leitura do JSON principal
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {input_path}")
        return
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar JSON em: {input_path}")
        return

    # Extração dos dados
    translations = data.get('translations', [])
    examples = data.get('examples', [])

    # Caminhos de saída
    translations_path = os.path.join(base_dir, 'translation.json')
    examples_path = os.path.join(base_dir, 'examples.json')

    # Escrita dos arquivos
    with open(translations_path, 'w', encoding='utf-8') as f_trans:
        json.dump(translations, f_trans, ensure_ascii=False, indent=2)

    with open(examples_path, 'w', encoding='utf-8') as f_ex:
        json.dump(examples, f_ex, ensure_ascii=False, indent=2)

    print("✅ Arquivos 'translation.json' e 'examples.json' foram criados na pasta 'data/' com sucesso.")
