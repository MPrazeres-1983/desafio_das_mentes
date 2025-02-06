# Desafio das Mentes 🎓🧠

**Criado por:** Mário Prazeres  

## 📌 Sobre o Jogo  

**Desafio das Mentes** é um jogo de perguntas e respostas competitivo, onde de **1 a 4 jogadores** (humanos ou BOTs) disputam para ver quem tem mais conhecimento. A cada rodada, os jogadores enfrentam perguntas de categorias variadas, com diferentes níveis de dificuldade.

### 🎮 Modos de Jogo  

#### 🔹 **Modo Solo**
- Apenas um jogador humano participa.  
- O objetivo é acumular o maior número de pontos possíveis sem ser eliminado.  

#### 🔹 **Modo Normal (Multijogador)**  
- Entre **2 a 4 jogadores** podem participar.  
- Pode incluir jogadores humanos e/ou BOTs.  
- Os BOTs respondem conforme a dificuldade da rodada:  

| Dificuldade | Rodadas  | Probabilidade de Acerto |
|------------|----------|------------------------|
| Fácil      | 1 – 5    | 80%                    |
| Médio      | 6 – 10   | 65%                    |
| Difícil    | 11+      | 50%                    |

###### 🏆 Regras do Jogo  

1️⃣ **Participantes**  
- **Modo Solo**: Apenas 1 jogador (humano).  
- **Modo Normal**: De 2 a 4 jogadores (humanos e/ou BOTs).  

2️⃣ **Objetivo**  
- Responder corretamente ao maior número de perguntas.  
- Permanecer no jogo enquanto os outros jogadores forem eliminados por respostas erradas.  

3️⃣ **Mecânica**  
- As perguntas pertencem a categorias específicas: Artes, Ciência e Tecnologia, Cultura Geral, Desporto, Geografia, História, etc.  
- As perguntas possuem três níveis de dificuldade progressivos:  
- **Rodadas 1 a 5**: Dificuldade 1 (fácil).  
- **Rodadas 6 a 10**: Dificuldade 2 (média).  
- **Rodadas 11 em diante**: Dificuldade 3 (difícil).  

4️⃣ **Pontuação**  
- Cada resposta correta vale **1 ponto**.  
- Respostas erradas eliminam o jogador da partida.  

5️⃣ **Modo Solo**  
- O jogador joga sozinho e tenta alcançar a maior pontuação possível antes de ser eliminado.  

6️⃣ **BOTs**  
- BOTs simulam jogadores e respondem com diferentes probabilidades de acerto.  
- São permitidos até **3 BOTs** no **Modo Normal**.  

7️⃣ **Registo de Recordes**  
- No final do jogo, os recordes são guardados automaticamente no ficheiro `recordes.json`.
- Os recordes incluem os nomes dos jogadores e as respetivas pontuações.  

8️⃣ **Como Vencer**  
- O **último jogador restante** será declarado **vencedor**.  
- Se todos os jogadores forem eliminados na mesma rodada e com a mesma pontuação, o jogo termina **empatado**.  

# 🚀 Como Jogar  

Para iniciar o jogo, execute o seguinte comando na pasta raiz:

python src/main.py

Passos no Jogo
1️⃣ Escolha o modo de jogo (Solo ou Multijogador).
2️⃣ Insira os nomes dos jogadores.
3️⃣ Responda corretamente às perguntas para acumular pontos:

Resposta Correta: O jogador ganha 1 ponto.
Resposta Errada: O jogador é eliminado.
4️⃣ No final, o vencedor é declarado e os recordes são guardados.

## 📂 Estrutura do Projeto

## 📂 Estrutura do Projeto

- **desafio_das_mentes/**
  - 📁 **data/**
    - 📄 `records.json`
  - 📁 **perguntas/**
    - 📄 `artes.json`
    - 📄 `alimentacao.json`
    - 📄 `ciencia_e_tecnologia.json`
    - 📄 `ciencias_naturais.json`
    - 📄 `cultura_geral.json`
    - 📄 `desporto.json`
    - 📄 `entretenimento.json`
    - 📄 `geografia.json`
    - 📄 `historia.json`
    - 📄 `mitologia.json`
  - 📁 **src/**
    - 📄 `banco_perguntas.py`
    - 📄 `interface.py`
    - 📄 `jogador.py`
    - 📄 `jogo.py`
    - 📄 `main.py`
    - 📄 `pergunta.py`
    - 📄 `jogo_solo.py`
    - 📄 `jogador_bot.py`
    - 📄 `recordes.py`
  - 📁 **sons/**
    - 🔊 `correto.wav`
    - 🔊 `errado.wav`
  - 📄 `requirements.txt`
  - 📄 `README.md`


📌 Funcionalidades Atuais

✔ Seleção de 1 a 4 jogadores.

✔ Escolha de categoria no início de cada rodada.

✔ Sistema de dificuldade crescente:

Rodadas 1 a 5: Perguntas de dificuldade 1.
Rodadas 6 a 10: Perguntas de dificuldade 2.
Rodadas 11 em diante: Perguntas de dificuldade 3.

✔ Aleatoriedade das alternativas para maior desafio.

✔ Eliminação progressiva dos jogadores em caso de erro.

✔ Tkinter para 100% de jogabilidade em interface gráfica.

✔ BOTs inteligentes que se ajustam à dificuldade.

✔ Sons para respostas corretas e incorretas.

✔ Edição ou remoção de jogadores que tenham sido criados por engano.

📌 Funcionalidades Planeadas 🔜

🛠️ Novos modos de jogo "cronometrados".

🛠️ Migrar para SQL (não é prioridade por enquanto).

🎖 Créditos

Criado por Mário Prazeres – Universidade Aberta (UAb)

Sons retirados do site Freesound
