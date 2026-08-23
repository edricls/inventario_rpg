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


def atualizar_personagem(personagem_id, nivel, nex, origem, atributos, historia):
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
        db.commit()
        return {
            "nivel": personagem_db.nivel,
            "nex": personagem_db.nex,
            "origem": personagem_db.origem,
            "atributos": personagem_db.atributos,
            "historia": personagem_db.historia,
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
        return habilidades if isinstance(habilidades, list) else []
    except (TypeError, ValueError):
        return []


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