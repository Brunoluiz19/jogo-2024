import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 1000
altura_tela = 805
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Cores
BRANCO = (255,255,255)

# Carrega as imagens
imagem_inicio = pygame.image.load('imagem jogo\_ee80465a-bcb5-435d-90fc-9275a5ca9f2a.jpeg').convert_alpha()
imagem_fundo = pygame.image.load('imagem jogo\Fundo.png').convert()
imagem_morte = pygame.image.load('imagem jogo\_4328f170-e6c9-4d9e-b2bd-367e5ab09727.jpeg').convert_alpha()

# Redimensiona as imagens para ajustar à tela
imagem_inicio = pygame.transform.scale(imagem_inicio, (largura_tela, altura_tela))
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, altura_tela))
imagem_morte = pygame.transform.scale(imagem_morte, (largura_tela, altura_tela))


# Limites laterais
LIMITE_ESQUERDO = 70
LIMITE_DIREITO = largura_tela - 70
# Variáveis do jogo
distancia_percorrida = 0/100
recorde = 0
melhores_recordes = []

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
        carro = "imagem jogo\Carro.png"
        self.image = pygame.image.load(carro)
        self.image = pygame.transform.scale(self.image, (48, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - self.rect.width)
        # Define a posição do jogador na parte inferior da tela
        self.rect.y = altura_tela - self.rect.height - 20  # Ajuste a posição conforme necessário
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
        carro1 = 'imagem jogo\Carro.png'
        self.image = pygame.image.load(carro1)
        self.image = pygame.transform.scale(self.image, (48, 100))
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
    todos_sprites.empty()
    inimigos.empty()
    todos_sprites.add(jogador)
    distancia_percorrida = 0
    for _ in range(5):
        x = random.randrange(LIMITE_ESQUERDO, LIMITE_DIREITO - 50)
        inimigo = Inimigo()
        inimigo.rect.x = x
        todos_sprites.add(inimigo)
        inimigos.add(inimigo)

# Tela de início
iniciar_jogo()

# Variáveis de fases
NUM_FASES = 10
fase_atual = 0
metas_fases = [500, 1000, 1500, 2000, 2500, 5000, 8000, 10000, 12000, 15000]  # Distância necessária para cada fase
taxas_aumento_fases = [2, 3, 4, 5, 6, 7, 8, 9, 9.5, 10]  # Taxa de aumento de velocidade para cada fase

# Função para determinar a fase atual
def determinar_fase(distancia_percorrida):
    for i in range(NUM_FASES):
        if (distancia_percorrida/100) < metas_fases[i]:
            return i
    return NUM_FASES - 1

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

        # Atualiza a fase
        nova_fase = determinar_fase(distancia_percorrida)
        if nova_fase > fase_atual:
            fase_atual = nova_fase
            # Ajusta a velocidade dos inimigos para a nova fase
            for inimigo in inimigos:
                inimigo.velocidade += taxas_aumento_fases[fase_atual]

        # Verifica se o jogador colidiu com algum inimigo
        if pygame.sprite.spritecollide(jogador, inimigos, False):
            em_tela_morte = True

            # Atualiza o recorde se a distância percorrida for maior que o recorde atual
            if (distancia_percorrida/100) > recorde:
                recorde = (distancia_percorrida/100)
                # Adiciona o recorde à lista de melhores recordes se ele não estiver lá
                if recorde not in melhores_recordes:
                    melhores_recordes.append(recorde)
                    # Mantém apenas os três melhores recordes
                    melhores_recordes.sort(reverse=True)
                    melhores_recordes = melhores_recordes[:3]

        # Calcula a distância percorrida pelo jogador
        distancia_percorrida += jogador.velocidade

        # Verifica e ajusta as velocidades para evitar que os inimigos se sobreponham
        for inimigo1 in inimigos:
            for inimigo2 in inimigos:
                if inimigo1 != inimigo2 and inimigo1.rect.colliderect(inimigo2.rect):
                    # Se houver colisão, ajusta as velocidades para que não se sobreponham
                    if inimigo1.rect.y < inimigo2.rect.y:
                        inimigo1.rect.y -= 5
                        inimigo2.rect.y += 5
                    else:
                        inimigo1.rect.y += 5
                        inimigo2.rect.y -= 5

        # Desenha na tela
        tela.blit(imagem_fundo, (0, 0))  # Desenha a imagem de fundo
        todos_sprites.draw(tela)

        # Desenha a distância percorrida e o recorde na tela
        desenhar_texto(f'Distância Percorrida: {int(distancia_percorrida/100)}', 20, BRANCO, largura_tela // 2, 20)
        desenhar_texto(f'Recorde: {recorde}', 20, BRANCO, largura_tela // 2, 50)

        # Atualiza a tela
        pygame.display.flip()

    elif em_tela_inicial:
        tela.blit(imagem_inicio, (0, 0))  # Desenha a imagem de início
        desenhar_texto("Pressione qualquer tecla para começar", 50, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    elif em_tela_morte:
        tela.blit(imagem_morte, (0, 0))  # Desenha a imagem de morte
        desenhar_texto("Você Bateu! Pressione qualquer tecla para reiniciar ou Esc para sair", 50, BRANCO, largura_tela // 2, altura_tela // 2)
        pygame.display.flip()

    clock.tick(240)

# Finaliza o Pygame
pygame.quit()
sys.exit()
