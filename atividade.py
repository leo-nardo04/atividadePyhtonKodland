# Escolhi o gênero Platformer
# Fiz diversos comentários ao longo do código para usar de de apoio, pois há coisas novas para mim

# Tela
WIDTH = 800
HEIGHT = 600

# Física
GRAVITY = 1
JUMP_STRENGTH = -20

# Listas de Jogo
platforms = []
enemies = []


class Player:
    def __init__(self, x, y, idle_frames, walk_frames):
        # Guarda as listas de animação
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames

        # O Actor começa com o primeiro frame de "parado"
        self.actor = Actor(self.idle_frames[0], (x, y))

        self.vy = 0
        self.on_ground = False

        # --- Novas variáveis para Animação (Req 7 e 8) ---
        self.is_walking = False
        self.facing_direction = 1  # 1 = direita, -1 = esquerda

        self.animation_timer = 0
        self.current_frame = 0
        self.actor.flip_x = True

    def draw(self):
        self.actor.draw()

    def update(self):
        """
        O 'update' principal agora delega para
        funções de movimento e animação.
        """
        self.update_movement()
        self.update_animation()

    def update_movement(self):
        # Começamos assumindo que o jogador não está andando
        self.is_walking = False

        # Movimento horizontal
        if keyboard.left:
            self.actor.x -= 5
            self.is_walking = True
            self.facing_direction = -1  # Marcamos que está virado p/ esquerda
        elif keyboard.right:
            self.actor.x += 5
            self.is_walking = True
            self.facing_direction = 1  # Marcamos que está virado p/ direita

        # --- Gravidade e Colisão com Plataforma
        self.vy += GRAVITY
        self.actor.y += self.vy
        self.on_ground = False
        for platform in platforms:
            if self.actor.colliderect(platform):
                if self.vy > 0:
                    self.actor.bottom = platform.top
                    self.vy = 0
                    self.on_ground = True
                    break

        # Lógica do Pulo
        if (keyboard.space or keyboard.up) and self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False

    def update_animation(self):
        # 'self.animation_timer' age como um 'delay'
        # Aumentamos 1 a cada frame (60x por segundo)
        self.animation_timer += 1
        # A cada 10 frames, trocamos a imagem
        # (Ajuste o '10' para animar mais rápido ou mais devagar)

        if self.animation_timer % 8 == 0:
            self.current_frame += 1  # Avança para o próximo frame
            # Decide qual lista de animação usar
            if self.is_walking:
                active_list = self.walk_frames
            else:
                active_list = self.idle_frames

            # Reseta o contador de frames se chegar ao fim da lista
            # current_frame variável 'i' que percorre o vetor de animação, respeitando a ordem
            if self.current_frame >= len(active_list):
                self.current_frame = 0

            # Define a imagem do Actor para o novo frame
            new_image = active_list[self.current_frame]
            self.actor.image = new_image

        # --- Espelhar a Imagem ---
        # Isso 'vira' o sprite sem precisar de imagens 'left'
        if self.facing_direction == -1:
            self.actor.flip_x = True  # Vira horizontalmente
        else:
            self.actor.flip_x = False  # Normal


class Enemy:
    def __init__(self, image_file, x, y, patrol_range=80):
        self.actor = Actor(image_file, (x, y))
        self.speed = 2  # Velocidade corrigida
        self.direction = 1
        self.patrol_min_x = x - patrol_range
        self.patrol_max_x = x + patrol_range

    def draw(self):
        self.actor.draw()

    def update(self):
        self.actor.x += self.speed * self.direction

        if self.actor.right > self.patrol_max_x:
            self.direction = -1  # Apenas inverte a direção
        elif self.actor.left < self.patrol_min_x:
            self.direction = 1


# -----------------------------------------------------------------
try:
    player_idle_list = ['astro_idle_1', 'astro_idle_2']
    player_walk_list = ['astro_walk_1', 'astro_walk_2']

    player = Player(100, 300, player_idle_list, player_walk_list)

    # 1. Construindo o Chão...
    for i in range(13):
        x_pos = 32 + (i * 64)
        y_pos = 568
        chao_bloco = Actor('chao', (x_pos, y_pos))
        platforms.append(chao_bloco)  # (Renomeado)

    # 2. Construindo a Plataforma 1...
    for i in range(3):
        x_pos = 132 + (i * 64)
        y_pos = 400
        bloco = Actor('plataforma', (x_pos, y_pos))
        platforms.append(bloco)  # (Renomeado)

    # 3. Construindo a Plataforma 2...
    for i in range(4):
        x_pos = 532 + (i * 64)
        y_pos = 250
        bloco = Actor('plataforma', (x_pos, y_pos))
        platforms.append(bloco)

    ### 4. Criando Inimigos (Renomeado) ###
    enemy_1 = Enemy('inimigo', 550, 193)
    enemies.append(enemy_1)

    enemy_2 = Enemy('inimigo', 300, 511)
    enemies.append(enemy_2)

except FileNotFoundError as e:
    print(f"\n--- ERRO ---")
    print(f"Não consegui encontrar um arquivo de imagem: {e.filename}")
    print("Verifique se todas as imagens (chao, plataforma, inimigo, astro_idle_*, astro_walk_*) estão na pasta 'images/'")
    print("------------\n")
    quit()
# -----------------------------------------------------------------


def draw():
    screen.clear()

    for platform in platforms:
        platform.draw()

    for enemy in enemies:
        enemy.draw()

    player.draw()


def update():
    player.update()

    for enemy in enemies:
        enemy.update()
        if player.actor.colliderect(enemy.actor):
            print("Você foi pego!")
            player.actor.pos = (100, 300)
            player.vy = 0
