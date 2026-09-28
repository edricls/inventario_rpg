import json


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


def calcular_defesa(personagem, atributos=None):
    atributos_texto = atributos if atributos is not None else personagem.atributos
    agilidade = 0
    for atributo in (atributos_texto or "").split(","):
        nome, separador, valor = atributo.partition("=")
        if separador and nome.strip() == "Agilidade":
            try:
                agilidade = int(valor.strip())
            except ValueError:
                agilidade = 0
            break

    return 10 + agilidade


def carregar_valores_editados(personagem):
    try:
        valores = json.loads(getattr(personagem, "valores_editados", None) or "{}")
        if isinstance(valores, dict):
            return {
                chave: int(valor)
                for chave, valor in valores.items()
                if isinstance(valor, (int, float, str)) and str(valor).lstrip("-").isdigit()
            }
    except (TypeError, ValueError):
        pass
    return {}


def calcular_recursos(personagem, pericias=None, nivel=None, atributos=None, valores_editados=None):
    nivel_atual = nivel if nivel is not None else personagem.nivel
    pv, pd = calcular_pv_pd(personagem, nivel_atual, atributos)
    defesa = calcular_defesa(personagem, atributos)
    totais_pericias = {
        item.get("nome"): item.get("total", 0)
        for item in (pericias or [])
        if isinstance(item, dict)
    }

    def obter_total(nome):
        try:
            return int(totais_pericias.get(nome, 0))
        except (TypeError, ValueError):
            return 0

    bases = {
        "pv": pv,
        "pd": pd,
        "pd_turno": int(nivel_atual),
        "defesa": defesa,
        "esquiva": defesa + obter_total("Reflexos"),
        "bloqueio": obter_total("Fortitude"),
    }
    ajustes = valores_editados if valores_editados is not None else carregar_valores_editados(personagem)
    return {
        nome: valor + int(ajustes.get(nome, 0))
        for nome, valor in bases.items()
    }