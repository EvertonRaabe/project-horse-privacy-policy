"""
emoji_img.py — Project Horse
Sistema de Emoji como Imagem PNG (Twemoji) para Kivy.
"""
import os, re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
EMOJI_DIR = os.path.join(BASE_DIR, 'emoji')

EMOJI_MAP = {
    '☀':  '2600',  '♀':  '2640',  '♂':  '2642',
    '⚕':  '2695',  '⚙':  '2699',  '⚠':  '26a0',  '⚡': '26a1',
    '✅': '2705',  '✨': '2728',  '❌': '274c',  '❤':  '2764',
    '🌧': '1f327', '🌬': '1f32c', '🌳': '1f333', '🌵': '1f335',
    '🌾': '1f33e', '🌿': '1f33f', '🍎': '1f34e', '🎨': '1f3a8',
    '🎪': '1f3aa', '🎮': '1f3ae', '🎰': '1f3b0', '🏁': '1f3c1',
    '🏅': '1f3c5', '🏆': '1f3c6', '🏇': '1f3c7', '🏋': '1f3cb',
    '🏟': '1f3df', '🏠': '1f3e0', '🏦': '1f3e6', '🐎': '1f40e',
    '🐴': '1f434', '👑': '1f451', '👔': '1f454', '👨': '1f468',
    '💀': '1f480', '💉': '1f489', '💊': '1f48a', '💞': '1f49e',
    '💨': '1f4a8', '💪': '1f4aa', '💰': '1f4b0', '💳': '1f4b3',
    '💾': '1f4be', '📂': '1f4c2', '📅': '1f4c5', '📈': '1f4c8',
    '📜': '1f4dc', '📰': '1f4f0', '🔧': '1f527', '🔨': '1f528',
    '🔩': '1f529', '🚪': '1f6aa', '🛒': '1f6d2', '🟢': '1f7e2',
    '🤝': '1f91d', '🥇': '1f947', '🥈': '1f948', '🥉': '1f949',
    '🥕': '1f955', '🥗': '1f957', '🦠': '1f9a0', '🦶': '1f9b6',
    '🧑': '1f9d1', '🧴': '1f9f4', '🩹': '1fa79', '🪮': '1faae',
    '💵': '1f4b5', '💸': '1f4b8', '📺': '1f4fa', '🎲': '1f3b2',
    '⏳': '23f3',  '🔒': '1f512', '📊': '1f4ca', '🎯': '1f3af',
    '⭐': '2b50',  '💡': '1f4a1', '🎖': '1f396', '🌟': '1f31f',
}

_EMOJI_CHARS = ''.join(re.escape(c) for c in EMOJI_MAP)
_SPLIT_RE    = re.compile(f'([{_EMOJI_CHARS}])')
TWEMOJI_CDN  = 'https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/72x72/'


def emoji_path(char):
    cp = EMOJI_MAP.get(char)
    if not cp: return None
    p = os.path.join(EMOJI_DIR, f'{cp}.png')
    return p if os.path.exists(p) else None


def tem_emoji(texto):
    return bool(_SPLIT_RE.search(str(texto)))


def _partes(texto):
    return [p for p in _SPLIT_RE.split(str(texto)) if p]


def make_emoji_row(text, font_size, color, bold=False, halign='center'):
    """
    Cria um BoxLayout horizontal com Images (emoji) e Labels (texto).
    NAO tem size_hint nem height — quem chama define isso no container.
    """
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label     import Label
    from kivy.uix.image     import Image

    img_sz = int(font_size * 1.1)
    row = BoxLayout(orientation='horizontal', spacing=4,
                    size_hint=(1, 1))

    for parte in _partes(text):
        if parte in EMOJI_MAP:
            path = emoji_path(parte)
            if path:
                row.add_widget(Image(
                    source=path,
                    size_hint=(None, 1),
                    width=img_sz,
                    allow_stretch=True,
                    keep_ratio=True,
                ))
            else:
                row.add_widget(Label(
                    text=parte, font_size=font_size, color=color,
                    size_hint=(None, 1), width=img_sz,
                ))
        else:
            txt = f'[b]{parte}[/b]' if bold else parte
            lbl = Label(
                text=txt, font_size=font_size, color=color,
                halign=halign, valign='middle',
                markup=bold, size_hint=(1, 1),
            )
            lbl.bind(size=lambda w, s: setattr(w, 'text_size', s))
            row.add_widget(lbl)

    return row


