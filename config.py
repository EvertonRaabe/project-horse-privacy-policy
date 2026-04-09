import random, uuid

NOMES = [
    # Natureza e elementos
    'Pé de Vento','Relâmpago','Trovão','Estrela do Sul','Rosa Brava',
    'Furacão','Cometa','Meteoro','Brisa Real','Vulcão',
    'Sol Nascente','Lua Cheia','Vento Norte','Mar Bravio','Serra Alta',
    'Chuva de Ouro','Neblina','Aurora Boreal','Ventania','Maré Alta',
    'Chama Viva','Gelo Eterno','Raio de Sol','Terral','Correnteza',
    # Metais e pedras preciosas
    'Pegasus','Raio Negro','Tempestade','Prata Viva','Noite Eterna',
    'Ouro Vivo','Diamante','Safira','Esmeralda','Rubi',
    'Ônix','Topázio','Ametista','Granito','Bronze Imperial',
    # Força e poder
    'Touro Bravo','Leão do Cerrado','Falcão Real','Jaguar Negro','Corvo Veloz',
    'Trovão Dourado','Relâmpago Bravo','Rei da Pista','Guerreiro','Conquistador',
    # Épicos e lendários
    'Excalibur','Minotauro','Poseidon','Ares','Titã',
    'Lendário','Imortal','Invictus','Gladiador','Spartacus',
    # Brasileiros e regionais
    'Sertanejo','Pantaneiro','Gaúcho Bravo','Nordestino','Caatinga',
    'Rio Grande','Cerradão','Savana','Pampas','Caipira Nobre',
]

RACAS = {
    'Puro Sangue Inglês': {'vel':+0.50,'stamina':-10,'preco':1.6,'emoji':'🏆','desc':'O mais veloz. Pouca resistência.','cores_possiveis':[0,3,4,5,7]},
    'Árabe':              {'vel':+0.30,'stamina': +5,'preco':1.3,'emoji':'⭐','desc':'Elegante e rápido. Boa stamina.','cores_possiveis':[0,2,4,6]},
    'Turcomeno':          {'vel':+0.55,'stamina':-20,'preco':1.7,'emoji':'⚡','desc':'Velocidade extrema. Esgota rápido.','cores_possiveis':[2,4,6]},
    'Quarto de Milha':    {'vel':+0.40,'stamina':-15,'preco':1.2,'emoji':'💨','desc':'Sprint explosivo. Cansa em longas.','cores_possiveis':[0,1,3,5,7]},
    'Mustang':            {'vel':-0.05,'stamina':+20,'preco':0.8,'emoji':'🌵','desc':'Rústico e resistente.','cores_possiveis':[0,1,3,5,7]},
    'Appaloosa':          {'vel':-0.10,'stamina':+15,'preco':0.9,'emoji':'🎨','desc':'Pelagem única. Alta resistência.','cores_possiveis':[2,4,6,0]},
    'Mestiço':            {'vel': 0.00,'stamina':  0,'preco':0.7,'emoji':'🐴','desc':'Equilibrado e acessível.','cores_possiveis':list(range(8))},
}
RACAS_LISTA = list(RACAS.keys())

CORES = [
    [0.55,0.28,0.10,1],[0.12,0.10,0.09,1],[0.78,0.62,0.40,1],[0.38,0.22,0.10,1],
    [0.80,0.80,0.78,1],[0.30,0.18,0.08,1],[0.65,0.45,0.22,1],[0.20,0.12,0.06,1],
]
CORES_NOMES = ['Chestnut','Preto','Palomino','Baio','Cinza','Marrom Escuro','Dourado','Mogno']
CORES_CRINA = [
    [0.30,0.14,0.04,1],[0.08,0.06,0.05,1],[0.85,0.78,0.50,1],[0.10,0.06,0.02,1],
    [0.50,0.50,0.48,1],[0.10,0.06,0.02,1],[0.20,0.13,0.04,1],[0.10,0.06,0.02,1],
]

# ── Preços base dos cavalos (10x) ──────────────────────────────────────────────
PRECO_CAVALOS  = [1200,1500,1800,2500,1300,1750,1600,1900,2000,2200,1400,1700,2100,1600,1850]
VEL_BASE       = [2.0,2.5,2.7,2.8,2.2,2.4,2.1,2.6,2.9,2.3,2.15,2.45,2.75,2.35,2.55]
STAMINA_BASE   = [ 80, 70, 75, 90, 85, 65, 80, 70, 60, 75,  80,  70,  65,  85,  75]
SAUDE_BASE     = [100]*15
MEDALHAS       = ['🥇','🥈','🥉','🏅','']

