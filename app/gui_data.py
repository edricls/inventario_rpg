CLASSES = ["Combatente", "Especialista", "Ocultista", "Sobrevivente"]

TRILHAS_POR_CLASSE = {
    "Combatente": ["Aniquilador", "Guerreiro", "Operações Especiais", "Comandante de Campo", "Tropa de Choque"],
    "Especialista": ["Infiltrador", "Negociador", "Técnico", "Atirador de Elite", "Médico de Campo"],
    "Ocultista": ["Conduíte", "Flagelador", "Graduado", "Intuitivo", "Lâmina Paranormal"],
    "Sobrevivente": ["Durão", "Esperto", "Esotérico"]
}

ATRIBUTOS = [
    ("Força", "forca"),
    ("Agilidade", "agilidade"),
    ("Intelecto", "intelecto"),
    ("Presença", "presenca"),
    ("Vigor", "vigor")
]

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

ORIGENS = [
    "Acadêmico",
    "Agente de Saúde",
    "Amnésico",
    "Artista",
    "Atleta",
    "Chef",
    "Criminoso",
    "Cultista Arrependido",
    "Desgarrado",
    "Engenheiro",
    "Executivo",
    "Investigador",
    "Lutador",
    "Magnata",
    "Mercenário",
    "Militar",
    "Operário",
    "Policial",
    "Religioso",
    "Servidor Publico",
    "Teórico da Cospiração",
    "T.I",
    "Trabalhador Rural",
    "Trambiqueiro",
    "Universitário",
    "Vítima"
]

FILTROS_HABILIDADES = [
    "Combatente",
    "Especialista",
    "Ocultista",
    "Sobrevivente",
    "Mundano",
    "Poderes Paranormais",
    "Poderes Gerais",
    "Origens",
]

HABILIDADES_POR_CATEGORIA = {
    "Combatente": [
        "Golpe Pesado",
        "Tiro Certeiro",
        "Reflexos Defensivos",
    ],
    "Especialista": [
        "Perito",
        "Engenhosidade",
        "Eclético",
    ],
    "Ocultista": [
        "Camuflar Ocultismo",
        "Ritual Potente",
        "Criar Selo",
    ],
    "Sobrevivente": [
        "Empenho",
        "Cicatrizado",
        "Estágio 2 - Durão",
    ],
    "Mundano": [
        "Empenho",
    ],
    "Poderes Paranormais": [
        "Absorver Conhecimento",
        "Afortunado",
    ],
    "Poderes Gerais": [
        "Acrobático",
        "Atlético",
    ],
    "Origens": ORIGENS,
}