import os
import time
from jogador import Jogador
from banco_perguntas import BancoDePerguntas
from recordes import Recordes
from jogador_bot import JogadorBot


def limpar_tela():
    """
    Limpa a tela do terminal.
    """
    os.system("cls" if os.name == "nt" else "clear")


class Jogo:
    def __init__(self, jogadores_nomes, diretorio_perguntas="perguntas"):
        """
        Inicializa o jogo com a lista de jogadores e carrega o banco de perguntas.
        """
        self.jogadores = []
        for j in jogadores_nomes:
            if isinstance(j, Jogador):
                self.jogadores.append(j)
            else:
                self.jogadores.append(Jogador(j))
        self.banco_perguntas = BancoDePerguntas(diretorio=diretorio_perguntas)
        self.rodada = 1
        self.categoria_atual = None

    def definir_dificuldade(self):
        """
        Define a dificuldade da rodada com base no número da rodada.
        """
        if self.rodada <= 5:
            return 1
        elif self.rodada <= 10:
            return 2
        else:
            return 3

    def selecionar_categoria(self):
        """
        Permite ao jogador escolher uma categoria para a rodada.
        """
        print("\nCategorias disponíveis:")
        for i, categoria in enumerate(self.banco_perguntas.categorias):
            print(f"{i+1}. {categoria.capitalize()}")
        while True:
            try:
                escolha = int(input("Escolha uma categoria pelo número: ")) - 1
                if 0 <= escolha < len(self.banco_perguntas.categorias):
                    self.categoria_atual = self.banco_perguntas.categorias[escolha]
                    print(f"Categoria selecionada: {self.categoria_atual.capitalize()}")
                    time.sleep(2)
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Insira um número.")

    def iniciar(self):
        limpar_tela()
        print("Bem-vindo ao Desafio das Mentes!")
        self.selecionar_categoria()
        while True:
            limpar_tela()
            print(f"\n=== Rodada {self.rodada} ===")
            dificuldade = self.definir_dificuldade()
            respostas = {}
            # Cada jogador ativo responde a uma pergunta exclusiva
            for jogador in self.jogadores:
                if jogador.esta_ativo():
                    print(f"\nVez de {jogador.nome}:")
                    pergunta = self.banco_perguntas.obter_pergunta_aleatoria(
                        self.categoria_atual, dificuldade
                    )
                    if not pergunta:
                        print("Sem mais perguntas disponíveis nesta categoria!")
                        return
                    print(pergunta)
                    if hasattr(jogador, "responder"):
                        time.sleep(2)
                        resposta = jogador.responder(pergunta, self.rodada)
                        print(f"{jogador.nome} (BOT) escolheu: {resposta+1}")
                        respostas[jogador] = (pergunta, resposta)
                        time.sleep(1)
                    else:
                        while True:
                            try:
                                resposta = (
                                    int(input("Escolha a sua resposta (1-4): ")) - 1
                                )
                                if 0 <= resposta < 4:
                                    respostas[jogador] = (pergunta, resposta)
                                    break
                                else:
                                    print("Número inválido. Tente novamente.")
                            except ValueError:
                                print("Entrada inválida. Tente novamente.")
            # Processar as respostas da rodada
            acertos = []
            for jogador, (pergunta, resposta) in respostas.items():
                if pergunta.verificar_resposta(resposta):
                    print(f"{jogador.nome} acertou!")
                    jogador.adicionar_pontuacao(1)
                    acertos.append(jogador)
                else:
                    print(
                        f"{jogador.nome} errou! Resposta correta: {pergunta.alternativas_embaralhadas[pergunta.indice_resposta_embaralhada]}"
                    )
                    jogador.eliminar()
            # Critério de término: se apenas um jogador acertou nesta rodada, ele vence.
            if len(acertos) == 1:
                print(
                    f"\nParabéns, {acertos[0].nome}! Você é o vencedor com {acertos[0].pontuacao} pontos!"
                )
                recordes = Recordes()
                recordes.atualizar_recorde(acertos[0].nome, acertos[0].pontuacao)
                break
            elif len(acertos) == 0:
                print("\nNenhum jogador acertou. Todos foram eliminados. Fim de jogo!")
                break
            else:
                print(
                    "\nRodada concluída. Jogadores que acertaram continuam para a próxima rodada."
                )
            self.rodada += 1
            ativos = [j for j in self.jogadores if j.esta_ativo()]
            if len(ativos) <= 1:
                if ativos:
                    print(
                        f"\nParabéns, {ativos[0].nome}! Você venceu com {ativos[0].pontuacao} pontos!"
                    )
                    recordes = Recordes()
                    recordes.atualizar_recorde(ativos[0].nome, ativos[0].pontuacao)
                else:
                    print("Nenhum jogador permanece ativo. Fim de jogo!")
                break
            # Permite trocar de categoria a cada rodada, se desejar.
            print("\nDeseja trocar a categoria para a próxima rodada? (s/n)")
            escolha = input().strip().lower()
            if escolha == "s":
                self.selecionar_categoria()
