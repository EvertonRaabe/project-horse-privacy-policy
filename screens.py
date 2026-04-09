"""screens.py – Project Horse — visual polish + baias + campeonato + nomes na corrida"""
from config import ADMOB_MAX_POR_SEMANA
import random, math
from i18n import T, set_lang, get_lang
import sounds as _snd_mod
try:
    import notifications as _notif
except Exception:
    class _notif:
        @staticmethod
        def notif_semana_avancou(*a,**k): pass
        @staticmethod
        def notif_leilao_aberto(*a,**k): pass
        @staticmethod
        def notif_patrocinio_expirou(*a,**k): pass
        @staticmethod
        def notif_patrocinio_pagando(*a,**k): pass
        @staticmethod
        def notif_cavalo_risco(*a,**k): pass
        @staticmethod
        def notif_campeonato_encerrado(*a,**k): pass

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout    import BoxLayout
from kivy.uix.gridlayout   import GridLayout
from kivy.uix.scrollview   import ScrollView
from kivy.uix.widget       import Widget
from kivy.uix.label        import Label
from kivy.uix.textinput    import TextInput
from kivy.uix.progressbar  import ProgressBar
from kivy.uix.dropdown     import DropDown
from kivy.uix.button       import Button
from kivy.graphics          import Color, Rectangle, Ellipse, RoundedRectangle
from kivy.clock             import Clock
from kivy.core.window       import Window
from kivy.metrics           import dp

# ── Emoji PNG ─────────────────────────────────────────────────────────────────
try:
    from emoji_img import make_emoji_box, make_emoji_button, tem_emoji
    _EMOJI_OK = True
    print('[EMOJI] OK!')
except Exception as _err:
    _EMOJI_OK = False
    print(f'[EMOJI] FALHOU: {_err}')
    def tem_emoji(t): return False

def _elbl(txt, font_size, color, height, size_hint_y=None, halign='center', bold=False):
    import sys as _sys
    _is_android = not _sys.platform.startswith('linux') or 'ANDROID_ARGUMENT' in __import__('os').environ
    if _EMOJI_OK and tem_emoji(str(txt)) and _is_android:
        return make_emoji_box(text=str(txt), font_size=font_size, color=color,
                              bold=bold, halign=halign,
                              height=height, size_hint_y=size_hint_y)
    from kivy.uix.label import Label
    l = Label(text=str(txt), font_size=font_size, color=color,
              size_hint_y=size_hint_y, height=height, halign=halign, valign='middle')
    l.bind(size=lambda w,v: setattr(w,'text_size',(v[0],None)))
    return l

def _ebtn(txt, bg, fg, font_size, height, cb=None, bold=True, border=None, size_hint_x=1):
    # Emoji render only on Android — on desktop use plain Button (avoids freeze)
    import sys as _sys
    _is_android = not _sys.platform.startswith('linux') or 'ANDROID_ARGUMENT' in __import__('os').environ
    if _EMOJI_OK and tem_emoji(str(txt)) and _is_android:
        return make_emoji_button(str(txt), bg_color=bg, text_color=fg,
                                 font_size=font_size, height=height,
                                 bold=bold, border_color=border,
                                 cb=cb, size_hint_x=size_hint_x)
    from kivy.uix.button import Button
    b = Button(text=str(txt), background_normal='', background_color=bg,
               color=fg, font_size=font_size, bold=bold,
               size_hint_y=None, height=height, size_hint_x=size_hint_x)
    if cb: b.bind(on_release=cb)
    return b

from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton

from game_logic import (Jogo, Cavalo, criar_cavalo, MEDALHAS,
                        ITENS_COMIDA, ITENS_REMEDIO, ITENS_EQUIPAMENTO,
                        FUNCIONARIOS, RACAS_LISTA,
                        estrelas, calcular_preco_mercado, atualizar_preco_pos_corrida)
from storage    import salvar_jogo, carregar_jogo
from config     import (CORES, CORES_NOMES, CORES_CRINA, RACAS,
                        UI_BG,UI_CARD,UI_CARD2,UI_CARD3,
                        UI_GOLD,UI_GOLD_DIM,UI_GOLD_BG,
                        UI_GREEN,UI_GREEN_BG,UI_RED,UI_RED_BG,
                        UI_BLUE,UI_BLUE_BG,UI_PURPLE,UI_ORANGE,
                        UI_TEXT,UI_DIM,
                        PATROCINADORES_DISPONIVEIS,OPCOES_EMPRESTIMO,
                        CAMP_N_CORRIDAS,CAMP_PONTOS,
                        CAMP_PREMIO_CORRIDA,CAMP_PREMIO_FINAL,
                        PRECO_BAIA, PRECO_MIN_ESTRELA,
                        ESTRELAS_EMOJI, PRECO_MAX_ESTRELA,
                        PREMIO_CORRIDA_ESTRELA, COMPETICOES,
                        HARAS_TIPOS, HARAS_NIVEL_BAIAS,
                        CUSTO_MANUTENCAO_BASE, MAX_PATROCINADORES_TEMPORADA,
                        CAVALOS_LENDARIOS, LEILAO_INTERVALO_SEMANAS,
                        VEL_MAX_GLOBAL,
                        ADMOB_MAX_POR_SEMANA, ADMOB_RECOMPENSA_OURO,
                        REPUTACAO_NIVEL, REPUTACAO_PONTOS,
                        ENERGIA_GASTO_MIN, ENERGIA_GASTO_MAX, ENERGIA_RECUPERA_SEMANA,
                        PCT_REVENDA)

try:
    import admob as _admob
except Exception as _e_admob:
    print(f'[AdMob] Modulo admob nao carregado: {_e_admob}')
    _admob = None

try:
    import sounds as _snd
except Exception as _e_snd:
    print(f'[SONS] Módulo não carregado: {_e_snd}')
    class _snd:
        @staticmethod
        def tocar(n): pass
        @staticmethod
        def tocar_loop(n): pass
        @staticmethod
        def parar(n): pass
        @staticmethod
        def init_sons(): pass

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS DE CANVAS
# ═══════════════════════════════════════════════════════════════════════════════

def _set_bg(w, rgba):
    with w.canvas.before:
        Color(*rgba); r=Rectangle(pos=w.pos,size=w.size)
    w.bind(pos=lambda _,v: setattr(r,'pos',v), size=lambda _,v: setattr(r,'size',v))

def _rounded_bg(w, rgba, radius=12):
    with w.canvas.before:
        Color(*rgba); r=RoundedRectangle(pos=w.pos,size=w.size,radius=[radius])
    w.bind(pos=lambda _,v: setattr(r,'pos',v), size=lambda _,v: setattr(r,'size',v))

def _accent_bar(w, rgba, h=3):
    bar=Widget(size_hint_y=None,height=dp(h))
    with bar.canvas:
        Color(*rgba); r=Rectangle(pos=bar.pos,size=bar.size)
    bar.bind(pos=lambda _,v: setattr(r,'pos',v), size=lambda _,v: setattr(r,'size',v))
    return bar


# ═══════════════════════════════════════════════════════════════════════════════
#  COMPONENTES UI
# ═══════════════════════════════════════════════════════════════════════════════

def btn_primary(txt, cb=None, h=None):
    alt = h or dp(48)
    if _EMOJI_OK and tem_emoji(str(txt)):
        return make_emoji_button(str(txt), bg_color=UI_GOLD,
                                 text_color=(0.04,0.04,0.04,1),
                                 font_size=dp(15), height=alt, cb=cb)
    b=MDRaisedButton(text=txt, md_bg_color=UI_GOLD,
                     theme_text_color="Custom", text_color=(0.04,0.04,0.04,1),
                     size_hint_y=None, height=alt, elevation=4)
    b.bind(on_press=lambda *_: _snd.tocar('click'))
    if cb: b.bind(on_release=cb)
    return b

def btn_secondary(txt, cb=None, h=None):
    alt = h or dp(44)
    if _EMOJI_OK and tem_emoji(str(txt)):
        return make_emoji_button(str(txt), bg_color=(0.09,0.09,0.16,1),
                                 text_color=UI_TEXT, border_color=UI_GOLD_DIM,
                                 font_size=dp(14), height=alt, cb=cb)
    b=MDRectangleFlatButton(text=txt, size_hint_y=None, height=alt,
                             theme_text_color="Custom",
                             text_color=UI_TEXT, line_color=UI_GOLD_DIM)
    b.bind(on_press=lambda *_: _snd.tocar('click'))
    if cb: b.bind(on_release=cb)
    return b

def btn_danger(txt, cb=None, h=None):
    alt = h or dp(44)
    if _EMOJI_OK and tem_emoji(str(txt)):
        return make_emoji_button(str(txt), bg_color=UI_RED_BG,
                                 text_color=UI_RED, font_size=dp(14), height=alt, cb=cb)
    b=Button(text=txt, size_hint_y=None, height=alt,
             background_normal='', background_color=UI_RED_BG,
             color=UI_RED, font_size=dp(14), bold=True)
    b.bind(on_press=lambda *_: _snd.tocar('click'))
    if cb: b.bind(on_release=cb)
    return b

def btn_success(txt, cb=None, h=None):
    alt = h or dp(44)
    if _EMOJI_OK and tem_emoji(str(txt)):
        return make_emoji_button(str(txt), bg_color=UI_GREEN_BG,
                                 text_color=UI_GREEN, font_size=dp(14), height=alt, cb=cb)
    b=Button(text=txt, size_hint_y=None, height=alt,
             background_normal='', background_color=UI_GREEN_BG,
             color=UI_GREEN, font_size=dp(14), bold=True)
    b.bind(on_press=lambda *_: _snd.tocar('click'))
    if cb: b.bind(on_release=cb)
    return b

def btn_tab(txt, ativo=False, cb=None):
    bg=UI_GOLD if ativo else (0.15,0.15,0.25,1)
    fg=(0.04,0.04,0.04,1) if ativo else UI_DIM
    if _EMOJI_OK and tem_emoji(str(txt)):
        return make_emoji_button(str(txt), bg_color=bg, text_color=fg,
                                 font_size=dp(12), height=dp(40), bold=ativo, cb=cb)
    b=Button(text=txt, size_hint=(1,None), height=dp(40),
             background_normal='', background_color=bg,
             color=fg, font_size=dp(12), bold=ativo)
    if cb: b.bind(on_release=cb)
    return b

def lbl(txt, sz=15, cor=None, bold=False, halign='left', h=None, markup=False):
    cor = cor or UI_TEXT
    alt = h or dp(sz * 2.0)
    import sys as _sys
    _is_android = not _sys.platform.startswith('linux') or 'ANDROID_ARGUMENT' in __import__('os').environ
    if _EMOJI_OK and tem_emoji(str(txt)) and _is_android:
        return make_emoji_box(text=str(txt), font_size=dp(sz), color=cor,
                              bold=bold, halign=halign, height=alt, size_hint_y=None)
    if bold: txt, markup = f'[b]{txt}[/b]', True
    l = Label(text=txt, font_size=dp(sz), color=cor,
              size_hint_y=None, height=alt, halign=halign, markup=markup)
    l.bind(size=lambda w, v: setattr(w, 'text_size', (v[0], None)))
    return l

def sep(cor=None):
    s=Widget(size_hint_y=None,height=dp(1))
    with s.canvas:
        Color(*(cor or UI_GOLD_DIM)); r=Rectangle(pos=s.pos,size=s.size)
    s.bind(pos=lambda w,v: setattr(r,'pos',v), size=lambda w,v: setattr(r,'size',v))
    return s

def spacer(h=8):
    return Widget(size_hint_y=None, height=dp(h))

def mk_scroll():
    sv=ScrollView(size_hint=(1,1))
    box=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(8),padding=(dp(4),dp(4)))
    box.bind(minimum_height=box.setter('height'))
    sv.add_widget(box); return sv,box

def card(h=None, bg=None, radius=10):
    c=BoxLayout(orientation='vertical', size_hint_y=None,
                height=h or dp(100), padding=dp(12), spacing=dp(6))
    _rounded_bg(c, bg or UI_CARD, radius)
    return c

def hud_chip(txt, cor_bg, cor_txt=None):
    b=Button(text=txt, size_hint=(None,None), size=(dp(1),dp(28)),
             background_normal='', background_color=cor_bg,
             color=cor_txt or UI_TEXT, font_size=dp(12), bold=True)
    b.texture_update()
    b.width=b.texture_size[0]+dp(16)
    return b

def titulo_tela(txt, emoji='', cor=None, cb_voltar=None):
    """Cabeçalho de tela. cb_voltar ignorado — botão fica na barra inferior."""
    box=BoxLayout(size_hint_y=None, height=dp(70), padding=(dp(16),dp(8)))
    _set_bg(box, UI_CARD)
    box.add_widget(Label(
        text=f'[b]{emoji}  {txt}[/b]', markup=True,
        font_size=dp(22), color=cor or UI_GOLD, halign='left'))
    return box

def barra_voltar(manager, destino='menu', txt=None):
    """Barra fixa na base da tela com botão Voltar sempre visível."""
    t = txt or '🐴  Voltar'
    bar = BoxLayout(size_hint_y=None, height=dp(70),
                    padding=(dp(10), dp(6)), spacing=dp(8))
    _set_bg(bar, (0.06, 0.06, 0.12, 1))
    # linha separadora no topo da barra
    line = Widget(size_hint_y=None, height=dp(1))
    with line.canvas:
        Color(*UI_GOLD_DIM); r = Rectangle(pos=line.pos, size=line.size)
    line.bind(pos=lambda w,v: setattr(r,'pos',v), size=lambda w,v: setattr(r,'size',v))

    root = BoxLayout(orientation='vertical', size_hint_y=None,
                     height=dp(57), spacing=0)
    root.add_widget(line)
    btn = Button(text=t, background_normal='', background_color=(0.12,0.10,0.20,1),
                 color=UI_GOLD, font_size=dp(16), bold=True,
                 size_hint_y=None, height=dp(56))
    btn.bind(on_press=lambda *_: _snd.tocar('click'))
    btn.bind(on_release=lambda *_: setattr(manager, 'current', destino))
    root.add_widget(btn)
    return root


# ═══════════════════════════════════════════════════════════════════════════════
#  SPLASH
# ═══════════════════════════════════════════════════════════════════════════════
class SplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(0.04,0.04,0.08,1); Rectangle(pos=self.pos,size=self.size)
        root=BoxLayout(orientation='vertical',spacing=dp(12),padding=dp(48))
        self.add_widget(root)
        root.add_widget(Widget())
        root.add_widget(_elbl('🏇', font_size=dp(80), color=UI_TEXT, height=dp(100), size_hint_y=None, halign='center'))
        root.add_widget(Label(text='[b]PROJECT HORSE[/b]',markup=True,
                              font_size=dp(38),color=UI_GOLD,size_hint_y=None,height=dp(58)))
        root.add_widget(Label(text=T('simulador'),font_size=dp(17),
                              color=UI_DIM,size_hint_y=None,height=dp(30)))
        root.add_widget(Label(text='Produzido por Everton Lima',font_size=dp(13),
                              color=(0.35,0.35,0.45,1),size_hint_y=None,height=dp(24)))
        root.add_widget(Widget())
        pb_box=BoxLayout(size_hint_y=None,height=dp(12),padding=(dp(40),0))
        self._pb=ProgressBar(max=100,value=0)
        pb_box.add_widget(self._pb); root.add_widget(pb_box)
        root.add_widget(Label(text=T('carregar_save'),font_size=dp(12),color=UI_DIM,
                              size_hint_y=None,height=dp(24)))
        self._p=0; Clock.schedule_interval(self._tick,1/30)

    def _tick(self,dt):
        self._p+=2; self._pb.value=self._p
        if self._p>=100: Clock.unschedule(self._tick); self.manager.current='login'


# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
class LoginScreen(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        root=BoxLayout(orientation='vertical',spacing=dp(14),padding=(dp(36),dp(60)))
        self.add_widget(root)
        root.add_widget(Widget())
        root.add_widget(_elbl('🏇', font_size=dp(64), color=UI_TEXT, height=dp(80), size_hint_y=None, halign='center'))
        root.add_widget(Label(text='[b]PROJECT HORSE[/b]',markup=True,
                              font_size=dp(32),color=UI_GOLD,size_hint_y=None,height=dp(52)))
        root.add_widget(Label(text=T('slogan'),font_size=dp(15),
                              color=UI_DIM,size_hint_y=None,height=dp(28)))
        root.add_widget(spacer(20))
        self.nome=TextInput(hint_text=T('hint_nome'),multiline=False,
                            background_color=(0.11,0.11,0.19,1),
                            foreground_color=UI_TEXT,cursor_color=UI_GOLD,
                            font_size=dp(20),size_hint_y=None,height=dp(56),
                            padding=(dp(14),dp(14)))
        self.nome.bind(on_text_validate=self._novo)
        root.add_widget(self.nome)
        root.add_widget(spacer(8))
        root.add_widget(_ebtn(f'🎮  {T("novo_jogo")}',
                              bg=UI_GOLD, fg=(0.04,0.04,0.04,1),
                              font_size=dp(18), height=dp(54), cb=self._novo))
        root.add_widget(_ebtn(f'📂  {T("menu_carregar")} {T("menu_salvar")}',
                              bg=(0.09,0.09,0.16,1), fg=UI_TEXT,
                              font_size=dp(15), height=dp(46),
                              cb=lambda *_: self._carregar()))
        root.add_widget(spacer(12))
        _btns_row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        def _abrir_pp(*_):
            import webbrowser
            webbrowser.open('https://evertonraabe.github.io/project-horse-privacy-policy/')
        _btns_row.add_widget(_ebtn(f'⚙ {T("menu_config")}',
                                   bg=(0.09,0.09,0.16,1), fg=UI_TEXT,
                                   font_size=dp(13), height=dp(40),
                                   cb=lambda *_: self._abrir_config()))
        _btns_row.add_widget(_ebtn(f'🔧 {T("politica")}',
                                   bg=(0.09,0.09,0.16,1), fg=UI_TEXT,
                                   font_size=dp(13), height=dp(40), cb=_abrir_pp))
        root.add_widget(_btns_row)
        root.add_widget(Widget())

    def _novo(self,*_):
        n=self.nome.text.strip()
        if not n: self.nome.hint_text='⚠ Digite um nome!'; return
        self.manager.nome_jogador=n
        # Mostrar tutorial só na primeira partida
        self.manager.tutorial_pendente=True
        self.manager.current='menu'

    def _carregar(self,*_):
        novo=carregar_jogo()
        if novo: self.manager.jogo=novo
        self.manager.tutorial_pendente=False
        self.manager.current='menu'

    def _abrir_config(self,*_):
        _snd.tocar('click')
        # Mini popup de configurações inline
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout as _BL
        box = _BL(orientation='vertical', padding=dp(16), spacing=dp(12))
        _set_bg(box, (0.06,0.06,0.12,1))
        # Som
        box.add_widget(lbl(T('cfg_som'), sz=15, cor=UI_GOLD, bold=True, h=dp(28)))
        som_row = _BL(size_hint_y=None, height=dp(48), spacing=dp(8))
        mudo = _snd_mod.get_mudo()
        def _mk_som(txt, ativo):
            b = Button(text=txt, background_normal='',
                       background_color=UI_GREEN if ativo else (0.18,0.18,0.24,1),
                       color=(0.04,0.04,0.04,1) if ativo else UI_DIM,
                       font_size=dp(14), bold=ativo,
                       size_hint_y=None, height=dp(46))
            return b
        bon = _mk_som(T('cfg_som_on'), not mudo)
        boff= _mk_som(T('cfg_som_off'), mudo)
        def _set_mudo(v, popup):
            _snd_mod.set_mudo(v); popup.dismiss(); self._abrir_config()
        som_row.add_widget(bon); som_row.add_widget(boff)
        box.add_widget(som_row)
        # Idioma
        box.add_widget(sep())
        box.add_widget(lbl(T('cfg_idioma'), sz=15, cor=UI_GOLD, bold=True, h=dp(28)))
        lang = get_lang()
        popup_ref = [None]
        for cod, nome in [('pt','🇧🇷 Português'),('en','🇺🇸 English'),('es','🇲🇽 Español')]:
            ativo = (cod == lang)
            row = _BL(size_hint_y=None, height=dp(44), spacing=dp(8))
            _rounded_bg(row, UI_BLUE_BG if ativo else UI_CARD, 8)
            row.add_widget(lbl(f'[b]{nome}[/b]' if ativo else nome,
                               sz=14, cor=UI_BLUE if ativo else UI_TEXT, h=dp(36)))
            if not ativo:
                def _sel(_, c2=cod, pr=popup_ref):
                    set_lang(c2)
                    if pr[0]: pr[0].dismiss()
                    self.on_enter()   # recarrega login no idioma novo
                bb = Button(text=T('selecionar'), background_normal='',
                            background_color=(0.18,0.30,0.55,1),
                            color=UI_TEXT, font_size=dp(13),
                            size_hint=(None,None), size=(dp(110),dp(38)))
                bb.bind(on_release=_sel)
                row.add_widget(bb)
            else:
                row.add_widget(lbl('✅ Ativo', sz=12, cor=UI_GREEN, h=dp(36)))
            box.add_widget(row)
        popup = Popup(title=T('menu_config'), content=box,
                      size_hint=(0.90, None), height=dp(420))
        # Vincular set_mudo após criar popup
        bon.bind(on_release=lambda *_: _set_mudo(False, popup))
        boff.bind(on_release=lambda *_: _set_mudo(True, popup))
        popup_ref[0] = popup
        popup.open()


# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIGURACOES
# ═══════════════════════════════════════════════════════════════════════════════
class TelaConfig(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        h=BoxLayout(size_hint_y=None,height=dp(64),padding=(dp(8),dp(12)),spacing=dp(8))
        _set_bg(h,(0.06,0.08,0.14,1))
        h.add_widget(Label(text=f'[b]{T("cfg_titulo")}[/b]',markup=True,
                           font_size=dp(22),color=UI_GOLD))
        root.add_widget(h); root.add_widget(sep())
        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(18),dp(14)); box.spacing=dp(14)

        box.add_widget(lbl(T('cfg_som'),sz=16,cor=UI_TEXT,bold=True,h=dp(30)))
        mudo=_snd_mod.get_mudo()
        som_row=BoxLayout(size_hint_y=None,height=dp(56),spacing=dp(12))
        def _mk(txt,on):
            return Button(text=txt,background_normal='',
                          background_color=UI_GREEN if on else (0.18,0.18,0.24,1),
                          color=(0.04,0.04,0.04,1) if on else UI_DIM,
                          font_size=dp(15),bold=on,size_hint_y=None,height=dp(54))
        bon=_mk(T('cfg_som_on'),not mudo)
        boff=_mk(T('cfg_som_off'),mudo)
        bon.bind(on_release=lambda *_: (self._set_som(False),))
        boff.bind(on_release=lambda *_: (self._set_som(True),))
        som_row.add_widget(bon); som_row.add_widget(boff)
        box.add_widget(som_row)
        box.add_widget(sep())

        box.add_widget(lbl(T('cfg_idioma'),sz=16,cor=UI_TEXT,bold=True,h=dp(30)))
        lang=get_lang()
        for cod,nome,regiao in [('pt','Portugues','Brasil'),
                                  ('en','English','USA'),
                                  ('es','Espanol','Latinoamerica')]:
            ativo=(cod==lang)
            row=BoxLayout(size_hint_y=None,height=dp(64),spacing=dp(10),
                          padding=(dp(10),dp(6)))
            _rounded_bg(row,UI_BLUE_BG if ativo else UI_CARD,10)
            info=BoxLayout(orientation='vertical')
            info.add_widget(Label(
                text=f'[b]{nome}[/b]' if ativo else nome,
                markup=True,font_size=dp(17),
                color=UI_BLUE if ativo else UI_TEXT,halign='left'))
            info.add_widget(Label(text=regiao,font_size=dp(11),
                                   color=UI_DIM,halign='left'))
            row.add_widget(info)
            if ativo:
                row.add_widget(Label(
                    text='[ ATIVO ]',font_size=dp(13),color=UI_GREEN,
                    size_hint_x=None,width=dp(76)))
            else:
                bb=Button(text=T('selecionar'),background_normal='',
                          background_color=(0.18,0.30,0.55,1),
                          color=UI_TEXT,font_size=dp(13),
                          size_hint_x=None,width=dp(104),
                          size_hint_y=None,height=dp(42))
                bb.bind(on_release=lambda _,c=cod: self._set_lang(c))
                row.add_widget(bb)
            box.add_widget(row)


    def _set_som(self,mudo):
        _snd_mod.set_mudo(mudo)
        self.on_enter()

    def _set_lang(self,cod):
        set_lang(cod)
        self.on_enter()
        try:
            self.manager.get_screen('menu').on_enter()
        except Exception:
            pass

    def on_language_change(self):
        self.clear_widgets()
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class TelaMenu(Screen):
    def on_enter(self):
        if getattr(self.manager,'tutorial_pendente',False):
            self.manager.tutorial_pendente=False
            Clock.schedule_once(lambda *_: self._abrir_tutorial(),0.3)
            return
        self._construir()
    def _abrir_tutorial(self):
        if 'tutorial' not in self.manager.screen_names:
            from kivy.uix.screenmanager import Screen as _Scr
            t=TelaTutorial(name='tutorial')
            self.manager.add_widget(t)
        self.manager.current='tutorial'
    def _construir(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)

        # HUD limpo — sem botão de anúncio (movido para TelaBanco)
        hud=BoxLayout(size_hint_y=None,height=dp(56),padding=(dp(10),dp(6)),spacing=dp(10))
        _set_bg(hud,UI_CARD)

        # Semana
        hud.add_widget(Label(text=f'[b]{T("sem_label")} {jogo.semana}[/b]',markup=True,
                             font_size=dp(14),color=UI_GOLD,
                             size_hint_x=None,width=dp(68)))

        # Ouro
        _cor_din=UI_GREEN if jogo.dinheiro>=0 else UI_RED
        hud.add_widget(Label(text=f'[b]Ouro {jogo.dinheiro:,}[/b]',markup=True,
                             font_size=dp(15),color=_cor_din))

        # Reputação
        _nrh,_crh=jogo.nivel_reputacao()
        _rep_stars='★'*_nrh
        hud.add_widget(Label(text=f'{_rep_stars} {_crh["nome"][:8]}',
                             font_size=dp(11),color=UI_PURPLE,
                             size_hint_x=None,width=dp(90)))

        # Baias
        hud.add_widget(Label(text=f'🏠{jogo.baias_livres}/{jogo.baias}',
                             font_size=dp(12),color=UI_BLUE,
                             size_hint_x=None,width=dp(56)))

        # Dívida (só se tiver)
        div=jogo.divida_total()
        if div>0:
            hud.add_widget(Label(text=f'💳-{div:,}',
                                 font_size=dp(11),color=UI_RED,
                                 size_hint_x=None,width=dp(72)))

        # Campeonato (só se ativo)
        if jogo.em_campeonato():
            cp=jogo.campeonato
            hud.add_widget(Label(
                text=f"{cp.cfg['nome'][:5].upper()} {cp.corrida_atual}/{cp.n_corridas}",
                font_size=dp(11),color=cp.cfg['cor'],size_hint_x=None,width=dp(80)))

        root.add_widget(hud)
        root.add_widget(sep())

        nome_jog=getattr(self.manager,'nome_jogador','Haras')
        root.add_widget(lbl(f'🏠 {T("haras_label")} {nome_jog}',
                            sz=20, cor=UI_TEXT, bold=True, h=dp(44)))
        root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        box.padding=(dp(12),dp(8))

        b_corrida=_ebtn(f'🏁  {T("menu_corrida")}', bg=UI_GOLD,
                        fg=(0.04,0.04,0.04,1), font_size=dp(18),
                        height=dp(62), cb=lambda *_: self._ir('corrida'))
        box.add_widget(b_corrida)

        if jogo.em_campeonato():
            cp=jogo.campeonato; cfg=cp.cfg
            cor_camp=cfg['cor']
            b_camp=Button(
                text=f"{cfg['nome'].upper()} T{jogo.temporada} ({cp.corrida_atual}/{cp.n_corridas})",
                background_normal='',background_color=cor_camp,
                color=(0.04,0.04,0.04,1),font_size=dp(16),bold=True,
                size_hint_y=None,height=dp(52))
            b_camp.bind(on_release=lambda *_: self._ir('campeonato'))
            box.add_widget(b_camp)
        else:
            if jogo.leilao_ativo and jogo.leilao_lotes:
                banner=Button(
                    text='LEILAO ATIVO! Toque para ver cavalos raros!',
                    background_normal='',background_color=(0.14,0.09,0.02,1),
                    color=UI_GOLD,font_size=dp(13),bold=True,
                    size_hint_y=None,height=dp(46))
                banner.bind(on_release=lambda *_: self._ir('leilao'))
                box.add_widget(banner)
            box.add_widget(lbl(T('competicao'),sz=13,cor=UI_DIM,h=dp(24)))
            for tipo,cfg in COMPETICOES.items():
                pode,motivo=jogo.pode_entrar_campeonato(tipo)
                cor=cfg['cor'] if pode else (0.20,0.20,0.28,1)
                txt_btn=f"{cfg['emoji']}  {cfg['nome']}  —  Taxa {cfg['taxa']:,} Ouro"
                altura=dp(52)
                if not pode:
                    txt_btn+=f'\n({motivo})'
                    altura=dp(68)
                _cb_comp = (lambda *_,t=tipo: self._iniciar_campeonato(t)) if pode else None
                b = _ebtn(txt_btn, bg=cor,
                          fg=(0.04,0.04,0.04,1) if pode else UI_DIM,
                          font_size=dp(13), height=altura, cb=_cb_comp)
                box.add_widget(b)

        box.add_widget(sep())

        grid=GridLayout(cols=2,size_hint_y=None,spacing=dp(6))
        grid.bind(minimum_height=grid.setter('height'))
        for txt,tela in [
            (f'🐎 {T("menu_cavalos")}',    'cavalos'),
            (f'🛒 {T("menu_mercado")}',     'mercado'),
            (f'🤝 {T("menu_patrocinador")}','patrocinador'),
            (f'🏦 {T("menu_banco")}',       'banco'),
            (f'🌳 {T("menu_genealogia")}',  'genealogia'),
            (f'💞 {T("menu_cruzamento")}',  'cruzamento'),
            (f'📜 {T("menu_historico")}',   'historico'),
            (f'📅 {T("menu_calendario")}',  'calendario'),
            (f'💰 {T("menu_apostas")}',     'apostas'),
            (f'👔 {T("menu_funcionarios")}','funcionarios'),
            (f'🏆 {T("menu_trofeus")}',     'trofeus'),
            (f'🔨 {T("menu_leilao")}',      'leilao'),
            (f'⚙  {T("menu_config")}',     'config'),
            (f'🏅 Recordes',                  'recordes'),
        ]:
            b=_ebtn(txt, bg=UI_CARD2, fg=UI_TEXT, font_size=dp(13),
                    height=dp(46), cb=lambda _,t=tela: self._ir(t))
            grid.add_widget(b)
        box.add_widget(grid)

        box.add_widget(sep())
        box.add_widget(btn_secondary(f'💾 {T("menu_salvar")}',cb=lambda *_: (salvar_jogo(jogo),)))
        box.add_widget(btn_secondary(f'📂 {T("menu_carregar")}',cb=self._carregar))
        box.add_widget(btn_danger(f'🚪 {T("menu_sair")}',cb=lambda *_: self._sair()))

    def _ir(self,tela):
        if tela in self.manager.screen_names: self.manager.current=tela

    def _carregar(self,*_):
        novo=carregar_jogo()
        if novo: self.manager.jogo=novo
        self.on_enter()

    def _sair(self):
        from kivy.app import App; App.get_running_app().stop()

    def _iniciar_campeonato(self, tipo='regional'):
        jogo=self.manager.jogo
        pode,motivo=jogo.pode_entrar_campeonato(tipo)
        if not pode: return
        jogo.iniciar_campeonato(tipo)
        self.on_enter()

    def on_language_change(self):
        self.clear_widgets()
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  BANCO  ← ATUALIZADO: 1 empréstimo por vez, teto 10.000 Ouro
# ═══════════════════════════════════════════════════════════════════════════════
class TelaBanco(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self, UI_BG)
        jogo = self.manager.jogo
        root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('menu_banco'), '🏦'))
        root.add_widget(sep())

        sv, box = mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding = (dp(14), dp(10))

        # ── Situação atual ────────────────────────────────────────────────────
        div  = jogo.divida_total()
        parc = jogo.parcela_semanal_total()
        status_card = card(h=dp(68), bg=UI_RED_BG if div > 0 else UI_GREEN_BG)
        if div > 0:
            status_card.add_widget(lbl(f'💳 {T("divida_total")} {div:,} {T("item_ouro")}',
                                        sz=16, cor=UI_RED, bold=True, h=dp(28)))
            status_card.add_widget(lbl(f'{T("parcela_semanal")} {parc} Ouro',
                                        sz=13, cor=UI_DIM, h=dp(22)))
        else:
            status_card.add_widget(lbl(f'✅ {T("sem_dividas")}!',
                                        sz=17, cor=UI_GREEN, bold=True,
                                        halign='center', h=dp(36)))
        box.add_widget(status_card)

        # ── Empréstimos ativos ─────────────────────────────────────────────────
        if jogo.emprestimos_ativos:
            box.add_widget(lbl(T('emprestimos_ativos'), sz=13, cor=UI_DIM, h=dp(26)))
            for e in jogo.emprestimos_ativos:
                c2 = card(h=dp(44), bg=UI_CARD2)
                c2.add_widget(lbl(
                    f"  {e['nome']}  —  {e['semanas_restantes']} parcelas restantes",
                    sz=13, cor=UI_TEXT, h=dp(26)))
                box.add_widget(c2)
            box.add_widget(sep())

        # ── Aviso de bloqueio ─────────────────────────────────────────────────
        tem_emprestimo = len(jogo.emprestimos_ativos) >= 1
        if tem_emprestimo:
            aviso = card(h=dp(60), bg=UI_RED_BG)
            aviso.add_widget(lbl(T('emprestimo_ativo'),
                                  sz=14, cor=UI_RED, bold=True,
                                  halign='center', h=dp(28)))
            aviso.add_widget(lbl(T('quite_atual'),
                                  sz=12, cor=UI_DIM, halign='center', h=dp(22)))
            box.add_widget(aviso)
            box.add_widget(sep())

        # ── Opções de empréstimo ───────────────────────────────────────────────
        box.add_widget(lbl(T('solicitar_emprestimo'), sz=15, cor=UI_TEXT,
                            bold=True, h=dp(30)))

        for op in OPCOES_EMPRESTIMO:
            pode = not tem_emprestimo
            bg_card = UI_CARD if pode else (0.10, 0.10, 0.14, 1)

            c3 = BoxLayout(size_hint_y=None, height=dp(76),
                           padding=dp(12), spacing=dp(10))
            _rounded_bg(c3, bg_card)

            info = BoxLayout(orientation='vertical')
            info.add_widget(lbl(f'{op["valor"]:,} {T("item_ouro")}',
                                 sz=20,
                                 cor=UI_GOLD if pode else UI_DIM,
                                 bold=True, h=dp(32)))
            info.add_widget(lbl(f'10x {op["parcela"]} {T("item_ouro")}  •  {op["juros_pct"]}% {T("juros_label")}',
                                 sz=12, cor=UI_DIM, h=dp(22)))
            c3.add_widget(info)

            if pode:
                c3.add_widget(btn_primary(f'💰 {T("pegar_emprestimo")}',
                    cb=lambda _, o=op: self._pegar(o, jogo), h=dp(50)))
            else:
                bloq = Button(text=T('bloqueado'),
                              background_normal='',
                              background_color=(0.18, 0.18, 0.24, 1),
                              color=UI_DIM, font_size=dp(13),
                              size_hint_y=None, height=dp(50))
                c3.add_widget(bloq)

            box.add_widget(c3)

        # ── Ver Anúncio ───────────────────────────────────────────────────────
        box.add_widget(sep())
        box.add_widget(lbl(T('ver_anuncio_gratis'),sz=15,cor=UI_GOLD,bold=True,h=dp(30)))
        try:
            from config import ADMOB_MAX_POR_SEMANA as _ADMOB_MAX
        except Exception:
            _ADMOB_MAX = 3
        _adv=jogo.admob_vistos_semana; _adm=_ADMOB_MAX; _adr=_adm-_adv
        _adc=BoxLayout(size_hint_y=None,height=dp(80),padding=(dp(12),dp(8)),spacing=dp(10))
        _rounded_bg(_adc,UI_GOLD_BG if _adr>0 else (0.10,0.10,0.14,1))
        _adi=BoxLayout(orientation='vertical',spacing=dp(2))
        _adi.add_widget(lbl(T('ouro_por_ad'),sz=18,
                             cor=UI_GOLD if _adr>0 else UI_DIM,bold=True,h=dp(28)))
        _adi.add_widget(lbl(f'{_adv}/{_adm} vistos  •  {_adr} restantes',
                             sz=12,cor=UI_DIM,h=dp(20)))
        _adc.add_widget(_adi)
        def _ver_ad_banco(*_):
            try:
                def _resultado_banco(ganhou, _jogo=jogo, _screen=self):
                    try:
                        if ganhou:
                            ok,msg,_ = _jogo.registrar_anuncio_visto()
                        else:
                            ok,msg = False,'Anuncio nao disponivel no momento.'
                        _screen.on_enter()
                        from kivy.uix.popup import Popup; from kivy.uix.label import Label as _BL
                        Popup(title='Recompensa!' if ok else 'Ops',
                              content=_BL(text=msg,halign='center',color=UI_GOLD if ok else UI_RED),
                              size_hint=(0.75,0.28)).open()
                    except Exception as _e:
                        print(f'[AdMob] Erro resultado banco: {_e}')
                if _admob and _admob.anuncio_disponivel():
                    _admob.exibir_anuncio(_resultado_banco)
                elif _admob:
                    from kivy.uix.popup import Popup; from kivy.uix.label import Label as _BL
                    Popup(title='Aguarde',
                          content=_BL(text='Carregando anuncio... Tente em alguns segundos!',
                                      halign='center',color=UI_GOLD),
                          size_hint=(0.75,0.28)).open()
                else:
                    _resultado_banco(True)
            except Exception as _e:
                print(f'[AdMob] Erro ver_ad_banco: {_e}')
        if _adr>0:
            _btn_ad = Button(text=f'🎰 {T("ver_ad")}',
                             background_normal='', background_color=UI_GOLD,
                             color=(0.04,0.04,0.04,1), font_size=dp(16), bold=True,
                             size_hint_y=None, height=dp(58))
            _btn_ad.bind(on_release=_ver_ad_banco)
            _adc.add_widget(_btn_ad)
        else:
            _adc.add_widget(Button(text=T('amanha'),background_normal='',
                                   background_color=(0.18,0.18,0.24,1),
                                   color=UI_DIM,font_size=dp(13),
                                   size_hint_y=None,height=dp(58)))
        box.add_widget(_adc)

        # ── Informativo ────────────────────────────────────────────────────────
        box.add_widget(spacer(6))
        info_card = card(h=dp(44), bg=UI_CARD3)
        info_card.add_widget(lbl(
            'Max: 1 emprestimo ativo  |  Teto: 10.000 Ouro',
            sz=12, cor=UI_DIM, halign='center', h=dp(28)))
        box.add_widget(info_card)

        root.add_widget(btn_secondary(
            f'🔧  {T("voltar")}',
            cb=lambda *_: setattr(self.manager, 'current', 'menu')))

    def _pegar(self, op, jogo):
        jogo.tomar_emprestimo(op)
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  PATROCINADORES
# ═══════════════════════════════════════════════════════════════════════════════
class TelaPatrocinador(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('menu_patrocinador'), '🤝'))
        root.add_widget(sep())
        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(14),dp(10))

        if jogo.patrocinios_ativos:
            box.add_widget(lbl(f'✅ {T("contratos_ativos")}',sz=14,cor=UI_GREEN,bold=True,h=dp(28)))
            for p in jogo.patrocinios_ativos:
                c=card(h=dp(90),bg=UI_GREEN_BG)
                c.add_widget(lbl(f"{p['emoji']} {p['nome']}  —  {p['pagamento']} Ouro/sem",
                                  sz=16,cor=UI_GREEN,bold=True,h=dp(28)))
                st=f'🟢 {T("pagando")}' if p['ativo'] else f"⏳ {p['streak_atual']}/{p['condicao_semanas']} sem"
                c.add_widget(lbl(f"{st}  •  {p['semanas_restantes']} {T('sem_restantes')}",
                                  sz=12,cor=UI_DIM,h=dp(22)))
                c.add_widget(lbl(f"{T('cond_topo')} {p['condicao_pos']} {T('cond_seguidas')} {p['condicao_semanas']} {T('cond_semanas')}",
                                  sz=11,cor=(0.40,0.40,0.50,1),h=dp(20)))
                box.add_widget(c)
            box.add_widget(sep())

        pode_assinar = jogo.pode_assinar_patrocinio()
        usados = jogo.patrocinios_esta_temporada
        limite_card = card(h=dp(52), bg=UI_GOLD_BG if pode_assinar else UI_RED_BG)
        if pode_assinar:
            limite_card.add_widget(lbl(
                f'Patrocinios disponiveis: {MAX_PATROCINADORES_TEMPORADA - usados}/{MAX_PATROCINADORES_TEMPORADA} nesta temporada',
                sz=13,cor=UI_GOLD,halign='center',h=dp(36)))
        else:
            limite_card.add_widget(lbl(
                'Limite atingido: 1 patrocinador por temporada.',
                sz=13,cor=UI_RED,bold=True,halign='center',h=dp(36)))
        box.add_widget(limite_card); box.add_widget(sep())

        disp=jogo.contratos_disponiveis()
        if not disp:
            box.add_widget(lbl(T('contratos_assinados'),sz=14,cor=UI_DIM,halign='center'))
        else:
            box.add_widget(lbl(T('disponivel'),sz=14,cor=UI_TEXT,bold=True,h=dp(28)))
            for p in disp:
                c=card(h=dp(130),bg=UI_CARD2)
                c.add_widget(_accent_bar(c,UI_GOLD,h=3))
                c.add_widget(lbl(f"{p['emoji']} {p['nome']}",sz=17,cor=UI_GOLD,bold=True,h=dp(28)))
                c.add_widget(lbl(p['desc'],sz=12,cor=UI_DIM,h=dp(36)))
                c.add_widget(lbl(f"{p['pagamento']} {T('ouro_por_sem')} — {p['duracao']} {T('semanas')}",
                                  sz=13,cor=UI_GREEN,h=dp(22)))
                if pode_assinar:
                    c.add_widget(btn_primary(f'✅ {T("confirmar")}',cb=lambda _,pp=p: self._assinar(pp,jogo),h=dp(36)))
                else:
                    c.add_widget(lbl(T('pat_limite'),sz=11,cor=UI_RED,h=dp(28)))
                box.add_widget(c)


    def _assinar(self,t,jogo):
        if jogo.assinar_patrocinio(t):
            self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  CAMPEONATO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCampeonato(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo; cp=jogo.campeonato
        cfg=cp.cfg; cor=cfg['cor']
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(
            f"{cfg['nome']} T{jogo.temporada}  —  {cp.corrida_atual}/{cp.n_corridas} corridas",
            cfg['emoji'], cor))
        root.add_widget(sep(cor)); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(14),dp(10))

        badge=card(h=dp(60),bg=UI_CARD3)
        badge.add_widget(lbl(cfg['desc'],sz=13,cor=UI_TEXT,halign='center',h=dp(28)))
        badge.add_widget(lbl(
            f"{cfg['estrela_min']} estrela(s) minimo  |  Taxa paga: {cfg['taxa']:,} Ouro",
            sz=11,cor=UI_DIM,halign='center',h=dp(22)))
        box.add_widget(badge)

        prog_box=BoxLayout(size_hint_y=None,height=dp(44),padding=(0,dp(8)))
        pb=ProgressBar(max=cp.n_corridas,value=cp.corrida_atual)
        prog_box.add_widget(pb); box.add_widget(prog_box)
        pct=int(cp.corrida_atual/cp.n_corridas*100)
        box.add_widget(lbl(
            f'{pct}% completo  •  {cp.n_corridas-cp.corrida_atual} corridas restantes',
            sz=12,cor=UI_DIM,halign='center',h=dp(22)))
        box.add_widget(sep())

        box.add_widget(lbl(T('classif_atual'),sz=15,cor=UI_TEXT,bold=True,h=dp(28)))
        nome_jog=getattr(self.manager,'nome_jogador','Treinador')
        for rank,(nome,pts) in enumerate(cp.classificacao(),1):
            e_jog=(nome==nome_jog or (jogo.cavalos_jogador and
                   nome in [c.nome for c in jogo.cavalos_jogador]))
            bg=UI_GOLD_BG if e_jog else (UI_CARD if rank%2==0 else UI_CARD2)
            row=BoxLayout(size_hint_y=None,height=dp(40),padding=(dp(8),0))
            _rounded_bg(row,bg,6)
            med=['🥇','🥈','🥉'][rank-1] if rank<=3 else f'{rank}.'
            row.add_widget(Label(text=med,font_size=dp(16),size_hint_x=None,width=dp(30)))
            row.add_widget(Label(text=nome,font_size=dp(13),
                                  color=UI_GOLD if e_jog else UI_TEXT,halign='left'))
            row.add_widget(Label(text=f'[b]{pts} pts[/b]',markup=True,
                                  font_size=dp(15),color=UI_GOLD,
                                  size_hint_x=None,width=dp(60)))
            box.add_widget(row)
        box.add_widget(sep())

        box.add_widget(lbl(T('premiacao_final'),sz=14,cor=UI_TEXT,bold=True,h=dp(28)))
        for pos,premio in cp.premio_final.items():
            med=['🥇','🥈','🥉'][pos-1]
            box.add_widget(lbl(f'{med}  {premio:,} {T("item_ouro")}',sz=14,cor=UI_GOLD,halign='center',h=dp(26)))
        box.add_widget(sep())

        box.add_widget(lbl(T('premio_por_corrida'),sz=13,cor=UI_DIM,h=dp(24)))
        pc=cp.premio_corrida
        box.add_widget(lbl(
            f"1° {pc.get(1,0):,}Ou  |  2° {pc.get(2,0):,}Ou  |  3° {pc.get(3,0):,}Ou",
            sz=12,cor=UI_GOLD,halign='center',h=dp(22)))
        box.add_widget(sep())
        pts_txt=' • '.join([f'{p}°={v}pts' for p,v in list(CAMP_PONTOS.items())[:6]])
        box.add_widget(lbl(pts_txt,sz=12,cor=UI_DIM,halign='center',h=dp(22)))



