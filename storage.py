import json, os
from kivy.app import App
from game_logic import Jogo, Cavalo, FUNCIONARIOS, criar_cavalo, Campeonato, calcular_preco_mercado
from config import CORES

def caminho_save():
    try: base=App.get_running_app().user_data_dir
    except: base=os.getcwd()
    return os.path.join(base,'savegame.json')

def _c2d(c):
    return {'id':c.id,'nome':c.nome,'cor':c.cor,'preco':c.preco,'vel_base':c.vel_base,
            'stamina':c.stamina,'saude':c.saude,'energia':c.energia,'vitorias':c.vitorias,
            'raca':c.raca,'semana_nasc':c.semana_nasc,'idade_max':c.idade_max,
            'streak_top':c.streak_top,'historico_vitorias':c.historico_vitorias,
            'sexo':getattr(c,'sexo',None),
            'gestacao_semana':getattr(c,'gestacao_semana',None),
            'filho_pendente':getattr(c,'filho_pendente',None),
            'lendario':getattr(c,'lendario',False)}

def _d2c(d):
    import random
    c=Cavalo(d.get('nome','Cavalo'),d.get('cor',CORES[3]),d.get('preco',150),
             d.get('vel_base',2.0),d.get('stamina',80),d.get('saude',100),
             raca=d.get('raca','Mestiço'),semana_nasc=d.get('semana_nasc',-40))
    c.id=d.get('id',c.id); c.energia=d.get('energia',100)
    c.vitorias=d.get('vitorias',0); c.idade_max=d.get('idade_max',85)
    c.streak_top=d.get('streak_top',0)
    c.historico_vitorias=[(tuple(x) if isinstance(x,list) else x) for x in d.get('historico_vitorias',[])]
    c.sexo = d.get('sexo') or random.choice(['M','F'])
    c.gestacao_semana = d.get('gestacao_semana', None)
    c.filho_pendente  = d.get('filho_pendente', None)
    c.lendario        = d.get('lendario', False)
    return c

def salvar_jogo(jogo):
    camp_data=None
    if jogo.campeonato:
        cp=jogo.campeonato
        camp_data={'tipo':cp.tipo,'semana_inicio':cp.semana_inicio,
                   'corrida_atual':cp.corrida_atual,'encerrado':cp.encerrado,
                   'pontos':cp.pontos,'npc_nomes':cp.npc_nomes,
                   'cavalos_ids':cp.cavalos_ids}
    data={'dinheiro':jogo.dinheiro,'semana':jogo.semana,'baias':jogo.baias,'trofeus':jogo.trofeus,
          'leilao_ativo':jogo.leilao_ativo,'leilao_semana':jogo.leilao_semana,
          'semana_ultimo_leilao':jogo.semana_ultimo_leilao,
          'temporada':jogo.temporada,'haras_nivel':jogo.haras_nivel,
          'patrocinios_esta_temporada':jogo.patrocinios_esta_temporada,
          'cavalos_jogador':[_c2d(c) for c in jogo.cavalos_jogador],
          'cavalos_mercado':[_c2d(c) for c in jogo.cavalos_mercado],
          'funcionarios':[f.nome for f in jogo.funcionarios],
          'historico':jogo.historico,'patrocinios_ativos':jogo.patrocinios_ativos,
          'emprestimos_ativos':jogo.emprestimos_ativos,'campeonato':camp_data,
          'reputacao_pts':jogo.reputacao_pts,'admob_vistos_semana':jogo.admob_vistos_semana}
    path=caminho_save()
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.',exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(f'[SAVE] {path}')

def carregar_jogo():
    path=caminho_save()
    if not os.path.exists(path): return None
    with open(path,'r',encoding='utf-8') as f: data=json.load(f)
    jogo=Jogo()
    jogo.dinheiro=data.get('dinheiro',1000); jogo.semana=data.get('semana',1)
    jogo.baias=data.get('baias',2); jogo.temporada=data.get('temporada',1)
    jogo.haras_nivel=data.get('haras_nivel',0)
    jogo.patrocinios_esta_temporada=data.get('patrocinios_esta_temporada',0)
    jogo.cavalos_jogador=[_d2c(d) for d in data.get('cavalos_jogador',[])]
    jogo.cavalos_mercado=[_d2c(d) for d in data.get('cavalos_mercado',[])]
    if not jogo.cavalos_mercado: jogo.cavalos_mercado=jogo._gerar_mercado()
    jogo.funcionarios=[f for f in FUNCIONARIOS if f.nome in data.get('funcionarios',[])]
    jogo.historico=data.get('historico',[])
    jogo.patrocinios_ativos=data.get('patrocinios_ativos',[])
    jogo.trofeus=data.get('trofeus',[])
    jogo.leilao_ativo=data.get('leilao_ativo',False)
    jogo.leilao_semana=data.get('leilao_semana',0)
    jogo.semana_ultimo_leilao=data.get('semana_ultimo_leilao',0)
    # Lotes não são serializados - leilão reinicia se estava ativo
    jogo.leilao_lotes=[]
    if jogo.leilao_ativo: jogo.leilao_ativo=False  # reinicia na próxima semana
    jogo.emprestimos_ativos=data.get('emprestimos_ativos',[])
    jogo.reputacao_pts=data.get('reputacao_pts',0)
    jogo.admob_vistos_semana=data.get('admob_vistos_semana',0)
    cd=data.get('campeonato')
    if cd:
        tipo=cd.get('tipo','regional')
        cp=Campeonato(cd['semana_inicio'], tipo)
        cp.corrida_atual=cd['corrida_atual']; cp.encerrado=cd['encerrado']
        cp.pontos=cd['pontos']; cp.npc_nomes=cd['npc_nomes']
        cp.cavalos_ids=cd.get('cavalos_ids',[])
        jogo.campeonato=cp
    print('[LOAD] OK'); return jogo
