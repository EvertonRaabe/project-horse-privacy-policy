"""sounds.py – Project Horse — sons gerados programaticamente via WAV PCM puro.
Correções:
  - "No free channels available" → usa mixer com canais dedicados por som
  - Som de fim de corrida mais suave (derrota agora é neutro/dramático leve)
  - Som de clique em todos os botões
"""
import struct, math, os, tempfile

_tmpdir = tempfile.mkdtemp(prefix='prjhorse_snd_')
_sounds  = {}
_inicializado = False
_mudo    = False


# ── Gerador de WAV ──────────────────────────────────────────────────────────────
def _make_wav_torcida(dur=2.2, sr=22050):
    """Gera ruído de torcida leve: murmúrio + aplausos suaves com fade."""
    import random as _rnd
    _rnd.seed(77)
    n = int(sr * dur)
    samples = []
    for i in range(n):
        t = i / sr
        noise  = _rnd.uniform(-1, 1)
        voices = (
            0.30 * math.sin(2*math.pi*480  * t + _rnd.uniform(-0.1,0.1)) +
            0.25 * math.sin(2*math.pi*720  * t + _rnd.uniform(-0.1,0.1)) +
            0.20 * math.sin(2*math.pi*1100 * t + _rnd.uniform(-0.1,0.1)) +
            0.15 * math.sin(2*math.pi*1600 * t + _rnd.uniform(-0.1,0.1)) +
            0.10 * math.sin(2*math.pi*2200 * t + _rnd.uniform(-0.1,0.1))
        )
        attack, sustain = 0.25, 1.40
        release = dur - attack - sustain
        if t < attack:
            env = t / attack
        elif t < attack + sustain:
            env = 0.85 + 0.15 * math.sin(2*math.pi*2.8*t)
        else:
            env = max(0.0, 1.0 - (t-attack-sustain)/release)
        s = (0.60*noise*0.4 + 0.40*voices) * env * 0.38
        samples.append(max(-1.0, min(1.0, s)))
    raw = struct.pack(f'<{len(samples)}h', *[int(s*32767) for s in samples])
    nc=1; bps=2
    hdr = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF',36+len(raw),b'WAVE',
        b'fmt ',16,1,nc,sr,sr*bps,bps,16,b'data',len(raw))
    return hdr+raw


def _make_wav(notes, sr=22050, vol=0.45):
    """
    notes: lista de (freq_hz, duracao_ms, env_ms)
    freq=0 → silêncio, env_ms → envelope fade in/out.
    """
    samples = []
    for freq, dur_ms, env_ms in notes:
        n = max(1, int(sr * dur_ms / 1000))
        e = max(1, int(sr * env_ms / 1000))
        for i in range(n):
            if freq > 0:
                # Mistura senoide + harmônico para som mais natural
                s = (0.7 * math.sin(2 * math.pi * freq * i / sr) +
                     0.3 * math.sin(2 * math.pi * freq * 2 * i / sr))
                s *= vol
                if i < e:       s *= i / e
                elif i > n - e: s *= (n - i) / max(1, e)
            else:
                s = 0.0
            samples.append(max(-1.0, min(1.0, s)))

    raw = struct.pack(f'<{len(samples)}h', *[int(s * 32767) for s in samples])
    nc  = 1; bps = nc * 16 // 8
    hdr = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + len(raw), b'WAVE',
        b'fmt ', 16, 1, nc, sr, sr * bps, bps, 16,
        b'data', len(raw)
    )
    return hdr + raw


# ── Definições dos sons ─────────────────────────────────────────────────────────

# Galope: batidas graves rítmicas — 1 ciclo de ~330ms
_galope_ciclo = [
    (140, 55, 4), (0, 25, 0),
    (120, 55, 4), (0, 25, 0),
    (148, 55, 4), (0, 25, 0),
    (128, 55, 4), (0, 25, 0),
]

# Vitória: fanfarra ascendente com acorde final
_vitoria = [
    (523, 70,  5), (659, 70,  5), (784, 70,  5),
    (0,   15,  0),
    (784, 55,  5), (880, 55,  5), (1047,160, 12),
    (0,   35,  0),
    (1047,55,  5), (1175,55,  5), (1319,200, 20),
    (0,   30,  0),
    (1047,80,  8), (1319,280, 30),
]

# fim_corrida gerado por função própria (ver _make_wav_torcida)

# Derrota: apenas 2 notas suaves descendentes (bem mais curto e leve)
_derrota = [
    (440, 110, 12),
    (0,   25,  0),
    (370, 180, 20),
]

# Clique de botão: toque seco e rápido
_click = [(900, 18, 2), (0, 4, 0), (720, 14, 2)]  # toque seco rápido

# Moeda: brilhante e rápido
_moeda = [(880,35,4),(0,8,0),(1047,50,4),(0,8,0),(1320,100,8)]