# ═══════════════════════════════════════════════════════════════════════════════
#  PRÉ-CORRIDA
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCorrida(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo; ev=jogo.sortear_evento()
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)

        header=BoxLayout(size_hint_y=None,height=dp(60),padding=(dp(8),dp(10)),spacing=dp(8))
        _set_bg(header,UI_CARD)
        header.add_widget(Label(text=f'[b]Semana {jogo.semana}[/b]',markup=True,
                                font_size=dp(22),color=UI_GOLD))
        if jogo.em_campeonato():
            cp=jogo.campeonato; cfg=cp.cfg
            header.add_widget(Label(
                text=f"[b]{cfg['emoji']} {cfg['nome']} — Corrida {cp.corrida_atual+1}/{cp.n_corridas}[/b]",
                markup=True,font_size=dp(14),color=cfg['cor']))
        root.add_widget(header); root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(14),dp(10))

        ev_card=card(h=dp(72),bg=UI_CARD3)
        ev_card.add_widget(lbl(f'📰 {T("evento_semana")}',sz=12,cor=UI_DIM,h=dp(20)))
        ev_card.add_widget(lbl(ev['texto'],sz=16,cor=UI_TEXT,bold=True,h=dp(34)))
        box.add_widget(ev_card)

        aptos=jogo.cavalos_aptos()
        if jogo.cavalos_jogador:
            if jogo.em_campeonato() and jogo.campeonato.cavalos_ids:
                cav_vez = jogo.campeonato.cavalo_da_vez(jogo.cavalos_jogador)
                lineup  = jogo.campeonato.lineup_nomes(jogo.cavalos_jogador)
            else:
                cav_vez = aptos[0] if aptos else None
                lineup  = []

            if cav_vez:
                cat = estrelas(cav_vez.vel_base)
                premios_cat = PREMIO_CORRIDA_ESTRELA.get(cat,{1:300,2:150,3:80})
                h_info = dp(100) if lineup else dp(80)
                c_info=card(h=h_info,bg=UI_CARD)
                c_info.add_widget(lbl(f'{T("correndo_agora")} {cav_vez.nome}  [{cav_vez.raca}]',
                                      sz=15,cor=UI_GOLD,bold=True,h=dp(28)))
                c_info.add_widget(lbl(f'{cat} estrela(s)  |  Vel {cav_vez.vel_base:.2f}  |  {cav_vez.status_idade(jogo.semana)}',
                                      sz=12,cor=UI_TEXT,h=dp(22)))
                if lineup:
                    lineup_str = ' → '.join(lineup)
                    c_info.add_widget(lbl(f'{T("escala")} {lineup_str}',sz=10,cor=UI_DIM,h=dp(18)))
                c_info.add_widget(lbl(f'{T("premios")} 1 {premios_cat.get(1,0):,}Ou  2 {premios_cat.get(2,0):,}Ou  3 {premios_cat.get(3,0):,}Ou',
                                      sz=11,cor=UI_DIM,h=dp(20)))
                box.add_widget(c_info)
            else:
                box.add_widget(card(h=dp(52),bg=UI_RED_BG))
                box.children[0].add_widget(
                    lbl(T('nenhum_apto'),sz=14,cor=UI_RED,halign='center',h=dp(36)))

        if jogo.cavalo_apostado:
            a_card=card(h=dp(48),bg=UI_GREEN_BG)
            a_card.add_widget(lbl(f'💰 {T("aposta_atual")} {jogo.valor_aposta} {T("item_ouro")} — {jogo.cavalo_apostado.nome}',
                                   sz=14,cor=UI_GREEN,h=dp(30)))
            box.add_widget(a_card)

        box.add_widget(spacer(12))
        b=_ebtn('🏁  CORRIDA!', bg=UI_GOLD, fg=(0.04,0.04,0.04,1),
                font_size=dp(22), height=dp(66), cb=self._iniciar)
        box.add_widget(b)
        box.add_widget(btn_secondary(f'🔧  {T("ir_menu")}',cb=lambda *_: setattr(self.manager,'current','menu')))

    def _iniciar(self,*_):
        _snd.init_sons()
        _snd.tocar('largada')
        try: self.manager.remove_widget(self.manager.get_screen('corrida_visual'))
        except: pass
        cv=TelaCorridaVisual(self.manager.jogo,self._fim,name='corrida_visual')
        self.manager.add_widget(cv); self.manager.current='corrida_visual'

    def _fim(self): self.manager.current='menu'


# ═══════════════════════════════════════════════════════════════════════════════
#  DRAW HORSE
# ═══════════════════════════════════════════════════════════════════════════════
def draw_horse(x,y,cor,crina,frame,scale=1.0):
    s=scale
    Color(0,0,0,0.18); Ellipse(pos=(x+8*s,y-5*s),size=(68*s,9*s))
    Color(*cor)
    Ellipse(pos=(x+4*s,y+10*s),size=(66*s,32*s))
    Ellipse(pos=(x,    y+20*s),size=(28*s,24*s))
    Ellipse(pos=(x+54*s,y+14*s),size=(22*s,28*s))
    Ellipse(pos=(x+60*s,y+26*s),size=(17*s,26*s))
    Ellipse(pos=(x+63*s,y+38*s),size=(25*s,20*s))
    Ellipse(pos=(x+80*s,y+36*s),size=(13*s,10*s))
    Color(cor[0]*.45,cor[1]*.45,cor[2]*.45,1)
    Ellipse(pos=(x+90*s,y+38*s),size=(4*s,3*s))
    Color(0.05,0.03,0.01,1); Ellipse(pos=(x+75*s,y+49*s),size=(7*s,6*s))
    Color(1,1,1,0.9);         Ellipse(pos=(x+77*s,y+51*s),size=(2*s,2*s))
    Color(*cor)
    Rectangle(pos=(x+65*s,y+55*s),size=(4*s,9*s))
    Rectangle(pos=(x+70*s,y+56*s),size=(4*s,7*s))
    Color(*crina)
    Rectangle(pos=(x+18*s,y+42*s),size=(50*s,5*s))
    Rectangle(pos=(x+58*s,y+46*s),size=(10*s,8*s))
    tdx=8*s if frame%2==0 else -4*s
    Rectangle(pos=(x+tdx,    y+26*s),size=(6*s,16*s))
    Rectangle(pos=(x+tdx-3*s,y+14*s),size=(5*s,14*s))
    Color(cor[0]*.75,cor[1]*.75,cor[2]*.75,1); lw=int(6*s)
    if frame%2==0:
        Rectangle(pos=(x+57*s,y-18*s),size=(lw,26*s))
        Rectangle(pos=(x+66*s,y+  0), size=(lw,16*s))
        Rectangle(pos=(x+11*s,y-14*s),size=(lw,22*s))
        Rectangle(pos=(x+ 2*s,y+  4*s),size=(lw,14*s))
    else:
        Rectangle(pos=(x+61*s,y- 6*s),size=(lw,16*s))
        Rectangle(pos=(x+68*s,y-14*s),size=(lw,20*s))
        Rectangle(pos=(x+15*s,y- 8*s),size=(lw,18*s))
        Rectangle(pos=(x+ 7*s,y-14*s),size=(lw,22*s))
    Color(0.10,0.06,0.02,1)
    if frame%2==0:
        Rectangle(pos=(x+57*s,y-22*s),size=(lw,5*s))
        Rectangle(pos=(x+11*s,y-18*s),size=(lw,5*s))
    else:
        Rectangle(pos=(x+68*s,y-18*s),size=(lw,5*s))
        Rectangle(pos=(x+ 7*s,y-18*s),size=(lw,5*s))


def draw_horse_lendario(x, y, cor, crina, frame, scale=1.0):
    s = scale
    Color(1.0, 0.84, 0.0, 0.12); Ellipse(pos=(x-10*s, y-8*s), size=(120*s, 88*s))
    Color(1.0, 0.90, 0.2, 0.18); Ellipse(pos=(x-5*s,  y-4*s), size=(110*s, 78*s))
    Color(1.0, 0.95, 0.4, 0.10); Ellipse(pos=(x-2*s,  y-2*s), size=(104*s, 70*s))
    draw_horse(x, y, cor, crina, frame, scale)
    Color(1.0, 0.95, 0.50, 0.35)
    for px, py in [(x+57*s, y-22*s), (x+11*s, y-18*s)]:
        Ellipse(pos=(px-2*s, py), size=(10*s, 6*s))


# ═══════════════════════════════════════════════════════════════════════════════
#  HORSE CANVAS
# ═══════════════════════════════════════════════════════════════════════════════
class HorseCanvas(Widget):
    def __init__(self, cav, **kwargs):
        super().__init__(**kwargs)
        self.cav   = cav
        self._frame = 0
        self._clk   = Clock.schedule_interval(self._tick, 0.45)
        self.bind(pos=self._redraw, size=self._redraw)

    def _tick(self, dt):
        self._frame = (self._frame + 1) % 2
        self._redraw()

    def _redraw(self, *_):
        if self.width < 10 or self.height < 10:
            return
        self.canvas.clear()
        ci = CORES.index(self.cav.cor) if self.cav.cor in CORES else 0
        sc = min(self.width * 0.006, self.height * 0.014)
        sc = max(0.8, min(sc, 2.8))
        horse_w = 100 * sc
        horse_h = 80  * sc
        hx = self.x + (self.width  - horse_w) * 0.35
        hy = self.y + (self.height - horse_h) * 0.45
        with self.canvas:
            Color(0.14, 0.22, 0.40, 1)
            Rectangle(pos=(self.x, self.y + self.height * 0.40),
                      size=(self.width, self.height * 0.60))
            Color(0.18, 0.48, 0.22, 1)
            Rectangle(pos=(self.x, self.y),
                      size=(self.width, self.height * 0.42))
            Color(0, 0, 0, 0.22)
            Ellipse(pos=(hx + 8*sc, hy - 4*sc), size=(68*sc, 8*sc))
            if getattr(self.cav, 'lendario', False):
                draw_horse_lendario(hx, hy, self.cav.cor, CORES_CRINA[ci], self._frame, scale=sc)
            else:
                draw_horse(hx, hy, self.cav.cor, CORES_CRINA[ci], self._frame, scale=sc)

    def stop(self):
        if self._clk:
            Clock.unschedule(self._clk)
            self._clk = None


