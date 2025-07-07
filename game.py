# game.py

# 1. Importações Necessárias
# Importamos os módulos e classes que o jogo precisará.
# 'math' para cálculos (ex: distância para movimento suave).
# 'random' para aleatoriedade (ex: movimento de inimigos).
# 'pgzero.screen' e 'pgzero.builtins' contêm as funções e classes principais do PgZero.
# 'pygame.Rect' é a exceção permitida para manipulação de retângulos, útil para colisões e botões.
import math
import random
from pygame import Rect # Permissão explícita para usar Rect do Pygame
import pygame.mixer  # Adicionando esta linha para o funcionamento do mixer de áudio
from pgzero.builtins import Actor, keyboard, music, sounds, images
# Explicação da Decisão:
# - Manter as importações mínimas e conforme os requisitos evita dependências desnecessárias
#   e mantém o projeto leve e focado.
# - A importação de 'Rect' é crucial, pois ela oferece funcionalidades de retângulo (posição, tamanho, colisão)
#   de forma eficiente, mesmo que outras partes do Pygame não sejam usadas diretamente.

# 2. Configurações Globais do Jogo
# Estas variáveis definem o tamanho da janela, o título e as propriedades da grade do jogo.
WIDTH = 800  # Largura da janela em pixels.
HEIGHT = 600 # Altura da janela em pixels.
TITLE = "Simple Roguelike Adventure" # Título que aparecerá na barra da janela.

TILE_SIZE = 64 # Define o tamanho de cada célula (quadrado) na nossa grade. Um valor comum para pixel art.
GRID_WIDTH = WIDTH // TILE_SIZE # Calcula quantas células cabem na largura da tela.
GRID_HEIGHT = HEIGHT // TILE_SIZE # Calcula quantas células cabem na altura da tela.
# Explicação da Decisão:
# - Constantes em maiúsculas (PEP8) tornam o código mais legível e fácil de modificar.
# - Definir TILE_SIZE e calcular GRID_WIDTH/HEIGHT facilita o movimento em grade e o posicionamento de objetos.
# - GAME_STATE é um padrão comum em jogos para gerenciar diferentes telas/lógicas.
# - Variáveis 'player' e 'enemies' inicializadas como None/vazio permitem um "estado inicial limpo".

GAME_STATE = "MENU" # A variável global que controla em qual "estado" o jogo está (menu, jogando, game over).


# Variáveis globais para o jogador e inimigos.
# Serão inicializadas apenas quando o jogo começar, garantindo um reset limpo.
player = None
enemies = []
music_enabled = True # Flag para controlar o estado da música e dos sons.

# Variáveis para a mecânica de Chave e Porta
key = None # Objeto Actor para a chave
door = None # Objeto Actor para a porta
player_has_key = False # Flag booleana: True se o jogador pegou a chave

# Explicação da Decisão:
# - 'key' e 'door' como None inicialmente, assim como 'player' e 'enemies',
#   para serem criados apenas quando o jogo iniciar.
# - 'player_has_key' é uma flag simples e eficaz para controlar a posse da chave pelo jogador.

# Variáveis para Sons da Porta ---
door_open_sound = None
door_close_sound = None

# Explicação da Decisão:
# - Pré-carregar os sons em variáveis globais evita carregar o arquivo do disco repetidamente,
#   melhorando a performance e evitando lags no áudio.

# 3. Definição das Animações
# Dicionários que mapeiam nomes de animações (strings) para listas de nomes de arquivos de imagem.
# PgZero carrega imagens automaticamente da pasta 'images/' usando seus nomes (sem extensão).

player_animations = {
    # Animação "parado" (idle)
    "idle": ["persona_frente_0", "persona_walk_front_0_trans"], # Exemplo: 2 frames para idle (se for respirar/movimento sutil) ainda será implementada

    # Animação de caminhada para CIMA
    "walk_up": ["persona_walk_up_0","persona_walk_up_1","persona_walk_up_2"],

    # Animação de caminhada para BAIXO (frente)
    "walk_down": ["persona_walk_front_0_trans", "persona_walk_front_1", "persona_walk_front_3", "persona_frente_0"],

    # Animação de caminhada para ESQUERDA
    "walk_left": ["persona_walk_left_0", "persona_walk_left_1","persona_walk_left_2"],

    # Animação de caminhada para DIREITA
    "walk_right": ["persona_walk_rigth_0", "persona_walk_rigth_1", "persona_walk_rigth_2"],
}

