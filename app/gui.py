import customtkinter as ctk
from tkinter import messagebox
from app.database import SessionLocal
from app.models import Personagem

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GerenciadorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Inventário RPG")
        self.geometry("960x720")
        self.minsize(800, 600)

        # Criar abas
        self.notebook = ctk.CTkTabview(self, width=900, height=640)
        self.notebook.pack(padx=20, pady=20, fill="both", expand=True)

        self.notebook.add("Criar Personagem")
        self.notebook.add("Listar Personagens")

        self.frame_criar = self.notebook.tab("Criar Personagem")
        self.frame_listar = self.notebook.tab("Listar Personagens")

        self.criar_aba_criar()
        self.criar_aba_listar()

    def criar_aba_criar(self):
        campos = [
            ("Nome", "nome"),
            ("Classe", "classe"),
            ("Nível", "nivel"),
            ("NEX", "nex"),
            ("Trilha", "trilha"),
            ("História", "historia")
        ]

        self.trilhas_por_classe = {
            "Combatente": ["Aniquilador", "Guerreiro", "Operações Especiais", "Comandante de Campo", "Tropa de Choque"],
            "Especialista": ["Infiltrador", "Negociador", "Técnico", "Atirador de Elite", "Médico de Campo"],
            "Ocultista": ["Conduíte", "Flagelador", "Graduado", "Intuitivo", "Lâmina Paranormal"],
            "Sobrevivente": ["Durão", "Esperto", "Esotérico"]
        }

        self.entradas = {}
        row = 0

        for label, chave in campos:
            ctk.CTkLabel(self.frame_criar, text=label + ":").grid(row=row, column=0, sticky="w", padx=10, pady=10)

            if chave == "historia":
                entrada = ctk.CTkTextbox(self.frame_criar, width=560, height=140)
            elif chave == "classe":
                entrada = ctk.CTkOptionMenu(
                    self.frame_criar,
                    values=["Combatente", "Especialista", "Ocultista", "Sobrevivente"],
                    width=560,
                    command=self.atualizar_trilha_opcoes
                )
                entrada.set("Combatente")
            elif chave == "trilha":
                entrada = ctk.CTkOptionMenu(
                    self.frame_criar,
                    values=self.trilhas_por_classe["Combatente"],
                    width=560
                )
                entrada.set(self.trilhas_por_classe["Combatente"][0])
            else:
                entrada = ctk.CTkEntry(self.frame_criar, width=560)

            entrada.grid(row=row, column=1, sticky="ew", padx=10, pady=10)
            self.entradas[chave] = entrada

            if chave == "nex":
                row += 1
                atributos_label = ctk.CTkLabel(self.frame_criar, text="Atributos:")
                atributos_label.grid(row=row, column=0, sticky="nw", padx=10, pady=10)

                atributos_frame = ctk.CTkFrame(self.frame_criar)
                atributos_frame.grid(row=row, column=1, sticky="ew", padx=10, pady=10)

                atributos = [
                    ("Força", "forca"),
                    ("Agilidade", "agilidade"),
                    ("Intelecto", "intelecto"),
                    ("Presença", "presenca"),
                    ("Vigor", "vigor")
                ]

                for col, (texto, chave_attr) in enumerate(atributos):
                    ctk.CTkLabel(atributos_frame, text=texto).grid(row=0, column=col, sticky="w", padx=5, pady=(0, 5))
                    entrada_attr = ctk.CTkEntry(atributos_frame, width=100)
                    entrada_attr.grid(row=1, column=col, sticky="ew", padx=5, pady=5)
                    self.entradas[chave_attr] = entrada_attr
                    atributos_frame.columnconfigure(col, weight=1)

            row += 1

        self.frame_criar.columnconfigure(1, weight=1)

        ctk.CTkButton(self.frame_criar, text="Salvar Personagem", command=self.salvar_personagem).grid(
            row=row, column=1, sticky="e", padx=10, pady=20
        )

    def atualizar_trilha_opcoes(self, classe_selecionada):
        trilhas = self.trilhas_por_classe.get(classe_selecionada, [])
        trilha_menu = self.entradas.get("trilha")
        if trilha_menu is None:
            return
        trilha_menu.configure(values=trilhas)
        if trilhas:
            trilha_menu.set(trilhas[0])

    def criar_aba_listar(self):
        button_frame = ctk.CTkFrame(self.frame_listar)
        button_frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkButton(button_frame, text="Atualizar Lista", command=self.atualizar_lista).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(button_frame, text="ID para remover:").pack(side="left", padx=(0, 5))
        self.remover_id_entry = ctk.CTkEntry(button_frame, width=120)
        self.remover_id_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            button_frame,
            text="Remover Personagem",
            command=self.remover_personagem,
            fg_color="#D32F2F",
            hover_color="#C62828"
        ).pack(side="left")

        self.texto_lista = ctk.CTkTextbox(self.frame_listar, width=900, height=520)
        self.texto_lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.texto_lista.configure(state="disabled")

        self.atualizar_lista()

    def salvar_personagem(self):
        try:
            nome = self.entradas["nome"].get().strip()
            classe = self.entradas["classe"].get().strip()

            if not nome or not classe:
                messagebox.showerror("Erro", "Nome e Classe são obrigatórios!")
                return

            nivel = int(self.entradas["nivel"].get() or 1)
            nex = int(self.entradas["nex"].get() or 0)

            atributos_campos = [
                ("Força", "forca"),
                ("Agilidade", "agilidade"),
                ("Intelecto", "intelecto"),
                ("Presença", "presenca"),
                ("Vigor", "vigor")
            ]
            atributos_valores = []
            for label, chave in atributos_campos:
                valor_texto = self.entradas[chave].get().strip()
                if valor_texto == "":
                    valor_texto = "0"
                else:
                    int(valor_texto)
                atributos_valores.append(f"{label}={valor_texto}")
            atributos_texto = ", ".join(atributos_valores)

            novo_p = Personagem(
                nome=nome,
                classe=classe,
                nivel=nivel,
                nex=nex,
                atributos=atributos_texto,
                trilha=self.entradas["trilha"].get().strip(),
                historia=self.entradas["historia"].get("1.0", "end").strip()
            )

            db = SessionLocal()
            db.add(novo_p)
            db.commit()
            db.close()

            for entrada in self.entradas.values():
                if isinstance(entrada, ctk.CTkTextbox):
                    entrada.delete("1.0", "end")
                else:
                    entrada.delete(0, "end")

            messagebox.showinfo("Sucesso", f"Personagem '{nome}' salvo com sucesso!")
            self.atualizar_lista()

        except ValueError:
            messagebox.showerror("Erro", "Nível, NEX e atributos devem ser números!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def remover_personagem(self):
        personagem_id_text = self.remover_id_entry.get().strip()
        if not personagem_id_text:
            messagebox.showerror("Erro", "Digite o ID do personagem a remover.")
            return

        try:
            personagem_id = int(personagem_id_text)
        except ValueError:
            messagebox.showerror("Erro", "O ID deve ser um número inteiro.")
            return

        db = SessionLocal()
        try:
            personagem = db.query(Personagem).filter(Personagem.id == personagem_id).first()
            if not personagem:
                messagebox.showerror("Erro", f"Nenhum personagem encontrado com ID {personagem_id}.")
                return

            confirmar = messagebox.askyesno(
                "Confirmar remoção",
                f"Deseja realmente remover o personagem '{personagem.nome}'?"
            )
            if not confirmar:
                return

            db.delete(personagem)
            db.commit()
            messagebox.showinfo("Removido", f"Personagem '{personagem.nome}' removido com sucesso.")
            self.remover_id_entry.delete(0, "end")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover personagem: {str(e)}")
        finally:
            db.close()

    def atualizar_lista(self):
        self.texto_lista.configure(state="normal")
        self.texto_lista.delete("1.0", "end")

        try:
            db = SessionLocal()
            personagens = db.query(Personagem).all()
            db.close()

            if not personagens:
                self.texto_lista.insert("end", "Nenhum personagem encontrado no banco de dados.")
            else:
                texto = f"{'='*80}\n"
                texto += f"{'PERSONAGENS REGISTRADOS':^80}\n"
                texto += f"{'='*80}\n\n"

                for p in personagens:
                    texto += f"ID: {p.id}\n"
                    texto += f"Nome: {p.nome}\n"
                    texto += f"Classe: {p.classe}\n"
                    texto += f"Nível: {p.nivel}\n"
                    texto += f"NEX: {p.nex}%\n"
                    texto += f"Trilha: {p.trilha}\n"
                    texto += f"Atributos: {p.atributos}\n"
                    texto += f"História: {p.historia}\n"
                    texto += f"{'-'*80}\n\n"

                self.texto_lista.insert("end", texto)

        except Exception as e:
            self.texto_lista.insert("end", f"Erro ao carregar personagens: {str(e)}")

        self.texto_lista.configure(state="disabled")


def iniciar_gui():
    app = GerenciadorGUI()
    app.mainloop()


if __name__ == "__main__":
    iniciar_gui()
