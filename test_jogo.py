#!/usr/bin/env python3
"""
Script de teste para verificar se o jogo está funcionando corretamente
"""

import sys
import os

# Define o display headless para testes em ambiente sem interface gráfica
os.environ['SDL_VIDEODRIVER'] = 'dummy'

try:
    print("🧪 Iniciando testes do jogo...")
    print("=" * 50)

    # Testa importação do pygame
    print("✓ Importando pygame...")
    import pygame
    print(f"  Versão do Pygame: {pygame.version.ver}")

    # Testa importação do módulo do jogo
    print("✓ Importando módulo do jogo...")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Importa as classes do jogo
    from atravessar_rua import Jogador, Carro, JogoAtraversarRua

    print("✓ Classes importadas com sucesso")

    # Inicializa pygame
    print("✓ Inicializando Pygame...")
    pygame.init()

    # Testa criação do jogador
    print("✓ Testando classe Jogador...")
    jogador = Jogador(100, 100)
    assert jogador.rect.x == 100
    assert jogador.rect.y == 100
    print(f"  Jogador criado em posição ({jogador.rect.x}, {jogador.rect.y})")

    # Testa movimento do jogador
    jogador.mover(1, 0)
    assert jogador.rect.x == 105  # velocidade padrão é 5
    print(f"  Movimento testado: nova posição ({jogador.rect.x}, {jogador.rect.y})")

    # Testa criação de carro
    print("✓ Testando classe Carro...")
    from atravessar_rua import VERMELHO
    carro = Carro(50, 200, 3, VERMELHO, 1)
    assert carro.rect.x == 50
    assert carro.rect.y == 200
    print(f"  Carro criado em posição ({carro.rect.x}, {carro.rect.y})")

    # Testa movimento do carro
    pos_inicial = carro.rect.x
    carro.update()
    assert carro.rect.x > pos_inicial
    print(f"  Movimento testado: nova posição ({carro.rect.x}, {carro.rect.y})")

    # Testa inicialização do jogo (sem executar o loop)
    print("✓ Testando inicialização do jogo...")
    jogo = JogoAtraversarRua()
    assert jogo.estado == "menu"
    assert jogo.pontuacao == 0
    assert jogo.nivel == 1
    assert jogo.vidas == 3
    print(f"  Estado inicial: {jogo.estado}")
    print(f"  Pontuação: {jogo.pontuacao}")
    print(f"  Nível: {jogo.nivel}")
    print(f"  Vidas: {jogo.vidas}")

    # Testa criação de carros
    print("✓ Testando criação de carros...")
    num_carros = len(jogo.carros)
    print(f"  Número de carros criados: {num_carros}")
    assert num_carros > 0

    # Testa reset do jogo
    print("✓ Testando reset do jogo...")
    jogo.inicializar_jogo()
    assert jogo.jogador is not None
    print("  Jogo reiniciado com sucesso")

    pygame.quit()

    print("=" * 50)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 50)
    print("\n🎮 O jogo está pronto para ser executado!")
    print("Execute: python atravessar_rua.py")

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de que o pygame está instalado:")
    print("  pip install pygame")
    sys.exit(1)

except AssertionError as e:
    print(f"❌ Teste falhou: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