# ═══════════════════════════════════════════════════════════════════════════════
#  CORRIDA VISUAL
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCorridaVisual(Screen):
    def __init__(self,jogo,on_fim,**kwargs):
        super().__init__(**kwargs)
        self.jogo=jogo; self.on_fim=on_fim
        self.tempo=0.0; self.duracao=15.0
        self.frame_anim=0; self.frame_timer=0.0
        self.cloud_off=0.0; self.fence_off=0.0
        self.dust=[]; self.encerrada=False
        self._clk=None; self._nlabels=[]
        self._galope_tocando=False
        self._nome_textures={}
        self._ordem_chegada=[]
        ev=jogo.evento_atual
        self.clima='chuva' if (ev and ev.get('tipo')=='vel_global' and ev.get('valor',0)<0) else 'sol'
        self.tipo_pista=random.choice(['terra','grama'])
        self.rain_drops=[]
        self._preparar()

    def _preparar(self):
        jogo=self.jogo
        pool=list(jogo.cavalos_mercado)

        if jogo.em_campeonato() and jogo.campeonato.cavalos_ids:
            cav_vez = jogo.campeonato.cavalo_da_vez(jogo.cavalos_jogador)
            partic  = [cav_vez] if cav_vez else []
        else:
            aptos = jogo.cavalos_aptos()
            partic = aptos[:1]

        if jogo.em_campeonato():
            cat_estrela = jogo.campeonato.estrela_min
        elif partic:
            cat_estrela = estrelas(partic[0].vel_base)
        else:
            cat_estrela = 1
        self.cat_estrela = cat_estrela

        from config import ESTRELAS_VEL
        tier = next((t for t in ESTRELAS_VEL if t[0]==cat_estrela),(3,2.1,3.0))
        vmin_tier, vmax_tier = tier[1], tier[2]

        if jogo.em_campeonato():
            cp=jogo.campeonato
            for npc_nome in cp.npc_nomes[:4]:
                npc_vel = random.uniform(vmin_tier, vmax_tier)
                nc=criar_cavalo(npc_nome,'Puro Sangue Inglês',semana_nasc=-40,
                                vel_base=npc_vel, stamina=random.randint(60,90))
                nc.nome=npc_nome
                partic.append(nc)
        else:
            pool_filtrado=[c for c in pool if estrelas(c.vel_base)==cat_estrela]
            if not pool_filtrado:
                for i in range(min(5-len(partic),4)):
                    nome_npc=random.choice(['Rival','Campeao','Veloz','Fugaz','Agil'])+f'#{i+1}'
                    nc=criar_cavalo(nome_npc,'Mestico',semana_nasc=-40,
                                    vel_base=random.uniform(vmin_tier,vmax_tier))
                    partic.append(nc)
            else:
                partic+=random.sample(pool_filtrado,min(5-len(partic),len(pool_filtrado)))
                while len(partic)<5:
                    nome_npc=random.choice(['Rival','Campeao','Veloz','Fugaz','Agil','Brilho'])+f'#{len(partic)}'
                    nc=criar_cavalo(nome_npc,'Mestico',semana_nasc=-40,
                                    vel_base=random.uniform(vmin_tier,vmax_tier))
                    partic.append(nc)

        self.partic=partic
        self.pos_x=[20.0]*len(partic); self.dist=[0.0]*len(partic)
        self.elim=[]; self._ordem_chegada=[]; self.largura=Window.width*0.82

    def on_enter(self):
        _snd.init_sons()
        _snd.tocar_loop('galope')
        self._galope_tocando=True
        self._clk=Clock.schedule_interval(self._update,1/60)

    def on_leave(self):
        self._parar()
        try: _snd.parar_tudo()
        except Exception: pass

    def _popup_resumo_semana(self):
        r = getattr(self, '_resumo_semana', None)
        if not r: return
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout as _BL

        receitas = r['premio'] + r['ganho_pat'] + r['ganho_ap']
        despesas = r['pago_emp'] + r['custo_func'] + r['custo_mant']
        saldo_liq = receitas - despesas
        cor_liq = UI_GREEN if saldo_liq >= 0 else UI_RED

        box = _BL(orientation='vertical', padding=dp(16), spacing=dp(8))
        _set_bg(box, (0.06, 0.06, 0.12, 1))

        def _linha(txt, val, cor=UI_TEXT, bold=False):
            row = _BL(size_hint_y=None, height=dp(28))
            row.add_widget(lbl(txt, sz=13, cor=cor if not bold else UI_GOLD, h=dp(28)))
            sinal = '+' if val >= 0 else ''
            row.add_widget(lbl(f'{sinal}{val:,} Ouro', sz=13,
                               cor=UI_GREEN if val > 0 else (UI_RED if val < 0 else UI_DIM),
                               h=dp(28), halign='right'))
            return row

        box.add_widget(lbl(f'📅 {T("sem_label")} {r["semana"]} — {T("balanco_label")}', sz=15,
                           cor=UI_GOLD, bold=True, h=dp(32)))

        # Receitas
        box.add_widget(lbl(f'── {T("receitas_label")} ──', sz=11, cor=UI_DIM, h=dp(22)))
        if r['premio']:    box.add_widget(_linha(f'🏁 {T("premio_corrida_label")}', r['premio'], UI_GREEN))
        if r['ganho_ap']:  box.add_widget(_linha(f'🎰 {T("aposta_label")}', r['ganho_ap'], UI_GREEN))
        if r['ganho_pat']: box.add_widget(_linha(f'🤝 {T("menu_patrocinador")}', r['ganho_pat'], UI_GREEN))
        if not any([r['premio'], r['ganho_ap'], r['ganho_pat']]):
            box.add_widget(lbl(T('nenhuma_receita'), sz=12, cor=UI_DIM, h=dp(22)))

        # Despesas
        box.add_widget(lbl(f'── {T("despesas_label")} ──', sz=11, cor=UI_DIM, h=dp(22)))
        if r['custo_mant']:  box.add_widget(_linha(f'🐎 {T("manutencao_label")}', -r['custo_mant'], UI_RED))
        if r['custo_func']:  box.add_widget(_linha(f'👔 {T("func_label")}', -r['custo_func'], UI_RED))
        if r['pago_emp']:    box.add_widget(_linha(f'🏦 {T("parcela_emp_label")}', -r['pago_emp'], UI_RED))

        # Separador
        box.add_widget(sep())

        # Líquido
        row_liq = _BL(size_hint_y=None, height=dp(32))
        row_liq.add_widget(lbl(T('resultado_liquido'), sz=14, cor=UI_TEXT, bold=True, h=dp(32)))
        sinal = '+' if saldo_liq >= 0 else ''
        row_liq.add_widget(lbl(f'{sinal}{saldo_liq:,} Ouro', sz=14,
                               cor=cor_liq, bold=True, h=dp(32), halign='right'))
        box.add_widget(row_liq)

        # Saldo final
        box.add_widget(lbl(f'💰 {T("saldo_ouro")} {r["saldo_depois"]:,} {T("item_ouro")}',
                           sz=13, cor=UI_GOLD, h=dp(26)))

        if r['leilao_novo']:
            box.add_widget(lbl(f'🔨 {T("leilao_aberto_notif")}',
                               sz=13, cor=UI_GOLD, bold=True, h=dp(26)))

        popup = Popup(title='Resumo Financeiro', content=box,
                      size_hint=(0.88, None),
                      height=dp(min(520, 160 + 28*8)))
        popup.open()
        self._resumo_semana = None  # limpar após mostrar

    def _parar(self):
        if self._clk: Clock.unschedule(self._clk); self._clk=None
        if self._galope_tocando:
            _snd.parar('galope'); self._galope_tocando=False
        _snd.parar('fim_corrida')
        _snd.parar('vitoria')

    def _ceu(self,W,H,ty):
        if self.clima=='chuva':
            paleta=[(0.20,0.20,0.26,1),(0.25,0.25,0.31,1),(0.30,0.30,0.36,1),(0.35,0.35,0.41,1)]
        else:
            paleta=[(0.25,0.45,0.80,1),(0.33,0.55,0.88,1),(0.42,0.65,0.95,1),(0.52,0.74,1.00,1)]
        for i,c in enumerate(paleta):
            sh=(H-ty)/4; Color(*c); Rectangle(pos=(0,ty+i*sh),size=(W,sh+2))

    def _sol(self,W,H,ty):
        if self.clima=='chuva': return
        cx,cy=W*.88,ty+(H-ty)*.80
        Color(1,.95,.60,.20); Ellipse(pos=(cx-38,cy-38),size=(76,76))
        Color(1,.90,.30,.50); Ellipse(pos=(cx-24,cy-24),size=(48,48))
        Color(1,.97,.65,1);   Ellipse(pos=(cx-15,cy-15),size=(30,30))

    def _chuva_draw(self,W,H,ty):
        if self.clima!='chuva': return
        for _ in range(7):
            self.rain_drops.append([random.uniform(0,W),random.uniform(ty*0.5,H),random.uniform(10,20)])
        Color(0.60,0.72,0.92,0.50)
        for d in self.rain_drops:
            Rectangle(pos=(d[0],d[1]),size=(2,d[2]))
        self.rain_drops=[[x-2,y-d-5,d] for x,y,d in self.rain_drops if y>ty-30]

    def _nuvens_chuva(self,W,H,ty,off):
        Color(0.28,0.28,0.34,.96)
        for fx,fy in [(0.05,.92),(0.30,.85),(0.58,.93),(0.80,.87)]:
            cx=(fx*W+off*0.25)%(W+160)-80; cy=ty+(H-ty)*fy*.42
            Ellipse(pos=(cx,cy),size=(130,36))
            Ellipse(pos=(cx+42,cy+12),size=(100,28))
            Ellipse(pos=(cx-18,cy+7),size=(80,22))

    def _montanhas(self,W,ty):
        for r,g,b,a,xb,w,h in [
            (0.30,0.48,0.35,.80, 0,     W*.40, 68),
            (0.25,0.42,0.30,.80, W*.25, W*.50, 85),
            (0.35,0.52,0.40,.70, W*.58, W*.22, 55),
        ]:
            Color(r,g,b,a)
            Ellipse(pos=(xb,ty-8),      size=(w,18))
            Ellipse(pos=(xb+w*.08,ty),  size=(w*.84,h))

    def _nuvens(self,W,H,ty,off):
        if self.clima=='chuva': self._nuvens_chuva(W,H,ty,off); return
        Color(1,1,1,.85)
        for fx,fy in [(0.10,.85),(0.35,.78),(0.60,.88),(0.82,.80)]:
            cx=(fx*W+off)%(W+140)-70; cy=ty+(H-ty)*fy*.44
            Ellipse(pos=(cx,    cy),    size=(96,30))
            Ellipse(pos=(cx+30, cy+12), size=(74,24))
            Ellipse(pos=(cx-20, cy+7),  size=(60,20))

    def _tribuna(self,W,ty):
        Color(0.16,0.14,0.12,.95); Rectangle(pos=(0,ty-4),size=(W,16))
        Color(0.22,0.20,0.18,.95); Rectangle(pos=(0,ty+10),size=(W,8))
        cols=[(0.85,.28,.28),(0.28,.68,.44),(0.28,.38,.80),(0.80,.74,.22),
              (0.70,.44,.24),(0.50,.48,.75),(0.90,.50,.20)]
        heads=[(40,6),(85,11),(140,5),(205,9),(270,7),(335,10),
               (410,4),(485,8),(555,11),(625,5),(705,9),(775,4),(850,10),(920,6)]
        for ci,(hx,hh) in enumerate(heads):
            if hx<W:
                Color(*cols[ci%len(cols)],.92); Ellipse(pos=(hx,ty+hh),size=(15,15))

    def _pista(self,W,ty,n):
        lh=ty/n
        if self.tipo_pista=='grama':
            if self.clima=='chuva': c1,c2=(.16,.38,.12,1),(.12,.32,.09,1)
            else:                   c1,c2=(.24,.58,.18,1),(.19,.50,.14,1)
        else:
            if self.clima=='chuva': c1,c2=(.48,.36,.22,1),(.53,.40,.26,1)
            else:                   c1,c2=(.68,.52,.34,1),(.74,.58,.38,1)
        for i in range(n):
            Color(*(c1 if i%2==0 else c2)); Rectangle(pos=(0,i*lh),size=(W,lh))
        if self.tipo_pista=='grama':
            Color(1,1,1,0.05)
            for i in range(n): Rectangle(pos=(0,i*lh+lh*.3),size=(W,lh*.35))
        Color(1,1,1,.22)
        for i in range(n+1): Rectangle(pos=(0,i*lh-1),size=(W,2))

    def _cerca(self,W,ty,off,n):
        ps=68; Color(.96,.94,.88,1)
        for px in range(-ps,int(W)+ps,ps):
            ax=(px+int(off))%(W+ps)-ps//2
            Rectangle(pos=(ax,   ty-30),size=(5,32))
            Rectangle(pos=(ax,   -2),   size=(5,20))
            if ax+ps<=W+ps:
                Rectangle(pos=(ax+3,ty-16),size=(ps,3))
                Rectangle(pos=(ax+3,ty-26),size=(ps,2))

    def _chegada(self,ty):
        fx=self.largura; sq=11
        for r in range(int(ty/sq)+1):
            for col in range(3):
                Color(1,1,1,1) if (r+col)%2==0 else Color(.05,.05,.05,1)
                Rectangle(pos=(fx+col*sq,r*sq),size=(sq,sq))
        Color(0.75,0.65,0.10,1); Rectangle(pos=(fx+16,ty+6), size=(5,62))
        Color(1,1,0,1)
        Rectangle(pos=(fx+21,ty+42),size=(30,10))
        Rectangle(pos=(fx+21,ty+30),size=(22,10))

    def _poeira(self):
        if self.clima=='chuva':
            for p in self.dust:
                Color(.42,.30,.16,p[2]*.7); Ellipse(pos=(p[0]-4,p[1]-4),size=(11+(1-p[2])*10,6))
        else:
            for p in self.dust:
                Color(.80,.65,.45,p[2]); Ellipse(pos=(p[0]-4,p[1]-4),size=(9+(1-p[2])*14,7))

    def _cavalos_draw(self,ty,n):
        lh=ty/n
        for i,cav in enumerate(self.partic):
            if i in self.elim: continue
            ci=CORES.index(cav.cor) if cav.cor in CORES else 0
            # y mínimo de dp(22) garante que as pernas do cavalo não saiam da tela
            _hy = max(dp(22), i*lh + lh*0.14)
            if getattr(cav,'lendario',False):
                draw_horse_lendario(self.pos_x[i],_hy,cav.cor,CORES_CRINA[ci],self.frame_anim,scale=0.68)
            else:
                draw_horse(self.pos_x[i],_hy,cav.cor,CORES_CRINA[ci],self.frame_anim,scale=0.68)

    def _nomes_draw(self,ty,n):
        from kivy.core.text import Label as CoreLabel
        from kivy.core.image import Image as CoreImage
        lh=ty/n
        for i,cav in enumerate(self.partic):
            if i in self.elim: continue
            key=id(cav)
            if key not in self._nome_textures:
                cl=CoreLabel(text=cav.nome, font_size=int(dp(12)), bold=True)
                cl.refresh()
                self._nome_textures[key]=cl.texture
            if key not in getattr(self,'_emoji_textures',{}):
                if not hasattr(self,'_emoji_textures'): self._emoji_textures={}
                rd=RACAS.get(cav.raca,{})
                emoji_char=rd.get('emoji','🐴')
                try:
                    from emoji_img import emoji_path as _ep
                    ep=_ep(emoji_char)
                    self._emoji_textures[key]=CoreImage(ep).texture if ep else None
                except Exception:
                    self._emoji_textures[key]=None
            tex=self._nome_textures.get(key)
            etex=self._emoji_textures.get(key)
            if not tex: continue
            nx=max(4, self.pos_x[i]+4)
            ny=max(dp(22), i*lh + lh*0.14) + dp(28)  # alinhado com o cavalo
            esz=int(dp(14))
            gap=4
            total_w=(esz+gap if etex else 0)+tex.width+8
            th=max(tex.height+4, esz+4)
            Color(0.0, 0.0, 0.0, 0.72)
            Rectangle(pos=(nx-4, ny-2), size=(total_w, th))
            Color(*cav.cor, 0.90)
            Rectangle(pos=(nx-4, ny-2), size=(3, th))
            cx=nx
            if etex:
                Color(1,1,1,1)
                Rectangle(pos=(cx, ny), size=(esz,esz), texture=etex)
                cx+=esz+gap
            Color(1, 1, 1, 1)
            Rectangle(pos=(cx, ny), size=tex.size, texture=tex)

    def _hud(self,W,H,jogo):
        Color(0.03,0.03,0.07,.94); Rectangle(pos=(0,H-dp(44)),size=(W,dp(44)))
        prog=min(1.0,self.tempo/self.duracao)
        Color(.15,.15,.22,1); Rectangle(pos=(0,H-dp(6)),size=(W,dp(6)))
        if prog<0.5:
            pr,pg,pb=0.10+(prog*2)*0.80,0.80,0.20
        else:
            pr,pg,pb=0.90,0.80-(prog-0.5)*2*0.60,0.10
        Color(pr,pg,pb,1); Rectangle(pos=(0,H-dp(6)),size=(W*prog,dp(6)))

    def _draw(self):
        W,H=Window.width,Window.height; ty=H*.48; n=len(self.partic)
        jogo=self.jogo
        self.canvas.clear()
        with self.canvas:
            self._ceu(W,H,ty); self._sol(W,H,ty); self._montanhas(W,ty)
            self._nuvens(W,H,ty,self.cloud_off); self._tribuna(W,ty)
            self._pista(W,ty,n); self._cerca(W,ty,self.fence_off,n)
            self._chegada(ty); self._chuva_draw(W,H,ty)
            self._poeira(); self._cavalos_draw(ty,n)
            self._nomes_draw(ty,n); self._hud(W,H,jogo)

    def _update(self,dt):
        if self.encerrada: return
        self.frame_timer+=dt
        if self.frame_timer>=0.13: self.frame_anim=(self.frame_anim+1)%2; self.frame_timer=0.0
        self.cloud_off+=dt*14; self.fence_off=(self.fence_off+dt*55)%68

        jogo=self.jogo; lh=(Window.height*.48)/max(1,len(self.partic))
        for i in range(len(self.partic)):
            if i not in self.elim: self.dust.append([self.pos_x[i]-5,i*lh+10,0.55])
        self.dust=[[p[0]-1,p[1]+random.uniform(-1,1),p[2]-.04] for p in self.dust if p[2]>0]

        self.tempo+=dt
        bt=jogo.bonus_treinador(); bta=jogo.bonus_tratador(); bn=jogo.bonus_nutri()
        for i,cav in enumerate(self.partic):
            if i in self.elim: continue
            isp=cav in jogo.cavalos_jogador
            vel=cav.vel_efetiva(bt if isp else 0,bta if isp else 0,
                                bn if isp else 0,jogo.semana)
            vel+=jogo.fator_vel_evento
            _ruido=random.uniform(-.4,.4)*jogo.fator_aleatorio
            dx=max(0.5,vel+_ruido)*dt*38   # pixels/s independente de fps
            self.pos_x[i]+=dx
            if i not in self.elim:
                self.dist[i]=self.pos_x[i]
            cav.energia=max(0,cav.energia-.02)
            if self.pos_x[i]>=self.largura:
                self.pos_x[i]=self.largura
                if i not in self.elim:
                    self.elim.append(i)
                    self._ordem_chegada.append(i)

        fim=(self.tempo>=self.duracao or len(self.elim)==len(self.partic))
        if fim:
            self.encerrada=True; self._parar(); self._draw()
            Clock.schedule_once(self._calcular_e_mostrar,0.1)
            return

        self._draw()

    def _calcular_e_mostrar(self,*_):
        jogo=self.jogo
        if self._galope_tocando:
            _snd.parar('galope'); self._galope_tocando=False

        nao_chegaram=[i for i in range(len(self.partic)) if i not in self._ordem_chegada]
        nao_chegaram_sorted=sorted(nao_chegaram, key=lambda i: self.dist[i], reverse=True)
        cls_idx = self._ordem_chegada + nao_chegaram_sorted

        linhas=[]; pos_jogador=len(self.partic)+1
        nomes_classificados=[]
        for rank,idx in enumerate(cls_idx,1):
            cav=self.partic[idx]
            med=MEDALHAS[rank-1] if rank<=4 else '  '
            cor_l=([UI_GOLD,(0.78,0.78,0.78,1),(0.82,0.52,0.20,1)][rank-1]
                   if rank<=3 else UI_TEXT)
            _en_str = f'  ⚡{cav.energia:.0f}' if cav in jogo.cavalos_jogador else ''
            linhas.append((f'{med} {rank}°  {cav.nome}  [{cav.raca}]{_en_str}',cor_l))
            nomes_classificados.append(cav.nome)
            atualizar_preco_pos_corrida(cav, rank)
            cav.registrar_vitoria(jogo.semana,rank)
            if cav in jogo.cavalos_jogador:
                _gasto = random.randint(ENERGIA_GASTO_MIN, ENERGIA_GASTO_MAX)
                cav.energia = max(0, cav.energia - _gasto)
            else:
                cav.energia = max(0, cav.energia - random.randint(30,50))
            if cav in jogo.cavalos_jogador: pos_jogador=rank

        cat = getattr(self, 'cat_estrela', 3)
        premios_cat = PREMIO_CORRIDA_ESTRELA.get(cat, {1:300,2:150,3:80})
        premio=0
        for rank,idx in enumerate(cls_idx,1):
            if self.partic[idx] in jogo.cavalos_jogador:
                if jogo.em_campeonato():
                    premio = jogo.campeonato.premio_corrida.get(rank, 0)
                else:
                    premio = premios_cat.get(rank, 0)
                premio=int(premio*jogo.fator_premio)
                jogo.dinheiro+=premio
                if premio>0: _snd.tocar('moeda')
                break

        class _W:
            def __init__(self,c): self.cavalo=c
        ganho_ap=jogo.resolver_aposta([_W(self.partic[i]) for i in cls_idx])
        if ganho_ap>0: _snd.tocar('moeda')
        ganho_pat=jogo.processar_patrocinios(pos_jogador)
        # Notificação se algum patrocínio expirou ou começou a pagar
        for _p in jogo.patrocinios_ativos:
            if _p.get('semanas_restantes',1)==0:
                _notif.notif_patrocinio_expirou(_p['nome'])
            elif _p.get('ativo') and _p.get('streak_atual',0)==_p.get('condicao_semanas',1):
                _notif.notif_patrocinio_pagando(_p['nome'],_p['pagamento'])
        pago_emp=jogo.processar_emprestimos()

        tipo_c = jogo.campeonato.tipo if jogo.em_campeonato() else 'avulsa'
        if pos_jogador<=3:
            jogo.registrar_medalha(pos_jogador, jogo.semana, tipo_c)

        if pos_jogador==1:
            _snd.tocar('vitoria')
            Clock.schedule_once(lambda *_: _snd.parar('vitoria'), 3.0)
        elif pos_jogador>3:
            _snd.tocar('fim_corrida')
            Clock.schedule_once(lambda *_: _snd.parar('fim_corrida'), 2.5)
        _rep_ganhos=0; _rep_subiu=False
        if pos_jogador==1:
            _g=jogo.ganhar_reputacao('vitoria_corrida'); _rep_ganhos+=_g[0]; _rep_subiu=_g[1]
        elif pos_jogador<=3:
            _g=jogo.ganhar_reputacao('podio_corrida'); _rep_ganhos+=_g[0]; _rep_subiu=_g[1]
        if premio>0:
            _g=jogo.ganhar_reputacao('semana_positiva'); _rep_ganhos+=_g[0]

        camp_ganhos={}; camp_pts=0; camp_fim=False; camp_premio_final=0
        nome_jog=getattr(self.manager,'nome_jogador','Treinador')
        if jogo.em_campeonato():
            cp=jogo.campeonato
            if jogo.cavalos_jogador:
                nomes_classificados_camp=[]
                for idx in cls_idx:
                    cav=self.partic[idx]
                    if cav in jogo.cavalos_jogador: nomes_classificados_camp.append(nome_jog)
                    else: nomes_classificados_camp.append(cav.nome)
                camp_ganhos=cp.registrar_corrida(nomes_classificados_camp)
                camp_pts=camp_ganhos.get(nome_jog,0)
            if cp.encerrado:
                camp_fim=True
                pos_final,camp_premio_final=cp.premio_final_jogador(nome_jog)
                jogo.dinheiro+=camp_premio_final
                _notif.notif_campeonato_encerrado(pos_final, camp_premio_final)
                if pos_final<=3:
                    jogo.registrar_trofeu_campeonato(pos_final, cp.tipo, jogo.temporada)
                    _g=jogo.ganhar_reputacao('vitoria_campeonato' if pos_final==1 else 'podio_campeonato')
                    _rep_ganhos+=_g[0]; _rep_subiu=_rep_subiu or _g[1]

        txt=' | '.join(t for t,_ in linhas)
        jogo.historico.append((jogo.semana,txt))
        # ── Avanço de semana: capturar todos os custos para resumo ─────
        _saldo_antes = jogo.dinheiro
        jogo.semana+=1
        _custo_func = jogo.cobrar_funcionarios()
        jogo.resetar_admob_semana(); jogo.recuperar_energia_semanal()
        jogo.verificar_leilao()
        custo_mant=jogo.cobrar_manutencao()
        nascidos=jogo.verificar_partos()
        jogo.aplicar_veterinario(); jogo.renovar_mercado()
        mortos=jogo.verificar_mortes()
        # Notificações push do SO
        _notif.notif_semana_avancou(jogo.semana, jogo.dinheiro)
        if jogo.leilao_ativo and jogo.leilao_lotes and jogo.leilao_semana==jogo.semana-1:
            _notif.notif_leilao_aberto(len(jogo.leilao_lotes))
        for _cav_risco in jogo.cavalos_jogador:
            if _cav_risco.saude < 25:
                _notif.notif_cavalo_risco(_cav_risco.nome); break
        # ── Guardar dados do resumo para mostrar no popup ────────────────
        self._resumo_semana = {
            'semana': jogo.semana - 1,
            'premio': premio,
            'ganho_pat': ganho_pat,
            'pago_emp': pago_emp,
            'custo_func': _custo_func,
            'custo_mant': custo_mant,
            'saldo_antes': _saldo_antes,
            'saldo_depois': jogo.dinheiro,
            'ganho_ap': ganho_ap,
            'leilao_novo': jogo.leilao_ativo and jogo.leilao_semana == jogo.semana - 1,
        }

        self.canvas.clear(); self.clear_widgets(); self._nlabels=[]
        _set_bg(self,UI_BG)

        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        # Popup de resumo financeiro da semana (aparece 0.6s após resultado)
        Clock.schedule_once(lambda *_: self._popup_resumo_semana(), 0.6)

        bg_h=UI_GOLD_BG if pos_jogador<=3 else UI_CARD
        header=BoxLayout(size_hint_y=None,height=dp(64),padding=(dp(16),dp(10)))
        _set_bg(header,bg_h)
        if pos_jogador==1: h_txt='🥇  VITÓRIA!'
        elif pos_jogador==2: h_txt='🥈  2° Lugar!'
        elif pos_jogador==3: h_txt='🥉  3° Lugar!'
        else: h_txt=f'🏁  {pos_jogador}° Lugar'
        header.add_widget(Label(text=f'[b]{h_txt}[/b]',markup=True,
                                font_size=dp(24),color=UI_GOLD if pos_jogador<=3 else UI_TEXT))
        root.add_widget(header); root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        box.padding=(dp(14),dp(10))

        box.add_widget(lbl(T('classif_final'),sz=14,cor=UI_DIM,bold=True,h=dp(26)))
        for texto,cor in linhas:
            c=card(h=dp(38),bg=UI_CARD)
            c.add_widget(lbl(texto,sz=16,cor=cor,h=dp(26)))
            box.add_widget(c)

        box.add_widget(sep())
        try:
            _nr,_cr=jogo.nivel_reputacao(); _pc,_pn,_pt=jogo.barra_reputacao()
            _prx,_cprx,_flt=jogo.proxima_reputacao()
            _rc=BoxLayout(orientation='vertical',size_hint_y=None,height=dp(70),
                          padding=(dp(10),dp(4)),spacing=dp(4))
            _rounded_bg(_rc,(0.07,0.05,0.15,1))
            _rh=BoxLayout(size_hint_y=None,height=dp(24))
            _rh.add_widget(lbl(f'{_cr["emoji"]} {_cr["nome"]}  —  {jogo.reputacao_pts} pts',
                               sz=13,cor=UI_PURPLE,bold=True,h=dp(22)))
            if _rep_ganhos>0:
                _rh.add_widget(lbl(f'+{_rep_ganhos} pts',sz=12,cor=UI_GREEN,h=dp(22)))
            _rc.add_widget(_rh)
            _rb=BoxLayout(size_hint_y=None,height=dp(10))
            _rounded_bg(_rb,(0.14,0.11,0.22,1))
            _fw=max(0.02,_pc); _rf=BoxLayout(size_hint=(_fw,1)); _rounded_bg(_rf,UI_PURPLE)
            _rb.add_widget(_rf)
            if _pc<0.99: _rb.add_widget(BoxLayout(size_hint=(1-_fw,1)))
            _rc.add_widget(_rb)
            if _rep_subiu:
                _rc.height=dp(92)
                _rc.add_widget(lbl(f'NIVEL SUBIU! {_cr["nome"]} {_cr["emoji"]}',
                                   sz=12,cor=UI_GOLD,bold=True,h=dp(22)))
            elif _prx:
                _rc.add_widget(lbl(f'Faltam {_flt} pts para {_cprx["nome"]}',sz=11,cor=UI_DIM,h=dp(18)))
            else:
                _rc.add_widget(lbl('Reputacao MAXIMA!',sz=11,cor=UI_GOLD,h=dp(18)))
            box.add_widget(_rc)
        except Exception: pass
        box.add_widget(sep())

        fin_grid=GridLayout(cols=2,size_hint_y=None,spacing=dp(6))
        fin_grid.bind(minimum_height=fin_grid.setter('height'))
        financeiro=[
            (f'Premio +{premio} Ouro',UI_GREEN_BG,UI_GREEN, premio>0),
            (f'Aposta +{ganho_ap} Ouro',UI_GREEN_BG,UI_GREEN, ganho_ap>0),
            (f'Patrocinio +{ganho_pat} Ouro',UI_GREEN_BG,UI_GREEN, ganho_pat>0),
            (f'Parcela -{pago_emp} Ouro',UI_RED_BG,UI_RED, pago_emp>0),
            (f'Manutencao -{custo_mant} Ouro',UI_RED_BG,UI_RED, custo_mant>0),
        ]
        for txt,bg,fg,show in financeiro:
            if show:
                b=Button(text=txt,background_normal='',background_color=bg,
                         color=fg,font_size=dp(13),size_hint_y=None,height=dp(38))
                fin_grid.add_widget(b)
        if fin_grid.children: box.add_widget(fin_grid)

        if jogo.em_campeonato() or camp_fim:
            box.add_widget(sep())
            _cp_ref = jogo.campeonato
            _cfg_ref = _cp_ref.cfg if _cp_ref else {}
            _cor_bg  = tuple(list(_cfg_ref.get('cor',(0.12,0.06,0.22,1)))[:3]+[0.22])
            camp_card=card(h=dp(80) if not camp_fim else dp(130), bg=_cor_bg)
            if camp_fim:
                emoji_c = _cfg_ref.get('emoji','🏆')
                nome_c  = _cfg_ref.get('nome','Competicao')
                cor_c   = _cfg_ref.get('cor',UI_PURPLE)
                camp_card.add_widget(lbl(
                    f'{emoji_c} {nome_c.upper()} T{jogo.temporada} — ENCERRADO!',
                    sz=15,cor=cor_c,bold=True,halign='center',h=dp(28)))
                if camp_premio_final>0:
                    camp_card.add_widget(lbl(f'{T("premio_final")} +{camp_premio_final:,} Ouro',
                                             sz=15,cor=UI_GOLD,halign='center',h=dp(26)))
                camp_card.add_widget(lbl(
                    'Volte ao menu para escolher a proxima competicao!',
                    sz=11,cor=UI_DIM,halign='center',h=dp(20)))
                camp_card.add_widget(lbl(
                    'Regional: qualquer | Nacional: 4🏆+ | Internacional: 5🏆',
                    sz=10,cor=UI_DIM,halign='center',h=dp(18)))
            else:
                cp2=jogo.campeonato
                cor2=cp2.cfg['cor']; emoji2=cp2.cfg['emoji']; nome2=cp2.cfg['nome']
                camp_card.add_widget(lbl(
                    f'{emoji2} {nome2} T{jogo.temporada} — Corrida {cp2.corrida_atual}/{cp2.n_corridas}',
                    sz=14,cor=cor2,bold=True,h=dp(28)))
                if camp_pts>0:
                    camp_card.add_widget(lbl(f'+{camp_pts} {T("pts_corrida")}',sz=13,cor=UI_GOLD,h=dp(24)))
                meu_pts=cp2.pontos.get(nome_jog,0)
                camp_card.add_widget(lbl(
                    f'Total: {meu_pts} pts  |  Faltam: {cp2.n_corridas-cp2.corrida_atual} corridas',
                    sz=12,cor=UI_DIM,h=dp(20)))
            box.add_widget(camp_card)

        for nm in nascidos:
            c_n=card(h=dp(44),bg=UI_GREEN_BG)
            c_n.add_widget(lbl(f'{T("nasceu")} {nm}!',sz=14,cor=UI_GREEN,bold=True,halign='center',h=dp(30)))
            box.add_widget(c_n)
        for nm in mortos:
            c_m=card(h=dp(40),bg=UI_RED_BG)
            c_m.add_widget(lbl(f'💀 {nm} morreu de velhice...',sz=13,cor=UI_RED,h=dp(26)))
            box.add_widget(c_m)

        subs = jogo.checar_substitucao_automatica()
        if subs['emergencia']:
            p = subs['emergencia']
            c_em = card(h=dp(80), bg=UI_GREEN_BG)
            c_em.add_widget(lbl(f'🐴 {T("potro_emergencia")}', sz=14, cor=UI_GREEN,
                                 bold=True, halign='center', h=dp(26)))
            c_em.add_widget(lbl(f'{T("doou_cavalo")} {p.nome} ({p.raca}) {T("ao_seu_haras")}',
                                 sz=12, cor=UI_TEXT, halign='center', h=dp(22)))
            c_em.add_widget(lbl(T('cuide_bem'),
                                 sz=11, cor=UI_DIM, halign='center', h=dp(18)))
            box.add_widget(c_em)

        if subs['alertas']:
            box.add_widget(sep())
            box.add_widget(lbl(f'⚠ {T("cavalos_risco")}', sz=13, cor=UI_ORANGE,
                                bold=True, h=dp(24)))
            for al in subs['alertas']:
                c_al = card(h=dp(48), bg=(0.14,0.08,0.02,1))
                c_al.add_widget(lbl(
                    f"⚠ {al['nome']} — {al['semanas_restantes']} semanas restantes "
                    f"(idade {al['idade']})",
                    sz=12, cor=UI_ORANGE, h=dp(22)))
                c_al.add_widget(lbl(
                    T('substituto'),
                    sz=10, cor=UI_DIM, h=dp(18)))
                box.add_widget(c_al)

        box.add_widget(sep())
        box.add_widget(lbl(f'💰 {T("saldo_ouro")} {jogo.dinheiro:,}',sz=20,cor=UI_GOLD,
                           bold=True,halign='center',h=dp(36)))
        box.add_widget(spacer(10))

        _nome_cav  = jogo.cavalos_jogador[0].nome if jogo.cavalos_jogador else 'seu cavalo'
        _nome_haras = getattr(self.manager,'nome_jogador','Treinador')
        if _rnd.random() < 0.40:
            Clock.schedule_once(
                lambda *_: _mostrar_jornal(self, pos_jogador, _nome_cav,
                                           _nome_haras, lambda: None), 1.2)

        if camp_fim:
            def _ir_menu_prox(*_):
                jogo.proxima_temporada()
                Clock.schedule_once(lambda __: self.on_fim(),0)
            btn_menu_prox=_ebtn(
                f'🏆  Escolher Proxima Competicao (T{jogo.temporada+1})',
                bg=_cfg_ref.get('cor',UI_PURPLE), fg=(0.04,0.04,0.04,1),
                font_size=dp(15), height=dp(60), cb=_ir_menu_prox)
            box.add_widget(btn_menu_prox)
            box.add_widget(spacer(6))

        btn_v=_ebtn('🏠  Voltar ao Menu', bg=UI_GOLD,
                    fg=(0.04,0.04,0.04,1), font_size=dp(18), height=dp(60),
                    cb=lambda *_: Clock.schedule_once(lambda __: self.on_fim(),0))
        box.add_widget(btn_v)