# ── Campeonato base ────────────────────────────────────────────────────────────
CAMP_N_CORRIDAS     = 12
CAMP_PONTOS         = {1:10,2:7,3:5,4:3,5:2,6:1}
CAMP_PREMIO_CORRIDA = {1:500,2:250,3:100}
CAMP_PREMIO_FINAL   = {1:5000,2:2500,3:1000}
CAMP_NOME_NPC       = ['Rancho Aurora','Haras Beltrano','Estábulo Norte',
                        'Haras Vitória','Rancho Estrela','Estábulo Sul']

# ── 3 Tipos de Competição ──────────────────────────────────────────────────────
COMPETICOES = {
    'regional': {
        'nome':          'Regional',
        'emoji':         '🏟',
        'cor':           (0.20,0.50,0.90,1),
        'n_corridas':    12,
        'estrela_min':   1,
        'min_cavalos':   1,
        'taxa':          500,
        'npc_nomes':     ['Rancho Aurora','Haras Beltrano','Estabulo Norte',
                          'Haras Vitoria','Rancho Estrela'],
        'premio_corrida':{1:800,   2:400,   3:150},
        'premio_final':  {1:8_000, 2:4_000, 3:1_500},
        'desc':          'Aberto a todos. 12 corridas. Taxa R$500.',
    },
    'nacional': {
        'nome':          'Nacional',
        'emoji':         'BR',
        'cor':           (0.10,0.75,0.35,1),
        'n_corridas':    10,
        'estrela_min':   4,
        'min_cavalos':   2,
        'taxa':          3_000,
        'npc_nomes':     ['Elite Aurora','Haras Nacional','Campeoes do Sul',
                          'Estabulo Elite','Top Horse BR'],
        'premio_corrida':{1:5_000,  2:2_500,  3:1_000},
        'premio_final':  {1:50_000, 2:25_000, 3:10_000},
        'desc':          'Cavalos 4+ estrelas. 2 cavalos revezam. 10 corridas. Taxa R$3.000.',
    },
    'internacional': {
        'nome':          'Internacional',
        'emoji':         'INTL',
        'cor':           (0.90,0.65,0.05,1),
        'n_corridas':    7,
        'estrela_min':   5,
        'min_cavalos':   5,
        'taxa':          10_000,
        'npc_nomes':     ['Dubai Champion','Paris Elite','Kentucky Star',
                          'Tokyo Thunder','London Pride'],
        'premio_corrida':{1:12_000,  2:6_000,   3:2_500},
        'premio_final':  {1:100_000, 2:50_000,  3:20_000},
        'desc':          '5 cavalos 5 estrelas revezam. 7 corridas. Taxa R$10.000.',
    },
}

# ── Haras ─────────────────────────────────────────────────────────────────────
HARAS_BAIAS_GRATIS = 2
HARAS_NIVEL_BAIAS  = {0:2, 1:5, 2:10, 3:20}

HARAS_TIPOS = {
    'pequeno': {'nome':'Haras Pequeno','nivel':1,'baias':5, 'preco':50_000,
                'desc':'Acomoda ate 5 cavalos. Ideal para iniciantes.'},
    'medio':   {'nome':'Haras Medio',  'nivel':2,'baias':10,'preco':100_000,
                'desc':'Acomoda ate 10 cavalos. Requer Haras Pequeno.'},
    'grande':  {'nome':'Haras Grande', 'nivel':3,'baias':20,'preco':250_000,
                'desc':'Acomoda ate 20 cavalos. O maior do pais!'},
}

# ── Custo de manutenção semanal ────────────────────────────────────────────────
CUSTO_MANUTENCAO_BASE = 200

# ── Patrocinadores ─────────────────────────────────────────────────────────────
MAX_PATROCINADORES_TEMPORADA = 1

PATROCINADORES_DISPONIVEIS = [
    {'nome':'Haras Real',   'emoji':'👑','condicao_pos':3,'condicao_semanas':3,'pagamento':500, 'duracao': 8,'desc':'Top 3 por 3 semanas - R$500/sem'},
    {'nome':'Racao Campeao','emoji':'🌾','condicao_pos':5,'condicao_semanas':2,'pagamento':300, 'duracao': 6,'desc':'Top 5 por 2 semanas - R$300/sem'},
    {'nome':'VetPlus',      'emoji':'💊','condicao_pos':1,'condicao_semanas':1,'pagamento':1000,'duracao': 5,'desc':'Vencer 1 corrida - R$1.000/sem'},
    {'nome':'Ferradura Ouro','emoji':'🔩','condicao_pos':3,'condicao_semanas':5,'pagamento':800, 'duracao':12,'desc':'Top 3 por 5 semanas - R$800/sem'},
    {'nome':'BetRun',       'emoji':'🎰','condicao_pos':2,'condicao_semanas':2,'pagamento':600, 'duracao': 7,'desc':'Top 2 por 2 semanas - R$600/sem'},
]

