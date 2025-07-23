import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.enums.languages import SupportedLanguages

class ReversoApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.exemplos = []

        self.root.title("Anki Lookup")
        self.root.geometry("750x600")
        self.root.configure(padx=10, pady=10)

        # ---------- Linha 0: Idiomas ----------
        idioma_frame = tk.Frame(root)
        idioma_frame.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 5))

        tk.Label(idioma_frame, text="De:").pack(side="left")
        self.source_lang = ttk.Combobox(idioma_frame, values=SupportedLanguages, width=15)
        self.source_lang.set("english")
        self.source_lang.pack(side="left", padx=(5, 20))

        tk.Label(idioma_frame, text="Para:").pack(side="left")
        self.target_lang = ttk.Combobox(idioma_frame, values=SupportedLanguages, width=15)
        self.target_lang.set("portuguese")
        self.target_lang.pack(side="left", padx=5)

        # ---------- Linha 1: Palavra ----------
        palavra_frame = tk.Frame(root)
        palavra_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 5))

        tk.Label(palavra_frame, text="Palavra:").pack(side="left")
        self.palavra_entry = tk.Entry(palavra_frame, width=40)
        self.palavra_entry.pack(side="left", padx=5, expand=True, fill="x")

        self.buscar_btn = tk.Button(palavra_frame, text="Buscar exemplos", command=self.on_buscar)
        self.buscar_btn.pack(side="left", padx=10)

        # ---------- Linha 2: Resultados ----------
        self.resultado_text = scrolledtext.ScrolledText(root, height=15, width=80, wrap=tk.WORD)
        self.resultado_text.grid(row=2, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

        # ---------- Linha 3: IDs + Salvar ----------
        id_frame = tk.Frame(root)
        id_frame.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

        tk.Label(id_frame, text="IDs (ex: 0,2,4):").pack(side="left")
        self.ids_entry = tk.Entry(id_frame, width=25)
        self.ids_entry.pack(side="left", padx=5)

        self.salvar_btn = tk.Button(id_frame, text="💾 Salvar CSV", command=self.on_salvar_csv)
        self.salvar_btn.pack(side="left", padx=10)

        # ---------- Linha 4: Anki ----------
        anki_frame = tk.Frame(root)
        anki_frame.grid(row=4, column=0, columnspan=2, sticky="we", pady=(5, 10))

        
        tk.Label(anki_frame, text="Deck:").pack(side="left")
        self.deck_var = tk.StringVar(value="Carregando...")
        self.deck_menu = ttk.Combobox(anki_frame, textvariable=self.deck_var, state="readonly", width=30)
        self.deck_menu.pack(side="left", padx=5)

        self.anki_btn = tk.Button(anki_frame, text="📥 Enviar para Anki", command=self.on_enviar_anki)
        self.anki_btn.pack(side="left", padx=10)

        # ---------- Linha 5: Limpar sessão ----------
        self.limpar_btn = tk.Button(root, text="🧹 Limpar sessão", command=self.on_limpar_sessao)
        self.limpar_btn.grid(row=5, column=0, columnspan=2, pady=(0, 5))

        # ---------- Linha 6: Status ----------
        self.status_label = tk.Label(root, text="Pronto.", anchor="w")
        self.status_label.grid(row=6, column=0, columnspan=2, sticky="we")

        # Expansão para texto
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(1, weight=1)

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
            self.resultado_text.insert(tk.END, f"[{ex['id']}] Source: {ex['source']}\n")
            self.resultado_text.insert(tk.END, f"          Target: {ex['target']}\n")
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

    def on_limpar_sessao(self):
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todos os arquivos da sessão?")
        if confirm:
            self.controller.limpar_sessao()
            messagebox.showinfo("Sessão limpa", "Todos os arquivos foram apagados.")
            self.set_status("🧹 Sessão limpa.")
