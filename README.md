# Simple Roguelike Adventure

Um jogo Roguelike clássico desenvolvido em Python usando Pygame Zero, com foco em mecânicas de movimentação em grade, coleta de itens e sobrevivência.

## Descrição

**Simple Roguelike Adventure** é um jogo com visão de cima e movimento baseado em grade que demonstra as principais mecânicas do gênero Roguelike. O jogador deve navegar por um ambiente hostil, evitar inimigos e completar o objetivo principal: encontrar uma chave e usá-la para abrir uma porta misteriosa.

Este projeto foi desenvolvido para demonstrar habilidades em:
- Programação Python
- Programação Orientada a Objetos (POO)
- Desenvolvimento de jogos com Pygame Zero
- Gerenciamento de estados e mecânicas de jogo
- Implementação de sistemas de áudio e animação

## Funcionalidades Implementadas

### Menu Principal
- **Interface Intuitiva:** Botões clicáveis com feedback visual
- **Controles:** "Start Game", "Music On/Off", "Exit"
- **Som de Feedback:** Efeitos sonoros para interação com botões

### Sistema de Áudio Completo
- **Música de Fundo:** Reprodução contínua e loop infinito (`rpg_through_the_white_gates.wav`)
- **Efeitos Sonoros:**
  - Clique de botão: `button_click.wav`
  - Porta abrindo: `door-open-close.ogg`
  - Porta trancada: `door-close.ogg`
- **Controle de Volume:** Sistema de liga/desliga integrado

### Personagens Animados
- **Herói (Jogador):** Sprites personalizados da série `persona_*`
- **Múltiplos Inimigos:** IA autônoma com sprites `enemy_*`
- **Animações Fluidas:**
  - Estados: idle, walk_up, walk_down, walk_left, walk_right
  - Frames de transição (`_trans.png`) para movimento suave
  - Sincronização perfeita entre animação e movimento

### Mecânicas Roguelike
- **Movimento em Grade:** Sistema de tiles 64x64 pixels
- **Movimento Suave:** Transições animadas entre células
- **Colisão Inteligente:** Detecção entre jogador e inimigos
- **Spawn Estratégico:** Posicionamento automático de elementos com distâncias mínimas

### Sistema de Objetivos
- **Chave Coletável:** Item `key.png` posicionado aleatoriamente
- **Porta Interativa:** Transição visual de `door-closed.png` para `door-open.png`
- **HUD Informativo:** Indicador visual do status da chave
- **Tela de Vitória:** Feedback completo ao completar o objetivo

### Gerenciamento de Estados
- **MENU:** Tela inicial com opções
- **PLAYING:** Gameplay principal
- **GAME_OVER:** Tela de derrota com opções de reinício
- **VICTORY_SCREEN:** Tela de vitória com comemorações

## Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **Pygame Zero (PgZero)** - Framework de desenvolvimento de jogos
- **Módulos Padrão:** `math`, `random`
- **pygame.Rect** - Manipulação de colisões e UI
- **pygame.mixer** - Gerenciamento avançado de áudio

## Justificativa Técnica - pygame.mixer

Durante o desenvolvimento, foi identificada uma **inconsistência na API de música do Pygame Zero em ambientes Linux**. Conforme documentado na [documentação oficial](https://pygame-zero.readthedocs.io/en/stable/builtins.html#music):

> *"The underlying Pygame music API is not terribly robust. Some of the bugs described here are in Pygame itself, not Pygame Zero."*

A decisão de utilizar `pygame.mixer` diretamente foi tomada para:
- ✅ **Garantir funcionalidade crítica de áudio** em todos os ambientes
- ✅ **Demonstrar capacidade de debugging** e resolução de problemas técnicos
- ✅ **Aplicar pesquisa em documentação oficial** para soluções robustas
- ✅ **Priorizar requisitos funcionais** sobre restrições técnicas menores

## Como Rodar o Projeto

### Pré-requisitos
- **Python 3.x** instalado
- **pip** para gerenciamento de pacotes
- **Git** para clonagem do repositório

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/WilliamSoares21/game-project.git
cd game-project
```

2. **Crie e ative o ambiente virtual:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install pgzero
```

4. **Execute o jogo:**
```bash
pgzrun game.py
```

### Controles do Jogo
- **Setas do Teclado:** Movimentação do personagem
- **Mouse:** Interação com botões do menu
- **R:** Reiniciar jogo (telas de Game Over/Vitória)
- **Esc:** Voltar ao menu principal

## Estrutura do Projeto

```
game-project/
├── game.py                          # Código principal do jogo
├── README.md                        # Documentação do projeto
├── LICENSE                          # Licença do projeto
├── .gitignore                       # Arquivos ignorados pelo Git
├── images/                          # Assets visuais
│   ├── persona_frente_0.png         # Sprite inicial do jogador
│   ├── persona_walk_front_*.png     # Animações frente
│   ├── persona_walk_left_*.png      # Animações esquerda
│   ├── persona_walk_rigth_*.png     # Animações direita
│   ├── persona_walk_up_*.png        # Animações para cima
│   ├── enemy_front0.png             # Sprite inicial do inimigo
│   ├── enemy_walk_*.png             # Animações do inimigo
│   ├── key.png                      # Sprite da chave
│   ├── door-closed.png              # Sprite da porta fechada
│   └── door-open.png                # Sprite da porta aberta
├── sounds/                          # Efeitos sonoros
│   ├── button_click.wav             # Som de clique do menu
│   ├── door-open-close.ogg          # Som de porta abrindo
│   └── door-close.ogg               # Som de porta trancada
├── music/                           # Música de fundo
│   ├── rpg_through_the_white_gates.wav    # Música principal
│   └── rpg_through_the_white_gates_original.ogg  # Versão original
└── .venv/                           # Ambiente virtual Python
```

## Créditos dos Assets

### Áudio
- **Música de Fundo:** [RPG Through The White Gates](https://opengameart.org/content/rpgthroughthewhitegates) - OpenGameArt.org
- **Som de Clique do Menu:** [Menu Selection Click](https://opengameart.org/content/menu-selection-click) - OpenGameArt.org
- **Som de Porta Fechando:** [Door Close](https://pixabay.com/sound-effects/door-close-79921/) - Pixabay
- **Som de Porta Abrindo:** [Door Open and Close](https://pixabay.com/sound-effects/door-open-close-45475/) - Pixabay

### Sprites e Visuais
- **Animações de Caminhada:** [Walking Animation Tutorial](https://community.aseprite.org/t/still-learning-or-trying-to-learn-to-do-walking-animation) - Aseprite Community
- **Ícones de Chave:** [Key Icons](https://opengameart.org/content/key-icons) - OpenGameArt.org
- **Sprites de Porta:** [Animated Bamboo Door Sprite](https://opengameart.org/content/animated-bamboo-door-sprite) - OpenGameArt.org

### Desenvolvimento
- **Programação e Design:** William Soares
- **Framework:** Pygame Zero Community  
- **Integração, Adaptação e Manipulação de Imagens:** Customizações próprias dos assets originais, com edição e ajustes realizados utilizando o GIMP

## Contato

**William Soares**
- GitHub: [WilliamSoares21](https://github.com/WilliamSoares21)
- Projeto: [Simple Roguelike Adventure](https://github.com/WilliamSoares21/game-project)

---

*Desenvolvido como estudo em Python usando Pygame Zero*

## Licença

Este projeto utiliza assets de terceiros sob suas respectivas licenças. Consulte os links dos créditos para mais informações sobre os termos de uso de cada asset.
