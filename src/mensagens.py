class MensagemJogo:
    """Classe base para mensagens do jogo."""

    def exibir(self, jogador):
        raise NotImplementedError("Este método deve ser implementado nas subclasses")


class MensagemAcerto(MensagemJogo):
    """Mensagem exibida quando um jogador acerta uma pergunta."""

    def exibir(self, jogador):
        return f"🎉 Parabéns, {jogador.nome}! Acertaste a pergunta! 🎯"


class MensagemErro(MensagemJogo):
    """Mensagem exibida quando um jogador erra uma pergunta."""

    def exibir(self, jogador):
        return f"❌ Oh não, {jogador.nome}! Erraste a pergunta! 😞"
