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

DESCRICOES_HABILIDADES = {
    "Golpe Pesado": "O dano de suas armas corpo a corpo aumenta em mais um dado do mesmo tipo.",
    "Tiro Certeiro": "Se estiver usando uma arma de disparo, você soma sua Agilidade nas rolagens de dano e ignora a penalidade contra alvos envolvidos em combate corpo a corpo (mesmo se não usar a ação mirar). Pré-requisito: treinado em Pontaria.",
    "Reflexos Defensivos": "Você recebe +2 em Defesa e em testes de resistência. Pré-requisitos: Agi 2.",
    "Perito": "Escolha duas perícias nas quais você é treinado (exceto Luta e Pontaria). Quando faz um teste de uma dessas perícias, você pode gastar 2 PE para somar +1d6 no resultado do teste. Conforme avança de NEX, você pode gastar +1 PE para aumentar o dado de bônus. Por exemplo, em NEX 55%, pode gastar 4 PE para receber +1d10 no teste.",
    "Engenhosidade": "Em NEX 40%, quando usa sua habilidade Eclético, você pode gastar 2 PE adicionais para receber os benefícios de ser veterano na perícia. Em NEX 75%, pode gastar 4 PE adicionais para receber os benefícios de ser expert na perícia.",
    "Eclético": "Quando faz um teste de uma perícia, você pode gastar 2 PE para receber os benefícios de ser treinado nesta perícia.",
    "Camuflar Ocultismo": "Você pode gastar uma ação livre para esconder símbolos e sigilos que estejam desenhados ou gravados em objetos ou em sua pele, tornando-os invisíveis para outras pessoas além de você mesmo. Além disso, quando lança um ritual, pode gastar +2 PE para lançá-lo sem usar componentes ritualísticos e sem gesticular (o que permite conjurar um ritual com as mãos presas), usando apenas concentração. Outros seres só perceberão que você lançou um ritual se passarem num teste de Ocultismo (DT 25).",
    "Ritual Potente": "Você soma seu Intelecto nas rolagens de dano ou nos efeitos de cura de seus rituais. Pré-requisito: Int 2.",
    "Criar Selo": "Você sabe fabricar selos paranormais de rituais que conheça. Fabricar um selo gasta uma ação de interlúdio e um número de PE iguais ao custo de conjurar o ritual. Você pode ter um número máximo de selos criados a qualquer momento igual à sua Presença.",
    "Empenho": "Você pode não ter treinamento especial, mas compensa com dedicação e esforço. Quando faz um teste de perícia, você pode gastar 1 PE para receber +2 nesse teste.",
    "Cicatrizado": "No 5º estágio, você já viu — e sobreviveu — a sua cota de horrores. Isso deixou marcas em seu corpo e sua mente, mas também o deixou mais forte. Escolha um tipo de perigo paranormal que seu personagem já enfrentou, de um elemento específico (Sangue, Morte…). Você possui algum trauma em relação a esse perigo e sofre –d20 em testes de resistência contra ele. Contudo, uma vez por sessão de jogo você pode se esforçar ao máximo para não se deixar cair ou se abater. Como uma reação, você pode sacrificar 1 PV permanentemente para ignorar um dano mental ou gasto de PE, ou pode sacrificar permanentemente 1 PE para reduzir um dano físico à metade.",
    "Estágio 2 - Durão": "Você recebe +4 PV. Quando subir para o 3º estágio, recebe +2 PV.",
    "Absorver Conhecimento": "Você se conecta com o Conhecimento do Outro Lado para adquirir informação de forma paranormal, sem precisar gastar tempo de pesquisa. Se estiver empunhando uma fonte de conhecimento escrito (como um livro, um texto aberto em um celular ou uma pedra de runas), você pode gastar 1 PE e uma ação completa para fazer uma pergunta a esta fonte. Se a resposta estiver armazenada na fonte, você a obtém automaticamente. Se usar este poder em conjunto com a ação de interlúdio ler, você aumenta o dado de bônus recebido por esta ação em um passo (de d6 para 1d8, por exemplo). Afinidade: quando usa um ritual de Conhecimento que tenha como alvo 1 pessoa (exceto você), se puder tocar o alvo o custo desse ritual é reduzido em –1 PE.",
    "Afortunado": "A Energia considera resultados medíocres entediantes. Uma vez por rolagem, você pode rolar novamente um resultado 1 em qualquer dado que não seja d20.Afinidade: além disso, uma vez por teste, você pode rolar novamente um resultado 1 em d20.",
    "Acrobático": "Você possui um talento natural para piruetas, cambalhotas e outras acrobacias complexas. Você recebe treinamento em Acrobacia ou, se já for treinado nesta perícia, recebe +2 nela. Além disso, terreno difícil não reduz seu deslocamento nem o impede de realizar investidas. Pré-requisito: Agi 2.",
    "Atlético": "Você possui um corpo atlético, resultado de uma fortuita disposição genética ou árduo treinamento. Você recebe treinamento em Atletismo ou, se já for treinado nesta perícia, recebe +2 nela. Além disso, recebe +3m em seu deslocamento. Pré-requisito: For 2.",
}