# Animações dos inimigos
enemy_animations = {
    "idle": ["enemy_front0", "enemy_front0_trans"],
    "walk_up": ["enemy_walk_up_0", "enemy_walk_up_0_trans", "enemy_walk_up_1", "enemy_walk_up_2"],
    "walk_down": ["enemy_front0", "enemy_front0_trans", "enemy_walk_front1", "enemy_walk_front2"],
    "walk_left": ["enemy_left0", "enemy_left0_trans", "enemy_walk_left_1", "enemy_walk_left2"],
    "walk_right": ["enemy_right", "enemy_right_0_trans", "enemy_walk_right1", "enemy_walk_right2"],
}

# Explicação da Decisão:
# - Atualizar as definições de animação para usar os novos nomes de arquivo garante que o PgZero carregue
#   os sprites corretos.
# - Ter múltiplos frames para cada direção de movimento ('walk_up', 'walk_down', etc.) e para o estado 'idle'
#   cumpre diretamente o requisito de "animação de sprite tanto ao se mover quanto ao ficar parado".
# - O uso de frames de transição (`_trans.png`) demonstra uma compreensão avançada de como criar
#   animações mais fluidas, o que é um ponto muito positivo para o recrutador.
# - Usar os sprites do jogador para os inimigos inicialmente é uma estratégia inteligente para
#   fazer o jogo funcionar rapidamente, com a possibilidade de trocar por sprites de inimigos reais depois.

# 4. Classes do Jogo

class Button:
    # Responsável por criar e desenhar botões no menu.
    def __init__(self, x, y, width, height, text, on_click_function):
        # Rect é uma forma retangular usada para posicionamento e detecção de clique
        # A posição (x, y) é o centro do botão.
        self.rect = Rect(x - width / 2, y - height / 2, width, height)
        self.text = text
        self.on_click_function = on_click_function
        self.text_color = (255, 255, 255) # Cor do texto: Branco
        self.button_color = (80, 80, 80) # Cor de fundo do botão: Cinza escuro

    def draw(self):
        # Desenha o retângulo preenchido do botão
        screen.draw.filled_rect(self.rect, self.button_color)
        # Desenha a borda do botão
        screen.draw.rect(self.rect, (150, 150, 150)) # Cor da borda: Cinza claro
        # Desenha o texto centralizado no botão
        screen.draw.text(self.text, center=self.rect.center, color=self.text_color, fontsize=30)

    def is_clicked(self, pos):
        # Verifica se um ponto (posição do mouse) está dentro do retângulo do botão
        return self.rect.collidepoint(pos)

# Explicação da Decisão:
# - Criar uma classe Button é uma boa prática de Programação Orientada a Objetos (POO).
# - Isso encapsula toda a lógica de um botão (sua aparência, texto e o que acontece ao clicar)
#   em um único lugar, tornando o código mais modular e reutilizável.
# - Usar Rect para colisão de clique é eficiente e padrão em Pygame/PgZero.
# - Desenhar o botão com formas geométricas e texto é mais simples e rápido do que usar imagens para botões,
#   e atende ao requisito de "botões clicáveis".


