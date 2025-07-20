import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.services.reverso_service import ReversoScraperService
from tools.separar_json import separar_json
import csv

class ReversoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tradutor com Reverso")

        self.reverso = ReversoScraperService()
        self.exemplos = []

        # ---------- Linha 1: Idiomas ----------
        tk.Label(root, text="Idioma origem:").grid(row=0, column=0, sticky="w")
        self.source_lang = ttk.Combobox(root, values=["english", "french", "spanish", "german"], width=15)
        self.source_lang.set("english")
        self.source_lang.grid(row=0, column=1)

        tk.Label(root, text="Idioma destino:").grid(row=0, column=2, sticky="w")
        self.target_lang = ttk.Combobox(root, values=["portuguese", "english", "french", "spanish"], width=15)
        self.target_lang.set("portuguese")
        self.target_lang.grid(row=0, column=3)

        # ---------- Linha 2: Palavra ----------
        tk.Label(root, text="Palavra:").grid(row=1, column=0, sticky="w")
        self.palavra_entry = tk.Entry(root, width=40)
        self.palavra_entry.grid(row=1, column=1, columnspan=3, pady=5, sticky="we")

        # ---------- Linha 3: Buscar ----------
        self.buscar_btn = tk.Button(root, text="Buscar exemplos", command=self.buscar_exemplos)
        self.buscar_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # ---------- Linha 4: Resultados ----------
        self.resultado_text = scrolledtext.ScrolledText(root, height=15, width=80)
        self.resultado_text.grid(row=3, column=0, columnspan=4, padx=5)

        # ---------- Linha 5: IDs ----------
        tk.Label(root, text="IDs para salvar (ex: 0,2,4):").grid(row=4, column=0, sticky="w", pady=5)
        self.ids_entry = tk.Entry(root, width=30)
        self.ids_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        # ---------- Linha 6: Salvar ----------
        self.salvar_btn = tk.Button(root, text="Salvar selecionados", command=self.salvar_csv)
        self.salvar_btn.grid(row=4, column=3, sticky="e", padx=5)

        # ---------- Linha 7: Status ----------
        self.status_label = tk.Label(root, text="Pronto.", anchor="w")
        self.status_label.grid(row=5, column=0, columnspan=4, sticky="we", pady=(5, 0))

        self.buscar_btn = tk.Button(root, text="Buscar exemplos", command=self.buscar_exemplos, takefocus=True)
        self.salvar_btn = tk.Button(root, text="Salvar selecionados", command=self.salvar_csv, takefocus=True)

        # ---------- Atalhos ----------
        root.bind("<Control-w>", lambda e: self.palavra_entry.focus_set())
        root.bind("<Control-l>", lambda e: self.source_lang.focus_set())
        root.bind("<Control-f>", lambda e: self.ids_entry.focus_set())
        root.bind("<Control-Return>", lambda e: self.salvar_csv())
        root.bind("<Control-b>", lambda e: self.buscar_exemplos())            # Buscar

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

        # Salva o JSON
        output_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'output.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        separar_json()

        caminho_json = os.path.join(output_dir, 'examples.json')
        with open(caminho_json, 'r', encoding='utf-8') as f:
            self.exemplos = json.load(f)

        for exemplo in self.exemplos:
            self.resultado_text.insert(tk.END, f"[{exemplo['id']}] EN: {exemplo['source']}\n")
            self.resultado_text.insert(tk.END, f"         PT: {exemplo['target']}\n")
            self.resultado_text.insert(tk.END, "-" * 40 + "\n")

        self.set_status("✅ Pronto.")

    def salvar_csv(self):
        entrada = self.ids_entry.get().strip()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite os IDs a salvar.")
            return

        ids = [int(i.strip()) for i in entrada.split(",") if i.strip().isdigit()]
        selecionados = [
            (ex['source'], ex['target'])
            for ex in self.exemplos if ex['id'] in ids
        ]

        if not selecionados:
            messagebox.showinfo("Nada a salvar", "Nenhum exemplo com os IDs fornecidos.")
            return

        output_csv = os.path.join(os.path.dirname(__file__), 'data', 'exemplos_filtrados.csv')
        with open(output_csv, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(selecionados)

        messagebox.showinfo("Salvo", f"{len(selecionados)} exemplos salvos com sucesso!")
        self.set_status(f"✅ {len(selecionados)} exemplos salvos.")

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    app = ReversoApp(root)
    root.mainloop()