# ═══════════════════════════════════════════════════════════════════════════════
#  MEUS CAVALOS
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCavalos(Screen):
    def on_enter(self):
        for hp in getattr(self, '_previews', []): hp.stop()
        self._previews = []

        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)

        h=BoxLayout(size_hint_y=None,height=dp(64),padding=(dp(8),dp(8)),spacing=dp(8))
        _set_bg(h,UI_CARD)
        h.add_widget(lbl(f'🐎 {T("meus_cavalos")}', sz=18, cor=UI_GOLD, bold=True, h=dp(48)))
        h.add_widget(Label(text=f'[b]Baias: {jogo.baias_livres}/{jogo.baias}[/b]',
                           markup=True,font_size=dp(14),
                           color=UI_GREEN if jogo.baias_livres>0 else UI_RED))
        custo_m=jogo.custo_manutencao_semanal()
        if custo_m>0:
            h.add_widget(Label(text=f'{T("manut_label")} {custo_m} Ouro/sem',
                               font_size=dp(12),color=UI_RED,size_hint_x=None,width=dp(100)))
        h.add_widget(Label(text=f'Ouro {jogo.dinheiro:,}',font_size=dp(14),color=UI_GREEN))
        root.add_widget(h); root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        if not jogo.cavalos_jogador:
            box.add_widget(spacer(40))
            box.add_widget(lbl(T('nenhum_cavalo'),sz=16,cor=UI_DIM,halign='center'))
            box.add_widget(lbl(T('va_mercado'),sz=14,cor=UI_DIM,halign='center'))
        else:
            for cav in jogo.cavalos_jogador:
                card_w, hp = self._card(cav,jogo)
                box.add_widget(card_w)
                if hp: self._previews.append(hp)


    def on_leave(self):
        for hp in getattr(self, '_previews', []): hp.stop()
        self._previews = []

    def _card(self,cav,jogo):
        sem=jogo.semana; potro=cav.e_potro(sem)
        rd=RACAS.get(cav.raca,{})
        cat=estrelas(cav.vel_base)

        card_h = dp(170) if potro else dp(360)
        c=BoxLayout(orientation='vertical',size_hint_y=None,
                    height=card_h, padding=dp(10),spacing=dp(6))
        _rounded_bg(c,UI_CARD,12)

        bar=Widget(size_hint_y=None,height=dp(5))
        with bar.canvas:
            Color(*cav.cor); r=Rectangle(pos=bar.pos,size=bar.size)
        bar.bind(pos=lambda w,v: setattr(r,'pos',v),size=lambda w,v: setattr(r,'size',v))
        c.add_widget(bar)

        hp = None
        if not potro:
            preview_row = BoxLayout(size_hint_y=None,height=dp(160),spacing=dp(8))
            hp = HorseCanvas(cav, size_hint_x=0.55, size_hint_y=1)
            _rounded_bg(hp,(0.06,0.10,0.18,1),8)
            preview_row.add_widget(hp)

            stats_col = BoxLayout(orientation='vertical',spacing=dp(4),
                                  size_hint_x=0.45, padding=(dp(4),dp(4)))
            def stat_row(icon, val, cor):
                row=BoxLayout(size_hint_y=None,height=dp(26))
                row.add_widget(Label(text=icon,font_size=dp(13),color=UI_DIM,
                                    size_hint_x=None,width=dp(28)))
                row.add_widget(Label(text=str(val),font_size=dp(14),
                                    color=cor,bold=True,halign='left'))
                return row
            stats_col.add_widget(stat_row('Vel', f'{cav.vel_base:.2f}',UI_GOLD))
            stats_col.add_widget(stat_row('Enrg',f'{int(cav.energia)}%',
                                          UI_GREEN if cav.energia>50 else UI_RED))
            stats_col.add_widget(stat_row('Saude',f'{cav.saude}%',
                                          UI_GREEN if cav.saude>60 else UI_RED))
            stats_col.add_widget(stat_row('Stamp',f'{cav.stamina}%',UI_BLUE))
            stats_col.add_widget(stat_row('Vit.',str(cav.vitorias),UI_GOLD))
            custo_cat = CUSTO_MANUTENCAO_BASE * cat
            stats_col.add_widget(stat_row('Mant.',f'{custo_cat} Ouro/sem',UI_RED))
            preview_row.add_widget(stats_col)
            c.add_widget(preview_row)

        c.add_widget(lbl(f"{rd.get('emoji','H')} {cav.nome}",sz=17,cor=UI_GOLD,bold=True,h=dp(28)))
        sx_icon = '♂' if getattr(cav,'sexo','')=='M' else ('♀' if getattr(cav,'sexo','')=='F' else '')
        sx_cor  = (0.40,0.65,1.0,1) if getattr(cav,'sexo','')=='M' else (1.0,0.50,0.70,1) if getattr(cav,'sexo','')=='F' else UI_DIM
        c.add_widget(lbl(f'{sx_icon} {cav.raca}  |  {cat} {T("estrelas_label")}  |  {cav.status_idade(sem)}',
                          sz=12,cor=sx_cor,h=dp(20)))
        if getattr(cav,'em_gestacao',lambda:False)():
            sg=cav.semanas_gestacao(sem); pct=min(1.0,sg/8.0)
            g_row=BoxLayout(size_hint_y=None,height=dp(18),spacing=dp(6))
            g_row.add_widget(Label(text=f'{T("gestacao")} {sg}/8 {T("semanas")}',font_size=dp(10),
                                   color=(1.0,0.65,0.80,1),size_hint_x=None,width=dp(100)))
            prog=Widget(size_hint_x=1,size_hint_y=1)
            with prog.canvas:
                Color(0.15,0.10,0.12,1); RoundedRectangle(pos=prog.pos,size=prog.size,radius=[4])
                Color(1.0,0.42,0.65,1)
                prog._pct=pct
                RoundedRectangle(pos=prog.pos,size=(prog.width*pct,prog.height),radius=[4])
            prog.bind(size=lambda w,v,p=pct: w.canvas.ask_update())
            g_row.add_widget(prog)
            c.add_widget(g_row)

        c.add_widget(lbl(f'{T("val_mercado")} {cav.preco:,} {T("item_ouro")}  |  {T("rev_mercado")} {int(cav.preco*PCT_REVENDA):,} {T("item_ouro")}',
                          sz=11,cor=(0.50,0.60,0.50,1),h=dp(18)))

        if potro:
            falta=10-cav.idade(sem)
            c.add_widget(lbl(f'{T("potro_falta")} {falta} {T("semanas")}',
                              sz=13,cor=UI_BLUE,halign='center',h=dp(24)))
        else:
            hist=cav.mostrar_historico()
            c.add_widget(lbl(hist,sz=11,cor=UI_DIM,h=dp(32)))

        btns=BoxLayout(size_hint_y=None,height=dp(44),spacing=dp(8))
        btns.add_widget(btn_danger(f'💰 {T("vender")} {int(cav.preco*PCT_REVENDA):,} {T("item_ouro")}',
                                   cb=lambda *_,cv=cav: self._vender(cv,jogo)))
        if not potro:
            custo_e=max(50, PRECO_MIN_ESTRELA[cat]//20)
            btns.add_widget(btn_success(f'⚡ {T("energia")} {custo_e} {T("item_ouro")}',
                                        cb=lambda *_,cv=cav: self._energia(cv,jogo)))
            _can_train = cav.energia >= 20
            _tcor = UI_BLUE if _can_train else (0.20,0.20,0.30,1)
            if _can_train:
                _tbtn = btn_success(f'🏋 {T("treinar_btn2")}',
                                    cb=lambda *_,cv=cav: self._treinar(cv,jogo),
                                    h=dp(44))
            else:
                _tbtn = btn_secondary(f'🏋 {T("treinar_btn2")}', h=dp(44))
            btns.add_widget(_tbtn)
        c.add_widget(btns)
        return c, hp

    def _vender(self,cav,jogo):
        _snd.tocar('moeda')
        jogo.dinheiro+=int(cav.preco*PCT_REVENDA)
        jogo.cavalos_jogador.remove(cav)
        jogo.cavalos_mercado.append(cav)
        self.on_enter()

    def _energia(self,cav,jogo):
        cat=estrelas(cav.vel_base)
        custo=max(50, PRECO_MIN_ESTRELA[cat]//20)
        if jogo.dinheiro>=custo:
            cav.energia=100; jogo.dinheiro-=custo; self.on_enter()

    def _treinar(self,cav,jogo):
        if cav.energia < 20:
            return
        if jogo.dinheiro < 100:
            from kivy.uix.popup import Popup; from kivy.uix.label import Label as _PL
            Popup(title=T('sem_ouro_titulo'),
                  content=_PL(text='Precisa de 100 Ouro para treinar!',
                              halign='center',color=UI_RED),
                  size_hint=(0.7,0.25)).open(); return
        jogo.dinheiro -= 100
        cav.energia = max(0, cav.energia - 20)
        import random
        ganho = round(random.uniform(0.01, 0.05), 2)
        vmax  = RACAS.get(cav.raca, {}).get('vel_max', VEL_MAX_GLOBAL)
        antes = cav.vel_base
        cav.vel_base = round(min(vmax, cav.vel_base + ganho), 2)
        ganho_real = round(cav.vel_base - antes, 2)
        _snd.tocar('vitoria') if ganho_real >= 0.04 else _snd.tocar('moeda')
        self._treinar_popup(cav, ganho_real, antes)
        self.on_enter()

    def _treinar_popup(self, cav, ganho, vel_antes):
        from kivy.uix.popup     import Popup
        from kivy.uix.boxlayout import BoxLayout as BL
        from kivy.animation     import Animation
        import random as _rnd

        box = BL(orientation='vertical', padding=dp(12), spacing=dp(8))
        box.add_widget(Label(
            text=f'[b]🏋 Treino  —  {cav.nome}[/b]', markup=True,
            font_size=dp(15), color=UI_GOLD, size_hint_y=None, height=dp(28)))

        # ── Widget de pista igual à corrida real ─────────────────────────
        from kivy.uix.widget import Widget as _Wgt
        arena = _Wgt(size_hint_y=None, height=dp(130))
        ci = CORES.index(cav.cor) if cav.cor in CORES else 0
        crina = CORES_CRINA[ci]

        # Posições dos 3 obstáculos (fixas em % da largura)
        OBS_PCT = [0.30, 0.57, 0.82]
        OB_W, OB_H = dp(10), dp(28)   # largura e altura do obstáculo

        def _draw(frame=0):
            arena.canvas.clear()
            W, H = arena.width, arena.height
            if W <= 0: return
            px, py = arena.pos
            ty = H * 0.52   # linha do horizonte (igual à corrida)
            n  = 1          # 1 raia
            lh = ty

            with arena.canvas:
                # ── Céu ────────────────────────────────────────────────
                for i, col in enumerate([
                    (0.25,0.45,0.80,1),(0.33,0.55,0.88,1),
                    (0.42,0.65,0.95,1),(0.52,0.74,1.00,1)]):
                    sh = (H - ty) / 4
                    Color(*col)
                    Rectangle(pos=(px, py + ty + i*sh), size=(W, sh+2))
                # ── Sol ────────────────────────────────────────────────
                sx, sy = px + W*.88, py + ty + (H-ty)*.80
                Color(1,.95,.60,.20); Ellipse(pos=(sx-38,sy-38),size=(76,76))
                Color(1,.90,.30,.50); Ellipse(pos=(sx-24,sy-24),size=(48,48))
                Color(1,.97,.65,1);   Ellipse(pos=(sx-15,sy-15),size=(30,30))
                # ── Montanhas ─────────────────────────────────────────
                for r,g,b,a,xb,w,h2 in [
                    (0.30,0.48,0.35,.80,0,     W*.40,68),
                    (0.25,0.42,0.30,.80,W*.25, W*.50,85),
                    (0.35,0.52,0.40,.70,W*.58, W*.22,55)]:
                    Color(r,g,b,a)
                    Ellipse(pos=(px+xb, py+ty-8), size=(w, 18))
                    Ellipse(pos=(px+xb+w*.08, py+ty), size=(w*.84, h2))
                # ── Tribuna (torcida) ─────────────────────────────────
                Color(0.16,0.14,0.12,.95)
                Rectangle(pos=(px, py+ty-4), size=(W, 16))
                Color(0.22,0.20,0.18,.95)
                Rectangle(pos=(px, py+ty+10), size=(W, 8))
                cols_t=[(0.85,.28,.28),(0.28,.68,.44),(0.28,.38,.80),
                        (0.80,.74,.22),(0.70,.44,.24),(0.50,.48,.75)]
                for ci2, (hx,hh) in enumerate(
                        [(40,6),(85,11),(140,5),(205,9),(270,7),(335,10),
                         (410,4),(485,8),(555,11),(625,5),(705,9),(775,4)]):
                    if hx < W:
                        Color(*cols_t[ci2%len(cols_t)],.92)
                        Ellipse(pos=(px+hx, py+ty+hh), size=(15,15))
                # ── Pista (grama) ─────────────────────────────────────
                Color(.24,.58,.18,1)
                Rectangle(pos=(px, py), size=(W, ty))
                Color(.19,.50,.14,1)
                Rectangle(pos=(px, py), size=(W, ty*.5))
                Color(1,1,1,.05)
                Rectangle(pos=(px, py+ty*.30), size=(W, ty*.35))
                # ── Cerca ─────────────────────────────────────────────
                Color(.96,.94,.88,1)
                ps = 68
                fence_off = getattr(arena, '_fence_off', 0)
                for fpx in range(-ps, int(W)+ps, ps):
                    ax = (fpx + int(fence_off)) % (W+ps) - ps//2
                    Rectangle(pos=(px+ax,    py+ty-30), size=(5,32))
                    Rectangle(pos=(px+ax,    py-2),     size=(5,20))
                    if ax+ps <= W+ps:
                        Rectangle(pos=(px+ax+3, py+ty-16), size=(ps, 3))
                        Rectangle(pos=(px+ax+3, py+ty-26), size=(ps,  2))
                # ── 3 Obstáculos (barras de salto) ────────────────────
                for obs_pct in OBS_PCT:
                    ox = px + W * obs_pct
                    # Base do obstáculo
                    Color(0.80,0.25,0.05,1)
                    Rectangle(pos=(ox-OB_W/2, py+ty*.05), size=(OB_W, OB_H))
                    # Travessa horizontal
                    Color(1.0, 0.85, 0.10, 1)
                    Rectangle(pos=(ox-OB_W*1.5, py+ty*.05+OB_H*.6),
                               size=(OB_W*3, OB_H*.18))
                    # Stripes na travessa
                    Color(0.80,0.25,0.05,1)
                    Rectangle(pos=(ox-OB_W*1.5, py+ty*.05+OB_H*.6),
                               size=(OB_W*.6, OB_H*.18))
                    Rectangle(pos=(ox+OB_W*.2, py+ty*.05+OB_H*.6),
                               size=(OB_W*.6, OB_H*.18))
                # ── Cavalo ────────────────────────────────────────────
                cav_x  = getattr(arena, '_cav_x', W*0.05)
                cav_sy = getattr(arena, '_salto', 0)
                draw_horse(px + cav_x, py + ty*.08 + cav_sy,
                           cav.cor, crina, frame, scale=0.72)

        arena.bind(pos=lambda *_: _draw(getattr(arena,'_frame',0)),
                   size=lambda *_: _draw(getattr(arena,'_frame',0)))
        box.add_widget(arena)

        # ── Animação: cavalo percorre a pista e salta os 3 obstáculos ─
        arena._cav_x     = 0
        arena._salto     = 0
        arena._fence_off = 0
        arena._frame     = 0
        arena._anim_t    = 0.0
        arena._running   = True

        def _tick(dt):
            if not getattr(arena, '_running', False): return
            arena._fence_off = (arena._fence_off + dt*55) % 68
            arena._frame     = (arena._frame + 1) % 2
            _draw(arena._frame)
        _clk = Clock.schedule_interval(_tick, 0.13)

        W_ref = [None]
        def _start_anim(dt):
            W_ref[0] = arena.width or dp(300)
            W = W_ref[0]
            arena._cav_x = W * 0.04

            def _seg(x0, x1, s0, s1, dur, t='linear'):
                return Animation(_cav_x=x1, _salto=s1, duration=dur, transition=t)

            SH = dp(26)   # altura do salto
            segs = []
            for obs in OBS_PCT:
                ox = W * obs
                segs += [
                    _seg(0, ox - dp(10), 0,  0,   (ox - W*0.04)/(W*0.60+1e-6) * 1.0),
                    _seg(0, ox + dp(10), 0,  SH,  0.18, 'out_quad'),
                    _seg(0, ox + dp(30), SH, 0,   0.18, 'in_quad'),
                ]
            segs.append(_seg(0, W*1.05, 0, 0, 0.5))

            chain = segs[0]
            for s in segs[1:]: chain += s
            chain.bind(on_complete=lambda *_: _clk.cancel() or setattr(arena,'_running',False))
            chain.start(arena)

        Clock.schedule_once(_start_anim, 0.15)

        # ── Resultado ─────────────────────────────────────────────────
        box.add_widget(Label(
            text=(f'Vel  [b]{vel_antes:.2f}[/b]  →  [b]{cav.vel_base:.2f}[/b]'
                  f'  [color=00ff88](+{ganho:.2f})[/color]'),
            markup=True, font_size=dp(15), color=UI_TEXT,
            size_hint_y=None, height=dp(26)))
        box.add_widget(Label(
            text=f'Energia restante: [b]{int(cav.energia)}%[/b]  |  -20 gasta',
            markup=True, font_size=dp(12), color=UI_DIM,
            size_hint_y=None, height=dp(20)))

        def _fechar(*_):
            arena._running = False
            try: _clk.cancel()
            except Exception: pass
            pop.dismiss()

        pop = Popup(title=T('resultado_treino'),
                    content=box, size_hint=(0.92, 0.62),
                    auto_dismiss=False)
        box.add_widget(btn_primary('✅ Ok', cb=_fechar, h=dp(42)))
        pop.open()


# ═══════════════════════════════════════════════════════════════════════════════
#  MERCADO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaMercado(Screen):
    _CAT=['Cavalos','Haras','Equip.','Comida','Remedios']

    def __init__(self,**kwargs):
        super().__init__(**kwargs); self._aba=0; self._cav_idx=0

    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)

        h=BoxLayout(size_hint_y=None,height=dp(52),padding=(dp(8),dp(6)),spacing=dp(8))
        _set_bg(h,UI_CARD)
        h.add_widget(lbl('🛒 Mercado', sz=18, cor=UI_GOLD, bold=True, h=dp(40)))
        h.add_widget(Label(text=f'Ouro {jogo.dinheiro:,}',
                           font_size=dp(16),color=UI_GREEN))
        h.add_widget(lbl(f'🏠{jogo.baias_livres}/{jogo.baias}', sz=14, cor=UI_BLUE, h=dp(40)))
        root.add_widget(h); root.add_widget(sep())

        tabs=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(2))
        for i,n in enumerate(self._CAT):
            tabs.add_widget(btn_tab(n,ativo=(i==self._aba),
                                    cb=lambda _,idx=i: self._aba_tab(idx)))
        root.add_widget(tabs); root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        if   self._aba==0: self._aba_cavalos(box,jogo)
        elif self._aba==1: self._aba_haras(box,jogo)
        elif self._aba==2: self._aba_itens(box,jogo,ITENS_EQUIPAMENTO)
        elif self._aba==3: self._aba_itens(box,jogo,ITENS_COMIDA)
        else:              self._aba_itens(box,jogo,ITENS_REMEDIO)


    def _aba_tab(self,i): self._aba=i; self.on_enter()

    def _aba_haras(self,box,jogo):
        info=card(h=dp(92),bg=UI_CARD3)
        info.add_widget(lbl(T('seu_haras'),sz=16,cor=UI_BLUE,bold=True,h=dp(28)))
        info.add_widget(lbl(f'{jogo.info_haras_atual()}  —  {T("haras_nivel_sem")} {jogo.haras_nivel}',
                             sz=14,cor=UI_TEXT,h=dp(24)))
        info.add_widget(lbl(
            f'Baias: {jogo.baias_livres} livres / {jogo.baias} total  |  Cavalos: {len(jogo.cavalos_jogador)}',
            sz=12,cor=UI_DIM,h=dp(22)))
        box.add_widget(info)

        n_cols=5; grid=GridLayout(cols=n_cols,size_hint_y=None,spacing=dp(4))
        grid.bind(minimum_height=grid.setter('height'))
        for i in range(max(jogo.baias, 20)):
            desbloqueada = i < jogo.baias
            ocupada = i < len(jogo.cavalos_jogador)
            if not desbloqueada:
                bg=(0.10,0.10,0.14,1); fg=(0.25,0.25,0.30,1); txt='--'
            elif ocupada:
                bg=UI_RED_BG; fg=UI_RED; txt=jogo.cavalos_jogador[i].nome[:7]
            else:
                bg=UI_GREEN_BG; fg=UI_GREEN; txt='Livre'
            b=Button(text=txt,background_normal='',background_color=bg,
                     color=fg,font_size=dp(10),size_hint_y=None,height=dp(42))
            grid.add_widget(b)
        box.add_widget(grid)
        box.add_widget(sep())

        box.add_widget(lbl(T('comprar_haras'),sz=15,cor=UI_TEXT,bold=True,h=dp(28)))
        for tipo,cfg in HARAS_TIPOS.items():
            ja_tem = jogo.haras_nivel >= cfg['nivel']
            prox   = cfg['nivel'] == jogo.haras_nivel + 1
            pode   = prox and jogo.dinheiro >= cfg['preco']
            if ja_tem:
                bg_card = UI_GREEN_BG; cor_nome = UI_GREEN; status = '[OK] Adquirido'
            elif prox:
                bg_card = UI_CARD2; cor_nome = UI_GOLD; status = f"{cfg['preco']:,} Ouro"
            else:
                bg_card = UI_CARD; cor_nome = UI_DIM; status = 'Requer nivel anterior'

            ch = dp(100)
            c2 = BoxLayout(orientation='vertical',size_hint_y=None,height=ch,
                           padding=dp(10),spacing=dp(4))
            _rounded_bg(c2, bg_card, 8)
            c2.add_widget(lbl(cfg['nome'],sz=16,cor=cor_nome,bold=True,h=dp(26)))
            c2.add_widget(lbl(cfg['desc'],sz=11,cor=UI_DIM,h=dp(20)))
            row=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(8))
            row.add_widget(lbl(f"{cfg['baias']} baias  |  {status}",sz=12,cor=UI_TEXT,h=dp(28)))
            if not ja_tem and prox:
                bb=Button(text=T('comprar'),background_normal='',
                          background_color=UI_GOLD if pode else (0.25,0.25,0.30,1),
                          color=(0.04,0.04,0.04,1) if pode else UI_DIM,
                          font_size=dp(13),bold=pode,size_hint_y=None,height=dp(38))
                if pode:
                    bb.bind(on_release=lambda *_,t=tipo: self._comprar_haras(t,jogo))
                row.add_widget(bb)
            c2.add_widget(row)
            box.add_widget(c2)

    def _comprar_haras(self,tipo,jogo):
        ok,msg = jogo.comprar_haras(tipo)
        self.on_enter()

    def _aba_cavalos(self,box,jogo):
        if not jogo.pode_comprar_cavalo():
            warn=card(h=dp(60),bg=UI_RED_BG)
            warn.add_widget(lbl(f'⚠ {T("sem_baias")}',sz=15,cor=UI_RED,bold=True,halign='center',h=dp(28)))
            warn.add_widget(lbl(T('compre_baia'),sz=12,cor=UI_DIM,halign='center',h=dp(22)))
            box.add_widget(warn); box.add_widget(sep())

        if not jogo.cavalos_mercado:
            box.add_widget(lbl(T('mercado_vazio'),sz=15,cor=UI_DIM,halign='center')); return
        for cav in jogo.cavalos_mercado: box.add_widget(self._card_cav(cav,jogo))

    def _card_cav(self,cav,jogo):
        rd=RACAS.get(cav.raca,{})
        c=BoxLayout(orientation='vertical',size_hint_y=None,height=dp(158),
                    padding=dp(12),spacing=dp(5))
        _rounded_bg(c,UI_CARD2,10)
        bar=Widget(size_hint_y=None,height=dp(3))
        with bar.canvas:
            Color(*cav.cor); r=Rectangle(pos=bar.pos,size=bar.size)
        bar.bind(pos=lambda w,v: setattr(r,'pos',v),size=lambda w,v: setattr(r,'size',v))
        c.add_widget(bar)
        is_lend = getattr(cav,'lendario',False)
        sx = '♂' if getattr(cav,'sexo','')=='M' else ('♀' if getattr(cav,'sexo','')=='F' else '')
        cor_titulo = (1,0.90,0.30,1) if is_lend else UI_GOLD
        pref = '[LENDARIO] ' if is_lend else f"{rd.get('emoji','H')} "
        c.add_widget(lbl(f"{pref}{sx} {cav.nome}  —  {cav.raca}",
                          sz=15,cor=cor_titulo,bold=True,h=dp(26)))
        cat=estrelas(cav.vel_base)
        c.add_widget(lbl(f'{f"{cat}*"} Categoria {cat}🏆  •  {cav.status_idade(jogo.semana)}  •  máx {PRECO_MAX_ESTRELA[cat]:,} Ouro',sz=11,cor=UI_DIM,h=dp(18)))
        stats=BoxLayout(size_hint_y=None,height=dp(20))
        for txt,cor in [(f'⚡{cav.vel_base:.1f}',UI_GOLD),(f'💪{cav.stamina}%',UI_BLUE),
                        (f'❤{cav.saude}%',UI_GREEN),(f'🏆{cav.vitorias}v',UI_GOLD)]:
            stats.add_widget(_elbl(txt, font_size=dp(11), color=cor,
                                   height=dp(22), size_hint_y=None, halign='center'))
        c.add_widget(stats)
        dd=DropDown()
        for idx,nc in enumerate(CORES_NOMES):
            b2=Button(text=nc,size_hint_y=None,height=dp(36),
                      background_normal='',background_color=(0.12,0.12,0.20,1),color=UI_TEXT)
            b2.bind(on_release=lambda btn,i=idx: dd.select(i)); dd.add_widget(b2)
        cb=btn_secondary('🎨 Cor',h=dp(34))
        cb.size_hint=(None,None); cb.size=(dp(90),dp(34))
        cb.cor_idx=CORES.index(cav.cor) if cav.cor in CORES else 0
        cb.bind(on_release=dd.open)
        dd.bind(on_select=lambda inst,i,x=cb: setattr(x,'cor_idx',i))
        btns=BoxLayout(size_hint_y=None,height=dp(40),spacing=dp(6))
        btns.add_widget(cb)
        pode=jogo.pode_comprar_cavalo() and jogo.dinheiro>=cav.preco
        bb=_ebtn(f'🛒 {cav.preco:,} Ouro',
                 bg=UI_GOLD if pode else (0.25,0.25,0.30,1),
                 fg=(0.04,0.04,0.04,1) if pode else UI_DIM,
                 font_size=dp(14), height=dp(40),
                 cb=(lambda *_,cv=cav,xb=cb: self._comprar_cav(cv,xb,jogo)) if pode else None)
        btns.add_widget(bb); c.add_widget(btns)
        return c

    def _comprar_cav(self,cav,cor_btn,jogo):
        if not jogo.pode_comprar_cavalo() or jogo.dinheiro<cav.preco: return
        _snd.tocar('moeda')
        jogo.dinheiro-=cav.preco
        novo=criar_cavalo(cav.nome,cav.raca,semana_nasc=cav.semana_nasc,
                          vel_base=cav.vel_base,stamina=cav.stamina,
                          saude=cav.saude,preco=cav.preco,cor=CORES[cor_btn.cor_idx])
        novo.vitorias=cav.vitorias; novo.historico_vitorias=cav.historico_vitorias[:]
        jogo.cavalos_jogador.append(novo)
        if cav in jogo.cavalos_mercado: jogo.cavalos_mercado.remove(cav)
        self.on_enter()

    def _aba_itens(self,box,jogo,lista):
        if not jogo.cavalos_jogador:
            box.add_widget(lbl(f'⚠ {T("sem_cavalo_primeiro")}',sz=15,cor=UI_RED,halign='center')); return
        self._cav_idx=self._cav_idx%len(jogo.cavalos_jogador)
        cav=jogo.cavalos_jogador[self._cav_idx]
        sel=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(8),padding=(0,dp(4)))
        _rounded_bg(sel,UI_CARD,8)
        sel.add_widget(Label(text=T('para'),font_size=dp(13),color=UI_DIM,
                             size_hint_x=None,width=dp(44)))
        cb2=btn_secondary(f'🐎 {cav.nome}',h=dp(40))
        cb2.bind(on_release=lambda *_: self._prox_cav(jogo)); sel.add_widget(cb2)
        sel.add_widget(Label(text=f'E:{int(cav.energia)}% S:{cav.saude}%',
                             font_size=dp(11),color=UI_DIM))
        box.add_widget(sel); box.add_widget(spacer(6))
        for item in lista: box.add_widget(self._card_item(item,jogo))

    def _prox_cav(self,jogo):
        self._cav_idx=(self._cav_idx+1)%max(1,len(jogo.cavalos_jogador)); self.on_enter()

    def _card_item(self,item,jogo):
        c=BoxLayout(size_hint_y=None,height=dp(70),padding=dp(10),spacing=dp(10))
        _rounded_bg(c,UI_CARD,8)
        from kivy.uix.image import Image as _Img
        from emoji_img import emoji_path as _ep
        _path = _ep(item.emoji) if _EMOJI_OK else None
        if _path:
            c.add_widget(_Img(source=_path, size_hint=(None,None),
                              size=(dp(36),dp(36)), allow_stretch=True, keep_ratio=True))
        else:
            c.add_widget(Label(text=item.emoji,font_size=dp(26),
                               size_hint_x=None,width=dp(40)))
        info=BoxLayout(orientation='vertical',spacing=dp(2))
        info.add_widget(Label(text=f'[b]{item.nome}[/b]',markup=True,
                              font_size=dp(14),color=UI_TEXT,halign='left',
                              size_hint_y=None,height=dp(24)))
        info.add_widget(Label(text=item.descricao,font_size=dp(11),color=UI_DIM,
                              halign='left',size_hint_y=None,height=dp(18)))
        c.add_widget(info)
        pode=jogo.dinheiro>=item.preco
        bb=Button(text=f'{item.preco} Ouro',size_hint=(None,None),size=(dp(68),dp(44)),
                  background_normal='',
                  background_color=UI_GOLD if pode else (0.25,0.25,0.30,1),
                  color=(0.04,0.04,0.04,1) if pode else UI_DIM,
                  font_size=dp(13),bold=True)
        if pode: bb.bind(on_release=lambda *_,i=item: self._usar(i,jogo))
        c.add_widget(bb); return c

    def _usar(self,item,jogo):
        if jogo.dinheiro<item.preco or not jogo.cavalos_jogador: return
        jogo.dinheiro-=item.preco
        jogo.aplicar_item(item,jogo.cavalos_jogador[self._cav_idx%len(jogo.cavalos_jogador)])
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  LEILÃO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaLeilao(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self, UI_BG)
        jogo = self.manager.jogo
        root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        self.add_widget(root)

        h = BoxLayout(size_hint_y=None, height=dp(64), padding=(dp(8), dp(10)), spacing=dp(8))
        _set_bg(h, (0.10, 0.07, 0.02, 1))
        h.add_widget(lbl(f'🔨 {T("leilao_titulo2")}', sz=22, cor=UI_GOLD, bold=True, h=dp(44)))
        h.add_widget(Label(text=f'Ouro {jogo.dinheiro:,}',
                           font_size=dp(16), color=UI_GREEN))
        root.add_widget(h); root.add_widget(sep())

        sv, box = mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding = (dp(14), dp(10))

        if not jogo.leilao_ativo or not jogo.leilao_lotes:
            semanas_prox = LEILAO_INTERVALO_SEMANAS - (jogo.semana - jogo.semana_ultimo_leilao)
            semanas_prox = max(1, semanas_prox)
            box.add_widget(spacer(30))
            c = card(h=dp(110), bg=UI_CARD3)
            c.add_widget(lbl(T('sem_leilao'),
                              sz=17, cor=UI_DIM, halign='center', h=dp(32)))
            c.add_widget(lbl(f'{T("proximo_leilao")} {semanas_prox} {T("semanas")}',
                              sz=13, cor=UI_DIM, halign='center', h=dp(24)))
            c.add_widget(lbl(T('leilao_desc'),
                              sz=12, cor=UI_DIM, halign='center', h=dp(22)))
            c.add_widget(lbl(T('leilao_lendarios'),
                              sz=12, cor=UI_GOLD, halign='center', h=dp(22)))
            box.add_widget(c)
            return

        semanas_restantes = LEILAO_INTERVALO_SEMANAS - (jogo.semana - jogo.leilao_semana)
        urgencia = card(h=dp(48), bg=UI_RED_BG)
        urgencia.add_widget(lbl(
            f'LEILAO ATIVO! Encerra em {max(1,semanas_restantes)} semana(s)!',
            sz=14, cor=UI_RED, bold=True, halign='center', h=dp(32)))
        box.add_widget(urgencia)
        box.add_widget(sep())

        for idx, lote in enumerate(jogo.leilao_lotes):
            box.add_widget(self._card_lote(idx, lote, jogo))


    def _card_lote(self, idx, lote, jogo):
        cav = lote['cavalo']
        vendido = lote['vendido']
        lend = lote.get('lendario', getattr(cav, 'lendario', False))
        cat = estrelas(cav.vel_base)

        ch = dp(310) if lend else dp(250)
        c = BoxLayout(orientation='vertical', size_hint_y=None, height=ch,
                      padding=dp(12), spacing=dp(6))

        if lend:
            _rounded_bg(c, (0.12, 0.09, 0.02, 1), 14)
        else:
            _rounded_bg(c, UI_CARD2, 12)

        bar_row = BoxLayout(size_hint_y=None, height=dp(28), spacing=dp(6))
        bar = Widget(size_hint_x=None, width=dp(6), size_hint_y=1)
        with bar.canvas:
            Color(*(UI_GOLD if lend else cav.cor))
            r = Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(pos=lambda w, v: setattr(r, 'pos', v),
                 size=lambda w, v: setattr(r, 'size', v))
        bar_row.add_widget(bar)
        if lend:
            badge = Label(text=f'[b]{T("lendario_badge")}[/b]', markup=True,
                          font_size=dp(12), color=(0.04, 0.04, 0.04, 1),
                          size_hint_x=None, width=dp(90), size_hint_y=1)
            badge_bg = Widget(size_hint_x=None, width=dp(90), size_hint_y=1)
            with badge_bg.canvas:
                Color(*UI_GOLD)
                RoundedRectangle(pos=badge_bg.pos, size=badge_bg.size, radius=[6])
            bar_row.add_widget(badge_bg); bar_row.add_widget(badge)
        bar_row.add_widget(Label(text=''))
        c.add_widget(bar_row)

        if lend and not vendido:
            preview = HorseCanvas(cav, size_hint_y=None, height=dp(120))
            _rounded_bg(preview, (0.06, 0.10, 0.18, 1), 8)
            c.add_widget(preview)

        cor_nome = UI_GOLD if lend else UI_TEXT
        c.add_widget(lbl(cav.nome, sz=18 if lend else 16, cor=cor_nome, bold=True, h=dp(28)))

        if lend and hasattr(cav, 'lendario'):
            desc_cfg = next((d for d in CAVALOS_LENDARIOS if d['nome'] == cav.nome), None)
            if desc_cfg:
                c.add_widget(lbl(f'"{desc_cfg["descricao"]}"',
                                  sz=11, cor=UI_DIM, h=dp(18)))

        stats_row = BoxLayout(size_hint_y=None, height=dp(24))
        for txt, cor in [
            (f'Vel {cav.vel_base:.2f}', UI_GOLD),
            (f'Stamp {cav.stamina}%', UI_BLUE),
            (f'Saude {cav.saude}%', UI_GREEN),
            (f'{cat} estrela(s)', UI_GOLD),
        ]:
            stats_row.add_widget(Label(text=txt, font_size=dp(11), color=cor))
        c.add_widget(stats_row)

        lance = lote['lance_atual']
        n_lances = lote['n_lances']
        prox_lance = int(lance * (1 + 0.12))
        if not vendido:
            lance_row = BoxLayout(size_hint_y=None, height=dp(28))
            lance_row.add_widget(Label(
                text=f'{T("proximo_lance")} {prox_lance:,} Ouro',
                font_size=dp(14), color=UI_GOLD, bold=True, halign='left'))
            lance_row.add_widget(Label(
                text=f'({n_lances}/{5} lances dados)',
                font_size=dp(11), color=UI_DIM, halign='right'))
            c.add_widget(lance_row)

        if vendido:
            c.add_widget(lbl('ARREMATADO!', sz=15, cor=UI_GREEN, bold=True,
                              halign='center', h=dp(40)))
        elif not jogo.pode_comprar_cavalo():
            c.add_widget(lbl(T('sem_baia'), sz=13, cor=UI_RED,
                              halign='center', h=dp(40)))
        elif n_lances >= 5:
            c.add_widget(lbl(T('lance_max'), sz=13, cor=UI_RED,
                              halign='center', h=dp(40)))
        else:
            pode = jogo.dinheiro >= prox_lance
            bb = Button(
                text=f'DAR LANCE  {prox_lance:,} Ouro',
                background_normal='', font_size=dp(15), bold=True,
                background_color=UI_GOLD if pode else (0.25, 0.25, 0.30, 1),
                color=(0.04, 0.04, 0.04, 1) if pode else UI_DIM,
                size_hint_y=None, height=dp(50))
            if pode:
                bb.bind(on_release=lambda *_, i=idx: self._dar_lance(i, jogo))
            c.add_widget(bb)

        return c

    def _dar_lance(self, idx, jogo):
        ok, msg = jogo.confirmar_lance(idx)
        if ok:
            _snd.tocar('vitoria')
        else:
            _snd.tocar('fim_corrida')
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  GENEALOGIA
# ═══════════════════════════════════════════════════════════════════════════════
class TelaGenealogia(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('genealogia_titulo'),'🌳'))
        root.add_widget(sep()); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        if not jogo.cavalos_jogador:
            box.add_widget(lbl(T('sem_cavalos'),sz=16,cor=UI_DIM,halign='center'))
        for cav in jogo.cavalos_jogador:
            txt=cav.genealogia(); lines=txt.count('\n')+1
            c=card(h=dp(max(80,26*lines+20)),bg=UI_CARD)
            c.add_widget(lbl(txt,sz=12,cor=UI_TEXT,h=dp(24*lines)))
            box.add_widget(c)


