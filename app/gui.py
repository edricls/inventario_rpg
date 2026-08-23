import json
import customtkinter as ctk
from tkinter import messagebox, StringVar
from app.character_rules import (
    calcular_pv_pd,
    obter_limites_nivel,
    obter_nome_nivel,
    validar_nex_texto,
)
from app.character_storage import (
    atualizar_personagem,
    listar_personagens,
    remover_personagem,
    salvar_personagem as salvar_personagem_no_banco,
)
from app.gui_data import (
    ATRIBUTOS,
    ATRIBUTOS_PERICIAS,
    CLASSES,
    ORIGENS,
    PERICIAS,
    TRILHAS_POR_CLASSE,
    FILTROS_HABILIDADES,
    HABILIDADES_POR_CATEGORIA,
    DESCRICOES_HABILIDADES,
)
from app.models import Personagem
from app.pericia_storage import (
    carregar_dados_pericias,
    dados_pericias_padrao,
    salvar_dados_pericias,
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ScrollableOriginOptionMenu(ctk.CTkOptionMenu):
    def __init__(self, master, values, width=560, height=32, command=None):
        super().__init__(master, values=values, width=width, height=height, command=command, dynamic_resizing=False)
        self._dropdown_frame = None

    def _open_dropdown_menu(self):
        if self._dropdown_frame is not None:
            self._close_dropdown_menu()
            return

        root = self.winfo_toplevel()
        self._dropdown_frame = ctk.CTkFrame(
            root,
            corner_radius=8,
            border_width=1,
            fg_color=("#2B2B2B", "#1F1F1F"),
            border_color=("#4A4A4A", "#5A5A5A")
        )

        x = self.winfo_rootx() - root.winfo_rootx()
        y = self.winfo_rooty() - root.winfo_rooty() + self.winfo_height() + 4
        self._dropdown_frame.place(x=x, y=y)
        self._dropdown_frame.lift()

        scroll_frame = ctk.CTkScrollableFrame(
            self._dropdown_frame,
            width=max(self._desired_width, 220),
            height=180
        )
        scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        for value in self._values:
            button = ctk.CTkButton(
                scroll_frame,
                text=value,
                width=max(self._desired_width, 220),
                height=28,
                fg_color="transparent",
                hover_color=("#3A3A3A", "#4A4A4A"),
                anchor="w",
                command=lambda v=value: self._select_value(v)
            )
            button.pack(fill="x", padx=2, pady=2)

    def _select_value(self, value):
        self._current_value = value
        self._text_label.configure(text=value)

        if self._variable is not None:
            self._variable_callback_blocked = True
            self._variable.set(self._current_value)
            self._variable_callback_blocked = False

        if self._command is not None:
            self._command(self._current_value)

        self._close_dropdown_menu()

    def _close_dropdown_menu(self):
        if self._dropdown_frame is not None:
            self._dropdown_frame.destroy()
            self._dropdown_frame = None

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
        self.trilhas_por_classe = TRILHAS_POR_CLASSE

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
            values=CLASSES,
            width=560,
            command=self.atualizar_trilha_opcoes
        )
        classe_entrada.set("Combatente")
        classe_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["classe"] = classe_entrada
        row += 1

        self.nivel_label = ctk.CTkLabel(self.frame_criar, text="Nível:")
        self.nivel_label.grid(row=row, column=0, sticky="w", padx=10, pady=10)
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
        self.atualizar_estado_trilha()
        row += 1

        ctk.CTkLabel(self.frame_criar, text="Origem:").grid(row=row, column=0, sticky="w", padx=10, pady=10)
        origem_entrada = ScrollableOriginOptionMenu(
            self.frame_criar,
            values=ORIGENS,
            width=560,
            height=32
        )
        origem_entrada.set(ORIGENS[0])
        origem_entrada.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        self.entradas["origem"] = origem_entrada
        row += 1

        atributos_label = ctk.CTkLabel(self.frame_criar, text="Atributos:")
        atributos_label.grid(row=row, column=0, sticky="nw", padx=10, pady=10)

        atributos_frame = ctk.CTkFrame(self.frame_criar)
        atributos_frame.grid(row=row, column=1, columnspan=3, sticky="ew", padx=10, pady=10)

        for col, (texto, chave_attr) in enumerate(ATRIBUTOS):
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
        classe_selecionada = self.entradas["classe"].get().strip()
        limite_inferior, limite_superior = obter_limites_nivel(classe_selecionada)
        nome_nivel = obter_nome_nivel(classe_selecionada)

        # Limitar a no máximo 2 caracteres para o campo Nível/Estágio
        if len(nivel_texto) > 2:
            nivel_texto = nivel_texto[:2]
            self.entradas["nivel"].delete(0, "end")
            self.entradas["nivel"].insert(0, nivel_texto)
        if nivel_texto == "":
            self.nivel_erro_label.configure(text="")
            self.atualizar_estado_trilha()
            return True

        if not nivel_texto.isdigit():
            self.nivel_erro_label.configure(text=f"Digite um numero de {limite_inferior} a {limite_superior} para {nome_nivel}")
            self.atualizar_estado_trilha()
            return False

        nivel = int(nivel_texto)
        if nivel < limite_inferior or nivel > limite_superior:
            self.nivel_erro_label.configure(text=f"Digite um numero de {limite_inferior} a {limite_superior} para {nome_nivel}")
            self.atualizar_estado_trilha()
            return False

        self.nivel_erro_label.configure(text="")
        self.atualizar_estado_trilha()
        return True

    def validar_nex(self, event=None):
        nex_texto = self.entradas["nex"].get()
        _, _, erro = validar_nex_texto(nex_texto)
        if erro:
            self.nex_erro_label.configure(text=erro)
            return False

        self.nex_erro_label.configure(text="")
        return True

    def atualizar_trilha_opcoes(self, classe_selecionada, ajustar_nivel=True):
        trilha_menu = self.entradas.get("trilha")
        if trilha_menu is None:
            return

        self.nivel_label.configure(text="Estágio:" if classe_selecionada == "Sobrevivente" else "Nível:")
        nivel_texto = self.entradas["nivel"].get().strip()
        limite_inferior, limite_superior = obter_limites_nivel(classe_selecionada)
        if ajustar_nivel and (not nivel_texto.isdigit() or not limite_inferior <= int(nivel_texto) <= limite_superior):
            self.entradas["nivel"].delete(0, "end")
            self.entradas["nivel"].insert(0, str(limite_inferior))
            self.nivel_erro_label.configure(text="")

        nivel_texto = self.entradas["nivel"].get().strip()
        if nivel_texto.isdigit() and int(nivel_texto) < 2:
            return

        trilhas = self.trilhas_por_classe.get(classe_selecionada, [])
        trilha_menu.configure(values=trilhas)
        if trilhas:
            trilha_menu.set(trilhas[0])

    def atualizar_estado_trilha(self):
        trilha_menu = self.entradas.get("trilha")
        if trilha_menu is None:
            return

        nivel_texto = self.entradas["nivel"].get().strip()
        if nivel_texto.isdigit() and int(nivel_texto) < 2:
            trilha_menu.configure(values=["Nenhuma"], state="disabled")
            trilha_menu.set("Nenhuma")
            return

        trilha_menu.configure(state="normal")
        classe_selecionada = self.entradas["classe"].get().strip()
        self.atualizar_trilha_opcoes(classe_selecionada, ajustar_nivel=False)

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
            else:
                classe_selecionada = self.entradas["classe"].get().strip()
                limite_inferior, limite_superior = obter_limites_nivel(classe_selecionada)
                nome_nivel = obter_nome_nivel(classe_selecionada)
                if not nivel_texto.isdigit() or not (limite_inferior <= int(nivel_texto) <= limite_superior):
                    self.nivel_erro_label.configure(
                        text=f"Digite um numero de {limite_inferior} a {limite_superior} para {nome_nivel}"
                    )
                    return
                nivel = int(nivel_texto)

            nex_texto, nex, erro_nex = validar_nex_texto(self.entradas["nex"].get())
            if erro_nex:
                self.nex_erro_label.configure(text=erro_nex)
                return

            atributos_valores = []
            for label, chave in ATRIBUTOS:
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
                origem=self.entradas["origem"].get().strip(),
                historia=self.entradas["historia"].get("1.0", "end").strip(),
                pericias=json.dumps(dados_pericias_padrao(PERICIAS, ATRIBUTOS_PERICIAS))
            )

            salvar_personagem_no_banco(novo_p)

            self._limpar_formulario()

            messagebox.showinfo("Sucesso", f"Personagem '{nome}' salvo com sucesso!")
            self.nivel_erro_label.configure(text="")
            self.nex_erro_label.configure(text="")
            self.atualizar_lista()

        except ValueError:
            messagebox.showerror("Erro", "Nível, NEX e atributos devem ser números!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def _limpar_formulario(self):
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

    def _carregar_dados_pericias(self, personagem):
        return carregar_dados_pericias(personagem, PERICIAS, ATRIBUTOS_PERICIAS)

    def _salvar_pericias_personagem(self, personagem, dados_pericias):
        try:
            salvar_dados_pericias(personagem, dados_pericias)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar perícias: {str(e)}")

    def remover_personagem_confirm(self, personagem):
        confirmar = messagebox.askyesno(
            "Confirmar remoção",
            f"Deseja realmente remover o personagem '{personagem.nome}'?"
        )
        if not confirmar:
            return

        try:
            remover_personagem(personagem)
            messagebox.showinfo("Removido", f"Personagem '{personagem.nome}' removido com sucesso.")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover personagem: {str(e)}")

    def calcular_pv_pd(self, personagem, nivel=None, atributos=None):
        return calcular_pv_pd(personagem, nivel, atributos)

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
        origem_valor = getattr(personagem, "origem", None) or ""
        resumo_ficha = ctk.CTkLabel(
            header_frame,
            text=f"Classe: {personagem.classe} | Nível: {personagem.nivel} | NEX: {personagem.nex}% | Origem: {origem_valor or 'Não informada'}"
        )
        resumo_ficha.grid(row=1, column=1, sticky="w")

        tabview = ctk.CTkTabview(ficha)
        tabview.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tab_dados = tabview.add("Dados Gerais")
        tab_pericias = tabview.add("Perícias")
        tab_habilidades = tabview.add("Habilidades")
        tab_rituais = tabview.add("Rituais")
        tab_inventario = tabview.add("Inventário")

        habilidades_header = ctk.CTkFrame(tab_habilidades, fg_color="transparent")
        habilidades_header.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(
            habilidades_header,
            text="Adicionar Habilidade",
            command=lambda: self._abrir_seletor_habilidades(personagem)
        ).pack(side="left")

        info_frame = ctk.CTkFrame(tab_dados)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=0)
        info_frame.grid_columnconfigure(1, weight=1)

        pv_inicial, pd_inicial = self.calcular_pv_pd(personagem)
        recursos_frame_ficha = ctk.CTkFrame(info_frame)
        recursos_frame_ficha.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 8))
        recursos_frame_ficha.grid_columnconfigure((0, 1), weight=1)
        valor_pv_ficha = ctk.CTkLabel(recursos_frame_ficha, text=f"PV: {pv_inicial}", font=ctk.CTkFont(size=16, weight="bold"))
        valor_pv_ficha.grid(row=0, column=0, sticky="w", padx=10, pady=8)
        valor_pd_ficha = ctk.CTkLabel(recursos_frame_ficha, text=f"PD: {pd_inicial}", font=ctk.CTkFont(size=16, weight="bold"))
        valor_pd_ficha.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        label_classe = ctk.CTkLabel(info_frame, text="Classe:", anchor="w")
        valor_classe = ctk.CTkLabel(info_frame, text=personagem.classe, anchor="e")
        label_classe.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_classe.grid(row=1, column=1, sticky="e", padx=10, pady=(0, 8))

        label_nivel = ctk.CTkLabel(info_frame, text="Nível:", anchor="w")
        valor_nivel = ctk.CTkLabel(info_frame, text=str(personagem.nivel), anchor="e")
        label_nivel.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_nivel.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 8))

        label_nex = ctk.CTkLabel(info_frame, text="NEX:", anchor="w")
        valor_nex = ctk.CTkLabel(info_frame, text=f"{personagem.nex}%", anchor="e")
        label_nex.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_nex.grid(row=3, column=1, sticky="e", padx=10, pady=(0, 8))

        label_trilha = ctk.CTkLabel(info_frame, text="Trilha:", anchor="w")
        valor_trilha = ctk.CTkLabel(info_frame, text=personagem.trilha, anchor="e")
        label_trilha.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_trilha.grid(row=4, column=1, sticky="e", padx=10, pady=(0, 8))

        label_origem = ctk.CTkLabel(info_frame, text="Origem:", anchor="w")
        valor_origem = ctk.CTkLabel(info_frame, text=getattr(personagem, "origem", None) or "Não informada", anchor="e")
        label_origem.grid(row=5, column=0, sticky="w", padx=10, pady=(0, 8))
        valor_origem.grid(row=5, column=1, sticky="e", padx=10, pady=(0, 8))

        label_atributos = ctk.CTkLabel(info_frame, text="Atributos:", anchor="w")
        label_atributos.grid(row=6, column=0, sticky="nw", padx=10, pady=(0, 8))
        atributos_frame_ficha = ctk.CTkFrame(info_frame)
        atributos_frame_ficha.grid(row=6, column=1, sticky="ew", padx=10, pady=(0, 8))
        atributos_frame_ficha.grid_columnconfigure(tuple(range(5)), weight=1)

        atributos_nomes_ficha = [nome for nome, _ in ATRIBUTOS]
        atributos_salvos_ficha = {}
        for atributo in (personagem.atributos or "").split(","):
            nome, separador, valor = atributo.partition("=")
            if separador:
                atributos_salvos_ficha[nome.strip()] = valor.strip()

        valores_atributos_ficha = {}
        for coluna, nome_atributo in enumerate(atributos_nomes_ficha):
            ctk.CTkLabel(
                atributos_frame_ficha,
                text=nome_atributo,
                font=ctk.CTkFont(size=11)
            ).grid(row=0, column=coluna, sticky="w", padx=5, pady=(4, 0))
            valor_atributo = ctk.CTkLabel(
                atributos_frame_ficha,
                text=atributos_salvos_ficha.get(nome_atributo, "1"),
                font=ctk.CTkFont(size=16, weight="bold")
            )
            valor_atributo.grid(row=1, column=coluna, sticky="w", padx=5, pady=(0, 4))
            valores_atributos_ficha[nome_atributo] = valor_atributo

        ctk.CTkLabel(info_frame, text="História:", anchor="w").grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))
        historia_text = ctk.CTkTextbox(info_frame, width=460, height=180)
        historia_text.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        info_frame.grid_rowconfigure(8, weight=1)
        historia_text.insert("1.0", personagem.historia)
        historia_text.configure(state="disabled")

        tab_edicao = tabview.add("Editar Ficha")
        self._criar_aba_edicao(
            tabview,
            tab_edicao,
            personagem,
            {
                "valor_pv_ficha": valor_pv_ficha,
                "valor_pd_ficha": valor_pd_ficha,
                "resumo_ficha": resumo_ficha,
                "valor_nivel": valor_nivel,
                "valor_nex": valor_nex,
                "valor_origem": valor_origem,
                "valores_atributos_ficha": valores_atributos_ficha,
                "historia_text": historia_text,
            },
        )

        self._criar_aba_pericias(tab_pericias, personagem, ficha)

    def _abrir_seletor_habilidades(self, personagem):
        janela = ctk.CTkToplevel(self)
        janela.title(f"Adicionar Habilidade - {personagem.nome}")
        janela.geometry("620x520")
        janela.minsize(500, 400)
        janela.grab_set()

        filtro_frame = ctk.CTkFrame(janela)
        filtro_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(filtro_frame, text="Categoria:").pack(side="left", padx=(10, 8), pady=12)

        busca_frame = ctk.CTkFrame(janela, fg_color="transparent")
        busca_frame.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(
            busca_frame,
            text="Buscar Habilidades:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))
        busca_var = StringVar()
        busca_entrada = ctk.CTkEntry(
            busca_frame,
            textvariable=busca_var,
            placeholder_text="Digite o nome da habilidade"
        )
        busca_entrada.pack(side="left", fill="x", expand=True)

        conteudo_frame = ctk.CTkFrame(janela, fg_color="transparent")
        conteudo_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        conteudo_frame.grid_columnconfigure(0, weight=1)
        conteudo_frame.grid_columnconfigure(1, weight=2)
        conteudo_frame.grid_rowconfigure(0, weight=1)

        poderes_frame = ctk.CTkScrollableFrame(conteudo_frame)
        poderes_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        detalhes_frame = ctk.CTkFrame(conteudo_frame)
        detalhes_frame.grid(row=0, column=1, sticky="nsew")
        titulo_habilidade = ctk.CTkLabel(
            detalhes_frame,
            text="Selecione uma habilidade",
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=260
        )
        titulo_habilidade.pack(anchor="nw", padx=20, pady=(20, 12))
        descricao_habilidade = ctk.CTkLabel(
            detalhes_frame,
            text="A descricao da habilidade sera exibida aqui.",
            anchor="nw",
            justify="left",
            wraplength=260
        )
        descricao_habilidade.pack(fill="x", anchor="nw", padx=20, pady=(0, 20))

        categoria_atual = "Combatente"

        def atualizar_poderes(categoria=None):
            nonlocal categoria_atual
            if categoria is not None:
                categoria_atual = categoria

            for widget in poderes_frame.winfo_children():
                widget.destroy()

            termo_busca = busca_var.get().strip().lower()
            poderes = [
                poder for poder in HABILIDADES_POR_CATEGORIA.get(categoria_atual, [])
                if termo_busca in poder.lower()
            ]
            if not poderes:
                ctk.CTkLabel(
                    poderes_frame,
                    text="Nenhuma habilidade encontrada."
                ).pack(anchor="w", padx=10, pady=10)
                return

            for poder in poderes:
                ctk.CTkButton(
                    poderes_frame,
                    text=poder,
                    anchor="w",
                    fg_color="transparent",
                    hover_color=("#D9D9D9", "#3A3A3A"),
                    command=lambda habilidade=poder: exibir_detalhes(habilidade)
                ).pack(fill="x", padx=6, pady=3)

        def exibir_detalhes(habilidade):
            titulo_habilidade.configure(text=habilidade)
            descricao_habilidade.configure(
                text=DESCRICOES_HABILIDADES.get(
                    habilidade,
                    "Descricao desta habilidade ainda nao cadastrada."
                )
            )

        filtro = ctk.CTkOptionMenu(
            filtro_frame,
            values=FILTROS_HABILIDADES,
            command=atualizar_poderes,
            dynamic_resizing=False
        )
        filtro.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)
        filtro.set("Combatente")
        atualizar_poderes("Combatente")
        busca_var.trace_add("write", lambda *args: atualizar_poderes())
        busca_entrada.focus_set()

    def _criar_aba_edicao(self, tabview, tab_edicao, personagem, ficha_widgets):
        valor_pv_ficha = ficha_widgets["valor_pv_ficha"]
        valor_pd_ficha = ficha_widgets["valor_pd_ficha"]
        resumo_ficha = ficha_widgets["resumo_ficha"]
        valor_nivel = ficha_widgets["valor_nivel"]
        valor_nex = ficha_widgets["valor_nex"]
        valor_origem = ficha_widgets["valor_origem"]
        valores_atributos_ficha = ficha_widgets["valores_atributos_ficha"]
        historia_text = ficha_widgets["historia_text"]

        edicao_frame = ctk.CTkFrame(tab_edicao)
        edicao_frame.pack(fill="both", expand=True, padx=20, pady=20)
        edicao_frame.grid_columnconfigure(1, weight=1)

        pv_edicao, pd_edicao = self.calcular_pv_pd(personagem)
        recursos_frame_edicao = ctk.CTkFrame(edicao_frame)
        recursos_frame_edicao.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 8))
        recursos_frame_edicao.grid_columnconfigure((0, 1), weight=1)
        valor_pv_edicao = ctk.CTkLabel(recursos_frame_edicao, text=f"PV: {pv_edicao}", font=ctk.CTkFont(size=16, weight="bold"))
        valor_pv_edicao.grid(row=0, column=0, sticky="w", padx=10, pady=8)
        valor_pd_edicao = ctk.CTkLabel(recursos_frame_edicao, text=f"PD: {pd_edicao}", font=ctk.CTkFont(size=16, weight="bold"))
        valor_pd_edicao.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        ctk.CTkLabel(edicao_frame, text="Classe:", anchor="w").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        ctk.CTkLabel(edicao_frame, text=personagem.classe, anchor="e").grid(
            row=1, column=1, sticky="e", padx=10, pady=10
        )

        _, limite_nivel_edicao = obter_limites_nivel(personagem.classe)
        nome_nivel_edicao = obter_nome_nivel(personagem.classe)

        ctk.CTkLabel(edicao_frame, text=f"{nome_nivel_edicao}:", anchor="w").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        nivel_edicao = ctk.CTkOptionMenu(
            edicao_frame,
            values=[str(nivel) for nivel in range(1, limite_nivel_edicao + 1)],
            width=100
        )
        nivel_edicao.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        nivel_edicao.set(
            str(personagem.nivel)
            if 1 <= personagem.nivel <= limite_nivel_edicao
            else "1"
        )

        ctk.CTkLabel(edicao_frame, text="NEX:", anchor="w").grid(
            row=3, column=0, sticky="w", padx=10, pady=10
        )
        nex_edicao = ctk.CTkEntry(edicao_frame, width=100)
        nex_edicao.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        nex_edicao.insert(0, str(personagem.nex))

        nex_edicao_erro = ctk.CTkLabel(edicao_frame, text="", text_color="red", anchor="w")
        nex_edicao_erro.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 4))

        def validar_nex_edicao(event=None):
            nex_texto = nex_edicao.get()
            _, _, erro = validar_nex_texto(nex_texto)
            if erro:
                nex_edicao_erro.configure(text=erro)
                return False
            nex_edicao_erro.configure(text="")
            return True

        nex_edicao.bind("<KeyRelease>", validar_nex_edicao)
        nex_edicao.bind("<FocusOut>", validar_nex_edicao)
        validar_nex_edicao()

        ctk.CTkLabel(edicao_frame, text="Origem:", anchor="w").grid(
            row=5, column=0, sticky="w", padx=10, pady=10
        )
        origem_edicao = ScrollableOriginOptionMenu(edicao_frame, values=ORIGENS, width=460)
        origem_edicao.grid(row=5, column=1, sticky="ew", padx=10, pady=10)
        origem_edicao.set(getattr(personagem, "origem", None) or ORIGENS[0])

        ctk.CTkLabel(edicao_frame, text="Atributos:", anchor="w").grid(
            row=6, column=0, sticky="nw", padx=10, pady=10
        )
        atributos_frame_edicao = ctk.CTkFrame(edicao_frame)
        atributos_frame_edicao.grid(row=6, column=1, sticky="ew", padx=10, pady=10)
        atributos_frame_edicao.grid_columnconfigure(tuple(range(5)), weight=1)

        atributos_nomes = [nome for nome, _ in ATRIBUTOS]
        atributos_salvos = {}
        for atributo in (personagem.atributos or "").split(","):
            nome, separador, valor = atributo.partition("=")
            if separador:
                atributos_salvos[nome.strip()] = valor.strip()

        atributos_edicao = {}
        for coluna, nome_atributo in enumerate(atributos_nomes):
            ctk.CTkLabel(atributos_frame_edicao, text=nome_atributo).grid(
                row=0, column=coluna, sticky="w", padx=5, pady=(0, 5)
            )
            valor_atributo = ctk.CTkEntry(atributos_frame_edicao, width=70)
            valor_atributo.grid(row=1, column=coluna, sticky="ew", padx=5, pady=5)
            valor_atributo.insert(0, atributos_salvos.get(nome_atributo, "1"))
            atributos_edicao[nome_atributo] = valor_atributo

        ctk.CTkLabel(edicao_frame, text="História:", anchor="w").grid(
            row=7, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0)
        )
        historia_edicao = ctk.CTkTextbox(edicao_frame, height=260)
        historia_edicao.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        edicao_frame.grid_rowconfigure(8, weight=1)
        historia_edicao.insert("1.0", personagem.historia or "")

        def salvar_edicao():
            nivel_texto = nivel_edicao.get().strip()
            _, nex, erro_nex = validar_nex_texto(nex_edicao.get())
            if not nivel_texto.isdigit() or not 1 <= int(nivel_texto) <= limite_nivel_edicao:
                messagebox.showerror(
                    "Erro",
                    f"O {nome_nivel_edicao.lower()} deve ser um número entre 1 e {limite_nivel_edicao}."
                )
                return
            if erro_nex:
                messagebox.showerror("Erro", erro_nex + ".")
                return

            atributos_valores = []
            for nome_atributo in atributos_nomes:
                valor = atributos_edicao[nome_atributo].get().strip()
                if not valor.isdigit():
                    messagebox.showerror("Erro", f"O valor de {nome_atributo} deve ser numérico.")
                    return
                atributos_valores.append(f"{nome_atributo}={valor}")

            try:
                dados_atualizados = atualizar_personagem(
                    personagem.id,
                    int(nivel_texto),
                    nex,
                    origem_edicao.get().strip(),
                    ", ".join(atributos_valores),
                    historia_edicao.get("1.0", "end").strip(),
                )
                if dados_atualizados is None:
                    messagebox.showerror("Erro", "Personagem não encontrado no banco de dados.")
                    return

                personagem.nivel = dados_atualizados["nivel"]
                personagem.nex = dados_atualizados["nex"]
                personagem.origem = dados_atualizados["origem"]
                personagem.atributos = dados_atualizados["atributos"]
                personagem.historia = dados_atualizados["historia"]
                pv_atualizado, pd_atualizado = self.calcular_pv_pd(personagem)
                valor_pv_ficha.configure(text=f"PV: {pv_atualizado}")
                valor_pd_ficha.configure(text=f"PD: {pd_atualizado}")
                valor_pv_edicao.configure(text=f"PV: {pv_atualizado}")
                valor_pd_edicao.configure(text=f"PD: {pd_atualizado}")
                resumo_ficha.configure(
                    text=f"Classe: {personagem.classe} | Nível: {personagem.nivel} | NEX: {personagem.nex}% | Origem: {personagem.origem or 'Não informada'}"
                )
                valor_nivel.configure(text=str(personagem.nivel))
                valor_nex.configure(text=f"{personagem.nex}%")
                valor_origem.configure(text=personagem.origem or "Não informada")
                atributos_atualizados = {}
                for atributo in (personagem.atributos or "").split(","):
                    nome, separador, valor = atributo.partition("=")
                    if separador:
                        atributos_atualizados[nome.strip()] = valor.strip()
                for nome_atributo, valor_atributo in valores_atributos_ficha.items():
                    valor_atributo.configure(text=atributos_atualizados.get(nome_atributo, "1"))
                historia_text.configure(state="normal")
                historia_text.delete("1.0", "end")
                historia_text.insert("1.0", personagem.historia)
                historia_text.configure(state="disabled")
                self.atualizar_lista()
                tabview.set("Dados Gerais")
                messagebox.showinfo("Sucesso", "Ficha atualizada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar ficha: {str(e)}")

        ctk.CTkButton(
            edicao_frame,
            text="Salvar Alterações",
            command=salvar_edicao
        ).grid(row=9, column=1, sticky="e", padx=10, pady=10)

    def _criar_aba_pericias(self, tab_pericias, personagem, ficha):
        pericias_frame = ctk.CTkScrollableFrame(tab_pericias)
        pericias_frame.pack(fill="both", expand=True, padx=20, pady=20)

        headers = ["Pericia", "Treino", "Atributo", "Extra", "Total"]
        for index, titulo in enumerate(headers):
            ctk.CTkLabel(pericias_frame, text=titulo, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=index, padx=8, pady=(0, 6), sticky="w"
            )

        dados_pericias_salvos = self._carregar_dados_pericias(personagem)
        rows_state = []

        for row_index, (nome_pericia, atributo_pericia) in enumerate(zip(PERICIAS, ATRIBUTOS_PERICIAS), start=1):
            dados_pericia = next((item for item in dados_pericias_salvos if item.get("nome") == nome_pericia), None)
            if dados_pericia is None:
                dados_pericia = {
                    "nome": nome_pericia,
                    "atributo": atributo_pericia,
                    "treino": 0,
                    "extra": 0,
                    "total": 0,
                }

            ctk.CTkLabel(pericias_frame, text=nome_pericia, anchor="w").grid(
                row=row_index, column=0, padx=8, pady=2, sticky="w"
            )

            treino_menu = ctk.CTkOptionMenu(pericias_frame, values=["0", "5", "10", "15"], width=80)
            treino_menu.set(str(dados_pericia.get("treino", 0)))
            treino_menu.grid(row=row_index, column=1, padx=8, pady=2, sticky="w")

            ctk.CTkLabel(pericias_frame, text=atributo_pericia, anchor="w").grid(
                row=row_index, column=2, padx=8, pady=2, sticky="w"
            )

            extra_var = StringVar(value=str(dados_pericia.get("extra", 0)))
            ctk.CTkEntry(pericias_frame, textvariable=extra_var, width=80).grid(
                row=row_index, column=3, padx=8, pady=2, sticky="w"
            )

            total_var = StringVar(value=str(dados_pericia.get("total", 0)))
            ctk.CTkLabel(pericias_frame, textvariable=total_var, anchor="w", width=60).grid(
                row=row_index, column=4, padx=8, pady=2, sticky="w"
            )

            rows_state.append({
                "nome": nome_pericia,
                "atributo": atributo_pericia,
                "treino_menu": treino_menu,
                "extra_var": extra_var,
                "total_var": total_var,
            })

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
            personagens = listar_personagens()

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
                origem_valor = getattr(personagem, "origem", None) or ""
                ctk.CTkLabel(top_row, text=f"Classe: {personagem.classe} | Nível: {personagem.nivel} | NEX: {personagem.nex}% | Origem: {origem_valor or 'Não informada'}").grid(row=1, column=1, sticky="w")

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
