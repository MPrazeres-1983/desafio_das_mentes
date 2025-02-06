from jogo import Jogo
from recordes import Recordes
import os
import time


def limpar_tela():
    """
    Limpa a tela do terminal (funciona em Windows e Unix).
    """
    os.system("cls" if os.name == "nt" else "clear")


class JogoSolo(Jogo):
    def __init__(self, jogador, diretorio_perguntas="perguntas"):
        """
        Inicializa o jogo solo com um único jogador.
        """
        super().__init__([jogador], diretorio_perguntas)
        self.jogador = jogador

    def iniciar(self):
        limpar_tela()
        print("=========================================")
        print("     Bem-vindo ao Desafio das Mentes     ")
        print("               MODO SOLO                 ")
        print("=========================================\n")

        # Seleciona a categoria para a rodada
        self.selecionar_categoria()

        while self.jogador.esta_ativo():
            limpar_tela()
            print(f"\n=== Rodada {self.rodada} - Modo Solo ===")
            if self.rodada > 1:
                print("\n=== Nova Categoria ===")
                self.selecionar_categoria()
            dificuldade = self.definir_dificuldade()
            print(
                f"Selecionando pergunta da categoria '{self.categoria_atual}' com dificuldade {dificuldade}...\n"
            )
            pergunta = self.banco_perguntas.obter_pergunta_aleatoria(
                self.categoria_atual, dificuldade
            )
            if not pergunta:
                print("Sem mais perguntas nesta categoria!")
                break
            print(pergunta)
            resposta = self.receber_resposta_solo(pergunta)
            self.processar_resposta(self.jogador, resposta, pergunta)
            self.rodada += 1

        self.exibir_resultado()

    def receber_resposta_solo(self, pergunta):
        """
        Recebe a resposta do jogador (BOT ou humano) no modo solo.
        """
        if hasattr(self.jogador, "responder"):
            time.sleep(2)  # Simula o tempo de "pensar"
            resposta = self.jogador.responder(pergunta, self.rodada)
            print(f"{self.jogador.nome} (BOT) escolheu a resposta: {resposta + 1}")
            time.sleep(1)
            return resposta
        else:
            while True:
                try:
                    resposta = int(input("Escolha a sua resposta (1-4): ")) - 1
                    if 0 <= resposta < 4:
                        return resposta
                    else:
                        print("Escolha inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Tente novamente.")

    def processar_resposta(self, jogador, resposta, pergunta):
        """
        Processa a resposta do jogador: se correta, adiciona ponto; se errada, elimina o jogador.
        """
        if pergunta.verificar_resposta(resposta):
            print("Resposta correta!")
            jogador.adicionar_pontuacao(1)
        else:
            print("Resposta errada!")
            print(
                f"A resposta correta era: {pergunta.alternativas_embaralhadas[pergunta.indice_resposta_embaralhada]}"
            )
            jogador.eliminar()
        time.sleep(3)

    def exibir_resultado(self):
        """
        Exibe o resultado final e atualiza os recordes.
        """
        limpar_tela()
        print("\n=== Fim de Jogo - Modo Solo ===")
        time.sleep(2)
        recordes = Recordes()
        if self.jogador.esta_ativo():
            print(
                f"Parabéns, {self.jogador.nome}! Terminou com {self.jogador.pontuacao} pontos!"
            )
            recordes.atualizar_recorde(self.jogador.nome, self.jogador.pontuacao)
        else:
            print(
                f"{self.jogador.nome}, você foi eliminado! Sua pontuação final foi {self.jogador.pontuacao}."
            )
            recordes.atualizar_recorde(self.jogador.nome, self.jogador.pontuacao)
        recordes.exibir_recordes()
        recordes.guardar_recordes()