# ═══════════════════════════════════════════════════════════════════════════════
#  CRUZAMENTO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCruzamento(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.pai_idx=0; self.mae_idx=0; self.cor_idx=0

    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('cruzamento_titulo'),'💞'))
        root.add_widget(sep()); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(16),dp(12))

        machos=[c for c in jogo.cavalos_jogador
                if getattr(c,'sexo','')=='M' and c.pode_correr(jogo.semana)]
        femeas=[c for c in jogo.cavalos_jogador
                if getattr(c,'sexo','')=='F' and c.pode_correr(jogo.semana)
                and not getattr(c,'em_gestacao',lambda:False)()]

        erros=[]
        if not jogo.pode_comprar_cavalo():
            erros.append('Sem baia disponivel para o potro.')
        if not machos:
            erros.append('Nenhum cavalo macho adulto no haras.')
        if not femeas:
            erros.append('Nenhuma egua adulta disponivel (nao gestante).')
        if erros:
            for e in erros:
                w=card(h=dp(48),bg=UI_RED_BG)
                w.add_widget(lbl(f'⚠ {e}',sz=13,cor=UI_RED,halign='center',h=dp(32)))
                box.add_widget(w)
            return

        self.pai_idx=min(self.pai_idx,len(machos)-1)
        pai=machos[self.pai_idx]
        btn_pai=Button(text=f'M Pai: {pai.nome}  ({pai.raca})  Vel {pai.vel_base:.2f}',
                       background_normal='',background_color=(0.08,0.16,0.32,1),
                       color=(0.60,0.80,1.0,1),font_size=dp(14),bold=True,
                       size_hint_y=None,height=dp(48))
        def _prox_pai(*_):
            self.pai_idx=(self.pai_idx+1)%len(machos); self.on_enter()
        btn_pai.bind(on_release=_prox_pai)

        self.mae_idx=min(self.mae_idx,len(femeas)-1)
        mae=femeas[self.mae_idx]
        btn_mae=Button(text=f'F Mae: {mae.nome}  ({mae.raca})  Vel {mae.vel_base:.2f}',
                       background_normal='',background_color=(0.30,0.10,0.18,1),
                       color=(1.0,0.65,0.80,1),font_size=dp(14),bold=True,
                       size_hint_y=None,height=dp(48))
        def _prox_mae(*_):
            self.mae_idx=(self.mae_idx+1)%len(femeas); self.on_enter()
        btn_mae.bind(on_release=_prox_mae)

        box.add_widget(lbl(T('trocar_animal'),sz=12,cor=UI_DIM,h=dp(22)))
        box.add_widget(btn_pai); box.add_widget(btn_mae)
        box.add_widget(spacer(8))

        box.add_widget(lbl(T('nome_filhote'),sz=13,cor=UI_DIM,h=dp(22)))
        self.nome_inp=TextInput(hint_text=T('hint_potro'),multiline=False,
                                background_color=(0.11,0.11,0.19,1),
                                foreground_color=UI_TEXT,font_size=dp(18),
                                size_hint_y=None,height=dp(50))
        box.add_widget(self.nome_inp)

        box.add_widget(lbl(T('cor_filhote'),sz=13,cor=UI_DIM,h=dp(22)))
        dd=DropDown()
        for i,nc in enumerate(CORES_NOMES):
            b2=Button(text=nc,size_hint_y=None,height=dp(36),
                      background_normal='',background_color=(0.12,0.12,0.20,1),color=UI_TEXT)
            b2.bind(on_release=lambda btn,i=i: dd.select(i)); dd.add_widget(b2)
        self.cor_btn=btn_secondary(f'🎨 Cor: {CORES_NOMES[self.cor_idx]}',h=dp(40))
        self.cor_btn.bind(on_release=dd.open)
        dd.bind(on_select=lambda inst,i: (setattr(self,'cor_idx',i),
                                          setattr(self.cor_btn,'text',f'Cor: {CORES_NOMES[i]}')))
        box.add_widget(self.cor_btn)
        box.add_widget(spacer(8))

        if pai is not mae:
            raca_r=pai.raca if pai.raca==mae.raca else 'Mestio'
            if raca_r not in RACAS: raca_r='Mestico'
            vel_m=(pai.vel_base+mae.vel_base)/2
            sx_potro='M ou F (aleatorio)'
            prev=card(h=dp(80),bg=(0.06,0.12,0.08,1))
            prev.add_widget(lbl(f'Potro: {raca_r}  |  Vel ~{vel_m:.2f}  |  {estrelas(vel_m)} estrela(s)',
                                 sz=14,cor=UI_GREEN,bold=True,h=dp(28)))
            prev.add_widget(lbl(f'{T("sexo")} {sx_potro}  |  {T("nasce_semanas")}',
                                 sz=12,cor=UI_DIM,h=dp(22)))
            prev.add_widget(lbl('A egua ficara gestante e nao podera correr.',
                                 sz=11,cor=(1.0,0.65,0.80,1),h=dp(20)))
            box.add_widget(prev)

        box.add_widget(btn_primary(f'💞 {T("gestacao_btn")}',
                       cb=lambda *_: self._cruzar(machos,femeas,jogo),h=dp(54)))


    def _cruzar(self,machos,femeas,jogo):
        if jogo.dinheiro<800: return
        if self.pai_idx>=len(machos) or self.mae_idx>=len(femeas): return
        pai=machos[self.pai_idx]; mae=femeas[self.mae_idx]
        jogo.dinheiro-=800
        nome=self.nome_inp.text.strip() or 'Potro'
        cor=CORES[self.cor_idx]
        ok,msg=jogo.iniciar_gestacao(mae,pai,nome,cor)
        if ok:
            _snd.tocar('moeda')
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  GALERIA DE TROFÉUS
# ═══════════════════════════════════════════════════════════════════════════════
class TelaTrofeus(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self, UI_BG)
        jogo  = self.manager.jogo
        root  = BoxLayout(orientation='vertical', padding=0, spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('trofeus_titulo'),'🏆'))
        root.add_widget(sep((1, 0.84, 0, 1)))

        sv, box = mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding = (dp(14), dp(10))

        # Painel Reputação
        _nr,_cr=jogo.nivel_reputacao(); _pc,_pn,_pt=jogo.barra_reputacao()
        _prx,_cprx,_flt=jogo.proxima_reputacao()
        _rp=BoxLayout(orientation='vertical',size_hint_y=None,height=dp(118),
                      padding=(dp(12),dp(8)),spacing=dp(4))
        _rounded_bg(_rp,(0.07,0.05,0.16,1))
        _rt=BoxLayout(size_hint_y=None,height=dp(20))
        _rt.add_widget(lbl(T('reputacao_haras'),sz=11,cor=UI_DIM,h=dp(18)))
        _rt.add_widget(lbl(f'{jogo.reputacao_pts} pts totais',sz=11,cor=UI_DIM,h=dp(18)))
        _rp.add_widget(_rt)
        _rp.add_widget(lbl(f'★★ {_cr["nome"]}',sz=20,cor=UI_PURPLE,bold=True,h=dp(28)))
        _rb2=BoxLayout(size_hint_y=None,height=dp(12))
        _rounded_bg(_rb2,(0.14,0.11,0.22,1))
        _fw2=max(0.02,_pc); _rf2=BoxLayout(size_hint=(_fw2,1)); _rounded_bg(_rf2,UI_PURPLE)
        _rb2.add_widget(_rf2)
        if _pc<0.99: _rb2.add_widget(BoxLayout(size_hint=(1-_fw2,1)))
        _rp.add_widget(_rb2)
        if _prx:
            _rp.add_widget(lbl(f'{_pn}/{_pt} pts  —  {_flt} pts para {_cprx["nome"]} {_cprx["emoji"]}',
                               sz=11,cor=UI_DIM,h=dp(18)))
        else:
            _rp.add_widget(lbl(T('reputacao_max'),sz=11,cor=UI_GOLD,h=dp(18)))
        _rp.add_widget(lbl(T('bonus_rep'),sz=9,cor=(0.38,0.32,0.52,1),halign='center',h=dp(14)))
        box.add_widget(_rp)
        box.add_widget(sep())
        _gn=GridLayout(cols=5,size_hint_y=None,height=dp(50),spacing=dp(3))
        for _nk,_nv in REPUTACAO_NIVEL.items():
            _at=_nk<=_nr
            _cn=BoxLayout(orientation='vertical',spacing=dp(1))
            _rounded_bg(_cn,(0.11,0.09,0.22,1) if _at else (0.07,0.07,0.11,1))
            _stars_txt = '★'*_nk
            _cn.add_widget(lbl(_stars_txt,sz=9,cor=UI_GOLD if _at else UI_DIM,halign='center',h=dp(22)))
            _nivel_nome = T(f'nivel_{["iniciante","conhecido","respeitado","famoso","lendario"][_nk-1]}')
            _cn.add_widget(lbl(_nivel_nome[:7],sz=7,cor=UI_TEXT if _at else UI_DIM,halign='center',h=dp(16)))
            _cn.add_widget(lbl(f'{_nv["min_pts"]}pts',sz=7,cor=UI_DIM,halign='center',h=dp(12)))
            _gn.add_widget(_cn)
        box.add_widget(_gn)
        box.add_widget(sep())

        medalhas   = [t for t in jogo.trofeus if t['tipo'] == 'medalha']
        trofeus_c  = [t for t in jogo.trofeus if t['tipo'] == 'trofeu']
        ouros_m    = sum(1 for t in medalhas  if t['posicao'] == 1)
        pratas_m   = sum(1 for t in medalhas  if t['posicao'] == 2)
        bronzes_m  = sum(1 for t in medalhas  if t['posicao'] == 3)

        if not medalhas and not trofeus_c:
            box.add_widget(spacer(30))
            box.add_widget(lbl(T('nenhuma_conquista'), sz=17, cor=UI_DIM, halign='center'))
            box.add_widget(lbl(T('venca_corridas'), sz=13, cor=UI_DIM, halign='center'))
        else:
            box.add_widget(lbl(T('medalhas'), sz=15, cor=UI_GOLD, bold=True, h=dp(28)))
            row_med = BoxLayout(size_hint_y=None, height=dp(64), spacing=dp(8))
            for emoji_m, qtd, cor_m, bg_m in [
                ('🥇', ouros_m,   (1,.84,0,1),       UI_GOLD_BG),
                ('🥈', pratas_m,  (0.78,0.78,0.78,1), (0.12,0.12,0.16,1)),
                ('🥉', bronzes_m, (0.80,0.50,0.20,1), (0.14,0.08,0.04,1)),
            ]:
                c_med = BoxLayout(orientation='vertical', spacing=dp(2))
                _rounded_bg(c_med, bg_m, 10)
                c_med.add_widget(_elbl(emoji_m, font_size=dp(28), color=cor_m,
                                       height=dp(34), size_hint_y=None, halign='center'))
                c_med.add_widget(lbl(f'{qtd}x', sz=14, cor=cor_m, bold=True,
                                      halign='center', h=dp(22)))
                row_med.add_widget(c_med)
            box.add_widget(row_med)
            box.add_widget(spacer(6))

            if medalhas:
                por_temp = {}
                for m in medalhas:
                    por_temp.setdefault(m['temporada'], []).append(m)
                for temp in sorted(por_temp.keys(), reverse=True):
                    lista = por_temp[temp]
                    o = sum(1 for m in lista if m['posicao']==1)
                    p = sum(1 for m in lista if m['posicao']==2)
                    b = sum(1 for m in lista if m['posicao']==3)
                    h_row = BoxLayout(size_hint_y=None, height=dp(28), padding=(dp(8),0))
                    _rounded_bg(h_row, UI_CARD3, 6)
                    t_lbl = lbl(f'{T("temporada")} {temp}:', sz=11, cor=UI_DIM, h=dp(22))
                    t_lbl.size_hint_x = None
                    t_lbl.width = dp(100)
                    h_row.add_widget(t_lbl)
                    h_row.add_widget(_elbl(f'🥇{o}  🥈{p}  🥉{b}',
                                           font_size=dp(12), color=UI_TEXT,
                                           height=dp(22), size_hint_y=None, halign='left'))
                    box.add_widget(h_row)
                box.add_widget(spacer(4))

            box.add_widget(sep())

            if trofeus_c:
                box.add_widget(lbl(T('trofeus_camp'), sz=15, cor=UI_GOLD,
                                    bold=True, h=dp(28)))
                for t in reversed(trofeus_c):
                    pos   = t['posicao']
                    camp  = t['campeonato']
                    temp  = t['temporada']
                    cfg   = COMPETICOES.get(camp, {})
                    cor_c = cfg.get('cor', UI_PURPLE)
                    nome_c= cfg.get('nome', camp.title())
                    if pos==1:   ico_t,cor_p='🥇',(1,.84,0,1)
                    elif pos==2: ico_t,cor_p='🥈',(0.78,0.78,0.78,1)
                    else:        ico_t,cor_p='🥉',(0.80,0.50,0.20,1)

                    c = BoxLayout(size_hint_y=None, height=dp(68),
                                  padding=(dp(10),dp(6)), spacing=dp(8))
                    _rounded_bg(c, (0.08,0.06,0.02,1), 10)
                    barra = Widget(size_hint_x=None, width=dp(5))
                    with barra.canvas:
                        Color(*cor_c); Rectangle(pos=barra.pos, size=barra.size)
                    c.add_widget(barra)
                    from emoji_img import EmojiImage as _EI
                    c.add_widget(_EI(ico_t, size=(dp(40),dp(40))))
                    info = BoxLayout(orientation='vertical', spacing=dp(2))
                    info.add_widget(lbl(f'{pos}. Lugar — {nome_c}',
                                        sz=15, cor=cor_p, bold=True, h=dp(26)))
                    info.add_widget(lbl(f'{T("temporada")} {temp}  •  {nome_c}',
                                        sz=11, cor=UI_DIM, h=dp(20)))
                    c.add_widget(info)
                    box.add_widget(c)
                    box.add_widget(spacer(4))
                box.add_widget(sep())

        box.add_widget(lbl(T('recordes_haras'), sz=15, cor=UI_BLUE, bold=True, h=dp(28)))
        meus = jogo.cavalos_jogador

        def _rec_card(emoji_r, titulo, valor, detalhe=''):
            from emoji_img import EmojiImage as _EI
            c = BoxLayout(size_hint_y=None, height=dp(60),
                          padding=(dp(10),dp(6)), spacing=dp(10))
            _rounded_bg(c, UI_CARD2, 8)
            c.add_widget(_EI(emoji_r, size=(dp(36),dp(36))))
            info = BoxLayout(orientation='vertical')
            info.add_widget(lbl(titulo, sz=11, cor=UI_DIM, h=dp(18)))
            info.add_widget(lbl(valor,  sz=15, cor=UI_GOLD, bold=True, h=dp(24)))
            if detalhe:
                info.add_widget(lbl(detalhe, sz=10, cor=UI_DIM, h=dp(16)))
            c.add_widget(info)
            return c

        if meus:
            mv = max(meus, key=lambda c: c.vitorias)
            box.add_widget(_rec_card('🏇', 'Cavalo com mais vitorias',
                                      f'{mv.nome} — {mv.vitorias} vitorias',
                                      f'{mv.raca}  •  {mv.vel_base:.1f} vel'))
        else:
            box.add_widget(_rec_card('🏇', 'Cavalo com mais vitorias', 'Nenhum ainda'))

        total_vit = sum(c.vitorias for c in meus)
        box.add_widget(_rec_card('🏆', 'Total de vitorias do haras',
                                  f'{total_vit} vitorias',
                                  f'com {len(meus)} cavalos ativos'))

        if meus:
            mc = max(meus, key=lambda c: calcular_preco_mercado(c))
            box.add_widget(_rec_card('💰', 'Cavalo mais valioso',
                                      f'{mc.nome} — {calcular_preco_mercado(mc):,} Ouro',
                                      f'{mc.raca}  •  {estrelas(mc.vel_base)}🏆'))
        else:
            box.add_widget(_rec_card('💰', 'Cavalo mais valioso', 'Nenhum ainda'))

        if meus:
            mvel = max(meus, key=lambda c: c.vel_base)
            box.add_widget(_rec_card('⚡', 'Cavalo mais veloz',
                                      f'{mvel.nome} — {mvel.vel_base:.2f} vel',
                                      f'{mvel.raca}  •  {estrelas(mvel.vel_base)}🏆'))
        else:
            box.add_widget(_rec_card('⚡', 'Cavalo mais veloz', 'Nenhum ainda'))

        if meus:
            mst = max(meus, key=lambda c: c.stamina)
            box.add_widget(_rec_card('💪', 'Maior stamina',
                                      f'{mst.nome} — {mst.stamina}%',
                                      f'{mst.raca}'))
        else:
            box.add_widget(_rec_card('💪', 'Maior stamina', 'Nenhum ainda'))

        box.add_widget(_rec_card('📅', 'Temporadas jogadas',
                                  f'Temporada {jogo.temporada}',
                                  f'Semana {jogo.semana} no total'))
        box.add_widget(_rec_card('💳', 'Saldo atual',
                                  f'Ouro {jogo.dinheiro:,}'))

        box.add_widget(spacer(10))