# Largada: três bips crescentes + sinal de partida
_largada = [
    (440,55,5),(0,20,0),
    (440,55,5),(0,20,0),
    (440,55,5),(0,20,0),
    (880,220,15),
]

_DEFS = {
    'moeda':      _moeda,
    'galope':     _galope_ciclo * 30,   # ~10s
    'largada':    _largada,
    'vitoria':    _vitoria,
    'derrota':    _derrota,              # reduzido — 2 notas discretas
    'click':      _click,               # clique de botão
    'botao':      _click,               # alias para compatibilidade
}


# ── Inicialização ───────────────────────────────────────────────────────────────
def init_sons():
    global _inicializado
    if _inicializado:
        return
    try:
        from kivy.core.audio import SoundLoader
    except Exception as e:
        print(f'[SONS] SoundLoader indisponível: {e}')
        return

    # Aumentar canais do mixer SDL2 para evitar "No free channels"
    try:
        import sdl2
        sdl2.SDL_mixer.Mix_AllocateChannels(32)
    except Exception:
        pass
    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.set_num_channels(32)
    except Exception:
        pass

    ok = 0
    # Som de torcida — gerado por função própria
    try:
        path_t = os.path.join(_tmpdir, 'fim_corrida.wav')
        if not os.path.exists(path_t):
            with open(path_t, 'wb') as f:
                f.write(_make_wav_torcida())
        snd_t = SoundLoader.load(path_t)
        if snd_t:
            snd_t.volume = 0.55
            _sounds['fim_corrida'] = snd_t
            ok += 1
    except Exception as e:
        print(f'[SONS] Falha torcida: {e}')

    for nome, notes in _DEFS.items():
        if nome == 'fim_corrida': continue  # já gerado acima
        path = os.path.join(_tmpdir, f'{nome}.wav')
        try:
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(_make_wav(notes))
            snd = SoundLoader.load(path)
            if snd:
                snd.volume = 0.75
                _sounds[nome] = snd
                ok += 1
        except Exception as e:
            print(f'[SONS] Falha "{nome}": {e}')

    # Click tem volume menor
    if 'click' in _sounds:
        _sounds['click'].volume = 0.45
    if 'botao' in _sounds:
        _sounds['botao'].volume = 0.45

    _inicializado = True
    print(f'[SONS] {ok}/{len(_DEFS)} sons carregados. Dir: {_tmpdir}')


# ── API pública ─────────────────────────────────────────────────────────────────
def set_mudo(ativo: bool):
    global _mudo
    _mudo = ativo
    if ativo:
        for s in _sounds.values():
            try: s.stop()
            except: pass

def get_mudo() -> bool:
    return _mudo

def tocar(nome: str):
    """Toca um som — cria instância nova para permitir sobreposição."""
    if _mudo: return
    _garantir_init()
    s = _sounds.get(nome)
    if not s: return
    try:
        # Para o som anterior do mesmo tipo e reinicia
        # Isso evita acumulação de canais
        s.stop()
        s.seek(0)
        s.play()
    except Exception as e:
        print(f'[SONS] Erro tocar "{nome}": {e}')

# Controle de loops via Clock (evita bug on_stop do SDL2)
_loop_events = {}   # nome → Clock event

def tocar_loop(nome: str):
    """Toca em loop usando Clock — não depende de on_stop."""
    if _mudo: return
    _garantir_init()
    s = _sounds.get(nome)
    if not s: return
    # Cancela loop anterior se existir
    parar(nome)
    dur = getattr(s, 'length', 2.0) or 2.0
    if dur <= 0: dur = 2.0

    def _tick(dt):
        if _mudo: return
        if nome not in _loop_events: return   # foi parado
        try:
            s.stop()
            s.play()
        except Exception: pass

    try:
        s.stop()
        s.play()
        from kivy.clock import Clock as _Clk
        ev = _Clk.schedule_interval(_tick, dur)
        _loop_events[nome] = ev
    except Exception as e:
        print(f'[SONS] Erro loop "{nome}": {e}')

def parar(nome: str):
    """Para um som e cancela o loop Clock."""
    # Cancela Clock event primeiro
    ev = _loop_events.pop(nome, None)
    if ev:
        try:
            from kivy.clock import Clock as _Clk
            _Clk.unschedule(ev)
        except Exception: pass
    s = _sounds.get(nome)
    if not s: return
    try:
        s.loop = False
        s.stop()
    except Exception as e:
        print(f'[SONS] Erro parar "{nome}": {e}')

def parar_tudo():
    """Para todos os sons imediatamente."""
    for nome in list(_sounds.keys()) + list(_loop_events.keys()):
        parar(nome)

def click():
    """Atalho para toque de botão — chame de qualquer lugar."""
    tocar('click')

def _garantir_init():
    if not _inicializado:
        init_sons()