def make_emoji_box(text, font_size, color, bold, halign, height, size_hint_y):
    """Wrapper com height/size_hint_y para usar como Label."""
    from kivy.uix.boxlayout import BoxLayout
    box = BoxLayout(orientation='horizontal', spacing=4,
                    size_hint_y=size_hint_y, height=height)
    row = make_emoji_row(text, font_size, color, bold, halign)
    box.add_widget(row)
    return box


# ── EmojiButton: ButtonBehavior + BoxLayout (jeito correto no Kivy) ────────────
def make_emoji_button(txt, bg_color, text_color, font_size, height,
                      bold=True, border_color=None, cb=None,
                      size_hint_x=1, size_hint_y=None):
    """
    Cria um botão real com emoji como imagem.
    Usa ButtonBehavior + BoxLayout — o jeito correto no Kivy.
    """
    from kivy.uix.behaviors  import ButtonBehavior
    from kivy.uix.boxlayout  import BoxLayout
    from kivy.graphics        import Color, RoundedRectangle, Line

    class _EmojiBtn(ButtonBehavior, BoxLayout):
        def __init__(self, **kw):
            super().__init__(**kw)
            self._draw_bg()
            self.bind(pos=self._draw_bg, size=self._draw_bg)

        def _draw_bg(self, *_):
            self.canvas.before.clear()
            with self.canvas.before:
                Color(*bg_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp_val(8)])
                if border_color:
                    Color(*border_color)
                    Line(rounded_rectangle=(self.x, self.y,
                                            self.width, self.height, dp_val(8)),
                         width=1.2)

        def on_press(self):
            self.opacity = 0.7
            try:
                import sounds as _snd; _snd.tocar('click')
            except Exception: pass

        def on_release(self):
            self.opacity = 1.0
            if cb: cb(self)

    btn = _EmojiBtn(
        orientation='horizontal',
        size_hint_x=size_hint_x,
        size_hint_y=size_hint_y,
        height=height,
        padding=(dp_val(8), 0),
        spacing=dp_val(4),
    )
    row = make_emoji_row(txt, font_size, text_color, bold, halign='center')
    btn.add_widget(row)
    return btn


def dp_val(v):
    try:
        from kivy.metrics import dp
        return dp(v)
    except Exception:
        return v


def verificar_emojis():
    if not os.path.exists(EMOJI_DIR): return 0, len(EMOJI_MAP)
    ok = sum(1 for cp in EMOJI_MAP.values()
             if os.path.exists(os.path.join(EMOJI_DIR, f'{cp}.png')))
    return ok, len(EMOJI_MAP)


def baixar_todos(callback=None):
    import urllib.request
    os.makedirs(EMOJI_DIR, exist_ok=True)
    total, ok, falhas = len(EMOJI_MAP), 0, []
    for i, (char, cp) in enumerate(EMOJI_MAP.items(), 1):
        path = os.path.join(EMOJI_DIR, f'{cp}.png')
        if os.path.exists(path):
            ok += 1
            if callback: callback(i, total, cp)
            continue
        url = f'{TWEMOJI_CDN}{cp}.png'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as r: data = r.read()
            with open(path, 'wb') as f: f.write(data)
            ok += 1
        except Exception as ex:
            falhas.append((char, cp, str(ex)))
        if callback: callback(i, total, cp)
    return ok, falhas


def EmojiImage(emoji, size=(32, 32), **kwargs):
    """Widget Image com o PNG do emoji. Fallback para Label se PNG nao existe."""
    from kivy.uix.image import Image
    from kivy.uix.label import Label
    path = emoji_path(emoji)
    if path:
        return Image(source=path, size_hint=(None, None), size=size,
                     allow_stretch=True, keep_ratio=True, **kwargs)
    return Label(text=emoji, size_hint=(None, None), size=size,
                 font_size=min(size), **kwargs)