# ── Banco ──────────────────────────────────────────────────────────────────────
OPCOES_EMPRESTIMO = [
    {'valor':  2_000, 'parcela':  240, 'semanas': 10, 'juros_pct': 20},
    {'valor':  5_000, 'parcela':  580, 'semanas': 10, 'juros_pct': 16},
    {'valor': 10_000, 'parcela': 1_150,'semanas': 10, 'juros_pct': 15},
]
EMPRESTIMO_MAX_VALOR  = 10_000
EMPRESTIMO_MAX_ATIVOS = 1

# ── Eventos ────────────────────────────────────────────────────────────────────
EVENTOS_SEMANAIS = [
    {"texto":"🌧 Chuva forte! Pista pesada.","tipo":"vel_global","valor":-0.4},
    {"texto":"☀ Dia perfeito! Pista rapida.","tipo":"vel_global","valor":0.3},
    {"texto":"🎪 Festival! Premio dobrado.","tipo":"premio","valor":2.0},
    {"texto":"🦠 Epidemia! Cavalos perdem energia.","tipo":"energia","valor":-20},
    {"texto":"Tratador especial no haras!","tipo":"energia","valor":20},
    {"texto":"📈 Mercado aquecido!","tipo":"preco","valor":1.2},
    {"texto":"🤝 Evento especial! +R$500.","tipo":"dinheiro","valor":500},
    {"texto":"💨 Semana tranquila.","tipo":"nenhum","valor":0},
    {"texto":"⚡ Pista eletrica! Corrida imprevisivel.","tipo":"aleatorio","valor":1.8},
    {"texto":"🌬 Vento cruzado!","tipo":"aleatorio","valor":1.4},
]

# ── Paleta UI ──────────────────────────────────────────────────────────────────
UI_BG       = (0.04,0.04,0.08,1)
UI_CARD     = (0.09,0.09,0.16,1)
UI_CARD2    = (0.13,0.13,0.21,1)
UI_CARD3    = (0.07,0.11,0.19,1)
UI_GOLD     = (1.00,0.84,0.00,1)
UI_GOLD_DIM = (0.60,0.50,0.00,1)
UI_GOLD_BG  = (0.18,0.14,0.02,1)
UI_GREEN    = (0.15,0.78,0.42,1)
UI_GREEN_BG = (0.04,0.16,0.08,1)
UI_RED      = (0.90,0.25,0.25,1)
UI_RED_BG   = (0.18,0.05,0.05,1)
UI_BLUE     = (0.30,0.60,1.00,1)
UI_BLUE_BG  = (0.05,0.10,0.22,1)
UI_PURPLE   = (0.70,0.35,0.95,1)
UI_ORANGE   = (1.00,0.55,0.10,1)
UI_TEXT     = (0.96,0.96,0.96,1)
UI_DIM      = (0.50,0.50,0.60,1)

# ── Cavalos Lendários ──────────────────────────────────────────────────────────
CAVALOS_LENDARIOS = [
    {'nome':'Trovao Celestial','raca':'Turcomeno','vel':4.85,'stamina':88,
     'descricao':'Nascido de uma tempestade. Jamais foi derrotado.',
     'raridade':'LENDARIO','cor_idx':1,'crina_idx':1,'preco':750_000},
    {'nome':'Aurora Dourada','raca':'Puro Sangue Inglês','vel':4.92,'stamina':72,
     'descricao':'Pelo dourado que brilha como o sol nascente.',
     'raridade':'LENDARIO','cor_idx':6,'crina_idx':2,'preco':850_000},
    {'nome':'Sombra da Meia-Noite','raca':'Mestico','vel':4.78,'stamina':95,
     'descricao':'Invisivel na noite. Resistencia sobre-humana.',
     'raridade':'LENDARIO','cor_idx':7,'crina_idx':1,'preco':900_000},
    {'nome':'Vento Imortal','raca':'Arabe','vel':4.95,'stamina':80,
     'descricao':'Dizem que corre mais rapido que o vento.',
     'raridade':'LENDARIO','cor_idx':4,'crina_idx':4,'preco':950_000},
    {'nome':'Rex dos Pampas','raca':'Mustang','vel':4.70,'stamina':100,
     'descricao':'O mais resistente que ja pisou numa pista.',
     'raridade':'LENDARIO','cor_idx':3,'crina_idx':3,'preco':1_000_000},
    {'nome':'Cometa de Fogo','raca':'Quarto de Milha','vel':4.88,'stamina':65,
     'descricao':'Explosao pura nos primeiros metros. Inigualavel.',
     'raridade':'LENDARIO','cor_idx':0,'crina_idx':0,'preco':1_100_000},
]

