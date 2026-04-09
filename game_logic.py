import random
from config import (NOMES, CORES, CORES_CRINA, RACAS, RACAS_LISTA, PRECO_CAVALOS,
                    VEL_BASE, STAMINA_BASE, MEDALHAS, EVENTOS_SEMANAIS,
                    PATROCINADORES_DISPONIVEIS, OPCOES_EMPRESTIMO,
                    CAMP_N_CORRIDAS, CAMP_PONTOS, CAMP_PREMIO_CORRIDA,
                    CAMP_PREMIO_FINAL, CAMP_NOME_NPC, gerar_id, PRECO_BAIA,
                    ESTRELAS_VEL, PRECO_MAX_ESTRELA, PRECO_MIN_ESTRELA,
                    VEL_MAX_GLOBAL, COMPETICOES,
                    HARAS_TIPOS, HARAS_NIVEL_BAIAS, HARAS_BAIAS_GRATIS,
                    CUSTO_MANUTENCAO_BASE, MAX_PATROCINADORES_TEMPORADA,
                    CAVALOS_LENDARIOS, LEILAO_INTERVALO_SEMANAS,
                    LEILAO_DURACAO_SEMANAS, LEILAO_N_LOTES, LEILAO_ESTRELA_MIN,
                    LEILAO_LANCE_INICIAL_PCT, LEILAO_INCREMENTO_PCT,
                    LEILAO_MAX_LANCES,
                    ENERGIA_GASTO_MIN, ENERGIA_GASTO_MAX, ENERGIA_RECUPERA_SEMANA,
                    REPUTACAO_NIVEL, REPUTACAO_PONTOS, PRECO_MAX_LENDARIO,
                    GANHO_POR_VITORIA, PCT_REVENDA,
                    ADMOB_MAX_POR_SEMANA, ADMOB_RECOMPENSA_OURO)


# ══════════════════════════════════════════════════════════════════════════════
#  CAVALO
# ══════════════════════════════════════════════════════════════════════════════
class Cavalo:
    def __init__(self, nome, cor, preco, vel_base, stamina=80, saude=100,
                 pai=None, mae=None, historico_vitorias=None,
                 raca='Mestiço', semana_nasc=0):
        self.id          = gerar_id()
        self.lendario    = False
        self.nome        = nome
        self.cor         = cor
        self.preco       = preco
        self.vel_base    = vel_base
        self.stamina     = max(0, min(100, stamina))
        self.saude       = max(0, min(100, saude))
        self.energia     = 100
        self.vitorias    = 0
        self.raca        = raca
        self.semana_nasc = semana_nasc
        self.idade_max   = random.randint(80, 90)
        self.pai         = pai
        self.mae         = mae
        self.filhos      = []
        self.historico_vitorias = historico_vitorias or []
        self.streak_top  = 0
        self.sexo        = None   # 'M' ou 'F' — atribuído após criação
        self.gestacao_semana = None   # semana em que ficou prenha (None = não gestante)
        self.filho_pendente  = None   # dados do potro a nascer

    def idade(self, s):        return max(0, s - self.semana_nasc)
    def e_potro(self, s):      return self.idade(s) < 10
    def em_gestacao(self):     return self.gestacao_semana is not None
    def semanas_gestacao(self, s): return max(0, s - self.gestacao_semana) if self.em_gestacao() else 0
    def pode_correr(self, s):
        if self.em_gestacao(): return False   # gestante não corre
        return 10 <= self.idade(s) < self.idade_max
    def esta_morto(self, s):   return self.idade(s) >= self.idade_max

    def status_idade(self, s):
        if self.em_gestacao():
            sg = self.semanas_gestacao(s)
            restam = max(0, 8 - sg)
            return f'Prenha ({sg}/8 sem, nasce em {restam})'
        a = self.idade(s)
        sx = '♂' if self.sexo == 'M' else ('♀' if self.sexo == 'F' else '')
        if a < 10:  return f'{sx} Potro ({a} sem)'
        if a < 26:  return f'{sx} Jovem ({a} sem)'
        if a < 61:  return f'{sx} Adulto ({a} sem)'
        if a < 76:  return f'{sx} Veterano ({a} sem)'
        return f'{sx} Idoso ({a} sem)'

    def _fator_idade(self, s):
        a = self.idade(s)
        if a < 10:  return 0.0
        if a <= 25: return 0.75 + 0.015*(a-10)
        if a <= 60: return 1.00
        if a <= 75: return 1.00 - 0.008*(a-60)
        return max(0.70, 1.00 - 0.012*(a-60))

    def vel_efetiva(self, bt=0.0, bta=0.0, bn=0.0, semana_atual=1):
        fe  = (self.energia/100.0)*(1+bta)
        fs  = self.saude/100.0
        fst = (0.6+0.4*(self.stamina/100.0))*(1+bn)
        fi  = self._fator_idade(semana_atual)
        return min(VEL_MAX_GLOBAL, self.vel_base*fe*fs*fst*fi + bt)

    def registrar_vitoria(self, semana, pos):
        self.historico_vitorias.append((semana, pos))
        if pos == 1: self.vitorias += 1

    def mostrar_historico(self):
        if not self.historico_vitorias: return 'Sem corridas.'
        return '\n'.join([f'Sem {s}: {p}º' for s,p in self.historico_vitorias[-5:]])

    def genealogia(self, nivel=0):
        pad = '  '*nivel
        rd  = RACAS.get(self.raca, {})
        txt = f"{pad}{rd.get('emoji','🐴')} {self.nome}  ({self.raca})"
        if self.pai: txt += f"\n{pad}  ♂ {self.pai.nome} ({self.pai.raca})"
        if self.mae: txt += f"\n{pad}  ♀ {self.mae.nome} ({self.mae.raca})"
        for filho in self.filhos: txt += '\n' + filho.genealogia(nivel+1)
        return txt


