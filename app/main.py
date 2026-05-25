#Este é o arquivo principal, o "ponto de entrada" do seu programa.
#É o arquivo que você vai executar no terminal usando o comando python -m app.main.
from app.database import engine, Base, SessionLocal
from app.models import Personagem
from rich.console import Console # Usando a biblioteca Rich que você instalou

console = Console()

def iniciar_sistema():
    # Isso roda sempre, mas o SQLAlchemy é inteligente: se as tabelas 
    # já existirem no arquivo .db, ele não faz nada e não apaga seus dados.
    Base.metadata.create_all(bind=engine)

    # LOOP do jogo
    while True:
        console.print("\n[bold blue]=== GERENCIADOR DE INVENTÁRIO RPG ===[/bold blue]")
        print("1. Criar Novo Personagem")
        print("2. Listar Personagens Existentes")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            # O sistema SÓ vai criar o personagem se o usuário digitar 1
            nome_input = input("Digite o nome do personagem: ")
            classe_input = input("Digite a classe: ")
            nivel_input = int(input("Digite o nível: "))
            nex_input = int(input("Digite o NEX: "))
            atributos_input = input("Digite os atributos (ex: força=2, destreza=1, vigor=2, presença=3, inteligencia=4): ")
            trilha_input = input("Digite a trilha: ")
            historia_input = input("Digite a história do personagem: ")

            # Cria o molde dinamicamente com o que foi digitado no teclado
            novo_p = Personagem(nome=nome_input, classe=classe_input, nivel=nivel_input, nex=nex_input, atributos=atributos_input, trilha=trilha_input, historia=historia_input)

            # Salva no banco
            db = SessionLocal()
            db.add(novo_p)
            db.commit()
            db.close()

            console.print(f"[bold green]Sucesso:[/] {nome_input} foi salvo no banco de dados!")

        elif opcao == "2":
            # Aqui você faria uma busca (query) no banco para listar quem já existe
            print("Buscando personagens no banco...")
            # (Lógica de listagem virá depois)

        elif opcao == "3":
            print("Saindo do sistema... Até logo!")
            break # Quebra o loop 'while True' e encerra o programa
            
        else:
            console.print("[bold red]Opção inválida![/]")

if __name__ == "__main__":
    iniciar_sistema()