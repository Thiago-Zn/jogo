#!/usr/bin/env python3
"""
Script de teste para diagnosticar problemas do jogo
"""

import sys

print("=" * 60)
print("DIAGNOSTICO DO JOGO")
print("=" * 60)

# Teste 1: Python
print("\n[1/6] Verificando Python...")
print(f"    Versao: {sys.version}")
print("    [OK] Python detectado")

# Teste 2: Importar config
print("\n[2/6] Verificando config.py...")
try:
    import config
    print(f"    Largura: {config.LARGURA_TELA}, Altura: {config.ALTURA_TELA}")
    print("    [OK] config.py carregado")
except Exception as e:
    print(f"    [ERRO] Falha ao carregar config.py: {e}")
    input("\nPressione ENTER para sair...")
    sys.exit(1)

# Teste 3: Importar módulos
print("\n[3/6] Verificando modulos...")
try:
    from entities import Jogador, Carro
    print("    [OK] entities importado")
    
    from game import GameState, CollisionSystem
    print("    [OK] game importado")
    
    from ui import Menu, HUD, GameOverScreen
    print("    [OK] ui importado")
except Exception as e:
    print(f"    [ERRO] Falha ao importar modulos: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione ENTER para sair...")
    sys.exit(1)

# Teste 4: Pygame
print("\n[4/6] Verificando Pygame-CE...")
try:
    import pygame
    pygame.init()
    print(f"    Versao: {pygame.version.ver}")
    print("    [OK] Pygame inicializado")
except Exception as e:
    print(f"    [ERRO] Falha ao inicializar Pygame: {e}")
    print("    SOLUCAO: python -m pip install pygame-ce")
    input("\nPressione ENTER para sair...")
    sys.exit(1)

# Teste 5: Criar janela
print("\n[5/6] Testando criacao de janela...")
try:
    screen = pygame.display.set_mode((800, 600))
    print("    [OK] Janela criada com sucesso")
    pygame.quit()
except Exception as e:
    print(f"    [ERRO] Falha ao criar janela: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione ENTER para sair...")
    sys.exit(1)

# Teste 6: Criar instância do jogo
print("\n[6/6] Testando criacao do jogo...")
try:
    from atravessar_rua import JogoAtraversarRua
    jogo = JogoAtraversarRua()
    print("    [OK] Jogo criado com sucesso")
    print("\n" + "=" * 60)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\nO jogo esta pronto para executar.")
    print("Execute: python atravessar_rua.py")
    print("Ou clique em: executar_jogo.bat")
except Exception as e:
    print(f"    [ERRO] Falha ao criar jogo: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("ERRO ENCONTRADO!")
    print("=" * 60)

print("\n")
input("Pressione ENTER para sair...")

