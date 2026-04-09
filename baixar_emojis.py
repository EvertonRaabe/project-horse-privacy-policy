"""
baixar_emojis.py — Project Horse
Execute UMA VEZ no PC para baixar os 68 PNGs de emoji do Twemoji.
Depois coloque a pasta 'emoji/' junto com os outros arquivos do projeto.

Uso:
    python baixar_emojis.py
"""

import os
import urllib.request
import sys

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
EMOJI_DIR = os.path.join(BASE_DIR, 'emoji')

# URL correta (repositório migrou para jdecked/twemoji)
CDN = 'https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/72x72/'

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
    # Novos
    '💵': '1f4b5', '💸': '1f4b8', '📺': '1f4fa', '🎲': '1f3b2',
    '⏳': '23f3',  '🔒': '1f512', '📊': '1f4ca', '🎯': '1f3af',
    '⭐': '2b50',  '💡': '1f4a1', '🎖': '1f396', '🌟': '1f31f',
}


def baixar():
    os.makedirs(EMOJI_DIR, exist_ok=True)
    total  = len(EMOJI_MAP)
    ok     = 0
    falhas = []

    print(f'Baixando {total} emojis para: {EMOJI_DIR}')
    print('─' * 50)

    for i, (char, cp) in enumerate(EMOJI_MAP.items(), 1):
        path = os.path.join(EMOJI_DIR, f'{cp}.png')

        if os.path.exists(path):
            ok += 1
            print(f'[{i:2}/{total}] {char}  JA EXISTE ({cp}.png)')
            continue

        url = f'{CDN}{cp}.png'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
            with open(path, 'wb') as f:
                f.write(data)
            ok += 1
            tamanho = len(data)
            print(f'[{i:2}/{total}] {char}  OK  ({cp}.png  {tamanho//1024}KB)')
        except Exception as ex:
            falhas.append((char, cp))
            print(f'[{i:2}/{total}] {char}  FALHOU: {ex}')

    print('─' * 50)
    print(f'OK: {ok}/{total} baixados com sucesso')

    if falhas:
        print(f'FALHAS: {len(falhas)}: {[f[1] for f in falhas]}')
        print('Tente rodar novamente.')
    else:
        print()
        print('Todos os emojis prontos!')
        print()
        print('Proximos passos:')
        print('  1. A pasta emoji/ ja esta na pasta do projeto')
        print('  2. Confirme que emoji_img.py tambem esta la')
        print('  3. No buildozer.spec adicione:')
        print('       source.include_exts = py,png,jpg,kv,atlas,ttf')
        print('       source.include_patterns = emoji/*.png')

    return ok, falhas


if __name__ == '__main__':
    baixar()
