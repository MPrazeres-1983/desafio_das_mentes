import random
from jogador import Jogador


class JogadorBot(Jogador):
    def __init__(self, nome):
        """
        Inicializa o BOT com o nome.
        """
        super().__init__(nome)

    def responder(self, pergunta, rodada):
        """
        Responde à pergunta utilizando uma chance de acerto baseada na rodada.

        Probabilidades:
          - Rodadas 1-5 (Dificuldade 1): 80% de chance de acertar
          - Rodadas 6-10 (Dificuldade 2): 65% de chance de acertar
          - Rodadas 11+ (Dificuldade 3): 50% de chance de acertar

        :param pergunta: Instância da pergunta atual.
        :param rodada: Número da rodada atual.
        :return: Índice da resposta escolhida (de acordo com a ordem embaralhada).
        """
        if rodada <= 5:
            chance = 0.8
        elif rodada <= 10:
            chance = 0.65
        else:
            chance = 0.5

        if random.random() < chance:
            # BOT responde corretamente
            return pergunta.indice_resposta_embaralhada
        else:
            # BOT responde incorretamente: escolhe uma alternativa diferente da correta
            opcoes = list(range(len(pergunta.alternativas)))
            opcoes.remove(pergunta.indice_resposta_embaralhada)
            return random.choice(opcoes)

    def __str__(self):
        estado = "Ativo" if self.esta_ativo() else "Eliminado"
        return (
            f"[BOT] Jogador: {self.nome}, Pontuação: {self.pontuacao}, Estado: {estado}"
        )