SIMBOLOS_RITUAIS = ["Sangue", "Morte", "Conhecimento", "Energia"]

RITUAIS_POR_SIMBOLO = {
    "Sangue": ["Arma Atroz"],
    "Morte": ["Cicatrização"],
    "Conhecimento": ["Desfazer Sinapses"],
    "Energia": ["Coincidencia Forçada"],
}

DESCRICOES_RITUAIS = {
    "Arma Atroz": "A arma é recoberta por veias carmesim e passa a exalar uma aura de violência. Ela fornece +2 em testes de ataque e +1 na margem de ameaça.\n\nDiscente (+2 PE): muda o bônus para +5 em testes de ataque. Requer 2º círculo.\n\nVerdadeiro (+5 PE): muda o bônus para +5 em testes de ataque e +2 na margem de ameaça e no multiplicador de crítico. Requer 3º círculo e afinidade.",
    "Cicatrização": "Você acelera o tempo ao redor das feridas do alvo, que cicatrizam instantaneamente. O alvo recupera 3d8+3 PV, mas envelhece 1 ano automaticamente.\n\nDiscente (+2 PE): aumenta a cura para 5d8+5 PV. Requer 2º círculo.\n\nVerdadeiro (+9 PE): muda o alcance para “curto”, o alvo para “seres escolhidos” e aumenta a cura para 7d8+7 PV. Requer 4º círculo e afinidade com Morte.",
    "Desfazer Sinapses": "Enganam-se aqueles que pensam que o Conhecimento Paranormal é incapaz de causar dano físico; inexistir é um dos processos mais terríveis que podem acontecer com alguém. A entidade do Conhecimento inexiste bilhões de neurônios de dentro do cérebro do alvo, causando a angústia inexplicável do vazio. O alvo sofre 2d6+2 pontos de dano de Conhecimento e fica frustrado por uma rodada. Se passar no teste de resistência, sofre apenas metade do dano e evita a condição. O alvo precisa ter um cérebro; o efeito se reflete como uma dor de cabeça severa que faz sangrar levemente pelos olhos, narinas, orelhas e boca.\n\nDiscente (+2 PE): muda o alcance para longo, o dano para 3d6+3 e o alvo para até 5 seres a sua escolha. Requer 2º círculo.\n\nVerdadeiro (+5 PE): muda o alcance para extremo, o dano para 8d6+8 e a condição para esmorecido. Se passar no teste de resistência, em vez de esmorecido, fica frustrado. Requer 3º círculo.",
    "Coincidencia Forçada": "Você manipula os caminhos do caos para que o alvo tenha mais sorte. O alvo recebe +2 em testes de perícias.\n\nDiscente (+2 PE): muda o alvo para aliados à sua escolha. Requer 2º círculo.\n\nVerdadeiro (+5 PE): muda o alvo para aliados à sua escolha e o bônus para +5. Requer 3º círculo e afinidade."
    }