# ── Leilão ─────────────────────────────────────────────────────────────────────
LEILAO_INTERVALO_SEMANAS = 5
LEILAO_DURACAO_SEMANAS   = 1
LEILAO_N_LOTES           = 3
LEILAO_ESTRELA_MIN       = 4
LEILAO_LANCE_INICIAL_PCT = 0.60
LEILAO_INCREMENTO_PCT    = 0.12
LEILAO_MAX_LANCES        = 5
PRECO_BAIA               = 1000

# ── Sistema de Estrelas ────────────────────────────────────────────────────────
ESTRELAS_VEL = [
    (1, 0.0, 1.0),(2, 1.1, 2.0),(3, 2.1, 3.0),(4, 3.1, 4.0),(5, 4.1, 5.0),
]

# ── Preços por estrela (10x) ───────────────────────────────────────────────────
PRECO_MAX_ESTRELA  = {1: 10_000, 2: 20_000, 3: 30_000, 4: 40_000, 5: 50_000}
PRECO_MIN_ESTRELA  = {1:    500, 2:  2_000, 3:  5_000, 4: 10_000, 5: 20_000}
TETO_PRECO_CAVALOS = {'1':10_000,'2':20_000,'3':30_000,'4':40_000,'5':50_000}
PRECO_MAX_LENDARIO = 500_000   # lendários não têm teto normal

# Valorização por vitória (incremental sobre o preco atual)
GANHO_POR_VITORIA  = {1: 50, 2: 150, 3: 300, 4: 600, 5: 1_000}
# Percentual de revenda (40% do preco — flipar cavalos não deve ser lucrativo)
PCT_REVENDA        = 0.40

ESTRELAS_EMOJI     = {1:'1*', 2:'2*', 3:'3*', 4:'4*', 5:'5*'}
VEL_MAX_GLOBAL     = 5.0

PREMIO_CORRIDA_ESTRELA = {
    1: {1:   500, 2:  250, 3:  100},
    2: {1: 1_000, 2:  500, 3:  200},
    3: {1: 2_000, 2:1_000, 3:  400},
    4: {1: 5_000, 2:2_500, 3:1_000},
    5: {1:10_000, 2:5_000, 3:2_000},
}

# ── Cruzamento / Veterinário ───────────────────────────────────────────────────
CUSTO_CONSULTA_VETERINARIA = 500
CUSTO_CRUZAMENTO           = 800
CUSTO_TOTAL_CRUZAMENTO     = CUSTO_CONSULTA_VETERINARIA + CUSTO_CRUZAMENTO

# ── Reputação do Haras ─────────────────────────────────────────────────────────
REPUTACAO_NIVEL = {
    1: {'nome':'Iniciante',  'emoji':'⭐',         'min_pts':   0},
    2: {'nome':'Conhecido',  'emoji':'⭐⭐',       'min_pts':  50},
    3: {'nome':'Respeitado', 'emoji':'⭐⭐⭐',     'min_pts': 150},
    4: {'nome':'Famoso',     'emoji':'⭐⭐⭐⭐',   'min_pts': 350},
    5: {'nome':'Lendário',   'emoji':'⭐⭐⭐⭐⭐', 'min_pts': 700},
}

REPUTACAO_PONTOS = {
    'vitoria_corrida':     5,
    'podio_corrida':       2,
    'vitoria_campeonato': 30,
    'podio_campeonato':   15,
    'resposta_entrevista': 1,
    'entrevista_carisma':  3,
    'cavalo_lendario':    10,
    'semana_positiva':     1,
}

# ── AdMob ──────────────────────────────────────────────────────────────────────
ADMOB_RECOMPENSA_OURO  = 1_000
ADMOB_MAX_POR_SEMANA   = 3
ADMOB_APP_ID           = 'ca-app-pub-1629730681290593~2169149407'
ADMOB_REWARDED_ID      = 'ca-app-pub-1629730681290593/6324016838'

# ── Energia dos cavalos ───────────────────────────────────────────────────────
ENERGIA_GASTO_MIN      = 25   # gasto mínimo por corrida
ENERGIA_GASTO_MAX      = 45   # gasto máximo por corrida
ENERGIA_RECUPERA_SEMANA = 20  # recuperação por semana (sem item)

def gerar_id(): return str(uuid.uuid4())[:8].upper()