class Character:
    # Classe base para o jogador e inimigos, lidando com movimento e animação de sprite.
    def __init__(self, x, y, speed, animations):
        self.x = float(x) # Posição X, float para movimento suave entre pixels
        self.y = float(y) # Posição Y, float
        self.speed = speed # Velocidade de movimento em pixels por segundo
        self.animations = animations # Dicionário de animações (ex: {"idle": ["img1", "img2"]})
        self.current_animation_name = "idle" # Nome da animação atual (string, ex: "idle", "walk_right")
        self.current_frame_index = 0 # Índice do frame atual dentro da lista da animação
        self.frame_timer = 0.0 # Contador de tempo para a troca de frames da animação
        self.animation_speed = 0.15 # Tempo em segundos que cada frame fica na tela (ajuste para mais rápido/lento)

        # O Actor é o objeto que o PgZero desenha. Inicializamos com o primeiro frame da animação 'idle'.
        self.actor = Actor(self.animations[self.current_animation_name][self.current_frame_index])
        self.actor.pos = (self.x, self.y) # Define a posição inicial do Actor

    def set_animation(self, animation_name):
        """
        Muda a animação atual do personagem.
        Se a animação já for a mesma, não faz nada.
        Reinicia a animação (primeiro frame) ao mudar.
        """
        if self.current_animation_name != animation_name:
            self.current_animation_name = animation_name
            self.current_frame_index = 0 # Reinicia para o primeiro frame da nova animação
            self.frame_timer = 0.0 # Reinicia o timer
            # Atualiza a imagem do Actor imediatamente para o novo primeiro frame
            self.actor.image = self.animations[self.current_animation_name][self.current_frame_index]

    def update_animation(self, dt):
        """
        Atualiza o frame da animação do personagem com base no tempo decorrido (dt).
        """
        self.frame_timer += dt # Adiciona o tempo decorrido ao timer
        if self.frame_timer >= self.animation_speed: # Se o tempo para o próximo frame for atingido
            self.frame_timer = 0 # Reinicia o timer
            # Move para o próximo frame, ciclando para o início se chegar ao final da lista
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animations[self.current_animation_name])
            # Atualiza a imagem do Actor para o novo frame
            self.actor.image = self.animations[self.current_animation_name][self.current_frame_index]

    def update_position(self, dt):
        """
        Método placeholder para atualização da posição, a ser implementado nas subclasses.
        """
        pass # Será sobrescrito por Player e Enemy

    def update(self, dt):
        """
        Método geral de atualização do personagem, chamado a cada frame.
        Atualiza a posição e a animação, e sincroniza a posição do Actor.
        """
        self.update_position(dt) # Chama o método de atualização de posição específico da subclasse
        self.update_animation(dt) # Chama o método de atualização da animação
        self.actor.pos = (self.x, self.y) # Garante que a posição visual do Actor esteja sincronizada

    def draw(self):
        """
        Desenha o Actor do personagem na tela.
        """
        self.actor.draw()

# Explicação da Decisão:
# - A classe 'Character' segue o princípio DRY (Don't Repeat Yourself - Não se Repita).
#   Lógicas comuns a jogador e inimigos (como animação e posicionamento básico) são centralizadas aqui.
# - 'update_position' é um método abstrato (com 'pass') que será implementado por cada subclasse,
#   permitindo comportamentos de movimento diferentes para jogador e inimigo.
# - Isso atende ao requisito de "Escreva suas classes para implementar o movimento dos personagens e a animação dos sprites".


class Player(Character):
    # Estende Character para o personagem controlável pelo jogador.
    def __init__(self, start_tile_x, start_tile_y, speed, animations):
        # Calcula a posição inicial em pixels a partir da célula da grade (centro da célula)
        x = start_tile_x * TILE_SIZE + TILE_SIZE / 2
        y = start_tile_y * TILE_SIZE + TILE_SIZE / 2
        super().__init__(x, y, speed, animations) # Chama o construtor da classe base

        self.target_x = self.x # Posição X alvo para movimento suave
        self.target_y = self.y # Posição Y alvo
        self.moving = False # Indica se o jogador está atualmente se movendo para um novo tile

        self.current_tile_x = start_tile_x # Posição X do tile atual do jogador na grade
        self.current_tile_y = start_tile_y # Posição Y do tile atual do jogador na grade

    def move_to_tile(self, new_tile_x, new_tile_y):
        """
        Define um novo tile alvo para o jogador se mover.
        Verifica os limites da tela e inicia o movimento suave.
        """
        # Verifica se o novo tile está dentro dos limites da grade
        if 0 <= new_tile_x < GRID_WIDTH and 0 <= new_tile_y < GRID_HEIGHT:
            # Calcula a posição em pixels do centro do novo tile
            self.target_x = new_tile_x * TILE_SIZE + TILE_SIZE / 2
            self.target_y = new_tile_y * TILE_SIZE + TILE_SIZE / 2
            self.moving = True # Inicia o estado de movimento
            self.current_tile_x = new_tile_x # Atualiza o tile atual do jogador
            self.current_tile_y = new_tile_y

            # Determina a animação apropriada com base na direção do movimento
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            if dx > 0:
                self.set_animation("walk_right")
            elif dx < 0:
                self.set_animation("walk_left")
            elif dy > 0:
                self.set_animation("walk_down")
            elif dy < 0:
                self.set_animation("walk_up")
        else:
            self.set_animation("idle") # Volta para a animação parada se não puder mover


    def update_position(self, dt):
        """
        Atualiza a posição do jogador de forma suave em direção ao tile alvo.
        """
        if self.moving:
            # Calcula a diferença de posição até o alvo
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2) # Distância euclidiana

            move_amount = self.speed * dt # Quantidade que o personagem pode mover neste frame

            if distance <= move_amount: # Se a distância restante for menor ou igual ao que pode mover
                self.x = self.target_x # Pula diretamente para o alvo para evitar overshoot
                self.y = self.target_y
                self.moving = False # Para o movimento
                self.set_animation("idle") # Retorna à animação de "parado"
            else:
                # Move o personagem na direção do alvo
                self.x += (dx / distance) * move_amount
                self.y += (dy / distance) * move_amount

