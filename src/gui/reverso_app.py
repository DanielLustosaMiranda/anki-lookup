import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ReversoApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.exemplos = []

        self.root.title("Tradutor com Reverso")

        # --- Linha 0: Idiomas ---
        tk.Label(root, text="Idioma origem:").grid(row=0, column=0, sticky="w")
        self.source_lang = ttk.Combobox(root, values=["english", "french", "spanish", "german"], width=15)
        self.source_lang.set("english")
        self.source_lang.grid(row=0, column=1)

        tk.Label(root, text="Idioma destino:").grid(row=0, column=2, sticky="w")
        self.target_lang = ttk.Combobox(root, values=["portuguese", "english", "french", "spanish"], width=15)
        self.target_lang.set("portuguese")
        self.target_lang.grid(row=0, column=3)

        # --- Linha 1: Palavra ---
        tk.Label(root, text="Palavra:").grid(row=1, column=0, sticky="w")
        self.palavra_entry = tk.Entry(root, width=40)
        self.palavra_entry.grid(row=1, column=1, columnspan=3, pady=5, sticky="we")

        # --- Linha 2: Buscar ---
        self.buscar_btn = tk.Button(root, text="Buscar exemplos", command=self.on_buscar)
        self.buscar_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # --- Linha 3: Resultados ---
        self.resultado_text = scrolledtext.ScrolledText(root, height=15, width=80)
        self.resultado_text.grid(row=3, column=0, columnspan=4, padx=5)

        # --- Linha 4: IDs para salvar/enviar ---
        tk.Label(root, text="IDs para salvar/enviar (ex: 0,2,4):").grid(row=4, column=0, sticky="w", pady=5)
        self.ids_entry = tk.Entry(root, width=30)
        self.ids_entry.grid(row=4, column=1, columnspan=2, sticky="w")

        self.salvar_btn = tk.Button(root, text="Salvar selecionados CSV", command=self.on_salvar_csv)
        self.salvar_btn.grid(row=4, column=3, sticky="e", padx=5)

        # --- Linha 5: Deck e Anki ---
        tk.Label(root, text="Deck:").grid(row=5, column=0, sticky="w")
        self.deck_var = tk.StringVar(value="Carregando...")
        self.deck_menu = ttk.Combobox(root, textvariable=self.deck_var, state="readonly")
        self.deck_menu.grid(row=5, column=1, columnspan=2, sticky="we", padx=5)

        self.anki_btn = tk.Button(root, text="Enviar selecionados para Anki", command=self.on_enviar_anki)
        self.anki_btn.grid(row=5, column=3, sticky="e", padx=5)

        # --- Linha 6: Status ---
        self.status_label = tk.Label(root, text="Pronto.", anchor="w")
        self.status_label.grid(row=6, column=0, columnspan=4, sticky="we", pady=(5, 0))

        # Carrega decks do Anki
        self.listar_decks()

    def set_status(self, msg):
        self.status_label.config(text=msg)
        self.root.update_idletasks()

    def listar_decks(self):
        self.set_status("Carregando decks...")
        decks = self.controller.listar_decks()
        if decks:
            self.deck_menu["values"] = decks
            self.deck_var.set(decks[0])
            self.set_status("Decks carregados.")
        else:
            self.deck_var.set("Nenhum deck encontrado")
            self.set_status("Erro ao carregar decks.")

    def on_buscar(self):
        palavra = self.palavra_entry.get().strip()
        source = self.source_lang.get()
        target = self.target_lang.get()

        if not palavra:
            messagebox.showwarning("Aviso", "Digite uma palavra.")
            return

        self.set_status("🔍 Buscando exemplos...")
        self.resultado_text.delete(1.0, tk.END)

        exemplos = self.controller.buscar_exemplos(palavra, source, target)

        if not exemplos:
            self.set_status("⚠️ Nenhum exemplo encontrado.")
            messagebox.showinfo("Sem resultados", "Nenhum exemplo encontrado.")
            return

        self.exemplos = exemplos
        for ex in exemplos:
            self.resultado_text.insert(tk.END, f"[{ex['id']}] EN: {ex['source']}\n")
            self.resultado_text.insert(tk.END, f"          PT: {ex['target']}\n")
            self.resultado_text.insert(tk.END, "-" * 40 + "\n")

        self.set_status("✅ Pronto.")

    def on_salvar_csv(self):
        entrada = self.ids_entry.get().strip()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite os IDs a salvar.")
            return

        try:
            ids = [int(i.strip()) for i in entrada.split(",")]
        except ValueError:
            messagebox.showwarning("Aviso", "IDs inválidos.")
            return

        self.controller.salvar_csv(ids)
        messagebox.showinfo("Salvo", f"Exemplos com IDs {ids} salvos em CSV.")
        self.set_status(f"✅ Exemplos salvos.")

    def on_enviar_anki(self):
        entrada = self.ids_entry.get().strip()
        if not entrada:
            messagebox.showwarning("Aviso", "Digite os IDs a enviar.")
            return

        try:
            ids = [int(i.strip()) for i in entrada.split(",")]
        except ValueError:
            messagebox.showwarning("Aviso", "IDs inválidos.")
            return

        deck = self.deck_var.get()
        sucesso = self.controller.enviar_para_anki(ids, deck)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Exemplos com IDs {ids} enviados para o Anki no deck '{deck}'.")
            self.set_status("✅ Cartões enviados para o Anki.")
        else:
            messagebox.showerror("Erro", "Falha ao enviar para o Anki.")
            self.set_status("❌ Erro ao enviar cartões para o Anki.")