# ══════════════════════════════════════════════════════════════════════════════
#  ITENS
# ══════════════════════════════════════════════════════════════════════════════
class Item:
    def __init__(self, nome, preco, efeito, emoji='', descricao=''):
        self.nome=nome; self.preco=preco; self.efeito=efeito
        self.emoji=emoji; self.descricao=descricao

ITENS_COMIDA = [
    Item('Feno Básico',      75,'energia+15','🌾','+15 energia'),
    Item('Feno Premium',    150,'energia+30','🌿','+30 energia'),
    Item('Cenoura',          50,'energia+10','🥕','+10 energia'),
    Item('Aveia Energética', 225,'energia+45','🌾','+45 energia'),
    Item('Maçã do Campeão',  300,'energia+60;stamina+5','🍎','+60 energia +5 stamina'),
]
ITENS_REMEDIO = [
    Item('Curativo Básico',  125,'saude+20',         '🩹','+20 saúde'),
    Item('Antibiótico',      250,'saude+40',         '💊','+40 saúde'),
    Item('Soro Vitamínico',  350,'saude+60;stamina+8','💉','+60 saúde +8 stamina'),
    Item('Remédio Completo', 450,'saude=100',        '🧴','Saúde 100%'),
    Item('Elixir do Campeão',750,'saude=100;stamina+15;energia+50','✨','Saúde 100% +15st +50e'),
]
ITENS_EQUIPAMENTO = [
    Item('Escova de Pelos',   100,'energia+5',    '🪮','+5 energia'),
    Item('Ferradura Básica', 1000,'vel_base+0.15','🔧','+0.15 vel'),
    Item('Ferradura Pro',    1500,'vel_base+0.30','🔩','+0.30 vel'),
    Item('Sela de Corrida',  2000,'vel_base+0.50','🏇','+0.50 vel'),
    Item('Canga de Treino',   400,'stamina+20',   '💪','+20 stamina'),
    Item('Protetor de Patas', 200,'saude+10',     '🦶','+10 saúde'),
]
ITENS_MERCADO = ITENS_COMIDA+ITENS_REMEDIO+ITENS_EQUIPAMENTO


# ══════════════════════════════════════════════════════════════════════════════
#  FUNCIONÁRIOS
# ══════════════════════════════════════════════════════════════════════════════
class Funcionario:
    def __init__(self, nome, salario, efeito, emoji=''):
        self.nome=nome; self.salario=salario; self.efeito=efeito; self.emoji=emoji

FUNCIONARIOS = [
    Funcionario('Veterinário',  200,'Mantém saúde dos cavalos em 100%','👨‍⚕️'),
    Funcionario('Tratador',     150,'Energia dos cavalos +15% nas corridas','🧑‍🌾'),
    Funcionario('Treinador',    250,'Velocidade base dos seus cavalos +0.5','🏋️'),
    Funcionario('Nutricionista',180,'Stamina dos cavalos +20% nas corridas','🥗'),
]


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER criar_cavalo
# ══════════════════════════════════════════════════════════════════════════════
def criar_cavalo(nome, raca, semana_nasc=0, vel_base=None, stamina=None,
                 saude=100, preco=None, cor=None, sexo=None):
    rd  = RACAS.get(raca, RACAS['Mestiço'])
    v   = round(min(VEL_MAX_GLOBAL, max(1.0, (vel_base or random.uniform(1.9,2.8)) + rd['vel'])), 2)
    st  = max(10, min(100, (stamina or random.randint(60,90)) + rd['stamina']))
    pr  = int((preco or random.choice(PRECO_CAVALOS)) * rd['preco'])
    if cor is None: cor = CORES[random.choice(rd['cores_possiveis'])]
    cav = Cavalo(nome, cor, pr, v, st, saude, raca=raca, semana_nasc=semana_nasc)
    cav.sexo = sexo if sexo in ('M','F') else random.choice(['M','F'])
    return cav





def criar_cavalo_lendario(defn, semana_nasc=0):
    """Cria um cavalo lendário a partir de uma definição em CAVALOS_LENDARIOS."""
    rd   = RACAS.get(defn['raca'], RACAS['Mestiço'])
    v    = round(min(5.0, defn['vel'] + rd['vel']), 2)
    st   = max(10, min(100, defn['stamina'] + rd['stamina']))
    cor  = CORES[defn['cor_idx']]
    # Preço = teto da 5ª estrela × 1.8 (lendários valem mais)
    from config import PRECO_MAX_ESTRELA
    pr   = int(PRECO_MAX_ESTRELA[5] * 1.8)
    cav  = Cavalo(defn['nome'], cor, pr, v, st, 100,
                  raca=defn['raca'], semana_nasc=semana_nasc)
    cav.lendario = True
    cav.sexo = random.choice(['M','F'])
    return cav


# ══════════════════════════════════════════════════════════════════════════════
#  SISTEMA DE ESTRELAS
# ══════════════════════════════════════════════════════════════════════════════
def estrelas(vel: float) -> int:
    """Retorna a categoria (1-5 estrelas) de um cavalo pela sua vel_base."""
    for e, vmin, vmax in ESTRELAS_VEL:
        if vmin <= vel <= vmax:
            return e
    return 5  # acima de 5.0 → 5 estrelas


