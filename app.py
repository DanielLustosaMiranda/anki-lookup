import json
import os
from src.services.reverso_service import ReversoScraperService
from tools.separar_json import separar_json
import csv

source = "english"
target = "portuguese"

reverso = ReversoScraperService()

palavra = input("Digite uma palvra: ")

resposta = input("1 - get context\n2 - get translation\n")

if resposta == "1":
    data = reverso.get_context(palavra, source, target)
elif resposta == "2":
    data = reverso.get_context(palavra, source, target)

if data and 'examples' in data:
    print(f"\n✅ Dados recebidos. Primeiro exemplo: {data['examples'][0]['source']}")
else:
    print("\n⚠️ Dados recebidos, mas parecem estar vazios ou em formato inesperado.")

if data:
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)  # Garante que 'data/' exista

    output_filename = os.path.join(output_dir, "output.json")

    print(f"\nTentando escrever em '{output_filename}'...")

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"🎉 Arquivo salvo com sucesso em: {output_filename}")
    except IOError as e:
        print(f"❌ ERRO CRÍTICO: Falha ao salvar arquivo.")
        print(f"   Detalhes: {e}")
        

separar_json()
# Caminho para o arquivo JSON
# Define o caminho absoluto do arquivo
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
caminho = os.path.join(root_dir, 'examples.json')

# Lê e imprime os dados
with open(caminho, 'r', encoding='utf-8') as f:
    exemplos = json.load(f)

for exemplo in exemplos:
    print(f"[{exemplo['id']}]")
    print(f"EN: {exemplo['source']}")
    print(f"PT: {exemplo['target']}")
    print("-" * 40)

# Entrada do usuário (ex: 0, 2, 5)
entrada = input("Digite os IDs separados por vírgula (ex: 0,2,5): ")
ids = [int(id.strip()) for id in entrada.split(',') if id.strip().isdigit()]

# Filtra os exemplos
filtrados = [
    (ex['source'], ex['target'])
    for ex in exemplos if ex['id'] in ids
]

# Caminho do CSV de saída
output_path = os.path.join(os.path.dirname(__file__), 'data', 'exemplos_filtrados.csv')

# Escreve o CSV com aspas em volta de cada campo
with open(output_path, 'a', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    #writer.writerow(['source', 'target'])  # Cabeçalho
    writer.writerows(filtrados)

print(f"✅ CSV criado com {len(filtrados)} linhas em:\n   {output_path}")