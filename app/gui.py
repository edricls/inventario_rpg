import json
import customtkinter as ctk
from tkinter import messagebox, StringVar
from app.database import SessionLocal
from app.models import Personagem

PERICIAS = [
    "Acrobacia",
    "Adestramento",
    "Artes",
    "Atletismo",
    "Atualiadades",
    "Ciências",
    "Crime",
    "Diplomacia",
    "Enganação",
    "Fortitude",
    "Furtividade",
    "Iniciativa",
    "Intimidação",
    "Intuição",
    "Investigação",
    "Luta",
    "Medicina",
    "Ocultismo",
    "Percepção",
    "Pilotagem",
    "Pontaria",
    "Profissão",
    "Reflexos",
    "Religião",
    "Sobrevivência",
    "Tecnologia",
    "Tática",
    "Vontade"
]

ATRIBUTOS_PERICIAS = [
    "AGI",
    "PRE",
    "PRE",
    "FOR",
    "INT",
    "INT",
    "AGI",
    "PRE",
    "PRE",
    "VIG",
    "AGI",
    "AGI",
    "PRE",
    "PRE",
    "INT",
    "FOR",
    "INT",
    "INT",
    "PRE",
    "AGI",
    "AGI",
    "INT",
    "AGI",
    "PRE",
    "INT",
    "INT",
    "INT",
    "PRE"
]

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
        self.trilhas_por_classe = {
            "Combatente": ["Aniquilador", "Guerreiro", "Operações Especiais", "Comandante de Campo", "Tropa de Choque"],
            "Especialista": ["Infiltrador", "Negociador", "Técnico", "Atirador de Elite", "Médico de Campo"],
            "Ocultista": ["Conduíte", "Flagelador", "Graduado", "Intuitivo", "Lâmina Paranormal"],
            "Sobrevivente": ["Durão", "Esperto", "Esotérico"]
        }

        self.entradas = {}
        row = 0

        ctk.CTkLabel(self.frame_criar, text="Nome:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        nome_entrada = ctk.CTkEntry(self.frame_criar, width=560)
        nome_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["nome"] = nome_entrada
        row += 1

        ctk.CTkLabel(self.frame_criar, text="Classe:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        classe_entrada = ctk.CTkOptionMenu(
            self.frame_criar,
            values=["Combatente", "Especialista", "Ocultista", "Sobrevivente"],
            width=560,
            command=self.atualizar_trilha_opcoes
        )
        classe_entrada.set("Combatente")
        classe_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["classe"] = classe_entrada
        row += 1

        ctk.CTkLabel(self.frame_criar, text="Nível:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        nivel_entrada = ctk.CTkEntry(self.frame_criar, width=90)
        nivel_entrada.grid(row=row, column=1, sticky="w", padx=10, pady=(8, 0))
        self.entradas["nivel"] = nivel_entrada

        ctk.CTkLabel(self.frame_criar, text="NEX:").grid(row=row, column=2, sticky="w", padx=10, pady=10)
        nex_entrada = ctk.CTkEntry(self.frame_criar, width=90)
        nex_entrada.grid(row=row, column=3, sticky="w", padx=10, pady=(8, 0))
        self.entradas["nex"] = nex_entrada
        row += 1

        self.nivel_erro_label = ctk.CTkLabel(
            self.frame_criar,
            text="",
            text_color="red",
            anchor="w",
            height=18,
            font=ctk.CTkFont(size=12)
        )
        self.nivel_erro_label.grid(row=row, column=1, sticky="w", padx=10, pady=(0, 0))
        nivel_entrada.bind("<KeyRelease>", self.validar_nivel)
        nivel_entrada.bind("<FocusOut>", self.validar_nivel)

        self.nex_erro_label = ctk.CTkLabel(
            self.frame_criar,
            text="",
            text_color="red",
            anchor="w",
            height=18,
            font=ctk.CTkFont(size=12)
        )
        self.nex_erro_label.grid(row=row, column=3, sticky="w", padx=10, pady=(0, 0))
        nex_entrada.bind("<KeyRelease>", self.validar_nex)
        nex_entrada.bind("<FocusOut>", self.validar_nex)
        row += 1

        ctk.CTkLabel(self.frame_criar, text="Trilha:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        trilha_entrada = ctk.CTkOptionMenu(
            self.frame_criar,
            values=self.trilhas_por_classe["Combatente"],
            width=560
        )
        trilha_entrada.set(self.trilhas_por_classe["Combatente"][0])
        trilha_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["trilha"] = trilha_entrada
        row += 1

        atributos_label = ctk.CTkLabel(self.frame_criar, text="Atributos:")
        atributos_label.grid(row=row, column=0, sticky="nw", padx=10, pady=10)

        atributos_frame = ctk.CTkFrame(self.frame_criar)
        atributos_frame.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)

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
            entrada_attr.insert(0, "1")
            self.entradas[chave_attr] = entrada_attr
            atributos_frame.columnconfigure(col, weight=1)

        row += 1

        ctk.CTkLabel(self.frame_criar, text="História:").grid(row=row, column=0, sticky="nw", padx=10, pady=10)
        historia_entrada = ctk.CTkTextbox(self.frame_criar, width=560, height=140)
        historia_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["historia"] = historia_entrada
        row += 1

        self.frame_criar.columnconfigure(1, weight=1)
        self.frame_criar.columnconfigure(3, weight=1)

        ctk.CTkButton(self.frame_criar, text="Salvar Personagem", command=self.salvar_personagem).grid(
            row=row, column=3, sticky="e", padx=10, pady=20
        )

    def validar_nivel(self, event=None):
        nivel_texto = self.entradas["nivel"].get().strip()
        # Limitar a no máximo 2 caracteres para o campo Nível
        if len(nivel_texto) > 2:
            nivel_texto = nivel_texto[:2]
            self.entradas["nivel"].delete(0, "end")
            self.entradas["nivel"].insert(0, nivel_texto)
        if nivel_texto == "":
            self.nivel_erro_label.configure(text="")
            return True

        if not nivel_texto.isdigit():
            self.nivel_erro_label.configure(text="Digite um numero de 0 a 20")
            return False

        nivel = int(nivel_texto)
        if nivel < 0 or nivel > 20:
            self.nivel_erro_label.configure(text="Digite um numero de 0 a 20")
            return False

        self.nivel_erro_label.configure(text="")
        return True

    def validar_nex(self, event=None):
        nex_texto = self.entradas["nex"].get().strip()
        # Limitar a no máximo 2 caracteres para o campo NEX
        if len(nex_texto) > 2:
            nex_texto = nex_texto[:2]
            self.entradas["nex"].delete(0, "end")
            self.entradas["nex"].insert(0, nex_texto)
        if nex_texto == "":
            self.nex_erro_label.configure(text="")
            return True

        if not nex_texto.isdigit():
            self.nex_erro_label.configure(text="O Valor de Nex deve ser entre 0 e 100")
            return False

        nex = int(nex_texto)
        if nex < 0 or nex > 100:
            self.nex_erro_label.configure(text="O Valor de Nex deve ser entre 0 e 100")
            return False

        self.nex_erro_label.configure(text="")
        return True

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

        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_listar, width=900, height=520)
        self.lista_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.atualizar_lista()

    def salvar_personagem(self):
        try:
            nome = self.entradas["nome"].get().strip()
            classe = self.entradas["classe"].get().strip()

            if not nome or not classe:
                messagebox.showerror("Erro", "Nome e Classe são obrigatórios!")
                return

            nivel_texto = self.entradas["nivel"].get().strip()
            # Garantir que o texto do nível tenha no máximo 2 caracteres
            if len(nivel_texto) > 2:
                nivel_texto = nivel_texto[:2]
                self.entradas["nivel"].delete(0, "end")
                self.entradas["nivel"].insert(0, nivel_texto)
            if nivel_texto == "":
                nivel = 1
            elif not nivel_texto.isdigit() or not (0 <= int(nivel_texto) <= 20):
                self.nivel_erro_label.configure(text="Digite um numero de 0 a 20")
                return
            else:
                nivel = int(nivel_texto)

                nex_texto = self.entradas["nex"].get().strip()
                # Garantir que o texto do NEX tenha no máximo 2 caracteres
                if len(nex_texto) > 2:
                    nex_texto = nex_texto[:2]
                    self.entradas["nex"].delete(0, "end")
                    self.entradas["nex"].insert(0, nex_texto)
            if nex_texto == "":
                nex = 0
            elif not nex_texto.isdigit() or not (0 <= int(nex_texto) <= 100):
                self.nex_erro_label.configure(text="O Valor de Nex deve ser entre 0 e 100")
                return
            else:
                nex = int(nex_texto)

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
                    valor_texto = "1"
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
                historia=self.entradas["historia"].get("1.0", "end").strip(),
                pericias=json.dumps([
                    {"nome": nome_pericia, "atributo": atributo_pericia, "treino": 0, "extra": 0, "total": 0}
                    for nome_pericia, atributo_pericia in zip(PERICIAS, ATRIBUTOS_PERICIAS)
                ])
            )

            db = SessionLocal()
            db.add(novo_p)
            db.commit()
            db.close()

            for chave, entrada in self.entradas.items():
                if isinstance(entrada, ctk.CTkTextbox):
                    entrada.delete("1.0", "end")
                elif isinstance(entrada, ctk.CTkOptionMenu):
                    if chave == "classe":
                        entrada.set("Combatente")
                    elif chave == "trilha":
                        entrada.set(self.trilhas_por_classe["Combatente"][0])
                else:
                    entrada.delete(0, "end")

            messagebox.showinfo("Sucesso", f"Personagem '{nome}' salvo com sucesso!")
            self.nivel_erro_label.configure(text="")
            self.nex_erro_label.configure(text="")
            self.atualizar_lista()

        except ValueError:
            messagebox.showerror("Erro", "Nível, NEX e atributos devem ser números!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def remover_personagem(self):
        # método removido: remoção individual agora é feita por
        # `remover_personagem_confirm(personagem)` em cada card.
        return

    def _carregar_dados_pericias(self, personagem):
        if not personagem.pericias:
            return [
                {"nome": nome_pericia, "atributo": atributo_pericia, "treino": 0, "extra": 0, "total": 0}
                for nome_pericia, atributo_pericia in zip(PERICIAS, ATRIBUTOS_PERICIAS)
            ]

        try:
            dados = json.loads(personagem.pericias)
            if isinstance(dados, list):
                return dados
        except (TypeError, ValueError):
            pass

        return [
            {"nome": nome_pericia, "atributo": atributo_pericia, "treino": 0, "extra": 0, "total": 0}
            for nome_pericia, atributo_pericia in zip(PERICIAS, ATRIBUTOS_PERICIAS)
        ]

    def _salvar_pericias_personagem(self, personagem, dados_pericias):
        try:
            db = SessionLocal()
            personagem_db = db.query(Personagem).filter(Personagem.id == personagem.id).first()
            if personagem_db is None:
                db.close()
                return

            dados_json = json.dumps(dados_pericias)
            personagem_db.pericias = dados_json
            if hasattr(personagem, "pericias"):
                personagem.pericias = dados_json
            db.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar perícias: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()

    def remover_personagem_confirm(self, personagem):
        confirmar = messagebox.askyesno(
            "Confirmar remoção",
            f"Deseja realmente remover o personagem '{personagem.nome}'?"
        )
        if not confirmar:
            return

        db = SessionLocal()
        try:
            db.delete(personagem)
            db.commit()
            messagebox.showinfo("Removido", f"Personagem '{personagem.nome}' removido com sucesso.")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover personagem: {str(e)}")
        finally:
            db.close()

    def abrir_ficha(self, personagem):
        ficha = ctk.CTkToplevel(self)
        ficha.title(f"Ficha de {personagem.nome}")
        ficha.geometry("620x620")
        ficha.grab_set()

        header_frame = ctk.CTkFrame(ficha)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        photo_frame = ctk.CTkFrame(header_frame, width=140, height=140, corner_radius=20)
        photo_frame.grid(row=0, column=0, rowspan=2, padx=(0, 15), pady=0)
        photo_frame.grid_propagate(False)
        ctk.CTkLabel(photo_frame, text="Foto", font=ctk.CTkFont(size=18, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(header_frame, text=personagem.nome, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(header_frame, text=f"Classe: {personagem.classe} | Nível: {personagem.nivel} | NEX: {personagem.nex}%").grid(row=1, column=1, sticky="w")

        tabview = ctk.CTkTabview(ficha)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tab_dados = tabview.add("Dados Gerais")
        tab_pericias = tabview.add("Perícias")

        info_frame = ctk.CTkFrame(tab_dados)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=0)
        info_frame.grid_columnconfigure(1, weight=1)

        label_classe = ctk.CTkLabel(info_frame, text="Classe:", anchor="w")
        valor_classe = ctk.CTkLabel(info_frame, text=personagem.classe, anchor="e")
        label_classe.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_classe.grid(row=0, column=1, sticky="e", padx=10, pady=(0, 8))

        label_nivel = ctk.CTkLabel(info_frame, text="Nível:", anchor="w")
        valor_nivel = ctk.CTkLabel(info_frame, text=str(personagem.nivel), anchor="e")
        label_nivel.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_nivel.grid(row=1, column=1, sticky="e", padx=10, pady=(0, 8))

        label_nex = ctk.CTkLabel(info_frame, text="NEX:", anchor="w")
        valor_nex = ctk.CTkLabel(info_frame, text=f"{personagem.nex}%", anchor="e")
        label_nex.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_nex.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 8))

        label_trilha = ctk.CTkLabel(info_frame, text="Trilha:", anchor="w")
        valor_trilha = ctk.CTkLabel(info_frame, text=personagem.trilha, anchor="e")
        label_trilha.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_trilha.grid(row=3, column=1, sticky="e", padx=10, pady=(0, 8))

        label_atributos = ctk.CTkLabel(info_frame, text="Atributos:", anchor="w")
        valor_atributos = ctk.CTkLabel(info_frame, text=personagem.atributos, anchor="e", wraplength=320)
        label_atributos.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_atributos.grid(row=4, column=1, sticky="e", padx=10, pady=(0, 8))

        ctk.CTkLabel(info_frame, text="História:", anchor="w").grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))
        historia_text = ctk.CTkTextbox(info_frame, width=460, height=180)
        historia_text.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        info_frame.grid_rowconfigure(6, weight=1)
        historia_text.insert("1.0", personagem.historia)
        historia_text.configure(state="disabled")

        pericias_frame = ctk.CTkScrollableFrame(tab_pericias)
        pericias_frame.pack(fill="both", expand=True, padx=20, pady=20)

        headers = ["Pericia", "Treino", "Atributo", "Extra", "Total"]
        for index, titulo in enumerate(headers):
            ctk.CTkLabel(pericias_frame, text=titulo, font=ctk.CTkFont(weight="bold")).grid(
                row=0,
                column=index,
                padx=8,
                pady=(0, 6),
                sticky="w"
            )

        dados_pericias_salvos = self._carregar_dados_pericias(personagem)
        rows_state = []

        for row_index, (nome_pericia, atributo_pericia) in enumerate(zip(PERICIAS, ATRIBUTOS_PERICIAS), start=1):
            dados_pericia = next((item for item in dados_pericias_salvos if item.get("nome") == nome_pericia), None)
            if dados_pericia is None:
                dados_pericia = {"nome": nome_pericia, "atributo": atributo_pericia, "treino": 0, "extra": 0, "total": 0}

            ctk.CTkLabel(pericias_frame, text=nome_pericia, anchor="w").grid(
                row=row_index,
                column=0,
                padx=8,
                pady=2,
                sticky="w"
            )

            treino_menu = ctk.CTkOptionMenu(
                pericias_frame,
                values=["0", "5", "10", "15"],
                width=80
            )
            treino_menu.set(str(dados_pericia.get("treino", 0)))
            treino_menu.grid(
                row=row_index,
                column=1,
                padx=8,
                pady=2,
                sticky="w"
            )

            ctk.CTkLabel(pericias_frame, text=atributo_pericia, anchor="w").grid(
                row=row_index,
                column=2,
                padx=8,
                pady=2,
                sticky="w"
            )

            extra_var = StringVar(value=str(dados_pericia.get("extra", 0)))
            extra_entry = ctk.CTkEntry(pericias_frame, textvariable=extra_var, width=80)
            extra_entry.grid(
                row=row_index,
                column=3,
                padx=8,
                pady=2,
                sticky="w"
            )

            total_var = StringVar(value=str(dados_pericia.get("total", 0)))
            total_label = ctk.CTkLabel(pericias_frame, textvariable=total_var, anchor="w", width=60)
            total_label.grid(
                row=row_index,
                column=4,
                padx=8,
                pady=2,
                sticky="w"
            )

            row_state = {
                "nome": nome_pericia,
                "atributo": atributo_pericia,
                "treino_menu": treino_menu,
                "extra_var": extra_var,
                "total_var": total_var,
            }
            rows_state.append(row_state)

        def atualizar_todas_as_pericias(event=None):
            dados_para_salvar = []
            for row_state in rows_state:
                try:
                    treino = int(row_state["treino_menu"].get())
                except ValueError:
                    treino = 0

                valor_extra = row_state["extra_var"].get().strip()
                if valor_extra == "":
                    valor_extra = "0"
                if not valor_extra.isdigit():
                    valor_extra = "".join(ch for ch in valor_extra if ch.isdigit()) or "0"
                    row_state["extra_var"].set(valor_extra)

                try:
                    extra = int(valor_extra)
                except ValueError:
                    extra = 0

                total = treino + extra
                row_state["total_var"].set(str(total))
                dados_para_salvar.append({
                    "nome": row_state["nome"],
                    "atributo": row_state["atributo"],
                    "treino": treino,
                    "extra": extra,
                    "total": total,
                })

            self._salvar_pericias_personagem(personagem, dados_para_salvar)

        def salvar_e_fechar():
            atualizar_todas_as_pericias()
            ficha.destroy()

        for row_state in rows_state:
            row_state["extra_var"].trace_add("write", lambda *args, state=row_state: atualizar_todas_as_pericias())
            row_state["treino_menu"].configure(command=lambda value=None: atualizar_todas_as_pericias())
            row_state["extra_var"].set(row_state["extra_var"].get())

        atualizar_todas_as_pericias()

        ctk.CTkButton(ficha, text="Fechar", command=salvar_e_fechar).pack(padx=20, pady=(0, 20))

    def atualizar_lista(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        try:
            db = SessionLocal()
            personagens = db.query(Personagem).all()
            db.close()

            if not personagens:
                empty_label = ctk.CTkLabel(self.lista_scroll, text="Nenhum personagem encontrado no banco de dados.")
                empty_label.pack(pady=20)
                return

            for personagem in personagens:
                card = ctk.CTkFrame(self.lista_scroll, fg_color="#2B2B2B", corner_radius=15, border_width=1, border_color="#3A3A3A")
                card.pack(fill="x", padx=10, pady=8)

                top_row = ctk.CTkFrame(card)
                top_row.pack(fill="x", padx=12, pady=12)

                photo_frame = ctk.CTkFrame(top_row, width=120, height=120, corner_radius=16)
                photo_frame.grid(row=0, column=0, rowspan=2, padx=(0, 12), pady=0)
                photo_frame.grid_propagate(False)
                ctk.CTkLabel(photo_frame, text="Foto", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

                ctk.CTkLabel(top_row, text=personagem.nome, font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(top_row, text=f"Classe: {personagem.classe} | Nível: {personagem.nivel} | NEX: {personagem.nex}%").grid(row=1, column=1, sticky="w")

                footer_row = ctk.CTkFrame(card)
                footer_row.pack(fill="x", padx=12, pady=(0, 12))
                ctk.CTkButton(
                    footer_row,
                    text="Remover",
                    command=lambda p=personagem: self.remover_personagem_confirm(p),
                    fg_color="#D32F2F",
                    hover_color="#C62828"
                ).pack(side="right", padx=(0, 10))
                ctk.CTkButton(footer_row, text="Acessar Ficha", command=lambda p=personagem: self.abrir_ficha(p)).pack(side="right")

        except Exception as e:
            error_label = ctk.CTkLabel(self.lista_scroll, text=f"Erro ao carregar personagens: {str(e)}", text_color="#FF6B6B")
            error_label.pack(pady=20)


def iniciar_gui():
    app = GerenciadorGUI()
    app.mainloop()


if __name__ == "__main__":
    iniciar_gui()
