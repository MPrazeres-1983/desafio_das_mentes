class Jogador:
    def __init__(self, nome):
        """
        Inicializa um jogador com o nome, pontuação zero e estado ativo.
        """
        self.nome = nome
        self.pontuacao = 0
        self.ativo = True

    def adicionar_pontuacao(self, pontos=1):
        """Adiciona pontos à pontuação do jogador."""
        self.pontuacao += pontos

    def eliminar(self):
        """Elimina o jogador (define o estado como inativo)."""
        self.ativo = False

    def esta_ativo(self):
        """Retorna True se o jogador estiver ativo."""
        return self.ativo

    def __str__(self):
        estado = "Ativo" if self.ativo else "Eliminado"
        return f"Jogador: {self.nome}, Pontuação: {self.pontuacao}, Estado: {estado}"
