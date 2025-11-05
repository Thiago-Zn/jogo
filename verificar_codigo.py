#!/usr/bin/env python
"""
Script para verificar erros de sintaxe e indentação em todos os arquivos Python
"""

import py_compile
import os
import sys

def verificar_arquivo(caminho):
    """Verifica um arquivo Python"""
    try:
        py_compile.compile(caminho, doraise=True)
        print(f"[OK] {caminho}")
        return True
    except py_compile.PyCompileError as e:
        print(f"[ERRO] {caminho}")
        print(f"   Erro: {e}")
        return False

def main():
    """Verifica todos os arquivos Python do projeto"""
    arquivos = [
        "atravessar_rua.py",
        "config.py",
        "game/camera.py",
        "game/collision_system.py",
        "game/procedural_generator.py",
        "game/river_physics.py",
        "entities/carro.py",
        "entities/jogador.py",
        "entities/lilypad.py",
        "entities/safe_zone.py",
        "entities/tartaruga.py",
        "entities/tronco.py",
        "ui/button.py",
        "ui/game_over.py",
        "ui/hud.py",
        "ui/menu.py",
    ]
    
    print("=" * 60)
    print("VERIFICANDO CODIGO DO JOGO")
    print("=" * 60)
    print()
    
    erros = []
    sucessos = 0
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            if verificar_arquivo(arquivo):
                sucessos += 1
            else:
                erros.append(arquivo)
        else:
            print(f"AVISO: {arquivo} (nao encontrado)")
    
    print()
    print("=" * 60)
    print(f"Resultados: {sucessos} OK | {len(erros)} ERROS")
    
    if erros:
        print()
        print("ARQUIVOS COM ERROS:")
        for erro in erros:
            print(f"   - {erro}")
        sys.exit(1)
    else:
        print("TODOS OS ARQUIVOS ESTAO OK!")
        sys.exit(0)

if __name__ == "__main__":
    main()