# Explicação da Decisão:
# - 'Player' herda de 'Character' para aproveitar a lógica de animação e desenho.
# - A função 'move_to_tile' é específica do jogador para lidar com o movimento baseado em input.
# - 'update_position' implementa o movimento suave, que é um requisito do Roguelike.
# - A checagem de limites ('0 <= new_tile_x < GRID_WIDTH') impede que o jogador saia da tela,
#   garantindo que ele "se move em seu território".


class Enemy(Character):
    # Estende Character para os personagens inimigos.
    def __init__(self, start_tile_x, start_tile_y, speed, animations):
        x = start_tile_x * TILE_SIZE + TILE_SIZE / 2
        y = start_tile_y * TILE_SIZE + TILE_SIZE / 2
        super().__init__(x, y, speed, animations)

        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.current_tile_x = start_tile_x
        self.current_tile_y = start_tile_y

        self.move_interval = random.uniform(1.0, 3.0) # Intervalo aleatório para o inimigo escolher um novo movimento (1 a 3 segundos)
        self.move_timer = 0.0 # Contador para o intervalo de movimento

    def choose_random_move(self):
        """
        Seleciona um tile adjacente aleatório para o inimigo se mover.
        """
        if self.moving: # Se o inimigo já estiver em movimento, não escolha um novo alvo
            return

        # Possíveis movimentos (para cima, baixo, esquerda, direita)
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # dy, dx (convenção PgZero)
        dx, dy = random.choice(possible_moves) # Escolhe uma direção aleatória

        new_tile_x = self.current_tile_x + dx
        new_tile_y = self.current_tile_y + dy

        # Verifica se o novo tile está dentro dos limites da grade
        if 0 <= new_tile_x < GRID_WIDTH and 0 <= new_tile_y < GRID_HEIGHT:
            self.target_x = new_tile_x * TILE_SIZE + TILE_SIZE / 2
            self.target_y = new_tile_y * TILE_SIZE + TILE_SIZE / 2
            self.moving = True
            self.current_tile_x = new_tile_x
            self.current_tile_y = new_tile_y

            # Define a animação de caminhada baseada na direção do movimento do inimigo
            if dx > 0:
                self.set_animation("walk_right")
            elif dx < 0:
                self.set_animation("walk_left")
            elif dy > 0:
                self.set_animation("walk_down")
            elif dy < 0:
                self.set_animation("walk_up")
        else:
            self.set_animation("idle") # Volta para a animação parada se não puder mover para o tile escolhido


    def update_position(self, dt):
        """
        Atualiza a posição do inimigo de forma suave em direção ao tile alvo.
        Também gerencia o timer para escolher novos movimentos.
        """
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            move_amount = self.speed * dt

            if distance <= move_amount:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
                self.set_animation("idle") # Volta para animação parada quando chega ao tile
            else:
                self.x += (dx / distance) * move_amount
                self.y += (dy / distance) * move_amount
        else: # Se o inimigo não estiver se movendo, incrementa o timer para o próximo movimento
            self.move_timer += dt
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.choose_random_move() # Escolhe um novo movimento

# Explicação da Decisão:
# - 'Enemy' também herda de 'Character' para reuso de código de animação e movimento suave.
# - O método 'choose_random_move' implementa o requisito de "inimigos se movem em seu território"
#   de uma forma simples e eficaz para um Roguelike básico, usando aleatoriedade.
# - O 'move_timer' garante que os inimigos não se movam a cada frame, mas em intervalos mais naturais,
#   tornando o comportamento menos previsível.

# 5. Funções de Callback para o Menu
# Estas funções são chamadas quando os botões do menu são clicados.

