import random


class Pergunta:
    def __init__(self, id, texto, alternativas, resposta_correta, dificuldade):
        """
        Inicializa uma pergunta com os dados fornecidos e embaralha as alternativas,
        ajustando o índice da resposta correta.
        """
        self.id = id
        self.texto = texto
        self.alternativas = alternativas
        self.resposta_correta_original = resposta_correta
        self.dificuldade = dificuldade

        # Embaralha as alternativas ao iniciar a instância
        self.alternativas_embaralhadas, self.indice_resposta_embaralhada = (
            self._embaralhar_alternativas()
        )

    def _embaralhar_alternativas(self):
        """
        Embaralha as alternativas e retorna a nova lista junto com o índice atualizado
        da resposta correta.
        """
        indices = list(range(len(self.alternativas)))
        random.shuffle(indices)
        alternativas_embaralhadas = [self.alternativas[i] for i in indices]
        indice_resposta_embaralhada = indices.index(self.resposta_correta_original)
        return alternativas_embaralhadas, indice_resposta_embaralhada

    def verificar_resposta(self, indice):
        """
        Verifica se o índice fornecido corresponde à resposta correta.
        """
        return indice == self.indice_resposta_embaralhada

    def __str__(self):
        """
        Retorna uma representação formatada da pergunta e das alternativas.
        """
        alternativas_formatadas = "\n".join(
            [f"{i + 1}. {alt}" for i, alt in enumerate(self.alternativas_embaralhadas)]
        )
        return f"{self.texto}\n{alternativas_formatadas}"
