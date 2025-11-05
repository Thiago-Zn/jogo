#!/usr/bin/env python3
"""
🐸 ATRAVESSAR A RUA - Um jogo inspirado em Frogger 🐸
Desenvolvido para testar o potencial da IA como desenvolvedora de jogos

Objetivo: Atravesse a rua cheia de carros sem ser atingido!
Controles: Setas do teclado (↑ ↓ ← →)
"""

import pygame
import random
import sys

# ==================== CONFIGURAÇÕES ====================
# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (34, 177, 76)
VERDE_ESCURO = (20, 120, 50)
VERMELHO = (237, 28, 36)
AZUL = (0, 162, 232)
AMARELO = (255, 242, 0)
LARANJA = (255, 127, 39)
ROXO = (163, 73, 164)
CINZA = (127, 127, 127)
CINZA_ESCURO = (64, 64, 64)
ASFALTO = (50, 50, 50)

# Dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Configurações do jogo
FPS = 60
TAMANHO_CELULA = 50


# ==================== CLASSE DO JOGADOR ====================
class Jogador(pygame.sprite.Sprite):
    """Classe que representa o personagem controlado pelo jogador"""

    def __init__(self, x, y):
        super().__init__()
        self.tamanho = 40
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Posição inicial para reset
        self.pos_inicial_x = x
        self.pos_inicial_y = y

        # Velocidade de movimento
        self.velocidade = 5

        # Animação
        self.angulo = 0
        self.cor_principal = VERDE
        self.cor_secundaria = VERDE_ESCURO

        self.desenhar()

    def desenhar(self):
        """Desenha o personagem (um sapo estilizado)"""
        self.image.fill((0, 0, 0, 0))  # Transparente

        # Corpo do sapo
        pygame.draw.ellipse(self.image, self.cor_principal,
                          (5, 10, 30, 25))

        # Olhos
        pygame.draw.circle(self.image, BRANCO, (15, 15), 6)
        pygame.draw.circle(self.image, BRANCO, (25, 15), 6)
        pygame.draw.circle(self.image, PRETO, (15, 15), 3)
        pygame.draw.circle(self.image, PRETO, (25, 15), 3)

        # Pernas (traseiras)
        pygame.draw.ellipse(self.image, self.cor_secundaria, (2, 25, 12, 10))
        pygame.draw.ellipse(self.image, self.cor_secundaria, (26, 25, 12, 10))

    def mover(self, dx, dy):
        """Move o jogador, mantendo dentro dos limites da tela"""
        nova_x = self.rect.x + dx * self.velocidade
        nova_y = self.rect.y + dy * self.velocidade

        # Limites da tela
        if 0 <= nova_x <= LARGURA_TELA - self.tamanho:
            self.rect.x = nova_x
        if 50 <= nova_y <= ALTURA_TELA - self.tamanho - 50:
            self.rect.y = nova_y

    def resetar_posicao(self):
        """Retorna o jogador à posição inicial"""
        self.rect.x = self.pos_inicial_x
        self.rect.y = self.pos_inicial_y

    def chegou_ao_topo(self):
        """Verifica se o jogador chegou ao topo (venceu)"""
        return self.rect.y <= 80


# ==================== CLASSE DO CARRO ====================
class Carro(pygame.sprite.Sprite):
    """Classe que representa um carro obstáculo"""

    def __init__(self, x, y, velocidade, cor, direcao=1):
        super().__init__()
        self.largura = 60
        self.altura = 35
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocidade = velocidade
        self.cor = cor
        self.direcao = direcao  # 1 = direita, -1 = esquerda

        self.desenhar()

    def desenhar(self):
        """Desenha o carro com detalhes"""
        self.image.fill((0, 0, 0, 0))

        # Corpo do carro
        pygame.draw.rect(self.image, self.cor, (5, 8, 50, 20), border_radius=5)

        # Janelas
        cor_janela = (100, 180, 220, 150)
        if self.direcao == 1:  # Indo para direita
            pygame.draw.rect(self.image, cor_janela, (35, 12, 12, 12))
        else:  # Indo para esquerda
            pygame.draw.rect(self.image, cor_janela, (13, 12, 12, 12))

        # Rodas
        pygame.draw.circle(self.image, PRETO, (15, 30), 6)
        pygame.draw.circle(self.image, PRETO, (45, 30), 6)
        pygame.draw.circle(self.image, CINZA, (15, 30), 3)
        pygame.draw.circle(self.image, CINZA, (45, 30), 3)

        # Faróis
        if self.direcao == 1:
            pygame.draw.circle(self.image, AMARELO, (52, 12), 3)
            pygame.draw.circle(self.image, AMARELO, (52, 22), 3)
        else:
            pygame.draw.circle(self.image, AMARELO, (8, 12), 3)
            pygame.draw.circle(self.image, AMARELO, (8, 22), 3)

    def update(self):
        """Atualiza a posição do carro"""
        self.rect.x += self.velocidade * self.direcao

        # Reposiciona quando sai da tela
        if self.direcao == 1 and self.rect.x > LARGURA_TELA:
            self.rect.x = -self.largura
        elif self.direcao == -1 and self.rect.x < -self.largura:
            self.rect.x = LARGURA_TELA