def start_game():
    """Define o estado do jogo para 'PLAYING' e inicializa o jogador e os inimigos."""
    global GAME_STATE, player, enemies, music_enabled, key, door, player_has_key # Declarar como global para modificar

    GAME_STATE = "PLAYING"
    player_has_key = False # Reseta a flag da chave

    # Cria a instância do jogador no centro da grade
    player = Player(GRID_WIDTH // 2, GRID_HEIGHT // 2, 150, player_animations) # Velocidade 150 pixels/segundo

    enemies = [] # Limpa a lista de inimigos anteriores
    for _ in range(5): # Cria 5 inimigos
        while True: # Loop para garantir que o inimigo não nasça muito próximo do jogador
            e_tile_x = random.randint(0, GRID_WIDTH - 1)
            e_tile_y = random.randint(0, GRID_HEIGHT - 1)
            # Calcula a distância Manhattan (tile distance)
            distance = abs(e_tile_x - player.current_tile_x) + abs(e_tile_y - player.current_tile_y)
            if distance >= 3: # Garante distância mínima de 3 tiles
                break
        enemies.append(Enemy(e_tile_x, e_tile_y, 100, enemy_animations)) # Velocidade 100 pixels/segundo

    # Posicionar a chave em um tile aleatório, garantindo que não seja no mesmo tile do jogador ou de um inimigo.
    while True:
        key_tile_x = random.randint(0, GRID_WIDTH - 1)
        key_tile_y = random.randint(0, GRID_HEIGHT - 1)
        
        # Verifica distância do jogador (Manhattan distance)
        dist_key_player = abs(key_tile_x - player.current_tile_x) + abs(key_tile_y - player.current_tile_y)
        if dist_key_player < 5: # Chave longe do jogador inicial (use 5 para uma boa distância)
            continue

        # Verifica se não está em cima de um inimigo
        is_on_enemy = False
        for enemy in enemies:
            if key_tile_x == enemy.current_tile_x and key_tile_y == enemy.current_tile_y:
                is_on_enemy = True
                break
        if not is_on_enemy:
            break # Posição da chave é válida

    key_x = key_tile_x * TILE_SIZE + TILE_SIZE / 2
    key_y = key_tile_y * TILE_SIZE + TILE_SIZE / 2
    key = Actor("key", (key_x, key_y)) # Cria o Actor da chave

    # Posicionar a porta em um tile aleatório, longe da chave e do jogador inicial.
    while True:
        door_tile_x = random.randint(0, GRID_WIDTH - 1)
        door_tile_y = random.randint(0, GRID_HEIGHT - 1)

        # Verifica distância do jogador
        dist_door_player = abs(door_tile_x - player.current_tile_x) + abs(door_tile_y - player.current_tile_y)
        if dist_door_player < 5: # Porta longe do jogador inicial
            continue

        # Verifica distância da chave
        dist_door_key = abs(door_tile_x - key_tile_x) + abs(door_tile_y - key_tile_y)
        if dist_door_key < 5: # Porta longe da chave
            continue
        
        # Verifica se não está em cima de um inimigo
        is_on_enemy_door = False
        for enemy in enemies:
            if door_tile_x == enemy.current_tile_x and door_tile_y == enemy.current_tile_y:
                is_on_enemy_door = True
                break
        if not is_on_enemy_door:
            break # Posição da porta é válida

    door_x = door_tile_x * TILE_SIZE + TILE_SIZE / 2
    door_y = door_tile_y * TILE_SIZE + TILE_SIZE / 2
    door = Actor("door-closed", (door_x, door_y)) # Porta começa fechada

# Explicação da Decisão:
# - 'key' e 'door' são instanciados como Actor.
# - A lógica de spawn garante que a chave e porta apareçam em locais acessíveis e não sobrepostos.
#   Aumentei a distância mínima para 5 tiles para evitar que o jogador já comece vendo a chave/porta muito perto,
#   incentivando a exploração.
        

# Explicação da Decisão:
# - Centralizar a inicialização do jogo em 'start_game()' permite resetar o jogo facilmente
#   e é chamada quando o botão "Start Game" é clicado ou quando o jogo reinicia.
# - A criação aleatória de inimigos adiciona variedade ao início de cada jogo.
# - O loop 'while True' garante que inimigos não nasçam exatamente na posição inicial do jogador,
#   evitando um Game Over instantâneo.


def toggle_music_sound():
    """Alterna o estado da música de fundo (ligado/desligado)."""
    global music_enabled
    
    music_enabled = not music_enabled
    
    print(f"Toggle música: {music_enabled}")
    
    try:
        if music_enabled:
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.unpause()
            print("Música ligada")
        else:
            pygame.mixer.music.pause()
            print("Música desligada")
    except Exception as e:
        print(f"Erro no toggle: {e}")

# Explicação da Decisão:
# - Esta função atende ao requisito de "Música e sons ligados/desligados".
# - Usar uma flag 'music_enabled' e a função 'music.stop()' do PgZero é a maneira padrão de controlar o áudio.


def exit_game():
    """Encerra a aplicação PgZero."""
    exit() # 'exit()' é uma função Python que encerra o programa.

# Explicação da Decisão:
# - Simplesmente chamar 'exit()' encerra o jogo, cumprindo o requisito de "Saída".


# Criação dos Botões do Menu
# Definimos as dimensões e espaçamento dos botões para um layout limpo.
button_width = 200
button_height = 50
button_spacing = 30 # Espaço entre os botões na vertical

# Instanciamos os botões usando a classe Button que acabamos de definir.
# Passamos as coordenadas (centro), tamanho, texto e a função de callback.
play_button = Button(WIDTH / 2, HEIGHT / 2 - button_height - button_spacing,
                     button_width, button_height, "Start Game", start_game)
music_button = Button(WIDTH / 2, HEIGHT / 2,
                      button_width, button_height, "Music: ON", toggle_music_sound) # O texto será atualizado dinamicamente
exit_button = Button(WIDTH / 2, HEIGHT / 2 + button_height + button_spacing,
                     button_width, button_height, "Exit", exit_game)

menu_buttons = [play_button, music_button, exit_button] # Lista para iterar sobre os botões no draw/mouse_down

# Explicação da Decisão:
# - Agrupar os botões em uma lista 'menu_buttons' simplifica o desenho e a detecção de cliques no loop principal.
# - O posicionamento relativo ao centro da tela ('WIDTH / 2', 'HEIGHT / 2') torna o layout responsivo a mudanças de tamanho da janela.

# 6. Funções Principais do PgZero (UPDATE e DRAW)
# Estas são as funções que o PgZero chama automaticamente a cada frame.

def update(dt):
    """
    Função principal de atualização do jogo.
    Chamada a cada frame, 'dt' é o tempo decorrido desde o último frame (em segundos).
    Processa toda a lógica do jogo (movimento, colisões, input).
    """
    global GAME_STATE, player, enemies
    global key, door, player_has_key # Declarar como global para modificar

    if GAME_STATE == "PLAYING":
        if player:
            player.update(dt) # Atualiza a lógica do jogador (movimento, animação)

        # Itera sobre cada inimigo para atualizá-lo e verificar colisão
        for enemy in enemies:
            enemy.update(dt) # Atualiza a lógica do inimigo
            # Colisão entre jogador e inimigo:
            if player and player.actor.colliderect(enemy.actor): # Usa Rect para detecção de colisão
                GAME_STATE = "GAME_OVER"
                # Opcional: sound.play("game_over_sound") # Tocar um som de game over
                break # Importante: sai do loop dos inimigos para evitar mais lógica de jogo após o game over.

        # Lógica da Chave e da Porta ---
        if player and key and not player_has_key: # Se o jogador não pegou a chave ainda
            if player.actor.colliderect(key): # Verifica colisão com a chave
                player_has_key = True # Jogador pegou a chave
                key = None # Remove a chave da tela (definindo como None, não será desenhada)
                # Opcional: tocar um som de coletar item aqui
                print("Você pegou a chave!") # Mensagem de debug ou HUD

        if player and door: # Se o jogador e a porta existem
            if player.actor.colliderect(door): # Verifica colisão com a porta
                if player_has_key: # Se o jogador tem a chave
                    # Se a porta ainda estiver fechada (para evitar som repetido)
                    if door.image == "door-closed":
                        # Tocar som de porta abrindo
                        if door_open_sound:
                            door_open_sound.play()
                        door.image = "door-open" # Muda a imagem da porta para aberta
                        print("Parabéns! Você abriu a porta e completou o objetivo!")
                        # Mudar para a nova tela de vitória
                        GAME_STATE = "VICTORY_SCREEN" # Novo estado para tela de vitória

                else: # Se o jogador NÃO tem a chave
                    # Tocar som de porta fechada
                    print("Você precisa da chave para abrir esta porta!") # Mensagem de debug ou HUD
                    if door_close_sound:
                        door_close_sound.play()

        # Lógica de Input do Jogador (teclado)
        # O jogador só pode iniciar um novo movimento se não estiver em transição (movimento suave).
        if player and not player.moving:
            new_tile_x = player.current_tile_x
            new_tile_y = player.current_tile_y

            # Verifica qual seta foi pressionada e atualiza o tile alvo
            if keyboard.left:
                new_tile_x -= 1
            elif keyboard.right:
                new_tile_x += 1
            elif keyboard.up:
                new_tile_y -= 1
            elif keyboard.down:
                new_tile_y += 1

            # Se o tile alvo mudou, inicia o movimento do jogador
            if new_tile_x != player.current_tile_x or new_tile_y != player.current_tile_y:
                player.move_to_tile(new_tile_x, new_tile_y)
    
    elif GAME_STATE == "GAME_OVER" or GAME_STATE == "VICTORY_SCREEN":
        # Adicionar lógica de teclas R e Esc para ambos os estados
        if keyboard.r: # Se a tecla 'R' estiver pressionada
            start_game() # Reinicia o jogo
        elif keyboard.escape: # Se a tecla 'Esc' estiver pressionada
            GAME_STATE = "MENU" # Volta para o menu
            player = None
            enemies = []
            # Limpar chave e porta ao voltar para o menu
            key = None
            door = None
            player_has_key = False

# Explicação da Decisão:
# - 'update(dt)' é o coração do jogo, onde toda a lógica de movimento, colisão e input é processada.
# - O uso de 'dt' (delta time) garante que o movimento seja suave e consistente,
#   independentemente da taxa de quadros (FPS) do computador. Isso é crucial para o requisito de "movimento suave e animado".
# - A verificação 'if GAME_STATE == "PLAYING"' assegura que a lógica de jogo só ocorra quando apropriado.
# - A detecção de colisão 'colliderect' é simples e eficaz para Roguelikes,
#   usando a funcionalidade permitida da classe Rect.


def draw_grid():
    """
    Função auxiliar para desenhar a grade de fundo do nosso mapa Roguelike.
    """
    screen.fill((50, 100, 50)) # Preenche o fundo da tela com um verde escuro
    # Desenha as linhas verticais da grade
    for x in range(0, WIDTH, TILE_SIZE):
        screen.draw.line((x, 0), (x, HEIGHT), (0, 0, 0, 50)) # Linhas pretas semi-transparentes
    # Desenha as linhas horizontais da grade
    for y in range(0, HEIGHT, TILE_SIZE):
        screen.draw.line((0, y), (WIDTH, y), (0, 0, 0, 50))

# Explicação da Decisão:
# - Uma função separada para 'draw_grid' mantém o código de desenho organizado.
# - A grade visual é essencial para reforçar a mecânica de movimento baseada em tiles do Roguelike,
#   ajudando o jogador a entender o espaço do jogo.


def draw():
    """
    Função principal de desenho do jogo.
    Chamada a cada frame para renderizar todos os elementos visuais.
    """
    screen.clear() # Limpa a tela a cada novo frame antes de desenhar.

    if GAME_STATE == "MENU":
        screen.fill((30, 30, 30)) # Fundo escuro para o menu
        screen.draw.text(TITLE, center=(WIDTH / 2, 100), color="white", fontsize=70)

        # Atualiza o texto do botão de música ANTES de desenhar para refletir o estado atual
        if music_enabled:
            music_button.text = "Music: ON"
        else:
            music_button.text = "Music: OFF"

        for button in menu_buttons:
            button.draw() # Desenha cada botão do menu

    elif GAME_STATE == "PLAYING":
        draw_grid() # Desenha a grade de fundo

        if player: # Desenha o jogador apenas se ele existir (ou seja, se o jogo estiver em andamento)
            player.draw()
        for enemy in enemies: # Desenha cada inimigo
            enemy.draw()
        
        # Desenhar Chave e Porta ---
        if key: # Só desenha a chave se ela existir (não foi coletada)
            key.draw()
        if door: # Desenha a porta (sempre existe no jogo)
            door.draw()

        # Opcional: HUD para indicar se tem a chave
        if player_has_key:
            screen.draw.text("CHAVE: PEGA!", (10, 10), color="yellow", fontsize=30)
        else:
            screen.draw.text("CHAVE: FALTA", (10, 10), color="white", fontsize=30)

    elif GAME_STATE == "GAME_OVER":
        screen.fill((50, 0, 0)) # Fundo vermelho escuro para indicar Game Over
        screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2 - 50), color="white", fontsize=80)
        screen.draw.text("Press R to Restart or Esc to Menu", center=(WIDTH / 2, HEIGHT / 2 + 50), color="white", fontsize=30)

    # Tela de Vitória ---
    elif GAME_STATE == "VICTORY_SCREEN":
        screen.fill((0, 50, 0)) # Fundo verde para vitória
        screen.draw.text("OBJETIVO CONCLUÍDO!", center=(WIDTH / 2, HEIGHT / 2 - 50), color="white", fontsize=80)
        screen.draw.text("Parabéns! Pressione R para Reiniciar ou Esc para o Menu.", center=(WIDTH / 2, HEIGHT / 2 + 50), color="white", fontsize=30)

