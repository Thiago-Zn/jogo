# Diagnóstico de Problemas do Jogo

## Problema: Jogo fecha imediatamente ao executar

### Solução 1: Executar o script de diagnóstico
Execute o arquivo `testar_jogo.py` para identificar o problema:
```bash
python testar_jogo.py
```

### Solução 2: Verificar manualmente

1. **Verificar se Pygame-CE está instalado:**
   ```bash
   python -c "import pygame; print(pygame.version.ver)"
   ```
   Se der erro, instale:
   ```bash
   python -m pip install pygame-ce
   ```

2. **Verificar se todos os arquivos estão presentes:**
   - `atravessar_rua.py`
   - `config.py`
   - `entities/` (com `__init__.py`, `jogador.py`, `carro.py`)
   - `game/` (com `__init__.py`, `game_state.py`, `collision.py`)
   - `ui/` (com `__init__.py`, `menu.py`, `hud.py`, `game_over.py`)

3. **Executar diretamente pelo Python:**
   ```bash
   python atravessar_rua.py
   ```
   Isso mostrará mensagens de erro no terminal.

### Solução 3: Usar o script .bat melhorado

O arquivo `executar_jogo.bat` foi atualizado para:
- Mostrar erros claramente
- Pausar no final para você ver os erros
- Instalar pygame-ce automaticamente se necessário

### Erros Comuns

**Erro: "ModuleNotFoundError: No module named 'pygame'"**
- Solução: `python -m pip install pygame-ce`

**Erro: "Falha ao criar janela do jogo"**
- Verifique se você tem um ambiente gráfico (Windows Desktop)
- Não funciona em servidores sem GUI

**Erro: "Falha ao importar módulos"**
- Verifique se todos os arquivos estão no lugar correto
- Verifique se há erros de sintaxe nos arquivos Python

### Se ainda não funcionar

Execute o diagnóstico completo:
```bash
python testar_jogo.py
```

E envie a mensagem de erro completa para análise.

