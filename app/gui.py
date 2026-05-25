import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from app.database import SessionLocal
from app.models import Personagem

class GerenciadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Inventário RPG")
        self.root.geometry("800x600")
        
        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba 1: Criar Personagem
        self.frame_criar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_criar, text="Criar Personagem")
        self.criar_aba_criar()
        
        # Aba 2: Listar Personagens
        self.frame_listar = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_listar, text="Listar Personagens")
        self.criar_aba_listar()
    
    def criar_aba_criar(self):
        """Cria a interface para adicionar novo personagem"""
        
        campos = [
            ("Nome", "nome"),
            ("Classe", "classe"),
            ("Nível", "nivel"),
            ("NEX", "nex"),
            ("Atributos", "atributos"),
            ("Trilha", "trilha"),
            ("História", "historia")
        ]
        
        self.entradas = {}
        
        for idx, (label, chave) in enumerate(campos):
            ttk.Label(self.frame_criar, text=label + ":").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            
            if chave == "historia":
                # Campo de texto maior para história
                entrada = scrolledtext.ScrolledText(self.frame_criar, height=4, width=50)
            else:
                entrada = ttk.Entry(self.frame_criar, width=50)
            
            entrada.grid(row=idx, column=1, sticky="ew", padx=10, pady=5)
            self.entradas[chave] = entrada
        
        # Botão Salvar
        ttk.Button(self.frame_criar, text="Salvar Personagem", command=self.salvar_personagem).grid(
            row=len(campos), column=1, sticky="e", padx=10, pady=20
        )
        
        self.frame_criar.columnconfigure(1, weight=1)
    
    def criar_aba_listar(self):
        """Cria a interface para listar personagens"""
        
        # Botão para atualizar lista
        ttk.Button(self.frame_listar, text="Atualizar Lista", command=self.atualizar_lista).pack(padx=10, pady=10)
        
        # Área de texto para exibir personagens
        self.texto_lista = scrolledtext.ScrolledText(self.frame_listar, height=25, width=90)
        self.texto_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Atualizar lista automaticamente
        self.atualizar_lista()
    
    def salvar_personagem(self):
        """Salva um novo personagem no banco de dados"""
        
        try:
            # Validar campos obrigatórios
            nome = self.entradas["nome"].get().strip()
            classe = self.entradas["classe"].get().strip()
            
            if not nome or not classe:
                messagebox.showerror("Erro", "Nome e Classe são obrigatórios!")
                return
            
            # Criar personagem
            novo_p = Personagem(
                nome=nome,
                classe=classe,
                nivel=int(self.entradas["nivel"].get() or 1),
                nex=int(self.entradas["nex"].get() or 0),
                atributos=self.entradas["atributos"].get(),
                trilha=self.entradas["trilha"].get(),
                historia=self.entradas["historia"].get("1.0", tk.END)
            )
            
            # Salvar no banco
            db = SessionLocal()
            db.add(novo_p)
            db.commit()
            db.close()
            
            # Limpar campos
            for entrada in self.entradas.values():
                if isinstance(entrada, scrolledtext.ScrolledText):
                    entrada.delete("1.0", tk.END)
                else:
                    entrada.delete(0, tk.END)
            
            messagebox.showinfo("Sucesso", f"Personagem '{nome}' salvo com sucesso!")
            
            # Atualizar lista
            self.atualizar_lista()
            
        except ValueError:
            messagebox.showerror("Erro", "Nível e NEX devem ser números!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def atualizar_lista(self):
        """Atualiza a lista de personagens exibida"""
        
        self.texto_lista.delete("1.0", tk.END)
        
        try:
            db = SessionLocal()
            personagens = db.query(Personagem).all()
            db.close()
            
            if not personagens:
                self.texto_lista.insert(tk.END, "Nenhum personagem encontrado no banco de dados.")
            else:
                texto = f"{'='*80}\n"
                texto += f"{'PERSONAGENS REGISTRADOS':^80}\n"
                texto += f"{'='*80}\n\n"
                
                for p in personagens:
                    texto += f"Nome: {p.nome}\n"
                    texto += f"Classe: {p.classe}\n"
                    texto += f"Nível: {p.nivel}\n"
                    texto += f"NEX: {p.nex}\n"
                    texto += f"Trilha: {p.trilha}\n"
                    texto += f"Atributos: {p.atributos}\n"
                    texto += f"História: {p.historia}\n"
                    texto += f"{'-'*80}\n\n"
                
                self.texto_lista.insert(tk.END, texto)
        
        except Exception as e:
            self.texto_lista.insert(tk.END, f"Erro ao carregar personagens: {str(e)}")


def iniciar_gui():
    """Inicia a interface gráfica"""
    root = tk.Tk()
    app = GerenciadorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_gui()