def calcular_preco_mercado(cavalo) -> int:
    """
    Calcula o preço justo do cavalo levando em conta:
    velocidade (posição dentro do tier), vitórias, stamina e saúde.
    O preço é limitado ao máximo da estrela correspondente e nunca fica
    abaixo do mínimo definido por PRECO_MIN_ESTRELA.
    """
    e    = estrelas(cavalo.vel_base)
    pmax = PRECO_MAX_ESTRELA[e]
    pmin = PRECO_MIN_ESTRELA[e]

    tier_info = next((t for t in ESTRELAS_VEL if t[0] == e), (e, 0.0, 5.0))
    vmin, vmax = tier_info[1], tier_info[2]
    vel_frac = (cavalo.vel_base - vmin) / max(0.01, vmax - vmin)

    base       = pmin + (pmax - pmin) * vel_frac
    # Vitórias sobem preço devagar: +1% por vitória, máximo +30%
    win_bonus  = min(1.30, 1 + cavalo.vitorias * 0.01)
    cond       = 0.85 + 0.08 * cavalo.stamina / 100.0 + 0.07 * cavalo.saude / 100.0
    preco      = int(base * win_bonus * cond)
    # Lendários usam teto especial
    if getattr(cavalo, 'lendario', False):
        return max(pmin, min(PRECO_MAX_LENDARIO, preco * 4))
    return min(pmax, max(pmin, preco))


