print('[NOTIF] Sistema desativado para Android 12+')

def _enviar(titulo: str, msg: str):
    """Notificações desativadas temporariamente para evitar erro Android 12+"""
    print(f'[NOTIF DESATIVADA] {titulo}: {msg}')
    
# ── Eventos do jogo ────────────────────────────────────────────────────────────

def notif_semana_avancou(semana: int, dinheiro: int):
    """Disparada após cada corrida quando a semana avança."""
    _enviar(
        '🏇 Project Horse — Nova Semana!',
        f'Semana {semana} chegou. Você tem {dinheiro:,} Ouro. '
        'Hora de correr e ganhar mais!'
    )


def notif_leilao_aberto(n_cavalos: int):
    """Disparada quando um leilão novo é aberto."""
    _enviar(
        '🔨 Leilão Disponível!',
        f'{n_cavalos} cavalos raros estão no leilão agora. '
        'Dê seu lance antes que acabem!'
    )


def notif_patrocinio_expirou(nome_pat: str):
    """Disparada quando um patrocínio expira."""
    _enviar(
        '📋 Contrato Encerrado',
        f'O patrocínio de {nome_pat} chegou ao fim. '
        'Acesse Patrocinadores para buscar novos contratos.'
    )


def notif_patrocinio_pagando(nome_pat: str, valor: int):
    """Disparada quando um patrocínio começa a pagar."""
    _enviar(
        '💰 Patrocínio Ativo!',
        f'{nome_pat} está te pagando {valor:,} Ouro por semana. Bom trabalho!'
    )


def notif_cavalo_risco(nome_cavalo: str):
    """Disparada quando um cavalo está com saúde crítica."""
    _enviar(
        '⚠️ Cavalo em Risco!',
        f'{nome_cavalo} está com saúde crítica. '
        'Compre remédios no Mercado antes da próxima corrida.'
    )


def notif_campeonato_encerrado(posicao: int, premio: int):
    """Disparada ao fim de um campeonato."""
    if posicao == 1:
        msg = f'🥇 Você venceu o campeonato! Prêmio: {premio:,} Ouro. Lendário!'
    elif posicao <= 3:
        medals = {2: '🥈', 3: '🥉'}
        msg = f'{medals[posicao]} Pódio no campeonato! Prêmio: {premio:,} Ouro.'
    else:
        msg = f'Campeonato encerrado. Treina mais e tente de novo na próxima temporada!'
    _enviar('🏆 Campeonato Encerrado', msg)
