import json
import subprocess
import os
from typing import Dict, Optional
from utils.run_api import run_api

class ReversoScraperService:
    
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        self.scraper_script_path = os.path.join(project_root, 'reverso_scraper', 'get_data.js')

        if not os.path.isfile(self.scraper_script_path):
            raise FileNotFoundError(f"Script do scraper não encontrado em: {self.scraper_script_path}")
        
    def get_context(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict]:
        funcao = 'context'
        command = [
            'node',
            self.scraper_script_path,
            funcao,
            text,
            source_lang,
            target_lang
        ]

        print(f"🐍 Python: Executando comando -> {' '.join(command)}")
        return run_api(command)
        
    def get_translation(self, text: str, transSource: str, transTarget: str) -> Optional[Dict]:
        funcao = 'translation'
        command = [
            'node',
            self.scraper_script_path,
            funcao,
            text,
            transSource,
            transTarget
        ]

        print(f"🐍 Python: Executando comando -> {' '.join(command)}")
        return run_api(command)


if __name__ == "__main__":
    scprap = ReversoScraperService()
    print("--- Início do teste ---")

    # Vamos usar uma palavra diferente para garantir que não estamos vendo um resultado em cache
    data = scprap.get_context("blue", "english", "portuguese")
    print(data)
    
    # Imprime o início do resultado para confirmar que temos dados
    if data and 'examples' in data:
        print(f"\n✅ Dados recebidos. Primeiro exemplo: {data['examples'][0]['source']}")
    else:
        print("\n⚠️ Dados recebidos, mas parecem estar vazios ou em formato inesperado.")

    if data:
        output_filename = "reverso_output.json"
        
        # --- INÍCIO DO CÓDIGO DE DEPURAÇÃO ---
        
        # 1. Onde o Python acha que está agora?
        current_working_directory = os.getcwd()
        print(f"\n[DEBUG] Diretório de trabalho atual: {current_working_directory}")

        # 2. Onde exatamente ele vai tentar criar o arquivo?
        absolute_file_path = os.path.abspath(output_filename)
        print(f"[DEBUG] Caminho absoluto do arquivo a ser criado: {absolute_file_path}")
        
        # --- FIM DO CÓDIGO DE DEPURAÇÃO ---

        print(f"\nTentando escrever em '{output_filename}'...")

        try:
            formatted_text = json.dumps(data, indent=2, ensure_ascii=False)
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            
            print(f"🎉 Arquivo '{output_filename}' criado com sucesso!")
            print("[DICA] Verifique o diretório listado acima para encontrar seu arquivo.")

        except IOError as e:
            print(f"❌ ERRO CRÍTICO: Não foi possível escrever no arquivo. Verifique as permissões da pasta.")
            print(f"   Detalhes do erro: {e}")

    else:
        print("\n❌ A variável 'data' está vazia. O arquivo não foi criado.")

    print('\n--- Fim do teste ---')