# ==================== CLASSE PRINCIPAL DO JOGO ====================
class JogoAtraversarRua:
    """Classe principal que gerencia todo o jogo"""

    def __init__(self):
        pygame.init()

        # Configuração da tela
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("🐸 Atravessar a Rua - Frogger Style")
        self.relogio = pygame.time.Clock()

        # Fonte
        self.fonte_grande = pygame.font.Font(None, 72)
        self.fonte_media = pygame.font.Font(None, 48)
        self.fonte_pequena = pygame.font.Font(None, 32)

        # Estado do jogo
        self.estado = "menu"  # menu, jogando, game_over, vitoria
        self.pontuacao = 0
        self.nivel = 1
        self.vidas = 3
        self.tempo_inicio = 0
        self.melhor_pontuacao = 0

        # Grupos de sprites
        self.todos_sprites = pygame.sprite.Group()
        self.carros = pygame.sprite.Group()

        # Inicializar componentes
        self.jogador = None
        self.inicializar_jogo()

    def inicializar_jogo(self):
        """Inicializa ou reinicia o jogo"""
        # Limpar sprites
        self.todos_sprites.empty()
        self.carros.empty()

        # Criar jogador
        self.jogador = Jogador(LARGURA_TELA // 2 - 20, ALTURA_TELA - 80)
        self.todos_sprites.add(self.jogador)

        # Criar carros
        self.criar_carros()

        # Reset de tempo
        self.tempo_inicio = pygame.time.get_ticks()

    def criar_carros(self):
        """Cria os carros em diferentes faixas"""
        cores_carros = [VERMELHO, AZUL, LARANJA, ROXO, AMARELO]

        # Configuração das faixas (y, velocidade_base, direcao)
        faixas = [
            (150, 2, 1),
            (210, 3, -1),
            (270, 2.5, 1),
            (330, 3.5, -1),
            (390, 3, 1),
            (450, 4, -1),
        ]

        # Aumenta dificuldade com o nível
        modificador_velocidade = 1 + (self.nivel - 1) * 0.3
        carros_por_faixa = 2 + (self.nivel - 1) // 2

        for faixa_y, velocidade_base, direcao in faixas:
            velocidade = velocidade_base * modificador_velocidade

            for i in range(carros_por_faixa):
                # Distribui carros ao longo da faixa
                espacamento = LARGURA_TELA // carros_por_faixa
                x_inicial = i * espacamento + random.randint(-50, 50)

                if direcao == -1:
                    x_inicial = LARGURA_TELA - x_inicial

                cor = random.choice(cores_carros)
                carro = Carro(x_inicial, faixa_y, velocidade, cor, direcao)
                self.carros.add(carro)
                self.todos_sprites.add(carro)

    def processar_entrada(self):
        """Processa entrada do teclado"""
        teclas = pygame.key.get_pressed()

        if self.estado == "jogando":
            if teclas[pygame.K_UP]:
                self.jogador.mover(0, -1)
            if teclas[pygame.K_DOWN]:
                self.jogador.mover(0, 1)
            if teclas[pygame.K_LEFT]:
                self.jogador.mover(-1, 0)
            if teclas[pygame.K_RIGHT]:
                self.jogador.mover(1, 0)

    def verificar_colisoes(self):
        """Verifica colisões entre jogador e carros"""
        colisoes = pygame.sprite.spritecollide(
            self.jogador, self.carros, False,
            pygame.sprite.collide_rect_ratio(0.8)  # Colisão um pouco mais generosa
        )

        if colisoes:
            self.vidas -= 1
            self.jogador.resetar_posicao()

            if self.vidas <= 0:
                self.estado = "game_over"
                if self.pontuacao > self.melhor_pontuacao:
                    self.melhor_pontuacao = self.pontuacao

    def verificar_vitoria(self):
        """Verifica se o jogador chegou ao topo"""
        if self.jogador.chegou_ao_topo():
            # Pontuação baseada no tempo
            tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicio) / 1000
            bonus_tempo = max(0, int(100 - tempo_decorrido))
            self.pontuacao += 100 + bonus_tempo + (self.nivel * 50)

            # Próximo nível
            self.nivel += 1
            self.vidas = min(self.vidas + 1, 5)  # Ganha uma vida, max 5
            self.inicializar_jogo()

    def desenhar_fundo(self):
        """Desenha o cenário do jogo"""
        # Céu
        self.tela.fill(AZUL)

        # Área segura superior (grama)
        pygame.draw.rect(self.tela, VERDE, (0, 50, LARGURA_TELA, 80))

        # Decoração da grama
        for i in range(0, LARGURA_TELA, 30):
            pygame.draw.circle(self.tela, VERDE_ESCURO, (i, 70), 8)
            pygame.draw.circle(self.tela, VERDE_ESCURO, (i + 15, 90), 6)

        # Rua (asfalto)
        pygame.draw.rect(self.tela, ASFALTO, (0, 130, LARGURA_TELA, 380))

        # Faixas da rua
        for y in range(150, 510, 60):
            for x in range(0, LARGURA_TELA, 40):
                pygame.draw.rect(self.tela, AMARELO, (x, y - 2, 20, 4))

        # Área segura inferior (calçada)
        pygame.draw.rect(self.tela, CINZA, (0, 510, LARGURA_TELA, 90))

    def desenhar_hud(self):
        """Desenha informações na tela (HUD)"""
        # Pontuação
        texto_pontos = self.fonte_pequena.render(
            f"Pontos: {self.pontuacao}", True, BRANCO
        )
        self.tela.blit(texto_pontos, (10, 10))

        # Nível
        texto_nivel = self.fonte_pequena.render(
            f"Nível: {self.nivel}", True, BRANCO
        )
        self.tela.blit(texto_nivel, (LARGURA_TELA - 150, 10))

        # Vidas
        texto_vidas = self.fonte_pequena.render("Vidas:", True, BRANCO)
        self.tela.blit(texto_vidas, (LARGURA_TELA // 2 - 80, 10))

        for i in range(self.vidas):
            pygame.draw.circle(self.tela, VERMELHO,
                             (LARGURA_TELA // 2 + 10 + i * 30, 25), 10)

        # Timer
        tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicio) / 1000
        texto_tempo = self.fonte_pequena.render(
            f"Tempo: {tempo_decorrido:.1f}s", True, BRANCO
        )
        self.tela.blit(texto_tempo, (10, ALTURA_TELA - 40))

    def desenhar_menu(self):
        """Desenha o menu inicial"""
        self.tela.fill(AZUL)

        # Título
        titulo = self.fonte_grande.render("ATRAVESSAR A RUA", True, AMARELO)
        self.tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 100))

        # Subtítulo
        subtitulo = self.fonte_pequena.render("Inspirado em Frogger", True, BRANCO)
        self.tela.blit(subtitulo, (LARGURA_TELA // 2 - subtitulo.get_width() // 2, 180))

        # Instruções
        instrucoes = [
            "Use as SETAS do teclado para mover",
            "Evite os carros e chegue ao topo!",
            "",
            "Pressione ESPAÇO para começar",
            "Pressione ESC para sair"
        ]

        y_offset = 280
        for instrucao in instrucoes:
            texto = self.fonte_pequena.render(instrucao, True, BRANCO)
            self.tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, y_offset))
            y_offset += 40

        # Melhor pontuação
        if self.melhor_pontuacao > 0:
            melhor = self.fonte_pequena.render(
                f"Melhor Pontuação: {self.melhor_pontuacao}", True, VERDE
            )
            self.tela.blit(melhor, (LARGURA_TELA // 2 - melhor.get_width() // 2, 500))

        # Desenha um sapo animado
        sapo_demo = Jogador(LARGURA_TELA // 2 - 20, 220)
        self.tela.blit(sapo_demo.image, (LARGURA_TELA // 2 - 20, 220))

    def desenhar_game_over(self):
        """Desenha a tela de game over"""
        # Fundo semi-transparente
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        overlay.set_alpha(200)
        overlay.fill(PRETO)
        self.tela.blit(overlay, (0, 0))

        # Texto Game Over
        texto_go = self.fonte_grande.render("GAME OVER!", True, VERMELHO)
        self.tela.blit(texto_go, (LARGURA_TELA // 2 - texto_go.get_width() // 2, 200))

        # Pontuação final
        texto_pontos = self.fonte_media.render(
            f"Pontuação: {self.pontuacao}", True, BRANCO
        )
        self.tela.blit(texto_pontos, (LARGURA_TELA // 2 - texto_pontos.get_width() // 2, 300))

        # Nível alcançado
        texto_nivel = self.fonte_pequena.render(
            f"Nível Alcançado: {self.nivel}", True, BRANCO
        )
        self.tela.blit(texto_nivel, (LARGURA_TELA // 2 - texto_nivel.get_width() // 2, 370))

        # Instruções
        texto_reiniciar = self.fonte_pequena.render(
            "Pressione ESPAÇO para jogar novamente", True, AMARELO
        )
        self.tela.blit(texto_reiniciar,
                      (LARGURA_TELA // 2 - texto_reiniciar.get_width() // 2, 450))

        texto_menu = self.fonte_pequena.render(
            "Pressione ESC para voltar ao menu", True, BRANCO
        )
        self.tela.blit(texto_menu,
                      (LARGURA_TELA // 2 - texto_menu.get_width() // 2, 490))

    def executar(self):
        """Loop principal do jogo"""
        rodando = True

        while rodando:
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == "menu":
                            rodando = False
                        else:
                            self.estado = "menu"

                    if evento.key == pygame.K_SPACE:
                        if self.estado == "menu":
                            self.pontuacao = 0
                            self.nivel = 1
                            self.vidas = 3
                            self.inicializar_jogo()
                            self.estado = "jogando"
                        elif self.estado == "game_over":
                            self.pontuacao = 0
                            self.nivel = 1
                            self.vidas = 3
                            self.inicializar_jogo()
                            self.estado = "jogando"

            # Lógica do jogo
            if self.estado == "jogando":
                self.processar_entrada()
                self.carros.update()
                self.verificar_colisoes()
                self.verificar_vitoria()

            # Desenho
            if self.estado == "menu":
                self.desenhar_menu()
            elif self.estado == "jogando":
                self.desenhar_fundo()
                self.todos_sprites.draw(self.tela)
                self.desenhar_hud()
            elif self.estado == "game_over":
                self.desenhar_fundo()
                self.todos_sprites.draw(self.tela)
                self.desenhar_game_over()

            # Atualizar tela
            pygame.display.flip()
            self.relogio.tick(FPS)

        pygame.quit()
        sys.exit()


# ==================== EXECUÇÃO PRINCIPAL ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🐸 ATRAVESSAR A RUA - Frogger Style 🐸")
    print("=" * 50)
    print("\n🎮 Controles:")
    print("  ↑ ↓ ← → : Mover o sapo")
    print("  ESPAÇO  : Iniciar/Reiniciar")
    print("  ESC     : Menu/Sair")
    print("\n🎯 Objetivo:")
    print("  Atravesse a rua sem ser atingido pelos carros!")
    print("  Chegue ao topo para avançar de nível!")
    print("\n💡 Dicas:")
    print("  - Quanto mais rápido você chegar, mais pontos ganha!")
    print("  - Cada nível fica mais difícil")
    print("  - Você ganha uma vida extra a cada nível")
    print("\n🚀 Iniciando jogo...\n")

    try:
        jogo = JogoAtraversarRua()
        jogo.executar()
    except Exception as e:
        print(f"\n❌ Erro ao executar o jogo: {e}")
        print("Certifique-se de que o Pygame está instalado:")
        print("  pip install pygame")