def atualizar_preco_pos_corrida(cavalo, posicao: int):
    """Valoriza/desvaloriza o cavalo incrementalmente após cada corrida.
    Nunca recalcula do zero — cresce devagar sobre o preco atual.
    """
    e = estrelas(cavalo.vel_base)
    ganho_base = GANHO_POR_VITORIA.get(e, 300)
    if posicao == 1:
        delta = ganho_base           # +ganho completo por vitória
    elif posicao == 2:
        delta = ganho_base // 3      # +1/3 por 2° lugar
    elif posicao == 3:
        delta = ganho_base // 6      # +1/6 por 3° lugar
    elif posicao >= 5:
        delta = -(ganho_base // 4)   # perde um pouco nos últimos
    else:
        delta = 0
    novo = cavalo.preco + delta
    if getattr(cavalo, 'lendario', False):
        cavalo.preco = max(PRECO_MIN_ESTRELA[e], min(PRECO_MAX_LENDARIO, novo))
    else:
        cavalo.preco = max(PRECO_MIN_ESTRELA[e], min(PRECO_MAX_ESTRELA[e], novo))


# ══════════════════════════════════════════════════════════════════════════════
#  CAMPEONATO
# ══════════════════════════════════════════════════════════════════════════════
class Campeonato:
    """Gerencia uma temporada de corridas. Suporta 3 tipos: regional, nacional, internacional."""

    def __init__(self, semana_inicio, tipo='regional'):
        cfg = COMPETICOES.get(tipo, COMPETICOES['regional'])
        self.tipo            = tipo
        self.cfg             = cfg
        self.semana_inicio   = semana_inicio
        self.n_corridas      = cfg['n_corridas']
        self.estrela_min     = cfg['estrela_min']
        self.taxa            = cfg['taxa']
        self.premio_corrida  = cfg['premio_corrida']
        self.premio_final    = cfg['premio_final']
        self.corrida_atual   = 0
        self.encerrado       = False
        self.pontos          = {}
        self.npc_nomes       = [n + f' #{i+1}' for i, n in enumerate(cfg['npc_nomes'])]
        self.cavalos_ids     = []   # IDs dos cavalos escalonados (rotacao nacional/internacional)
        for n in self.npc_nomes:
            self.pontos[n] = 0

    def cavalo_da_vez(self, cavalos_jogador):
        """Retorna o cavalo que deve correr na rodada atual (rotacao)."""
        if not self.cavalos_ids:
            aptos = [c for c in cavalos_jogador if hasattr(c, 'vel_base')]
            return aptos[0] if aptos else None
        idx = self.corrida_atual % len(self.cavalos_ids)
        cid = self.cavalos_ids[idx]
        return next((c for c in cavalos_jogador if c.id == cid), None)

    def lineup_nomes(self, cavalos_jogador):
        """Lista de nomes dos cavalos em escala para exibição."""
        if not self.cavalos_ids:
            return []
        result = []
        for cid in self.cavalos_ids:
            c = next((h for h in cavalos_jogador if h.id == cid), None)
            result.append(c.nome if c else '???')
        return result

    def registrar_corrida(self, classificados_nomes):
        """classificados_nomes: lista [1°, 2°, …]. Retorna {nome: pts ganhos}."""
        ganhos = {}
        for pos, nome in enumerate(classificados_nomes, 1):
            pts = CAMP_PONTOS.get(pos, 0)
            self.pontos[nome] = self.pontos.get(nome, 0) + pts
            ganhos[nome]      = pts
        self.corrida_atual += 1
        if self.corrida_atual >= self.n_corridas:
            self.encerrado = True
        return ganhos

    def classificacao(self):
        return sorted(self.pontos.items(), key=lambda x: x[1], reverse=True)

    def premio_final_jogador(self, nome_jogador):
        """Retorna (posição, R$) do jogador na classificação final."""
        cls = [n for n, _ in self.classificacao()]
        if nome_jogador not in cls:
            return 0, 0
        pos = cls.index(nome_jogador) + 1
        return pos, self.premio_final.get(pos, 0)


# ══════════════════════════════════════════════════════════════════════════════
#  JOGO
# ══════════════════════════════════════════════════════════════════════════════
class Jogo:
    def __init__(self):
        self.dinheiro          = 1000
        self.semana            = 1
        self.temporada         = 1           # contador de temporadas
        self.haras_nivel       = 0           # 0=inicio(2 baias), 1=peq, 2=med, 3=grande
        self.baias             = HARAS_BAIAS_GRATIS   # começa com 2 baias grátis
        self.patrocinios_esta_temporada = 0  # limite: 1 por temporada
        self.cavalos_mercado   = self._gerar_mercado()
        self.cavalos_jogador   = []
        self.historico         = []
        self.cavalo_apostado   = None
        self.valor_aposta      = 0
        self.funcionarios      = []
        self.evento_atual      = None
        self.fator_vel_evento  = 0.0
        self.fator_premio      = 1.0
        self.fator_aleatorio   = 1.0
        self.patrocinios_ativos= []
        self.emprestimos_ativos= []
        self.ultimo_pos_jogador= 0
        self.campeonato        = None   # None = sem campeonato ativo
        self.trofeus           = []     # lista de troféus conquistados
        self.leilao_ativo      = False  # True quando há leilão em andamento
        self.leilao_semana     = 0      # semana em que o leilão começou
        self.leilao_lotes      = []     # lista de lotes: {cavalo, lance_atual, n_lances, vendido}
        self.semana_ultimo_leilao = 0   # para controlar frequência
        self.admob_vistos_semana = 0    # ads vistos na semana atual
        self.reputacao_pts     = 0      # pontos de reputação acumulados

    # ── Baias ──────────────────────────────────────────────────────────────────
    @property
    def baias_livres(self):
        return max(0, self.baias - len(self.cavalos_jogador))

    def comprar_baia(self):
        if self.dinheiro < PRECO_BAIA: return False
        self.dinheiro -= PRECO_BAIA
        self.baias    += 1
        return True

    def comprar_haras(self, tipo):
        """Compra/faz upgrade do haras. tipo: 'pequeno', 'medio', 'grande'."""
        cfg = HARAS_TIPOS.get(tipo)
        if not cfg:
            return False, 'Tipo invalido'
        if self.haras_nivel >= cfg['nivel']:
            return False, 'Ja possui haras desse nivel ou superior'
        if cfg['nivel'] > self.haras_nivel + 1:
            prev = [k for k,v in HARAS_TIPOS.items() if v['nivel']==self.haras_nivel+1]
            return False, f"Precisa comprar {prev[0] if prev else 'anterior'} antes"
        if self.dinheiro < cfg['preco']:
            return False, f"Precisa de R${cfg['preco']:,}"
        self.dinheiro   -= cfg['preco']
        self.haras_nivel = cfg['nivel']
        self.baias       = cfg['baias']
        return True, f"{cfg['nome']} adquirido! {cfg['baias']} baias desbloqueadas."

    def info_haras_atual(self):
        if self.haras_nivel == 0:
            return "Starter (2 baias gratis)"
        for k,v in HARAS_TIPOS.items():
            if v['nivel'] == self.haras_nivel:
                return v['nome']
        return "Desconhecido"

    def custo_manutencao_semanal(self):
        """Custo semanal de manutenção de todos os cavalos do jogador."""
        total = 0
        for c in self.cavalos_jogador:
            from config import ESTRELAS_VEL
            cat = estrelas(c.vel_base)
            total += CUSTO_MANUTENCAO_BASE * cat
        return total

    def cobrar_manutencao(self):
        custo = self.custo_manutencao_semanal()
        self.dinheiro -= custo   # pode ficar negativo
        return custo

    def pode_comprar_cavalo(self):
        return self.baias_livres > 0

    # ── Mercado ────────────────────────────────────────────────────────────────
    def _gerar_mercado(self):
        """Gera mercado inicial com mix de idades: potros, jovens e adultos."""
        cavalos = []
        # 3 potros (nasce agora, vai crescer)
        for _ in range(3):
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            nasc = self.semana - random.randint(0, 8)   # 0-8 semanas de vida
            c = criar_cavalo(nome, raca, semana_nasc=nasc)
            c.sexo = random.choice(['M','F'])
            cavalos.append(c)
        # 4 jovens/adultos prontos para correr
        for i in range(4):
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            nasc = self.semana - random.randint(15, 45)
            c = criar_cavalo(nome, raca, semana_nasc=nasc,
                             vel_base=VEL_BASE[i % len(VEL_BASE)],
                             stamina=STAMINA_BASE[i % len(STAMINA_BASE)])
            c.sexo = random.choice(['M','F'])
            cavalos.append(c)
        # 3 veteranos baratos
        for _ in range(3):
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            nasc = self.semana - random.randint(50, 65)
            c = criar_cavalo(nome, raca, semana_nasc=nasc)
            c.sexo = random.choice(['M','F'])
            cavalos.append(c)
        return cavalos

    def renovar_mercado(self):
        """
        Ciclo de vida do mercado:
        1. Remove cavalos mortos (idosos demais)
        2. Remove 1-2 aleatórios (foram 'vendidos para outros fazendeiros')
        3. Adiciona novos: mix de potros recém-nascidos e adultos
        4. Garante mínimo de 8 cavalos sempre
        """
        # 1. Remove mortos naturalmente
        vivos = [c for c in self.cavalos_mercado if not c.esta_morto(self.semana)]
        removidos_morte = len(self.cavalos_mercado) - len(vivos)
        self.cavalos_mercado = vivos

        # 2. Remove 1-2 por 'venda para outros' (simula demanda do mercado)
        n_rem = random.randint(1, 2)
        for _ in range(min(n_rem, len(self.cavalos_mercado))):
            self.cavalos_mercado.pop(random.randint(0, len(self.cavalos_mercado)-1))

        # 3. Adiciona novos a cada semana
        # 40% de chance de nascer um potro novo no mercado
        if random.random() < 0.40:
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            potro = criar_cavalo(nome, raca, semana_nasc=self.semana)
            potro.sexo = random.choice(['M','F'])
            self.cavalos_mercado.append(potro)

        # Sempre adiciona 1-2 cavalos adultos novos
        for _ in range(random.randint(1, 2)):
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            # Idade variada: jovem (15-30), adulto (30-55)
            faixa = random.choice(['jovem','adulto','adulto'])
            if faixa == 'jovem':
                nasc = self.semana - random.randint(10, 25)
            else:
                nasc = self.semana - random.randint(26, 55)
            c = criar_cavalo(nome, raca, semana_nasc=nasc)
            c.sexo = random.choice(['M','F'])
            self.cavalos_mercado.append(c)

        # 4. Garante mínimo de 8 cavalos
        while len(self.cavalos_mercado) < 8:
            raca = random.choice(RACAS_LISTA)
            nome = random.choice(NOMES)
            nasc = self.semana - random.randint(15, 50)
            c = criar_cavalo(nome, raca, semana_nasc=nasc)
            c.sexo = random.choice(['M','F'])
            self.cavalos_mercado.append(c)

    # ── Evento ─────────────────────────────────────────────────────────────────
    def sortear_evento(self):
        ev = random.choice(EVENTOS_SEMANAIS)
        self.evento_atual=ev; self.fator_vel_evento=0.0
        self.fator_premio=1.0; self.fator_aleatorio=1.0
        t,v = ev['tipo'],ev['valor']
        if   t=='vel_global':  self.fator_vel_evento=v
        elif t=='premio':      self.fator_premio=v
        elif t=='energia':     [setattr(c,'energia',max(0,min(100,c.energia+v))) for c in self.cavalos_jogador]
        elif t=='dinheiro':    self.dinheiro+=int(v)
        elif t=='aleatorio':   self.fator_aleatorio=v
        elif t=='preco':       [setattr(c,'preco',int(c.preco*v)) for c in self.cavalos_mercado]
        return ev

    # ── Item ───────────────────────────────────────────────────────────────────
    def aplicar_item(self, item, cavalo):
        for p in item.efeito.split(';'):
            p=p.strip()
            if   'energia+'  in p: cavalo.energia =min(100,cavalo.energia +int(p.split('+')[1]))
            elif 'energia='  in p: cavalo.energia =int(p.split('=')[1])
            elif 'saude+'    in p: cavalo.saude   =min(100,cavalo.saude   +int(p.split('+')[1]))
            elif 'saude='    in p: cavalo.saude   =int(p.split('=')[1])
            elif 'stamina+'  in p: cavalo.stamina =min(100,cavalo.stamina +int(p.split('+')[1]))
            elif 'vel_base+' in p: cavalo.vel_base=round(min(VEL_MAX_GLOBAL, cavalo.vel_base+float(p.split('+')[1])),2)

    # ── Funcionários ───────────────────────────────────────────────────────────
    def bonus_treinador(self): return 0.5  if any(f.nome=='Treinador'     for f in self.funcionarios) else 0.0
    def bonus_tratador(self):  return 0.15 if any(f.nome=='Tratador'      for f in self.funcionarios) else 0.0
    def bonus_nutri(self):     return 0.20 if any(f.nome=='Nutricionista' for f in self.funcionarios) else 0.0
    def aplicar_veterinario(self):
        if any(f.nome=='Veterinário' for f in self.funcionarios):
            for c in self.cavalos_jogador: c.saude=100
    def cobrar_funcionarios(self):
        c=sum(f.salario for f in self.funcionarios); self.dinheiro-=c; return c  # pode ficar negativo

    def resetar_admob_semana(self):
        self.admob_vistos_semana = 0

    def pode_ver_anuncio(self):
        """Retorna True se o jogador ainda pode ver anúncios esta semana."""
        vistos = getattr(self, 'admob_vistos_semana', 0)
        return vistos < ADMOB_MAX_POR_SEMANA

    def registrar_anuncio_visto(self):
        """Registra que o jogador assistiu um anúncio e dá a recompensa.
        Retorna (ok, mensagem, valor)."""
        if not self.pode_ver_anuncio():
            return False, f'Limite semanal atingido ({ADMOB_MAX_POR_SEMANA}/semana).', 0
        if not hasattr(self, 'admob_vistos_semana'):
            self.admob_vistos_semana = 0
        self.admob_vistos_semana += 1
        self.dinheiro += ADMOB_RECOMPENSA_OURO
        restantes = ADMOB_MAX_POR_SEMANA - self.admob_vistos_semana
        msg = f'+{ADMOB_RECOMPENSA_OURO} Ouro! ({restantes} anuncio(s) restante(s) esta semana)'
        return True, msg, ADMOB_RECOMPENSA_OURO

    def recuperar_energia_semanal(self):
        for cav in self.cavalos_jogador:
            cav.energia = min(100, cav.energia + ENERGIA_RECUPERA_SEMANA)

    def nivel_reputacao(self):
        """Retorna (nivel_int, dict_do_nivel) baseado nos pontos atuais."""
        nivel = 1
        for n, dados in sorted(REPUTACAO_NIVEL.items()):
            if self.reputacao_pts >= dados['min_pts']:
                nivel = n
        return nivel, REPUTACAO_NIVEL[nivel]

    def barra_reputacao(self):
        """Retorna (pct_atual, pts_no_nivel, pts_total_nivel) para barra de progresso."""
        nr, cr = self.nivel_reputacao()
        pts_inicio = cr['min_pts']
        proximo = REPUTACAO_NIVEL.get(nr + 1)
        if not proximo:
            return 1.0, self.reputacao_pts - pts_inicio, self.reputacao_pts - pts_inicio
        pts_total = proximo['min_pts'] - pts_inicio
        pts_feitos = self.reputacao_pts - pts_inicio
        pct = min(1.0, pts_feitos / max(1, pts_total))
        return pct, pts_feitos, pts_total

    def proxima_reputacao(self):
        """Retorna (True/False, dict_proximo, pts_faltando)."""
        nr, _ = self.nivel_reputacao()
        proximo = REPUTACAO_NIVEL.get(nr + 1)
        if not proximo:
            return False, None, 0
        faltando = proximo['min_pts'] - self.reputacao_pts
        return True, proximo, faltando

    def ganhar_reputacao(self, evento: str):
        """Adiciona pontos de reputação. Retorna (pts_ganhos, subiu_nivel)."""
        pts = REPUTACAO_PONTOS.get(evento, 0)
        if pts == 0:
            return 0, False
        nr_antes, _ = self.nivel_reputacao()
        self.reputacao_pts += pts
        nr_depois, _ = self.nivel_reputacao()
        return pts, nr_depois > nr_antes

    # ── Aposta ─────────────────────────────────────────────────────────────────
    def resolver_aposta(self, cls):
        if not self.cavalo_apostado or self.valor_aposta<=0: return 0
        nomes=[cw.cavalo.nome for cw in cls]
        pos=nomes.index(self.cavalo_apostado.nome)+1 if self.cavalo_apostado.nome in nomes else 99
        g=0
        if pos==1: g=int(self.valor_aposta*3.0*self.fator_premio)
        elif pos==2: g=int(self.valor_aposta*2.0*self.fator_premio)
        elif pos==3: g=int(self.valor_aposta*1.5*self.fator_premio)
        self.dinheiro+=g; self.cavalo_apostado=None; self.valor_aposta=0; return g

    # ── Patrocinadores ─────────────────────────────────────────────────────────
    def contratos_disponiveis(self):
        ativos={p['nome'] for p in self.patrocinios_ativos}
        return [p for p in PATROCINADORES_DISPONIVEIS if p['nome'] not in ativos]

    def pode_assinar_patrocinio(self):
        return self.patrocinios_esta_temporada < MAX_PATROCINADORES_TEMPORADA

    def assinar_patrocinio(self, t):
        if not self.pode_assinar_patrocinio():
            return False
        self.patrocinios_esta_temporada += 1
        self.patrocinios_ativos.append({
            'nome':t['nome'],'emoji':t['emoji'],'condicao_pos':t['condicao_pos'],
            'condicao_semanas':t['condicao_semanas'],'pagamento':t['pagamento'],
            'semanas_restantes':t['duracao'],'streak_atual':0,'ativo':False})
        return True

    def processar_patrocinios(self, pos_jogador):
        total=0
        for p in self.patrocinios_ativos:
            if pos_jogador<=p['condicao_pos']: p['streak_atual']+=1
            else: p['streak_atual']=0
            if p['streak_atual']>=p['condicao_semanas']: p['ativo']=True
            if p['ativo']:
                total+=p['pagamento']; self.dinheiro+=p['pagamento']
                p['semanas_restantes']-=1
        self.patrocinios_ativos=[p for p in self.patrocinios_ativos if p['semanas_restantes']>0]
        return total

    # ── Banco ──────────────────────────────────────────────────────────────────
    def tomar_emprestimo(self, op):
        self.dinheiro+=op['valor']
        self.emprestimos_ativos.append({
            'nome':f"R${op['valor']} ({op['juros_pct']}%)",
            'parcela':op['parcela'],'semanas_restantes':op['semanas'],'total_pago':0})

    def processar_emprestimos(self):
        total=0
        for e in self.emprestimos_ativos:
            p=min(e['parcela'],self.dinheiro); self.dinheiro-=p
            e['total_pago']+=p; e['semanas_restantes']-=1; total+=p
        self.emprestimos_ativos=[e for e in self.emprestimos_ativos if e['semanas_restantes']>0]
        return total

    def divida_total(self):       return sum(e['parcela']*e['semanas_restantes'] for e in self.emprestimos_ativos)
    def parcela_semanal_total(self): return sum(e['parcela'] for e in self.emprestimos_ativos)

    # ── Idade / morte ──────────────────────────────────────────────────────────
    def verificar_mortes(self):
        mortos=[c for c in self.cavalos_jogador if c.esta_morto(self.semana)]
        for c in mortos: self.cavalos_jogador.remove(c)
        return [c.nome for c in mortos]

    def cavalos_idosos(self):
        """Retorna cavalos com mais de 70 semanas (prestes a morrer)."""
        return [c for c in self.cavalos_jogador
                if c.idade(self.semana) >= 70 and not c.esta_morto(self.semana)]

    def gerar_potro_emergencia(self):
        """
        Gera um potro gratuito de raça aleatória quando o haras fica vazio.
        É uma doação de um fazendeiro vizinho — narrativa do jogo.
        Retorna o Cavalo gerado ou None se não há baia livre.
        """
        if len(self.cavalos_jogador) >= self.baias:
            return None   # sem baia, não gera
        nome  = random.choice(NOMES)
        raca  = random.choice(RACAS_LISTA)
        sexo  = random.choice(['M', 'F'])
        potro = criar_cavalo(nome, raca, semana_nasc=self.semana)
        potro.sexo = sexo
        self.cavalos_jogador.append(potro)
        return potro

    def checar_substitucao_automatica(self):
        """
        Verifica se o haras precisa de substituição automática.
        Retorna dict com: alertas (cavalos idosos) e emergencia (potro doado).
        """
        resultado = {'alertas': [], 'emergencia': None}

        # Aviso preventivo: cavalos com 70+ semanas
        for c in self.cavalos_idosos():
            semanas_restantes = max(0, c.idade_max - c.idade(self.semana))
            resultado['alertas'].append({
                'nome': c.nome,
                'semanas_restantes': semanas_restantes,
                'idade': c.idade(self.semana),
            })

        # Emergência: haras completamente vazio → gera potro doado
        if len(self.cavalos_jogador) == 0:
            potro = self.gerar_potro_emergencia()
            if potro:
                resultado['emergencia'] = potro

        return resultado

    def cavalos_aptos(self):
        return [c for c in self.cavalos_jogador if c.pode_correr(self.semana)]

    # ── Campeonato ─────────────────────────────────────────────────────────────
    # Reputação mínima por tipo de campeonato
    _REP_MIN = {'regional': 1, 'nacional': 3, 'internacional': 4}

    def pode_entrar_campeonato(self, tipo):
        """Verifica se o jogador tem cavalos aptos, dinheiro e reputação para a taxa."""
        cfg = COMPETICOES.get(tipo, COMPETICOES['regional'])
        if self.dinheiro < cfg['taxa']:
            return False, f"Sem ouro. Taxa: {cfg['taxa']:,}"
        rep_min = self._REP_MIN.get(tipo, 1)
        nr, _ = self.nivel_reputacao()
        if nr < rep_min:
            return False, f"Reputação {rep_min}+ estrelas necessária."
        aptos = self.cavalos_aptos()
        emin  = cfg['estrela_min']
        min_cav = cfg.get('min_cavalos', 1)
        qualificados = [c for c in aptos if estrelas(c.vel_base) >= emin]
        if len(qualificados) < min_cav:
            if min_cav == 1:
                return False, f"Precisa de um cavalo {emin}+ estrelas."
            return False, f"Precisa de {min_cav} cavalos {emin}+ estrelas."
        return True, ''

    def iniciar_campeonato(self, tipo='regional'):
        cfg = COMPETICOES.get(tipo, COMPETICOES['regional'])
        self.dinheiro -= cfg['taxa']
        cp = Campeonato(self.semana, tipo)
        # Determina cavalos para rotação (nacional=2, internacional=5)
        emin = cfg['estrela_min']
        min_cav = cfg.get('min_cavalos', 1)
        qualificados = sorted(
            [c for c in self.cavalos_aptos() if estrelas(c.vel_base) >= emin],
            key=lambda c: c.vel_base, reverse=True
        )
        if min_cav > 1:
            cp.cavalos_ids = [c.id for c in qualificados[:min_cav]]
        self.campeonato = cp

    def proxima_temporada(self, tipo='regional'):
        """Encerra o campeonato e inicia próxima temporada."""
        self.temporada  += 1
        self.campeonato  = None
        self.patrocinios_esta_temporada = 0   # reseta limite de patrocínio

    # ── Leilão ────────────────────────────────────────────────────────────────
    # ── Reprodução ────────────────────────────────────────────────────────────
    def iniciar_gestacao(self, mae, pai, nome_filho, cor_filho):
        """Inicia período de gestação na égua. O potro nasce em 8 semanas."""
        if mae.em_gestacao():
            return False, 'Egua ja esta gestante'
        if mae.sexo != 'F':
            return False, 'Apenas femeas podem gestar'
        if pai.sexo != 'M':
            return False, 'Apenas machos podem cruzar'
        if pai is mae:
            return False, 'Nao pode cruzar com si mesma'
        # Determina raça do filhote
        raca = pai.raca if pai.raca == mae.raca else 'Mestiço'
        if raca not in RACAS: raca = 'Mestiço'
        mae.gestacao_semana = self.semana
        mae.filho_pendente = {
            'nome':      nome_filho or 'Potro',
            'cor':       cor_filho,
            'raca':      raca,
            'vel_base':  round((pai.vel_base + mae.vel_base) / 2, 2),
            'stamina':   int((pai.stamina + mae.stamina) / 2),
            'pai_nome':  pai.nome,
            'mae_nome':  mae.nome,
        }
        return True, f'{mae.nome} esta gestante! Potro nasce em 8 semanas.'

    def verificar_partos(self):
        """Checa se alguma égua deve parir. Retorna lista de nomes nascidos."""
        nascidos = []
        for mae in list(self.cavalos_jogador):
            if not mae.em_gestacao(): continue
            if mae.semanas_gestacao(self.semana) < 8: continue
            # Hora do parto!
            fp = mae.filho_pendente or {}
            cor = fp.get('cor', CORES[0])
            raca = fp.get('raca', 'Mestiço')
            nome = fp.get('nome', 'Potro')
            potro = criar_cavalo(nome, raca, semana_nasc=self.semana,
                                 vel_base=fp.get('vel_base'),
                                 stamina=fp.get('stamina'),
                                 saude=100, cor=cor)
            potro.sexo = random.choice(['M', 'F'])
            # Referências genealógicas
            pai_obj = next((c for c in self.cavalos_jogador
                            if c.nome == fp.get('pai_nome')), None)
            potro.pai = pai_obj
            potro.mae = mae
            if pai_obj: pai_obj.filhos.append(potro)
            mae.filhos.append(potro)
            # Reseta gestação
            mae.gestacao_semana = None
            mae.filho_pendente  = None
            # Adiciona ao haras se houver baia
            if self.pode_comprar_cavalo():
                self.cavalos_jogador.append(potro)
                nascidos.append(potro.nome)
            else:
                nascidos.append(f'{potro.nome} (sem baia!)')
        return nascidos

    def verificar_leilao(self):
        """Checa se deve abrir novo leilão. Chamado no início de cada semana."""
        if self.leilao_ativo:
            # Encerra se passou mais de LEILAO_DURACAO_SEMANAS
            if self.semana - self.leilao_semana >= LEILAO_DURACAO_SEMANAS:
                self.leilao_ativo = False
                self.leilao_lotes = []
            return
        # Abre novo leilão a cada intervalo
        if (self.semana - self.semana_ultimo_leilao) >= LEILAO_INTERVALO_SEMANAS:
            self._abrir_leilao()

    def _abrir_leilao(self):
        """Gera lotes do leilão: mistura lendários + 4★/5★ do mercado."""
        import random as _r
        lotes = []
        # Cavalos lendários disponíveis (não repetir os que já possuímos)
        nomes_possuidos = {c.nome for c in self.cavalos_jogador}
        lends_disp = [d for d in CAVALOS_LENDARIOS if d['nome'] not in nomes_possuidos]

        # 1-2 lendários se disponíveis
        n_lend = min(_r.randint(1, 2), len(lends_disp))
        for d in _r.sample(lends_disp, n_lend):
            cav = criar_cavalo_lendario(d, semana_nasc=-(self.semana + _r.randint(40,60)))
            preco_inicial = int(cav.preco * LEILAO_LANCE_INICIAL_PCT)
            lotes.append({'cavalo': cav, 'lance_atual': preco_inicial,
                          'n_lances': 0, 'vendido': False, 'lendario': True})

        # Completar com cavalos de alta categoria do mercado
        altos = [c for c in self.cavalos_mercado if estrelas(c.vel_base) >= LEILAO_ESTRELA_MIN]
        _r.shuffle(altos)
        for cav in altos[:max(0, LEILAO_N_LOTES - n_lend)]:
            preco_inicial = int(calcular_preco_mercado(cav) * LEILAO_LANCE_INICIAL_PCT)
            lotes.append({'cavalo': cav, 'lance_atual': preco_inicial,
                          'n_lances': 0, 'vendido': False, 'lendario': False})

        if not lotes:
            # Garante pelo menos 1 lendário
            if CAVALOS_LENDARIOS:
                d = _r.choice(CAVALOS_LENDARIOS)
                cav = criar_cavalo_lendario(d, semana_nasc=-55)
                preco_inicial = int(cav.preco * LEILAO_LANCE_INICIAL_PCT)
                lotes.append({'cavalo': cav, 'lance_atual': preco_inicial,
                              'n_lances': 0, 'vendido': False, 'lendario': True})

        self.leilao_lotes        = lotes
        self.leilao_ativo        = True
        self.leilao_semana       = self.semana
        self.semana_ultimo_leilao= self.semana

    def dar_lance(self, idx):
        """Jogador dá um lance no lote idx. Retorna (ok, msg, novo_preco)."""
        if not self.leilao_ativo or idx >= len(self.leilao_lotes):
            return False, 'Leilao indisponivel', 0
        lote = self.leilao_lotes[idx]
        if lote['vendido']:
            return False, 'Lote ja vendido', 0
        if lote['n_lances'] >= LEILAO_MAX_LANCES:
            return False, 'Limite de lances atingido', 0
        novo = int(lote['lance_atual'] * (1 + LEILAO_INCREMENTO_PCT))
        if self.dinheiro < novo:
            return False, f'Precisa de R${novo:,}', novo
        return True, 'Lance valido', novo

    def confirmar_lance(self, idx):
        """Confirma compra pelo lance atual. Retorna (ok, msg)."""
        ok, msg, novo = self.dar_lance(idx)
        if not ok:
            return False, msg
        if not self.pode_comprar_cavalo():
            return False, 'Sem baia disponivel'
        lote = self.leilao_lotes[idx]
        self.dinheiro      -= novo
        lote['lance_atual']  = novo
        lote['n_lances']    += 1
        lote['vendido']      = True
        cav = lote['cavalo']
        # Remove do mercado normal se estava lá
        if cav in self.cavalos_mercado:
            self.cavalos_mercado.remove(cav)
        self.cavalos_jogador.append(cav)
        return True, f'{cav.nome} arrematado por R${novo:,}!'

    def em_campeonato(self):
        return self.campeonato is not None and not self.campeonato.encerrado

    def registrar_medalha(self, posicao, semana, tipo_corrida='avulsa'):
        """Registra uma medalha de corrida (posicoes 1,2,3)."""
        if posicao > 3:
            return
        medalha = {
            'tipo': 'medalha',
            'posicao': posicao,
            'semana': semana,
            'temporada': self.temporada,
            'corrida': tipo_corrida,
        }
        self.trofeus.append(medalha)

    def registrar_trofeu_campeonato(self, posicao, tipo_comp, temporada):
        """Registra um troféu de campeonato."""
        trofeu = {
            'tipo': 'trofeu',
            'posicao': posicao,
            'temporada': temporada,
            'campeonato': tipo_comp,
        }
        self.trofeus.append(trofeu)