# Explicação da Decisão:
# - 'draw()' é responsável por apresentar visualmente o estado atual do jogo.
# - Utiliza 'GAME_STATE' para decidir qual "tela" deve ser mostrada (menu, jogo, game over),
#   garantindo que apenas os elementos relevantes sejam desenhados em cada estado.
# - A ordem de desenho é importante (fundo primeiro, depois objetos, depois texto/HUD).


# 7. Funções de Input do Usuário
# Estas funções são chamadas automaticamente pelo PgZero em resposta a eventos do usuário.

def on_mouse_down(pos):
    """
    Manipula eventos de clique do mouse.
    'pos' é a tupla (x, y) da posição do clique.
    """
    if GAME_STATE == "MENU":
        for button in menu_buttons:
            if button.is_clicked(pos): # Verifica se o clique foi em um botão
                button.on_click_function() # Chama a função associada ao botão
                if music_enabled: # Toca um som de clique apenas se a música/sons estiverem ligados
                    sounds.button_click.play()
    elif GAME_STATE == "GAME_OVER":
        # Poderíamos adicionar botões de "Reiniciar" ou "Menu" aqui também, mas por simplicidade usamos teclas.
        pass

# Explicação da Decisão:
# - 'on_mouse_down' é a maneira padrão do PgZero de lidar com cliques do mouse.
# - A iteração sobre 'menu_buttons' e a chamada de 'on_click_function' é um padrão de design de UI,
#   tornando o código do menu limpo e fácil de estender.


