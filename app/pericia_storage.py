import json

from app.database import SessionLocal
from app.models import Personagem


def dados_pericias_padrao(nomes_pericias, atributos_pericias):
    return [
        {"nome": nome_pericia, "atributo": atributo_pericia, "treino": 0, "extra": 0, "total": 0}
        for nome_pericia, atributo_pericia in zip(nomes_pericias, atributos_pericias)
    ]


def carregar_dados_pericias(personagem, nomes_pericias, atributos_pericias):
    dados_padrao = dados_pericias_padrao(nomes_pericias, atributos_pericias)

    if not personagem.pericias:
        return dados_padrao

    try:
        dados = json.loads(personagem.pericias)
        if isinstance(dados, list):
            return dados
    except (TypeError, ValueError):
        pass

    return dados_padrao


def salvar_dados_pericias(personagem, dados_pericias):
    db = SessionLocal()
    try:
        personagem_db = db.query(Personagem).filter(Personagem.id == personagem.id).first()
        if personagem_db is None:
            return

        dados_json = json.dumps(dados_pericias)
        personagem_db.pericias = dados_json
        if hasattr(personagem, "pericias"):
            personagem.pericias = dados_json
        db.commit()
    finally:
        db.close()