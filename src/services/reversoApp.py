from src.services.reverso_service import ReversoScraperService
from src.services.anki_deck_manager import AnkiDeckManager
from tools.separar_json import separar_json
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv # Importação adicionada para uso em salvar_csv

class ReversoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tradutor com Reverso")

        self.reverso = ReversoScraperService()
        self.exemplos = []

        # --- Linha 1: Idiomas ---
        tk.Label(root, text="Idioma origem:").grid(row=0, column=0, sticky="w")
        self.source_lang = ttk.Combobox(root, values=["english", "french", "spanish", "german"], width=15)
        self.source_lang.set("english")
        self.source_lang.grid(row=0, column=1)

        tk.Label(root, text="Idioma destino:").grid(row=0, column=2, sticky="w")
        self.target_lang = ttk.Combobox(root, values=["portuguese", "english", "french", "spanish"], width=15)
        self.target_lang.set("portuguese")
        self.target_lang.grid(row=0, column=3)

        # --- Linha 2: Palavra ---
        tk.Label(root, text="Palavra:").grid(row=1, column=0, sticky="w")
        self.palavra_entry = tk.Entry(root, width=40)
        self.palavra_entry.grid(row=1, column=1, columnspan=3, pady=5, sticky="we")

        # --- Linha 3: Buscar ---
        self.buscar_btn = tk.Button(root, text="Buscar exemplos", command=self.buscar_exemplos)
        self.buscar_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # --- Linha 4: Resultados ---
        self.resultado_text = scrolledtext.ScrolledText(root, height=15, width=80)
        self.resultado_text.grid(row=3, column=0, columnspan=4, padx=5)

        # --- Linha 5: IDs ---
        tk.Label(root, text="IDs para salvar/enviar (ex: 0,2,4):").grid(row=4, column=0, sticky="w", pady=5)
        self.ids_entry = tk.Entry(root, width=30)
        self.ids_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        # --- Linha 6: Botões Salvar CSV e Enviar Anki ---
        self.salvar_btn = tk.Button(root, text="Salvar selecionados CSV", command=self.salvar_csv)
        self.salvar_btn.grid(row=4, column=3, sticky="e", padx=5)

        self.anki_btn = tk.Button(root, text="Enviar selecionados para Anki", command=self.salvar_no_anki)
        self.anki_btn.grid(row=5, column=3, sticky="e", padx=5)

        # --- Linha 7: Status ---
        self.status_label = tk.Label(root, text="Pronto.", anchor="w")
        self.status_label.grid(row=6, column=0, columnspan=4, sticky="we", pady=(5, 0))

        # --- Atalhos ---
        root.bind("<Control-w>", lambda e: self.palavra_entry.focus_set())
        root.bind("<Control-l>", lambda e: self.source_lang.focus_set())
        root.bind("<Control-f>", lambda e: self.ids_entry.focus_set())
        root.bind("<Control-Return>", lambda e: self.salvar_no_anki())
        root.bind("<Control-b>", lambda e: self.buscar_exemplos())

    def set_status(self, msg):
        self.status_label.config(text=msg)
        self.root.update_idletasks()

    def buscar_exemplos(self):
        palavra = self.palavra_entry.get().strip()
        source = self.source_lang.get()
        target = self.target_lang.get()

        if not palavra:
            messagebox.showwarning("Aviso", "Digite uma palavra.")
            return

        self.set_status("🔍 Buscando...")
        self.resultado_text.delete(1.0, tk.END)

        try:
            data = self.reverso.get_context(palavra, source, target)
        except Exception as e:
            self.set_status("❌ Erro ao buscar dados")
            messagebox.showerror("Erro", f"Erro ao buscar dados:\n{e}")
            return

        if not data or 'examples' not in data:
            self.set_status("⚠️ Nenhum exemplo encontrado.")
            messagebox.showinfo("Sem resultados", "Nenhum exemplo encontrado.")
            return

        # Calcula o caminho da raiz do projeto para consistência
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        # Define o diretório 'data' como subdiretório da raiz do projeto
        output_dir = os.path.join(root_dir, 'data') 
        os.makedirs(output_dir, exist_ok=True) # Garante que o diretório 'data' exista

        # Salva o JSON no local correto
        output_path = os.path.join(output_dir, 'output.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Chama a função separar_json. Ela já está configurada para ler 'output.json'
        # e salvar 'examples.json' no mesmo diretório 'data' da raiz do projeto.
        separar_json()

        # Agora, para LER o examples.json, usamos o MESMO 'output_dir'
        caminho_json = os.path.join(output_dir, 'examples.json') 
        
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                self.exemplos = json.load(f)
        except FileNotFoundError:
            self.set_status("❌ Erro: Arquivo de exemplos não encontrado.")
            messagebox.showerror("Erro", f"O arquivo de exemplos não foi encontrado em: {caminho_json}")
            return
        except json.JSONDecodeError:
            self.set_status("❌ Erro: Formato JSON inválido.")
            messagebox.showerror("Erro", f"Erro ao ler JSON em: {caminho_json}. Verifique o formato.")
            return

        self.resultado_text.delete(1.0, tk.END)
        for exemplo in self.exemplos:
            self.resultado_text.insert(tk.END, f"[{exemplo['id']}] EN: {exemplo['source']}\n")
            self.resultado_text.insert(tk.END, f"          PT: {exemplo['target']}\n")
            self.resultado_text.insert(tk.END, "-" * 40 + "\n")

        self.set_status("✅ Pronto.")

    def salvar_csv(self):
        entrada = self.ids_entry.get().strip()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite os IDs a salvar.")
            return

        # Garante que os IDs sejam inteiros válidos
        ids = []
        for i in entrada.split(","):
            try:
                ids.append(int(i.strip()))
            except ValueError:
                # Opcional: Avisar o usuário sobre IDs inválidos
                pass 
        
        if not ids: # Se nenhum ID válido foi fornecido
            messagebox.showwarning("Aviso", "Nenhum ID válido fornecido.")
            return


        selecionados = [
            (ex['source'], ex['target'])
            for ex in self.exemplos if ex['id'] in ids
        ]

        if not selecionados:
            messagebox.showinfo("Nada a salvar", "Nenhum exemplo com os IDs fornecidos.")
            return

        # Define o caminho de saída do CSV para o diretório 'data' na raiz do projeto
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        output_csv = os.path.join(root_dir, 'data', 'exemplos_filtrados.csv')
        
        try:
            with open(output_csv, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(selecionados)
        except IOError as e:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar o arquivo CSV:\n{e}")
            self.set_status("❌ Erro ao salvar CSV.")
            return

        messagebox.showinfo("Salvo", f"{len(selecionados)} exemplos salvos com sucesso!")
        self.set_status(f"✅ {len(selecionados)} exemplos salvos.")

    def salvar_no_anki(self):
        entrada = self.ids_entry.get().strip()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite os IDs a salvar.")
            return

        # Garante que os IDs sejam inteiros válidos
        ids = []
        for i in entrada.split(","):
            try:
                ids.append(int(i.strip()))
            except ValueError:
                # Opcional: Avisar o usuário sobre IDs inválidos
                pass
        
        if not ids: # Se nenhum ID válido foi fornecido
            messagebox.showwarning("Aviso", "Nenhum ID válido fornecido.")
            return

        selecionados = [
            {'Front': ex['source'], 'Back': ex['target']}
            for ex in self.exemplos if ex['id'] in ids
        ]

        if not selecionados:
            messagebox.showinfo("Nada a salvar", "Nenhum exemplo com os IDs fornecidos.")
            return

        deck_name = "Default"  # Pode mudar para deixar o usuário escolher
        
        manager = AnkiDeckManager(deck_name)
        sucesso = manager.add_cards(selecionados)
        if sucesso:
            messagebox.showinfo("Sucesso", f"{len(selecionados)} cartões adicionados ao Anki!")
            self.set_status(f"✅ {len(selecionados)} cartões enviados para o Anki.")
        else:
            messagebox.showerror("Erro Anki", "Falha ao conectar ou enviar cartões para o Anki.")
            self.set_status("❌ Erro ao enviar cartões para o Anki.")