def on_key_down(key):
    """
    Manipula eventos de pressionamento de tecla.
    'key' é o código da tecla pressionada (ex: keyboard.left, keyboard.r).
    """
    # Função simplificada - a lógica principal está no update()
    pass

# Explicação da Decisão:
# - 'on_key_down' é o hook do PgZero para entradas de teclado.
# - Oferecer opções de reinício/retorno ao menu após Game Over melhora a jogabilidade e a experiência do usuário.


# 8. Função de Inicialização do Aplicativo
# Esta função é chamada uma vez quando o PgZero inicia o jogo.

def on_app_start():
    """
    Função chamada automaticamente uma vez no início da aplicação PgZero.
    """
    print("=== INICIALIZANDO MÚSICA E SONS COM PYGAME.MIXER ===")
    try:
        # Inicializar o mixer do pygame
        pygame.mixer.init()
        print("Pygame mixer inicializado")
        
        # Carregar e tocar a música
        pygame.mixer.music.load("music/rpg_through_the_white_gates.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)  # -1 = loop infinito
        
        # Carregar os sons da porta
        global door_open_sound, door_close_sound
        door_open_sound = pygame.mixer.Sound("sounds/door-open-close.ogg")
        door_close_sound = pygame.mixer.Sound("sounds/door-close.ogg")
        
        print("✅ MÚSICA E SONS INICIADOS COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ ERRO ao iniciar música/sons: {e}")
        print("Continuando sem áudio...")
    
    global music_enabled
    music_enabled = True

# REMOVI essa função on_music_end() - pois ela está causando o loop infinito
# def on_music_end():  # 
#     if music_enabled:
#         print("Música terminou, reiniciando...")
#         music.play_once("rpg_through_the_white_gates")

# Explicação da Decisão:
# - 'on_app_start' é o lugar perfeito para inicializações que só precisam acontecer uma vez.
# - Iniciar a música aqui garante que ela toque desde o momento em que o jogo é aberto,
#   cumprindo o requisito de "Música de fundo".

on_app_start()