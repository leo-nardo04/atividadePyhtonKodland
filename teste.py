# Define o tamanho da tela
WIDTH = 600
HEIGHT = 400

# Posição inicial do nosso círculo
# (Usaremos um dicionário para guardar x e y)
player = {
    'x': 0,
    'y': 200,
    'radius': 20
}


def draw():
    """Tudo o que deve ser desenhado na tela"""
    screen.clear()  # Limpa a tela (preenche com preto por padrão)

    # Desenha o nosso "jogador" como um círculo
    screen.draw.filled_circle(
        (player['x'], player['y']),  # Posição (x, y)
        player['radius'],           # Raio
        'white'                     # Cor
    )


def update():
    """Tudo o que deve ser atualizado (lógica do jogo)"""

    # Movimenta o jogador
    if keyboard.left:
        player['x'] -= 51
    elif keyboard.right:
        player['x'] += 15
    elif keyboard.up:
        player['y'] -= 15
    elif keyboard.down:
        player['y'] += 15

# ---
# Lembrete de como executar:
# 1. Salve este código (ex: teste.py)
# 2. Abra o terminal na mesma pasta
# 3. Digite: py -m pgzrun teste.py
# ---