# ═══════════════════════════════════════════════════════════════════════════════
#  JORNAL / REPORTER
# ═══════════════════════════════════════════════════════════════════════════════
import random as _rnd

_NOTICIAS_VITORIA = [
    "{nome} DOMINA a pista e leva o 1° lugar com folga impressionante!",
    "CORRIDA HISTORICA: {nome} cruza a linha em primeiro lugar!",
    "O haras {haras} confirma seu favoritismo com vitoria de {nome}!",
    "{nome} deixa todos para tras e garante o topo do podio!",
    "Que corrida! {nome} vence com uma arrancada final eletrizante!",
    "INVENCIVEL! {nome} vence mais uma e segue sem ser batido!",
    "O haras {haras} esta em chamas — {nome} e simplesmente imparavel!",
    "{nome} protagoniza a corrida do ano e leva o ouro para casa!",
    "Especialistas apontam: {nome} pode ser o melhor da temporada!",
    "Com maestria, {nome} controla a corrida do inicio ao fim. 1° lugar!",
    "A torcida explodiu! {nome} cruza em 1° em uma corrida inesquecivel!",
    "VIRADA EPICA: {nome} largou atras mas voou na reta final!",
    "{nome} disparou na curva e ninguem mais chegou perto. Vitoria!",
    "O haras {haras} comemora: {nome} supera todos os adversarios!",
    "Tecnica e velocidade: {nome} mostra por que e o favorito da temporada!",
]
_NOTICIAS_DERROTA = [
    "{nome} termina em {pos}° lugar — treinador promete melhorias.",
    "Dia dificil para o haras {haras}: {nome} nao consegue o podio.",
    "{nome} mostra potencial mas ainda nao foi desta vez. {pos}° lugar.",
    "O favorito {nome} surpreende negativamente e termina em {pos}°.",
    "Corrida difícil para {nome} — o {pos}° lugar nao era o esperado.",
    "{nome} saiu bem mas perdeu ritmo no final. {pos}° lugar desta vez.",
    "Haras {haras} precisa rever estrategia apos {nome} terminar em {pos}°.",
    "Problemas de estamina? {nome} caiu de ritmo e fechou em {pos}°.",
    "{nome} tentou mas a concorrencia foi mais forte hoje. {pos}° lugar.",
    "Torcedores foram para casa desapontados. {nome} nao entregou.",
]
_NOTICIAS_TOP3 = [
    "{nome} garante o {pos}° lugar e traz premio para casa!",
    "Podio para o haras {haras}! {nome} em {pos}°!",
    "Excelente resultado: {nome} no {pos}° lugar desta corrida!",
    "{nome} sobe ao podio e mostra que esta evoluindo semana a semana!",
    "Que resultado! {pos}° lugar para {nome} e muito dinheiro no bolso!",
]
_NOTICIAS_CURIOSIDADE = [
    "BASTIDORES: dizem que o haras {haras} ja recusou proposta milionaria por {nome}.",
    "RUMORES: outros treinadores estao de olho em {nome}. Ha interesse externo!",
    "CURIOSIDADE: {nome} e descendente de uma linhagem historica de campeoes.",
    "MERCADO: o valor de {nome} subiu 30%% apos a ultima corrida segundo analistas.",
    "FATO: o haras {haras} e apontado como um dos mais promissores da regiao.",
    "TRIVIA: sabia que cavalos como {nome} treinam mais de 6 horas por dia?",
]
_PERGUNTAS = [
    {
        'pergunta': 'Reporter: "{nome} foi incrivel hoje! Qual o segredo do seu sucesso?"',
        'opcoes': [
            ('A) Muito treino e dedicacao!',      'moral'),
            ('B) Apenas seguimos o plano.',        'neutro'),
            ('C) Tivemos muita sorte hoje.',       'humilde'),
        ]
    },
    {
        'pergunta': 'Reporter: "Como voce avalia o desempenho de {nome} nesta corrida?"',
        'opcoes': [
            ('A) Excelente! Estamos no caminho certo.', 'otimista'),
            ('B) Bom, mas podemos melhorar mais.',       'realista'),
            ('C) Honestamente, esperava mais.',          'critico'),
        ]
    },
    {
        'pergunta': 'Reporter: "Quais sao os planos para as proximas corridas?"',
        'opcoes': [
            ('A) Vamos ao campeonato nacional!',          'ambicioso'),
            ('B) Foco em recuperar os cavalos primeiro.', 'cauteloso'),
            ('C) Ainda estamos avaliando as opcoes.',     'misterioso'),
        ]
    },
    {
        'pergunta': 'Reporter: "{nome} parece em grande forma. Ha planos de vende-lo?"',
        'opcoes': [
            ('A) Jamais! Ele e o coracao do haras.',   'leal'),
            ('B) Tudo tem um preco certo.',             'negociador'),
            ('C) Nao responderei isso agora.',          'esquivo'),
        ]
    },
    {
        'pergunta': 'Reporter: "O publico amou a corrida. Mensagem para os fas?"',
        'opcoes': [
            ('A) Obrigado pelo apoio de sempre!',           'grato'),
            ('B) Continuem acompanhando, vem mais por ai!', 'animado'),
            ('C) Os cavalos agradecem o carinho.',          'humilde'),
        ]
    },
]

def _mostrar_jornal(screen_ref, pos_jogador, nome_cav, nome_haras, on_fechar):
    from kivy.uix.modalview import ModalView
    from kivy.uix.boxlayout import BoxLayout

    modo = _rnd.choice(['noticia','reporter','curiosidade'])

    mv = ModalView(size_hint=(0.92, None), height=dp(380),
                   background_color=(0,0,0,0.7), auto_dismiss=False)
    outer = BoxLayout(orientation='vertical', padding=dp(4), spacing=0)
    _rounded_bg(outer, (0.07,0.07,0.12,1), 14)

    hdr = BoxLayout(size_hint_y=None, height=dp(44), padding=(dp(12),dp(6)))
    _rounded_bg(hdr, (0.12,0.10,0.04,1), 0)
    hdr.add_widget(_elbl(f'📰 {T("gazeta")}', font_size=dp(16),
                          color=UI_GOLD, height=dp(32), size_hint_y=None, halign='left'))
    outer.add_widget(hdr)
    outer.add_widget(sep((0.3,0.25,0.05,1)))

    corpo = BoxLayout(orientation='vertical', padding=(dp(14),dp(10)),
                      spacing=dp(10))

    if modo in ('noticia', 'curiosidade'):
        if modo == 'curiosidade':
            tmpl = _rnd.choice(_NOTICIAS_CURIOSIDADE)
            icone = '🔧'
            subtitulo = 'Voce sabia?'
        elif pos_jogador == 1:
            tmpl  = _rnd.choice(_NOTICIAS_VITORIA)
            icone = '🏆'
            subtitulo = f'Semana especial para o haras {nome_haras}!'
        elif pos_jogador <= 3:
            tmpl  = _rnd.choice(_NOTICIAS_TOP3)
            icone = '🥈'
            subtitulo = f'O haras {nome_haras} no podio!'
        else:
            tmpl  = _rnd.choice(_NOTICIAS_DERROTA)
            icone = '📜'
            subtitulo = 'A redacao acompanhou a corrida de perto.'

        titulo = tmpl.format(nome=nome_cav, haras=nome_haras, pos=pos_jogador)
        corpo.add_widget(_elbl(icone, font_size=dp(32), color=UI_GOLD,
                                height=dp(40), size_hint_y=None, halign='center'))
        corpo.add_widget(lbl(titulo, sz=14, cor=UI_TEXT, halign='center', h=dp(70)))
        corpo.add_widget(lbl(subtitulo, sz=11, cor=UI_DIM, halign='center', h=dp(22)))
        corpo.add_widget(spacer(8))
        btn_ok = btn_primary('❌ Fechar', cb=lambda *_: (mv.dismiss(), on_fechar()))
        corpo.add_widget(btn_ok)

    else:
        q = _rnd.choice(_PERGUNTAS)
        pergunta = q['pergunta'].format(nome=nome_cav, haras=nome_haras)
        corpo.add_widget(_elbl('📰 ENTREVISTA', font_size=dp(13), color=UI_DIM,
                                height=dp(22), size_hint_y=None, halign='left'))
        corpo.add_widget(lbl(pergunta, sz=13, cor=UI_TEXT, halign='left', h=dp(56)))
        corpo.add_widget(sep())

        def _responder(opcao_txt, tipo_tag, *_):
            mv.dismiss()
            try:
                _j=screen_ref.manager.jogo
                _j.ganhar_reputacao('entrevista_carisma' if tipo_tag in
                    ('moral','otimista','ambicioso','grato','animado')
                    else 'resposta_entrevista')
            except Exception: pass
            on_fechar()

        for txt, tag in q['opcoes']:
            b = btn_secondary(txt, cb=lambda *_, t=txt, tg=tag: _responder(t,tg))
            corpo.add_widget(b)

    outer.add_widget(corpo)
    mv.add_widget(outer)
    mv.open()


# ═══════════════════════════════════════════════════════════════════════════════
#  HISTÓRICO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaHistorico(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(T('menu_historico'),'📜'))
        root.add_widget(sep()); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        if not jogo.historico:
            box.add_widget(spacer(40))
            box.add_widget(lbl(T('nenhuma_corrida'),sz=16,cor=UI_DIM,halign='center'))
        else:
            for semana,res in reversed(jogo.historico[-20:]):
                c=card(h=dp(58),bg=UI_CARD)
                c.add_widget(lbl(f'{T("sem")} {semana}',sz=13,cor=UI_GOLD,bold=True,h=dp(22)))
                c.add_widget(lbl(res[:90]+('…' if len(res)>90 else ''),sz=12,cor=UI_TEXT,h=dp(22)))
                box.add_widget(c)


# ═══════════════════════════════════════════════════════════════════════════════
#  CALENDÁRIO
# ═══════════════════════════════════════════════════════════════════════════════
class TelaCalendario(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(f'Calendário — Sem {jogo.semana}','📅'))
        root.add_widget(sep()); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        for i in range(8):
            sem=jogo.semana+i
            if i==0:     txt,bg='🏆 Semana '+str(sem)+': CORRIDA ATUAL',UI_GOLD_BG
            elif i%3==0: txt,bg='🎪 Semana '+str(sem)+': Especial (x2)',UI_GREEN_BG
            else:        txt,bg='🏁 Semana '+str(sem)+': Corrida',UI_CARD
            c=card(h=dp(42),bg=bg)
            c.add_widget(lbl(txt,sz=14,cor=UI_GOLD if i==0 else UI_TEXT,h=dp(28)))
            box.add_widget(c)


