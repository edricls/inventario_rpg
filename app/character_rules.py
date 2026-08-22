def obter_limites_nivel(classe):
    return 1, 4 if classe == "Sobrevivente" else 20


def obter_nome_nivel(classe):
    return "Estágio" if classe == "Sobrevivente" else "Nível"


def validar_nex_texto(texto):
    texto_normalizado = str(texto).strip()
    if texto_normalizado == "":
        return texto_normalizado, 0, None

    if not texto_normalizado.isdigit() or not 0 <= int(texto_normalizado) <= 99:
        return texto_normalizado, None, "O valor de NEX deve ser entre 0 e 99"

    return texto_normalizado, int(texto_normalizado), None


def calcular_pv_pd(personagem, nivel=None, atributos=None):
    nivel_atual = nivel if nivel is not None else personagem.nivel
    nivel_atual = int(nivel_atual) if str(nivel_atual).isdigit() else 1
    atributos_texto = atributos if atributos is not None else personagem.atributos
    valores_atributos = {}
    for atributo in (atributos_texto or "").split(","):
        nome, separador, valor = atributo.partition("=")
        if separador:
            try:
                valores_atributos[nome.strip()] = int(valor.strip())
            except ValueError:
                valores_atributos[nome.strip()] = 0

    vigor = valores_atributos.get("Vigor", 0)
    presenca = valores_atributos.get("Presença", 0)
    niveis_adicionais = max(nivel_atual - 1, 0)

    if personagem.classe == "Combatente":
        pv = 20 + vigor + niveis_adicionais * (4 + vigor)
        pd = 6 + presenca + niveis_adicionais * (3 + presenca)
    elif personagem.classe == "Especialista":
        pv = 16 + vigor + niveis_adicionais * (3 + vigor)
        pd = 8 + presenca + niveis_adicionais * (4 + presenca)
    elif personagem.classe == "Ocultista":
        pv = 12 + vigor + niveis_adicionais * (2 + vigor)
        pd = 10 + presenca + niveis_adicionais * (5 + presenca)
    else:
        pv = 8 + vigor + niveis_adicionais * 2
        pd = 4 + presenca + niveis_adicionais * 2

    return pv, pd