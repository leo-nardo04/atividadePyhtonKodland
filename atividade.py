# Escolhi o genero Platformer
# pgzrun .\atividade.py

WIDTH = 800
HEIGHT = 600
GRAVITY = 1
JUMP_STRENGTH = -20

platforms = []
enemies = []
game_state = 'menu'
sound_on = True


class Player:
    def __init__(self, x, y, idle_frames_r, walk_frames_r, idle_frames_l, walk_frames_l):
        # Construtor do Player
        self.idle_frames_r = idle_frames_r
        self.walk_frames_r = walk_frames_r
        self.idle_frames_l = idle_frames_l
        self.walk_frames_l = walk_frames_l
        self.actor = Actor(self.idle_frames_r[0], (x, y))
        self.vy = 0
        self.on_ground = False
        self.is_walking = False
        self.facing_direction = 1
        self.animation_timer = 0
        self.current_frame = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.update_movement()
        self.update_animation()

    def update_movement(self):
        self.is_walking = False
        if keyboard.left:
            self.actor.x -= 5
            self.is_walking = True
            self.facing_direction = -1
        elif keyboard.right:
            self.actor.x += 5
            self.is_walking = True
            self.facing_direction = 1

        # Limites da Tela
        if self.actor.left < 0:
            self.actor.left = 0
        elif self.actor.right > WIDTH:
            self.actor.right = WIDTH

        # Fisica e Colisao
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
                elif self.vy < 0:
                    self.actor.top = platform.bottom
                    self.vy = 0
        if (keyboard.space or keyboard.up) and self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer % 8 == 0:
            self.current_frame += 1
            active_list = None
            if self.facing_direction == 1:
                if self.is_walking:
                    active_list = self.walk_frames_r
                else:
                    active_list = self.idle_frames_r
            else:
                if self.is_walking:
                    active_list = self.walk_frames_l
                else:
                    active_list = self.idle_frames_l
            if self.current_frame >= len(active_list):
                self.current_frame = 0
            new_image = active_list[self.current_frame]
            self.actor.image = new_image


class Enemy:
    def __init__(self, x, y, patrol_range, walk_frames_r, walk_frames_l):
        self.walk_frames_r = walk_frames_r
        self.walk_frames_l = walk_frames_l
        self.actor = Actor(self.walk_frames_r[0], (x, y))
        self.speed = 2
        self.direction = 1
        self.patrol_min_x = x - patrol_range
        self.patrol_max_x = x + patrol_range
        self.animation_timer = 0
        self.current_frame = 0

    def draw(self):
        self.actor.draw()

    def update(self):
        self.update_movement()
        self.update_animation()

    def update_movement(self):
        self.actor.x += self.speed * self.direction
        if self.actor.right > self.patrol_max_x:
            self.direction = -1
        elif self.actor.left < self.patrol_min_x:
            self.direction = 1

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer % 8 == 0:
            self.current_frame += 1
            active_list = None
            if self.direction == 1:
                active_list = self.walk_frames_r
            else:
                active_list = self.walk_frames_l
            if self.current_frame >= len(active_list):
                self.current_frame = 0
            new_image = active_list[self.current_frame]
            self.actor.image = new_image


player = None

player_idle_r = ['astro_idle_1', 'astro_idle_2']
player_walk_r = ['astro_walk_1', 'astro_walk_2']
player_idle_l = ['astro_idle_left_1', 'astro_idle_left_2']
player_walk_l = ['astro_walk_left_1', 'astro_walk_left_2']
enemy_walk_r = ['enemy_walk_1', 'enemy_walk_2']
enemy_walk_l = ['enemy_walk_left_1', 'enemy_walk_left_2']

for i in range(13):
    platforms.append(Actor('ground', (32 + (i * 64), 568)))
for i in range(3):
    platforms.append(Actor('platform', (132 + (i * 64), 400)))
for i in range(4):
    platforms.append(Actor('platform', (532 + (i * 64), 250)))

start_button = Rect((300, 225), (200, 50))  # (x, y), (largura, altura)
sound_button = Rect((300, 325), (200, 50))
quit_button = Rect((300, 425), (200, 50))

music.play('background_music')


def start_game():
    global player, enemies, game_state
    enemies = []
    player = Player(100, 300, player_idle_r, player_walk_r,
                    player_idle_l, player_walk_l)

    enemies.append(Enemy(550, 193, 80, enemy_walk_r, enemy_walk_l))
    enemies.append(Enemy(300, 511, 80, enemy_walk_r, enemy_walk_l))

    game_state = 'game'


def draw():
    screen.clear()
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'game':
        draw_game()


def update():
    if game_state == 'menu':
        update_menu()
    elif game_state == 'game':
        update_game()


def draw_menu():
    screen.draw.filled_rect(start_button, 'white')
    screen.draw.filled_rect(sound_button, 'white')
    screen.draw.filled_rect(quit_button, 'white')

    screen.draw.text("START", center=start_button.center,
                     color='black', fontsize=28)
    screen.draw.text("QUIT", center=quit_button.center,
                     color='black', fontsize=28)

    if sound_on:
        screen.draw.text("SOUND ON", center=sound_button.center,
                         color='black', fontsize=28)
    else:
        screen.draw.text("SOUND OFF", center=sound_button.center,
                         color='black', fontsize=28)


def draw_game():
    for platform in platforms:
        platform.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()


def update_menu():
    pass


def update_game():
    global game_state
    player.update()
    for enemy in enemies:
        enemy.update()
        if player.actor.colliderect(enemy.actor):
            print("Game Over!")
            game_state = 'menu'


def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'menu':
        if start_button.collidepoint(pos):
            print("Botao START clicado!")
            start_game()

        elif quit_button.collidepoint(pos):
            print("Botao QUIT clicado!")
            quit()

        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                print("Som LIGADO")
                music.unpause()
            else:
                print("Som DESLIGADO")
                music.pause()