# ═══════════════════════════════════════════════════════════════════════════════
#  APOSTAS
# ═══════════════════════════════════════════════════════════════════════════════
class TelaApostas(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela('Apostas','💰'))
        root.add_widget(sep())

        sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(14),dp(10))

        odds_card=card(h=dp(48),bg=UI_CARD3)
        odds_card.add_widget(lbl('🥇 x3.0   🥈 x2.0   🥉 x1.5',sz=14,cor=UI_TEXT,
                                  halign='center',h=dp(32)))
        box.add_widget(odds_card)

        if jogo.cavalo_apostado:
            a=card(h=dp(44),bg=UI_GREEN_BG)
            a.add_widget(lbl(f'✅ Aposta ativa: {jogo.valor_aposta} Ouro em {jogo.cavalo_apostado.nome}',
                              sz=14,cor=UI_GREEN,h=dp(28)))
            box.add_widget(a)

        self.val=TextInput(hint_text=f'💰 {T("valor_aposta_hint")}',multiline=False,
                           background_color=(0.11,0.11,0.19,1),foreground_color=UI_TEXT,
                           cursor_color=UI_GOLD,font_size=dp(22),
                           size_hint_y=None,height=dp(54))
        box.add_widget(self.val); box.add_widget(lbl(T('escolha_cavalo'),sz=13,cor=UI_DIM,h=dp(26)))

        todos=(jogo.cavalos_mercado+jogo.cavalos_jogador)[:12]
        for cav in todos:
            rd=RACAS.get(cav.raca,{})
            row=BoxLayout(size_hint_y=None,height=dp(50),spacing=dp(8),padding=(dp(8),dp(4)))
            _rounded_bg(row,UI_CARD,8)
            dot=Widget(size_hint=(None,None),size=(dp(14),dp(14)))
            with dot.canvas:
                Color(*cav.cor); e=Ellipse(pos=dot.pos,size=dot.size)
            dot.bind(pos=lambda w,v,ee=e: setattr(ee,'pos',v))
            row.add_widget(dot)
            row.add_widget(_elbl(f"{rd.get('emoji','🐴')} {cav.nome}  ⚡{cav.vel_base:.1f}",
                                  font_size=dp(13), color=UI_TEXT,
                                  height=dp(38), size_hint_y=None))
            row.add_widget(btn_primary('🏆 Apostar',cb=lambda _,c=cav: self._apostar(c,jogo),h=dp(38)))
            box.add_widget(row)


    def _apostar(self,cav,jogo):
        try: val=int(self.val.text)
        except: return
        if val<=0 or val>jogo.dinheiro: return
        jogo.dinheiro-=val; jogo.cavalo_apostado=cav; jogo.valor_aposta=val
        self.manager.current='corrida'


# ═══════════════════════════════════════════════════════════════════════════════
#  FUNCIONÁRIOS
# ═══════════════════════════════════════════════════════════════════════════════
class TelaFuncionarios(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self,UI_BG)
        jogo=self.manager.jogo
        custo=sum(f.salario for f in jogo.funcionarios)
        root=BoxLayout(orientation='vertical',padding=0,spacing=0)
        self.add_widget(root)
        root.add_widget(titulo_tela(f'{T("funcionarios_titulo")}  —  {custo} Ouro/sem','👔'))
        root.add_widget(sep()); sv,box=mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding=(dp(12),dp(8))
        for func in FUNCIONARIOS:
            cont=func in jogo.funcionarios
            c=card(h=dp(104),bg=UI_GREEN_BG if cont else UI_CARD2)
            if cont: c.add_widget(_accent_bar(c,UI_GREEN))
            header=BoxLayout(size_hint_y=None,height=dp(30))
            header.add_widget(_elbl(f'{func.emoji} {func.nome}', font_size=dp(16),
                                      color=UI_TEXT, height=dp(28), size_hint_y=None))
            header.add_widget(Label(text=f'{func.salario} Ouro/sem',font_size=dp(14),color=UI_GOLD))
            c.add_widget(header)
            c.add_widget(lbl(func.efeito,sz=12,cor=UI_DIM,h=dp(22)))
            if cont:
                c.add_widget(btn_danger(f'❌ {T("demitir")}',cb=lambda *_,f=func: self._demitir(f,jogo),h=dp(36)))
            else:
                c.add_widget(btn_success(f'✅ {T("contratar_btn")} {func.salario} {T("salario_sem")}',
                                          cb=lambda *_,f=func: self._contratar(f,jogo),h=dp(36)))
            box.add_widget(c)

    def _contratar(self,f,jogo):
        if f in jogo.funcionarios: return
        if jogo.dinheiro < f.salario:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as _PL
            Popup(title='Sem Ouro',
                  content=_PL(text=f'Precisa de {f.salario} Ouro para contratar!',
                              halign='center',color=UI_RED),
                  size_hint=(0.75,0.25)).open(); return
        jogo.dinheiro -= f.salario   # taxa de contratação = 1 salário
        jogo.funcionarios.append(f)
        self.on_enter()
    def _demitir(self,f,jogo):
        if f in jogo.funcionarios: jogo.funcionarios.remove(f)
        self.on_enter()


# ═══════════════════════════════════════════════════════════════════════════════
#  TELA RECORDES
# ═══════════════════════════════════════════════════════════════════════════════
class TelaRecordes(Screen):
    def on_enter(self):
        self.clear_widgets(); _set_bg(self, UI_BG)
        jogo  = self.manager.jogo
        nome_jog = getattr(self.manager, 'nome_jogador', 'Haras')
        root  = BoxLayout(orientation='vertical', padding=0, spacing=0)
        self.add_widget(root)

        # HUD
        hud = BoxLayout(size_hint_y=None, height=dp(52), padding=(dp(8),dp(8)), spacing=dp(8))
        _set_bg(hud, UI_CARD)
        hud.add_widget(lbl('🏅 RECORDES', sz=17, cor=UI_GOLD, bold=True, h=dp(52)))
        root.add_widget(hud)
        root.add_widget(sep())

        sv, box = mk_scroll(); root.add_widget(sv)
        root.add_widget(barra_voltar(self.manager))
        box.padding = (dp(14), dp(10))

        # ── Gera dados dos haras concorrentes ────────────────────────────────
        import random as _rnd
        _rnd.seed(42 + jogo.semana // 4)

        NOMES_HARAS = [
            'Rancho Aurora','Haras Beltrano','Estábulo Norte',
            'Haras Vitória','Rancho Estrela','Estábulo Sul',
            'Haras Imperial','Rancho Ouro Verde','Haras do Vale',
        ]

        # Dados do jogador
        patrimonio_jog = (jogo.dinheiro
                          + sum(c.preco for c in jogo.cavalos_jogador)
                          + jogo.haras_nivel * 5000)
        cavalos_jog    = len(jogo.cavalos_jogador)
        vitorias_jog   = sum(c.vitorias for c in jogo.cavalos_jogador)
        caro_jog       = max(jogo.cavalos_jogador, key=lambda x: x.preco) if jogo.cavalos_jogador else None

        # Dados NPC — gerados deterministicamente
        npcs = []
        _nomes_cav = [
            'Pé de Vento','Relâmpago','Trovão','Estrela do Sul','Rosa Brava',
            'Pegasus','Raio Negro','Tempestade','Prata Viva','Noite Eterna',
            'Furacão','Cometa','Meteoro','Brisa Real','Vulcão',
            'Ouro Vivo','Diamante','Safira','Esmeralda','Rubi',
            'Sol Nascente','Lua Cheia','Vento Norte','Mar Bravio','Serra Alta',
        ]
        for i, nome in enumerate(NOMES_HARAS):
            _rnd.seed(i * 31 + jogo.semana // 8)
            n_cav   = _rnd.randint(2, 8)
            pat     = _rnd.randint(8000, 120000) + jogo.semana * _rnd.randint(50, 200)
            vits    = _rnd.randint(0, jogo.semana // 2 + 1)
            caro_v  = _rnd.randint(1500, 80000)
            nome_cav = _nomes_cav[(i * 7 + jogo.semana // 4) % len(_nomes_cav)]
            npcs.append({'nome': nome, 'patrimonio': pat,
                         'cavalos': n_cav, 'vitorias': vits,
                         'caro': caro_v, 'nome_cav': nome_cav})

        # ── Seção 1: HARAS MAIS RICOS ────────────────────────────────────────
        def _section(titulo, cor):
            box.add_widget(lbl(titulo, sz=15, cor=cor, bold=True, h=dp(30)))
            box.add_widget(sep())

        def _linha_rank(rank, nome, valor, destaque=False):
            row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8),
                            padding=(dp(8),dp(4)))
            _rounded_bg(row, UI_GOLD_BG if destaque else (UI_CARD if rank%2==0 else UI_CARD2))
            med = ['🥇','🥈','🥉'][rank-1] if rank <= 3 else f'{rank}.'
            row.add_widget(lbl(str(med), sz=14,
                               cor=UI_GOLD if rank<=3 else UI_DIM, h=dp(34)))
            row.add_widget(lbl(nome, sz=13, cor=UI_GOLD if destaque else UI_TEXT,
                               bold=destaque, h=dp(34)))
            row.add_widget(lbl(valor, sz=13, cor=UI_GREEN if destaque else UI_DIM,
                               h=dp(34), halign='right'))
            return row

        # ── RANKING: PATRIMÔNIO ──────────────────────────────────────────────
        _section('💰  Haras Mais Ricos  —  Patrimônio Total', UI_GOLD)
        todos_pat = sorted(
            npcs + [{'nome': f'🏆 {nome_jog}', 'patrimonio': patrimonio_jog,
                     'cavalos': cavalos_jog, 'vitorias': vitorias_jog,
                     'caro': caro_jog.preco if caro_jog else 0}],
            key=lambda x: x['patrimonio'], reverse=True
        )
        rank_jog_pat = next(i+1 for i,h in enumerate(todos_pat) if '🏆' in h['nome'])
        for i, h in enumerate(todos_pat[:10]):
            dest = '🏆' in h['nome']
            box.add_widget(_linha_rank(i+1, h['nome'],
                           f'{h["patrimonio"]:,} Ouro', dest))
        if rank_jog_pat > 10:
            box.add_widget(lbl(f'  {T("sua_posicao_rank")} {rank_jog_pat}° — {patrimonio_jog:,} {T("item_ouro")}',
                               sz=12, cor=UI_GOLD, h=dp(26)))
        box.add_widget(spacer(10))

        # ── RANKING: QUANTIDADE DE CAVALOS ───────────────────────────────────
        _section('🐎  Maior Plantel  —  Qtd. de Cavalos', UI_BLUE)
        todos_cav = sorted(
            npcs + [{'nome': f'🏆 {nome_jog}', 'patrimonio': patrimonio_jog,
                     'cavalos': cavalos_jog, 'vitorias': vitorias_jog,
                     'caro': caro_jog.preco if caro_jog else 0}],
            key=lambda x: x['cavalos'], reverse=True
        )
        for i, h in enumerate(todos_cav[:8]):
            dest = '🏆' in h['nome']
            emoji_cav = '🐎' * min(5, h['cavalos'])
            box.add_widget(_linha_rank(i+1, h['nome'],
                           f'{h["cavalos"]} cavalos  {emoji_cav}', dest))
        box.add_widget(spacer(10))

        # ── RANKING: CAVALO MAIS CARO ────────────────────────────────────────
        _section('💰  Cavalos Mais Valiosos', UI_PURPLE)
        todos_caro = []
        for h in npcs:
            todos_caro.append({'haras': h['nome'], 'preco': h['caro'],
                               'nome_cav': h.get('nome_cav','Campeão')})
        if jogo.cavalos_jogador:
            mc = max(jogo.cavalos_jogador, key=lambda x: x.preco)
            todos_caro.append({'haras': f'🏆 {nome_jog}',
                               'preco': mc.preco, 'nome_cav': mc.nome})
        todos_caro.sort(key=lambda x: x['preco'], reverse=True)
        for i, h in enumerate(todos_caro[:8]):
            dest = '🏆' in h['haras']
            box.add_widget(_linha_rank(i+1,
                           f'{h["haras"]}  —  {h["nome_cav"]}',
                           f'{h["preco"]:,} Ouro', dest))
        box.add_widget(spacer(10))

        # ── RANKING: VITÓRIAS GLOBAIS ────────────────────────────────────────
        _section('🏆  Mais Vitórias Globais', (0.82,0.52,0.20,1))
        todos_vit = sorted(
            npcs + [{'nome': f'🏆 {nome_jog}', 'patrimonio': patrimonio_jog,
                     'cavalos': cavalos_jog, 'vitorias': vitorias_jog,
                     'caro': caro_jog.preco if caro_jog else 0}],
            key=lambda x: x['vitorias'], reverse=True
        )
        rank_jog_vit = next(i+1 for i,h in enumerate(todos_vit) if '🏆' in h['nome'])
        for i, h in enumerate(todos_vit[:10]):
            dest = '🏆' in h['nome']
            box.add_widget(_linha_rank(i+1, h['nome'],
                           f'{h["vitorias"]} vitórias', dest))
        if rank_jog_vit > 10:
            box.add_widget(lbl(f'  {T("sua_posicao_rank")} {rank_jog_vit}° — {vitorias_jog} {T("vitorias")}',
                               sz=12, cor=UI_GOLD, h=dp(26)))
        box.add_widget(spacer(16))

        # ── Seu resumo ───────────────────────────────────────────────────────
        box.add_widget(sep())
        box.add_widget(lbl(f'📈 {T("resumo_haras")}', sz=15, cor=UI_TEXT, bold=True, h=dp(30)))
        resumo_card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(110),
                                padding=(dp(12),dp(8)), spacing=dp(4))
        _rounded_bg(resumo_card, (0.07,0.07,0.14,1))
        resumo_card.add_widget(lbl(f'💰 Patrimônio:  {patrimonio_jog:,} Ouro  (#{rank_jog_pat}° no ranking)',
                                   sz=13, cor=UI_GOLD, h=dp(22)))
        resumo_card.add_widget(lbl(f'🐎 Cavalos:  {cavalos_jog}  |  🏆 Vitórias totais:  {vitorias_jog}  (#{rank_jog_vit}°)',
                                   sz=13, cor=UI_TEXT, h=dp(22)))
        if caro_jog:
            resumo_card.add_widget(lbl(f'💰 Cavalo mais caro:  {caro_jog.nome}  —  {caro_jog.preco:,} Ouro',
                                       sz=13, cor=UI_PURPLE, h=dp(22)))
        resumo_card.add_widget(lbl(f'🏠 {T("haras_nivel_sem")} {jogo.haras_nivel}  |  {T("sem_label")} {jogo.semana}',
                                   sz=12, cor=UI_DIM, h=dp(18)))
        box.add_widget(resumo_card)
        box.add_widget(spacer(10))

        root.add_widget(btn_secondary(
            f'🔧  Voltar', cb=lambda *_: setattr(self.manager,'current','menu')))


# ═══════════════════════════════════════════════════════════════════════════════
#  TUTORIAL (ONBOARDING)
# ═══════════════════════════════════════════════════════════════════════════════
class TelaTutorial(Screen):
    """Tela de boas-vindas exibida apenas no primeiro jogo.
    5 cards deslizáveis com dicas essenciais.
    """
    _STEPS = [
        {
            'emoji':  '🏇',
            'titulo_pt': 'Bem-vindo ao Project Horse!',
            'titulo_en': 'Welcome to Project Horse!',
            'titulo_es': '¡Bienvenido a Project Horse!',
            'texto_pt': 'Você é o novo dono de um haras. Compre cavalos, faça-os correr e construa o haras mais famoso do Brasil!',
            'texto_en': 'You are the new owner of a stable. Buy horses, race them and build the most famous stable in Brazil!',
            'texto_es': 'Eres el nuevo dueño de un haras. ¡Compra caballos, hazlos correr y construye el haras más famoso!',
            'cor': (0.10, 0.06, 0.22, 1),
        },
        {
            'emoji':  '🏆',
            'titulo_pt': 'Corridas & Campeonatos',
            'titulo_en': 'Races & Championships',
            'titulo_es': 'Carreras y Campeonatos',
            'texto_pt': 'Vença corridas para ganhar Ouro e reputação. Entre em Campeonatos para prêmios muito maiores. Cavalos com mais estrelas são mais rápidos!',
            'texto_en': 'Win races to earn Gold and reputation. Join Championships for much bigger prizes. More star horses run faster!',
            'texto_es': 'Gana carreras para obtener Oro y reputación. ¡Los Campeonatos tienen premios mucho mayores!',
            'cor': (0.08, 0.14, 0.08, 1),
        },
        {
            'emoji':  '💰',
            'titulo_pt': 'Cuide do seu Ouro',
            'titulo_en': 'Manage your Gold',
            'titulo_es': 'Cuida tu Oro',
            'texto_pt': 'A cada semana você paga manutenção dos cavalos e funcionários. Não deixe o saldo zerar! Use o Banco para empréstimos de emergência.',
            'texto_en': 'Every week you pay horse maintenance and staff costs. Don\'t go broke! Use the Bank for emergency loans.',
            'texto_es': 'Cada semana pagas mantenimiento y empleados. ¡No te quedes sin Oro! Usa el Banco en emergencias.',
            'cor': (0.14, 0.10, 0.02, 1),
        },
        {
            'emoji':  '🐎',
            'titulo_pt': 'Evolua seu Haras',
            'titulo_en': 'Upgrade your Stable',
            'titulo_es': 'Mejora tu Haras',
            'texto_pt': 'Compre mais baias, contrate Funcionários (treinador, tratador, nutricionista) e cruze cavalos para criar campeões únicos!',
            'texto_en': 'Buy more stalls, hire Staff (trainer, groom, nutritionist) and breed horses to create unique champions!',
            'texto_es': 'Compra establos, contrata Empleados y cruza caballos para crear campeones únicos.',
            'cor': (0.06, 0.10, 0.18, 1),
        },
        {
            'emoji':  '💡',
            'titulo_pt': 'Dica de Campeão',
            'titulo_en': 'Champion Tip',
            'titulo_es': 'Consejo de Campeón',
            'texto_pt': 'Fique de olho no Leilão! Ele aparece a cada 8 semanas com cavalos 4 e 5 estrelas raros. Também assine patrocinadores para renda extra semanal.',
            'texto_en': 'Watch the Auction! It appears every 8 weeks with rare 4 and 5-star horses. Also sign sponsors for weekly extra income.',
            'texto_es': '¡Atento a la Subasta! Aparece cada 8 semanas con caballos raros. Firma patrocinadores para ingresos extra.',
            'cor': (0.14, 0.04, 0.12, 1),
        },
    ]

    def on_enter(self):
        self.clear_widgets()
        _set_bg(self, (0.04, 0.04, 0.08, 1))
        self._step = 0
        self._build()

    def _build(self):
        self.clear_widgets()
        step  = self._STEPS[self._step]
        total = len(self._STEPS)
        lang  = get_lang()

        root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        _set_bg(self, step['cor'])
        self.add_widget(root)

        # Topo: pontos de progresso
        dots_box = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8),
                              padding=(dp(0), dp(10)))
        for i in range(total):
            dot = Widget(size_hint=(None, None), size=(dp(10 if i==self._step else 7),
                                                        dp(10 if i==self._step else 7)))
            cor_dot = UI_GOLD if i == self._step else (0.35, 0.35, 0.45, 1)
            with dot.canvas:
                Color(*cor_dot)
                dot._ell = Ellipse(pos=dot.pos, size=dot.size)
            dot.bind(pos=lambda w, v: setattr(w._ell, 'pos', v),
                     size=lambda w, v: setattr(w._ell, 'size', v))
            dots_box.add_widget(Widget())  # espaçador flex
            dots_box.add_widget(dot)
        dots_box.add_widget(Widget())
        root.add_widget(dots_box)

        # Emoji grande
        root.add_widget(Widget())
        root.add_widget(_elbl(step['emoji'], font_size=dp(88), color=UI_TEXT,
                              height=dp(110), size_hint_y=None, halign='center'))

        # Título
        titulo = step.get(f'titulo_{lang}', step['titulo_pt'])
        root.add_widget(Label(text=f'[b]{titulo}[/b]', markup=True,
                              font_size=dp(24), color=UI_GOLD,
                              size_hint_y=None, height=dp(64),
                              halign='center', valign='middle',
                              text_size=(Window.width - dp(40), None)))

        # Texto explicativo
        texto = step.get(f'texto_{lang}', step['texto_pt'])
        txt_lbl = Label(text=texto, font_size=dp(16), color=UI_TEXT,
                        size_hint_y=None, halign='center', valign='middle',
                        padding=(dp(20), 0))
        txt_lbl.bind(width=lambda w, v: setattr(w, 'text_size', (v - dp(40), None)))
        txt_lbl.bind(texture_size=lambda w, v: setattr(w, 'height', v[1] + dp(16)))
        root.add_widget(txt_lbl)

        root.add_widget(Widget())

        # Botões navegação
        nav = BoxLayout(size_hint_y=None, height=dp(56),
                         padding=(dp(16), dp(8)), spacing=dp(12))

        if self._step > 0:
            nav.add_widget(btn_secondary(f'◀ {T("anterior")}',
                                          cb=self._anterior, h=dp(40)))
        else:
            nav.add_widget(Widget())

        # Contador
        nav.add_widget(lbl(f'{self._step+1}/{total}', sz=13,
                           cor=UI_DIM, h=dp(40)))

        if self._step < total - 1:
            nav.add_widget(btn_primary(f'{T("proximo")} ▶',
                                        cb=self._proximo, h=dp(40)))
        else:
            nav.add_widget(btn_primary(f'🎮 {T("novo_jogo")}!',
                                        cb=self._comecar, h=dp(40)))

        root.add_widget(nav)

        # Pular tutorial
        pular = Button(text=f'({T("voltar")})',
                       background_normal='', background_color=(0,0,0,0),
                       color=UI_DIM, font_size=dp(12),
                       size_hint_y=None, height=dp(28))
        pular.bind(on_release=self._comecar)
        root.add_widget(pular)
        root.add_widget(spacer(6))

    def _proximo(self, *_):
        _snd.tocar('click')
        self._step = min(self._step + 1, len(self._STEPS) - 1)
        self._build()

    def _anterior(self, *_):
        _snd.tocar('click')
        self._step = max(self._step - 1, 0)
        self._build()

    def _comecar(self, *_):
        _snd.tocar('click')
        # Garante que o menu está construído
        self.manager.get_screen('menu')._construir()
        self.manager.current = 'menu'
