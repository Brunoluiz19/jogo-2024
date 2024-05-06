import random

# Constantes do jogo
NAÇÕES = ['USA', 'Rússia', 'China', 'Reino Unido', 'França']
TABULEIRO_LINHAS = 10
TABULEIRO_COLUNAS = 10
NAVIO_PEQUENO = 2
NAVIO_MEDIO = 3
NAVIO_GRANDE = 4

# Classe para representar um navio
class Navio:
    def __init__(self, tamanho, x, y, orientacao):
        self.tamanho = tamanho
        self.x = x
        self.y = y
        self.orientacao = orientacao
        self.danificado = False

# Classe para representar um jogador
class Jogador:
    def __init__(self, nação, tabuleiro):
        self.nação = nação
        self.tabuleiro = tabuleiro
        self.navios = []

    def alocar_navios(self):
        for _ in range(5):
            tamanho = random.choice([NAVIO_PEQUENO, NAVIO_MEDIO, NAVIO_GRANDE])
            x = random.randint(0, TABULEIRO_LINHAS - 1)
            y = random.randint(0, TABULEIRO_COLUNAS - 1)
            orientacao = random.choice(['h', 'v'])
            navio = Navio(tamanho, x, y, orientacao)
            self.navios.append(navio)
            self.alocar_navio_no_tabuleiro(navio)

    def alocar_navio_no_tabuleiro(self, navio):
        if navio.orientacao == 'h':
            for i in range(navio.tamanho):
                self.tabuleiro[navio.x][navio.y + i] = 'N'
        else:
            for i in range(navio.tamanho):
                self.tabuleiro[navio.x + i][navio.y] = 'N'

    def verificar_atingido(self, x, y):
        for navio in self.navios:
            if navio.x <= x < navio.x + navio.tamanho and navio.y <= y < navio.y + navio.tamanho:
                navio.danificado = True
                return True
        return False

    def imprimir_tabuleiro(self):
        print('  A B C D E F G H I J')
        for i, linha in enumerate(self.tabuleiro):
            print(f'{i+1} ', end='')
            for celula in linha:
                print(celula, end=' ')
            print()

# Função para jogar um tiro
def jogar_tiro(jogador_atacante, jogador_defensor, x, y):
    if jogador_defensor.verificar_atingido(x, y):
        print('Você atingiu um navio!')
        jogador_defensor.tabuleiro[x][y] = 'X'
    else:
        print('Você errou!')
        jogador_defensor.tabuleiro[x][y] = 'O'

# Função para verificar se todos os navios de um jogador foram afundados
def verificar_vitoria(jogador):
    for navio in jogador.navios:
        if not navio.danificado:
            return False
    return True

# Inicializar o jogo
jogador1 = Jogador(random.choice(NAÇÕES), [[' ' for _ in range(TABULEIRO_COLUNAS)] for _ in range(TABULEIRO_LINHAS)])
jogador2 = Jogador(random.choice(NAÇÕES), [[' ' for _ in range(TABULEIRO_COLUNAS)] for _ in range(TABULEIRO_LINHAS)])

jogador1.alocar_navios()
jogador2.alocar_navios()

# Sorteio do primeiro jogador
jogador_atual = random.choice([jogador1, jogador2])

# Loop do jogo
while True:
    print(f'Vez de {jogador_atual.nação}')
    jogador_atual.imprimir_tabuleiro()
    x = int(input('Digite a linha do tiro (1-10): ')) - 1
    y = ord(input('Digite a coluna do tiro (A-J): ').upper()) - 65
    jogar_tiro(jogador_atual, jogador_atual == jogador1 and jogador2 or jogador1, x, y)
    if verificar_vitoria(jogador_atual == jogador1 and jogador2 or jogador1):
        print(f'{jogador_atual.nação} venceu!')
        break
    jogador_atual = jogador_atual == jogador1 and jogador2 or jogador1