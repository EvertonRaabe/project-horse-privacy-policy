import os, sys

# ─────────────────────────────────────────────────────────────────────────────
#  DETECÇÃO DO ARQUIVO DE FONTE
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _validar_fonte(path):
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
        validos = [b'\x00\x01\x00\x00', b'true', b'OTTO', b'ttcf']
        return any(magic.startswith(v) for v in validos)
    except Exception:
        return False

def _achar_fonte():
    for nome in ['NotoSans-Regular.ttf', 'DejaVuSans.ttf']:
        p = os.path.join(BASE_DIR, nome)
        if os.path.exists(p) and _validar_fonte(p):
            print(f'[FONTE] Usando fonte local: {nome}')
            return p
    for p in [
        '/system/fonts/DroidSans.ttf',
        '/system/fonts/DroidSansFallback.ttf',
        '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
    ]:
        if os.path.exists(p):
            print(f'[FONTE] Usando: {os.path.basename(p)}')
            return p
    return None

FONTE_PATH = _achar_fonte()

from kivy.core.text import LabelBase

def _registrar(path):
    if not path:
        return
    try:
        for nome in ('Roboto', 'RobotoMono', 'RobotoThin', 'RobotoLight', 'RobotoMedium'):
            try:
                LabelBase.register(nome, fn_regular=path, fn_bold=path,
                                   fn_italic=path, fn_bolditalic=path)
            except Exception:
                pass
        print(f'[FONTE] Registrada: {os.path.basename(path)}')
    except Exception as e:
        print(f'[FONTE] Erro: {e}')

_registrar(FONTE_PATH)

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivy.core.window import Window
from game_logic import Jogo
from screens import (SplashScreen, LoginScreen, TelaMenu,
                     TelaCorrida, TelaCavalos, TelaMercado,
                     TelaGenealogia, TelaCruzamento, TelaHistorico,
                     TelaCalendario, TelaApostas, TelaFuncionarios,
                     TelaBanco, TelaPatrocinador, TelaCampeonato,
                     TelaTrofeus, TelaConfig, TelaLeilao, TelaRecordes,
                     TelaTutorial)


class Gerenciador(ScreenManager):
    _TELAS_MENU = {
        'corrida', 'cavalos', 'mercado', 'patrocinador', 'banco', 'campeonato',
        'genealogia', 'cruzamento', 'historico', 'calendario', 'apostas',
        'funcionarios', 'trofeus', 'config', 'leilao', 'recordes', 'tutorial',
    }

    def __init__(self, **kwargs):
        super().__init__(transition=FadeTransition(duration=0.20), **kwargs)
        self.jogo = Jogo()
        self.nome_jogador = 'Treinador'
        self.tutorial_pendente = False
        Window.bind(on_keyboard=self._tecla_voltar)
        for cls, name in [
            (SplashScreen,     'splash'),
            (LoginScreen,      'login'),
            (TelaMenu,         'menu'),
            (TelaCorrida,      'corrida'),
            (TelaCavalos,      'cavalos'),
            (TelaMercado,      'mercado'),
            (TelaPatrocinador, 'patrocinador'),
            (TelaBanco,        'banco'),
            (TelaCampeonato,   'campeonato'),
            (TelaGenealogia,   'genealogia'),
            (TelaCruzamento,   'cruzamento'),
            (TelaHistorico,    'historico'),
            (TelaCalendario,   'calendario'),
            (TelaApostas,      'apostas'),
            (TelaFuncionarios, 'funcionarios'),
            (TelaTrofeus,      'trofeus'),
            (TelaConfig,       'config'),
            (TelaLeilao,       'leilao'),
            (TelaRecordes,     'recordes'),
            (TelaTutorial,     'tutorial'),
        ]:
            self.add_widget(cls(name=name))

    def _tecla_voltar(self, window, key, *args):
        if key not in (27, 1001):
            return False
        tela = self.current
        if tela in self._TELAS_MENU:
            self.current = 'menu'
            return True
        if tela == 'corrida_visual':
            return True
        if tela == 'menu':
            self._confirmar_saida()
            return True
        return True  # login/splash — consome sem fechar

    def _confirmar_saida(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label as _L
        from kivy.uix.button import Button as _B
        box = BoxLayout(orientation='vertical', padding=16, spacing=12)
        box.add_widget(_L(text='Sair do jogo?', font_size=18,
                          color=(1,1,1,1), halign='center',
                          size_hint_y=None, height=40))
        btns = BoxLayout(size_hint_y=None, height=48, spacing=10)
        pop = Popup(title='', content=box, size_hint=(0.7, 0.32),
                    separator_height=0, background_color=(0,0,0,0.8))
        b_sim = _B(text='Sair', background_normal='',
                   background_color=(0.7,0.1,0.1,1), color=(1,1,1,1))
        b_nao = _B(text='Cancelar', background_normal='',
                   background_color=(0.1,0.4,0.1,1), color=(1,1,1,1))
        b_sim.bind(on_release=lambda *_: (
            pop.dismiss(),
            __import__('kivy.app', fromlist=['App']).App.get_running_app().stop()
        ))
        b_nao.bind(on_release=lambda *_: pop.dismiss())
        btns.add_widget(b_sim)
        btns.add_widget(b_nao)
        box.add_widget(btns)
        pop.open()


class ProjectHorseApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette  = "Green"
        self.theme_cls.theme_style     = "Dark"
        Window.clearcolor              = (0.04, 0.04, 0.08, 1)
        return Gerenciador()

    def on_start(self):
        _registrar(FONTE_PATH)
        # Inicializa AdMob após o app estar pronto
        try:
            from admob import inicializar
            inicializar()
        except Exception as e:
            print(f'[AdMob] Erro ao inicializar: {e}')


if __name__ == '__main__':
    ProjectHorseApp().run()
