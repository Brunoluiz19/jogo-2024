import pygame
import random
import sys
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 1000
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Limites laterais
LIMITE_ESQUERDO = 100
LIMITE_DIREITO = largura_tela - 100

# Variáveis do jogo
distancia_percorrida = 0
recorde = 0
melhores_recordes = []
ultima_atualizacao = time.time()

# Função para desenhar texto na tela
def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_retangulo = texto_surface.get_rect()
    texto_retangulo.center = (x, y)
    tela.blit(texto_surface, texto_retangulo)

# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect(center=(largura_tela // 2, altura_tela - 100))
        self.velocidade = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > LIMITE_ESQUERDO:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LIMITE_DIREITO:
            self.rect.x += self.velocidade
        if teclas[pygame.K_a] and self.rect.left > LIMITE_ESQUERDO:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_d] and self.rect.right < LIMITE_DIREITO:
            self.rect.x += self.velocidade

# Classe do inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.velocidade = random.uniform(2, 3)  # Mudança para permitir velocidades decimais

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura_tela:
            self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.velocidade = random.uniform(3, 4)  # Mudança para permitir velocidades decimais

# Grupo de sprites
todos_sprites = pygame.sprite.Group()
jogador = Jogador()
inimigos = pygame.sprite.Group()
todos_sprites.add(jogador)

# Função para iniciar o jogo
def iniciar_jogo():
    global distancia_percorrida
    global recorde
    global ultima_atualizacao
    todos_sprites.empty()
    inimigos.empty()
    todos_sprites.add(jogador)
    distancia_percorrida = 0
    ultima_atualizacao = time.time()
    posicoes_ocupadas = set()
    for _ in range(5):
        while True:
            x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - 50)
            if x not in posicoes_ocupadas:
                posicoes_ocupadas.add(x)
                break
        inimigo = Inimigo()
        inimigo.rect.x = x
        todos_sprites.add(inimigo)
        inimigos.add(inimigo)

# Tela de início
iniciar_jogo()

# Loop do jogo
rodando = True
em_tela_inicial = True
em_tela_morte = False
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if (em_tela_inicial or em_tela_morte) and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  # Sai do jogo se pressionar Esc
                rodando = False
            else:
                iniciar_jogo()
                em_tela_inicial = False
                em_tela_morte = False

    if not em_tela_inicial and not em_tela_morte:
        # Atualizações
        todos_sprites.update()

        # Verifica se o jogador colidiu com algum inimigo
        if pygame.sprite.spritecollide(jogador, inimigos, False):
            em_tela_morte = True

            # Atualiza o recorde se a distância percorrida for maior que o recorde atual
            if distancia_percorrida > recorde:
                recorde = distancia_percorrida
                # Adiciona o recorde à lista de melhores recordes se ele não estiver lá
                if recorde not in melhores_recordes:
                    melhores_recordes.append(recorde)
                    # Mantém apenas os três melhores recordes
                    melhores_recordes.sort(reverse=True)
                    melhores_recordes = melhores_recordes[:3]

        # Calcula a distância percorrida pelo jogador
        distancia_percorrida += jogador.velocidade

        # Verifica se a distância aumentou 300 para aumentar a velocidade dos inimigos vermelhos
        if distancia_percorrida % 300 == 0:
            for inimigo in inimigos:
                inimigo.velocidade += 0.5  # Aumento de velocidade dos inimigos vermelhos

        # Desenha na tela
        tela.fill(PRETO)
        todos_sprites.draw(tela)

        # Desenha os limites laterais
        pygame.draw.line(tela, BRANCO, (LIMITE_ESQUERDO, 0), (LIMITE_ESQUERDO, altura_tela), 5)
        pygame.draw.line(tela, BRANCO, (LIMITE_DIREITO, 0), (LIMITE_DIREITO, altura_tela), 5)

        # Desenha a distância percorrida e o recorde na tela
        desenhar_texto(f'Distância Percorrida: {distancia_percorrida}', 20, BRANCO, largura_tela // 2, 20)
        desenhar_texto(f'Recorde: {recorde}', 20, BRANCO, largura_tela // 2, 50)

        # Atualiza a tela
        pygame.display.flip()

    elif em_tela_inicial:
        tela.fill(PRETO)
        desenhar_texto("Pressione qualquer tecla para começar", 30, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    elif em_tela_morte:
        tela.fill(PRETO)
        desenhar_texto("Você morreu! Pressione qualquer tecla para reiniciar ou Esc para sair", 30, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    clock.tick(60)

# Finaliza o Pygame
pygame.quit()
sys.exit()