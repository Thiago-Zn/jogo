# 🎮 Como Jogar - Guia Rápido v2.0

## 🚀 Instalação Rápida (1 minuto)

### Opção 1: Instalação automática (Recomendado)

**Windows:**
```bash
executar_jogo.bat
```

### Opção 2: Instalação manual
```bash
# Instale o Pygame-CE
pip install pygame-ce
# ou
python -m pip install pygame-ce

# Execute o jogo
python atravessar_rua.py
```

### Opção 3: Instalador completo
**Windows:**
```bash
instalar_e_jogar.bat
```

## 🎯 Controles

| Tecla | Ação |
|-------|------|
| **↑** ou **W** | Mover para CIMA |
| **↓** ou **S** | Mover para BAIXO |
| **←** ou **A** | Mover para ESQUERDA |
| **→** ou **D** | Mover para DIREITA |
| **ESPAÇO** | Começar / Recomeçar |
| **ESC** | Menu / Sair |

## 🎮 Como Jogar

### Passo 1: Inicie o jogo
```bash
python atravessar_rua.py
```

### Passo 2: Tela de Menu
- Você verá o menu principal com instruções
- Pressione **ESPAÇO** para começar

### Passo 3: Jogando
1. **Objetivo**: Leve o sapo (personagem verde) do fundo da tela até o topo
2. **Desafio**: Evite ser atingido pelos carros que se movem horizontalmente
3. **Movimento**: Use as setas ou WASD para navegar
4. **Vidas**: Você começa com 3 vidas ❤️❤️❤️
5. **Tempo**: Quanto mais rápido chegar, mais pontos ganha!

### Passo 4: Avançando de Nível
- Ao chegar no topo, você avança para o próximo nível
- Cada nível aumenta a dificuldade:
  - Mais carros na rua
  - Carros mais rápidos
- Você ganha **1 vida extra** a cada nível completado (máximo 5 vidas)

### Passo 5: Game Over
- Se perder todas as vidas, é Game Over
- Pressione **ESPAÇO** para jogar novamente
- Pressione **ESC** para voltar ao menu

## 💡 Dicas Essenciais

1. **Observe antes de atravessar**
   - Pause e veja o padrão dos carros
   - Identifique os espaços seguros

2. **Movimento lateral**
   - Use as setas ← → ou A/D para evitar carros
   - Você não precisa ir em linha reta!

3. **Não tenha pressa**
   - O bônus de tempo é pequeno
   - É melhor chegar devagar do que perder uma vida

4. **Planeje sua rota**
   - Carros se movem em padrões previsíveis
   - Encontre os "corredores" seguros

5. **Use todo o espaço**
   - Você pode recuar se necessário
   - Às vezes é melhor voltar e esperar

## 🏆 Sistema de Pontuação

- **100 pontos**: Por atravessar a rua
- **até 100 pontos**: Bônus de velocidade
- **50 × nível**: Bônus progressivo

### Exemplo:
- Nível 1, rápido: 100 + 80 + 50 = **230 pontos**
- Nível 5, rápido: 100 + 90 + 250 = **440 pontos**

## 🐛 Resolução de Problemas

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame-ce
# ou
pip3 install pygame-ce
# ou
python -m pip install pygame-ce
```

### "Python 3.14 não funciona"
O jogo agora funciona perfeitamente com Python 3.14 usando Pygame-CE!

### O jogo não abre
- Certifique-se de ter um ambiente gráfico (não funciona em servidores sem GUI)
- Teste se o pygame está funcionando:
```bash
python -c "import pygame; print(pygame.version.ver)"
```

### O jogo está muito rápido/lento
- O jogo roda a 60 FPS
- Se estiver muito lento, feche outros programas
- Se estiver muito rápido, pode ser um problema de sincronização (raro)

## 🎓 Estratégias Avançadas

### Para Iniciantes
- Fique mais tempo nas áreas seguras (grama)
- Atravesse uma faixa por vez
- Não se preocupe com o tempo

### Para Jogadores Intermediários
- Memorize os padrões dos carros
- Aproveite os espaços entre carros
- Busque o bônus de tempo

### Para Experts
- Domine o movimento diagonal
- Calcule a velocidade dos carros
- Tente alcançar o nível 10+!

## 📊 Desafios

- 🥉 **Bronze**: Alcançar nível 3
- 🥈 **Prata**: Alcançar nível 5
- 🥇 **Ouro**: Alcançar nível 8
- 💎 **Diamante**: Alcançar nível 10
- 🏆 **Mestre**: Alcançar nível 15+

## ✨ Novidades da v2.0

- ✅ Biblioteca Pygame-CE (compatível com Python 3.14)
- ✅ Código modular e organizado
- ✅ Suporte a WASD além das setas
- ✅ Melhor performance
- ✅ Gráficos mais suaves
- ✅ Melhor compatibilidade

## 🏗️ Estrutura do Código

O código foi reorganizado em módulos:

- **entities/**: Jogador e Carros
- **game/**: Lógica do jogo (estados, colisões)
- **ui/**: Interface (menu, HUD, game over)
- **utils/**: Utilitários (cores, helpers)
- **config.py**: Todas as configurações

## 🎉 Divirta-se!

Boa sorte atravessando a rua! O recorde mundial é nível 20... você consegue chegar lá? 🚀

---

**Versão 2.0 - Agora com Pygame-CE e código modular!**

**Dúvidas?** Leia o README.md completo para mais informações.
