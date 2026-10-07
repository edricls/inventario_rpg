import json

from app.database import SessionLocal
from app.models import Personagem


def listar_personagens():
    db = SessionLocal()
    try:
        return db.query(Personagem).all()
    finally:
        db.close()


def salvar_personagem(personagem):
    db = SessionLocal()
    try:
        db.add(personagem)
        db.commit()
    finally:
        db.close()


def atualizar_personagem(
    personagem_id,
    nivel,
    nex,
    origem,
    atributos,
    historia,
    deslocamento="9m/6q",
    valores_editados=None,
):
    db = SessionLocal()
    try:
        personagem_db = db.query(Personagem).filter(Personagem.id == personagem_id).first()
        if personagem_db is None:
            return None

        personagem_db.nivel = nivel
        personagem_db.nex = nex
        personagem_db.origem = origem
        personagem_db.atributos = atributos
        personagem_db.historia = historia
        personagem_db.deslocamento = deslocamento
        if valores_editados is not None:
            personagem_db.valores_editados = valores_editados
        db.commit()
        return {
            "nivel": personagem_db.nivel,
            "nex": personagem_db.nex,
            "origem": personagem_db.origem,
            "atributos": personagem_db.atributos,
            "historia": personagem_db.historia,
            "deslocamento": personagem_db.deslocamento,
            "valores_editados": personagem_db.valores_editados,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def remover_personagem(personagem):
    db = SessionLocal()
    try:
        db.delete(personagem)
        db.commit()
    finally:
        db.close()


def carregar_habilidades(personagem):
    if not personagem.habilidades:
        return []

    try:
        habilidades = json.loads(personagem.habilidades)
        if not isinstance(habilidades, list):
            return []

        return [
            habilidade.get("nome") if isinstance(habilidade, dict) else habilidade
            for habilidade in habilidades
            if isinstance(habilidade, (dict, str))
            and (
                isinstance(habilidade, str)
                or isinstance(habilidade.get("nome"), str)
            )
        ]
    except (TypeError, ValueError):
        return []


def obter_descricao_habilidade(personagem, nome_habilidade):
    if not personagem.habilidades:
        return None

    try:
        habilidades = json.loads(personagem.habilidades)
        if not isinstance(habilidades, list):
            return None

        for habilidade in habilidades:
            if isinstance(habilidade, dict) and habilidade.get("nome") == nome_habilidade:
                return habilidade.get("descricao")
        return None
    except (TypeError, ValueError):
        return None


def salvar_descricao_habilidade(personagem, nome_habilidade, descricao):
    if not personagem.habilidades:
        habilidades = []
    else:
        try:
            habilidades = json.loads(personagem.habilidades)
        except (TypeError, ValueError):
            habilidades = []

    if not isinstance(habilidades, list):
        habilidades = []

    novas_habilidades = []
    encontrado = False
    for habilidade in habilidades:
        if isinstance(habilidade, dict) and habilidade.get("nome") == nome_habilidade:
            habilidade_atualizada = dict(habilidade)
            habilidade_atualizada["descricao"] = descricao
            novas_habilidades.append(habilidade_atualizada)
            encontrado = True
        elif isinstance(habilidade, str) and habilidade == nome_habilidade:
            novas_habilidades.append({"nome": habilidade, "descricao": descricao})
            encontrado = True
        else:
            novas_habilidades.append(habilidade)

    if not encontrado:
        novas_habilidades.append({"nome": nome_habilidade, "descricao": descricao})

    salvar_habilidades(personagem, novas_habilidades)


def salvar_habilidades(personagem, habilidades):
    db = SessionLocal()
    try:
        personagem_db = db.query(Personagem).filter(Personagem.id == personagem.id).first()
        if personagem_db is None:
            return

        habilidades_json = json.dumps(habilidades, ensure_ascii=False)
        personagem_db.habilidades = habilidades_json
        personagem.habilidades = habilidades_json
        db.commit()
    finally:
        db.close()


def carregar_rituais(personagem):
    if not personagem.rituais:
        return []

    try:
        rituais = json.loads(personagem.rituais)
        if not isinstance(rituais, list):
            return []
        return [
            ritual if isinstance(ritual, dict) else {"nome": ritual, "simbolo": None}
            for ritual in rituais
            if isinstance(ritual, (dict, str))
        ]
    except (TypeError, ValueError):
        return []


def obter_descricao_ritual(personagem, nome_ritual):
    if not personagem.rituais:
        return None

    try:
        rituais = json.loads(personagem.rituais)
        if not isinstance(rituais, list):
            return None

        for ritual in rituais:
            if isinstance(ritual, dict) and ritual.get("nome") == nome_ritual:
                return ritual.get("descricao")
        return None
    except (TypeError, ValueError):
        return None


def salvar_descricao_ritual(personagem, nome_ritual, descricao):
    if not personagem.rituais:
        rituais = []
    else:
        try:
            rituais = json.loads(personagem.rituais)
        except (TypeError, ValueError):
            rituais = []

    if not isinstance(rituais, list):
        rituais = []

    novos_rituais = []
    encontrado = False
    for ritual in rituais:
        if isinstance(ritual, dict) and ritual.get("nome") == nome_ritual:
            ritual_atualizado = dict(ritual)
            ritual_atualizado["descricao"] = descricao
            novos_rituais.append(ritual_atualizado)
            encontrado = True
        elif isinstance(ritual, str) and ritual == nome_ritual:
            novos_rituais.append({"nome": ritual, "simbolo": None, "descricao": descricao})
            encontrado = True
        else:
            novos_rituais.append(ritual)

    if not encontrado:
        novos_rituais.append({"nome": nome_ritual, "simbolo": None, "descricao": descricao})

    salvar_rituais(personagem, novos_rituais)


def salvar_rituais(personagem, rituais):
    db = SessionLocal()
    try:
        personagem_db = db.query(Personagem).filter(Personagem.id == personagem.id).first()
        if personagem_db is None:
            return

        rituais_json = json.dumps(rituais, ensure_ascii=False)
        personagem_db.rituais = rituais_json
        personagem.rituais = rituais_json
        db.commit()
    finally:
        db.close()