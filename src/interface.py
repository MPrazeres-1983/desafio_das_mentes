import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from banco_perguntas import BancoDePerguntas
from jogador import Jogador
from jogador_bot import JogadorBot
from recordes import Recordes
import os
import pygame
from mensagens import (
    MensagemAcerto,
    MensagemErro,
)  # Importa as novas classes


# Inicializar o mixer de som do pygame
pygame.mixer.init()


def tocar_som(nome_arquivo):
    """Executa o som imediatamente sem bloquear o jogo."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sons"))
    caminho_som = os.path.join(base_path, nome_arquivo)

    if os.path.exists(caminho_som):
        pygame.mixer.Sound(caminho_som).play()
    else:
        print(f"❌ ERRO: O ficheiro de som não foi encontrado -> {caminho_som}")


class JogoInterface(tk.Tk):
    def __init__(self):
        """
        Inicializa a interface do jogo, configura estilos e mostra o menu principal.
        """
        super().__init__()
        self.title("Desafio das Mentes")
        self.geometry("800x600")

        # Variáveis do jogo
        self.jogadores = []  # Lista geral de jogadores
        self.jogadores_ativos = []  # Usada no modo Normal
        self.banco_perguntas = BancoDePerguntas()
        self.recordes = Recordes()
        self.rodada = 1
        self.modo_jogo = tk.StringVar(value="solo")  # "solo" ou "normal"
        self.categoria_rodada = None  # Categoria escolhida para a rodada (modo Normal)
        self.indice_jogador_atual = 0  # Controle do turno no modo Normal
        self.respostas_rodada = {}  # Armazena as respostas de cada jogador na rodada

        # Configuração visual
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=("Helvetica", 10))
        self.style.configure("TLabel", font=("Helvetica", 12))

        self.mostrar_menu_principal()

    def limpar_tela(self):
        """
        Remove todos os widgets da janela.
        """
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        """
        Exibe o menu principal com opções de modo de jogo, regras, recordes e sair.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        titulo = ttk.Label(
            frame, text="Desafio das Mentes", font=("Helvetica", 24, "bold")
        )
        titulo.pack(pady=20)

        frame_modos = ttk.LabelFrame(frame, text="Modo de Jogo", padding=10)
        frame_modos.pack(fill="x", pady=10)
        ttk.Radiobutton(
            frame_modos, text="Solo", variable=self.modo_jogo, value="solo"
        ).pack(side="left", padx=10)
        ttk.Radiobutton(
            frame_modos, text="Normal", variable=self.modo_jogo, value="normal"
        ).pack(side="left", padx=10)

        ttk.Button(
            frame, text="Novo Jogo", command=self.iniciar_configuracao_jogo
        ).pack(pady=10)
        ttk.Button(frame, text="Ver Recordes", command=self.mostrar_recordes).pack(
            pady=10
        )
        ttk.Button(frame, text="Regras", command=self.mostrar_regras).pack(pady=10)
        ttk.Button(frame, text="Sair", command=self.quit).pack(pady=10)

    def iniciar_configuracao_jogo(self):
        """
        Tela de configuração para adicionar jogadores.
        Reinicia as variáveis dos jogos anteriores e permite adicionar, remover ou editar jogadores.
        """
        # Reinicia os dados dos jogos anteriores
        self.jogadores = []
        self.jogadores_ativos = []
        self.rodada = 1
        self.respostas_rodada = {}

        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        ttk.Label(
            frame, text="Configuração do Jogo", font=("Helvetica", 18, "bold")
        ).pack(pady=10)

        # Frame para adicionar jogadores
        frame_jogadores = ttk.LabelFrame(frame, text="Jogadores", padding=10)
        frame_jogadores.pack(fill="x", pady=10)

        # Entry para nome do jogador
        self.entry_nome = ttk.Entry(frame_jogadores)
        self.entry_nome.pack(side="left", padx=5)

        # Checkbox para BOT
        self.is_bot = tk.BooleanVar()
        ttk.Checkbutton(frame_jogadores, text="BOT", variable=self.is_bot).pack(
            side="left"
        )

        # Botão adicionar
        ttk.Button(
            frame_jogadores, text="Adicionar Jogador", command=self.adicionar_jogador
        ).pack(side="left", padx=5)

        # Lista de jogadores
        self.lista_jogadores = tk.Listbox(frame, height=5)
        self.lista_jogadores.pack(fill="x", pady=10)

        # Botões para remover e editar jogadores
        frame_botoes_config = ttk.Frame(frame)
        frame_botoes_config.pack(pady=10)
        ttk.Button(
            frame_botoes_config, text="Remover Jogador", command=self.remover_jogador
        ).pack(side="left", padx=5)
        ttk.Button(
            frame_botoes_config, text="Editar Jogador", command=self.editar_jogador
        ).pack(side="left", padx=5)

        # Botões de controle
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=20)
        ttk.Button(frame_botoes, text="Iniciar Jogo", command=self.iniciar_jogo).pack(
            side="left", padx=5
        )
        ttk.Button(
            frame_botoes, text="Voltar", command=self.mostrar_menu_principal
        ).pack(side="left", padx=5)

    def adicionar_jogador(self):
        """
        Adiciona um novo jogador à lista, considerando se é BOT ou humano.
        """
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Insira um nome para o jogador!")
            return
        if self.is_bot.get():
            jogador = JogadorBot(nome)
        else:
            jogador = Jogador(nome)
        self.jogadores.append(jogador)
        self.lista_jogadores.insert(
            tk.END, f"{'[BOT] ' if self.is_bot.get() else ''}{nome}"
        )
        self.entry_nome.delete(0, tk.END)
        self.is_bot.set(False)

    def remover_jogador(self):
        """
        Remove o jogador selecionado da lista.
        """
        idx = self.lista_jogadores.curselection()
        if idx:
            index = idx[0]
            self.lista_jogadores.delete(index)
            del self.jogadores[index]
        else:
            messagebox.showwarning("Aviso", "Selecione um jogador para remover!")

    def editar_jogador(self):
        """
        Permite editar o nome do jogador selecionado.
        """
        idx = self.lista_jogadores.curselection()
        if idx:
            index = idx[0]
            novo_nome = simpledialog.askstring("Editar Jogador", "Digite o novo nome:")
            if novo_nome:
                self.jogadores[index].nome = novo_nome
                self.lista_jogadores.delete(index)
                bot_flag = (
                    "[BOT] " if hasattr(self.jogadores[index], "responder") else ""
                )
                self.lista_jogadores.insert(index, f"{bot_flag}{novo_nome}")
        else:
            messagebox.showwarning("Aviso", "Selecione um jogador para editar!")

    def iniciar_jogo(self):
        """
        Inicia o jogo conforme o modo selecionado:
          - Modo Solo: verifica se há exatamente 1 jogador.
          - Modo Normal: verifica se há pelo menos 2 jogadores.
        """
        if self.modo_jogo.get() == "solo":
            if len(self.jogadores) != 1:
                messagebox.showwarning(
                    "Aviso", "O modo solo requer exatamente 1 jogador!"
                )
                return
            self.mostrar_tela_jogo_solo()
        elif self.modo_jogo.get() == "normal":
            if len(self.jogadores) < 2:
                messagebox.showwarning(
                    "Aviso", "O modo normal requer pelo menos 2 jogadores!"
                )
                return
            self.jogadores_ativos = self.jogadores.copy()
            self.rodada = 1
            self.mostrar_selecao_categoria_normal()
        else:
            messagebox.showerror("Erro", "Modo de jogo inválido!")

    # ------------- Modo Solo (GUI) -------------
    def mostrar_tela_jogo_solo(self):
        """
        Configura a tela de jogo para o modo Solo.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        info = ttk.Label(frame, text=f"Rodada: {self.rodada}", font=("Helvetica", 14))
        info.pack(side="left", padx=10)
        self.frame_pergunta = ttk.LabelFrame(frame, text="Pergunta", padding=10)
        self.frame_pergunta.pack(fill="both", expand=True, pady=10)
        self.mostrar_selecao_categoria_solo()

    def mostrar_selecao_categoria_solo(self):
        """
        Permite ao jogador solo escolher uma categoria para a rodada.
        """
        for widget in self.frame_pergunta.winfo_children():
            widget.destroy()
        ttk.Label(
            self.frame_pergunta, text="Escolha uma categoria:", font=("Helvetica", 12)
        ).pack(pady=10)
        for categoria in self.banco_perguntas.categorias:
            ttk.Button(
                self.frame_pergunta,
                text=categoria.capitalize(),
                command=lambda cat=categoria: self.selecionar_categoria_solo(cat),
            ).pack(pady=5)

    def selecionar_categoria_solo(self, categoria):
        """
        Define a categoria escolhida para o modo Solo e exibe a pergunta.
        """
        self.categoria_atual = categoria
        self.mostrar_pergunta_solo()

    def mostrar_pergunta_solo(self):
        """
        Exibe uma pergunta do banco (da categoria e dificuldade atuais) para o modo Solo.
        """
        for widget in self.frame_pergunta.winfo_children():
            widget.destroy()
        dificuldade = self.definir_dificuldade()
        pergunta = self.banco_perguntas.obter_pergunta_aleatoria(
            self.categoria_atual, dificuldade
        )
        if not pergunta:
            messagebox.showinfo("Aviso", "Sem mais perguntas nesta categoria!")
            self.mostrar_selecao_categoria_solo()
            return
        ttk.Label(
            self.frame_pergunta,
            text=pergunta.texto,
            wraplength=600,
            font=("Helvetica", 12),
        ).pack(pady=10)
        for i, alternativa in enumerate(pergunta.alternativas_embaralhadas):
            ttk.Button(
                self.frame_pergunta,
                text=f"{i+1}. {alternativa}",
                command=lambda idx=i: self.processar_resposta_solo(pergunta, idx),
            ).pack(pady=5)

    def processar_resposta_solo(self, pergunta, resposta):
        """
        Processa a resposta do jogador solo. Se errar, encerra o jogo.
        """
        jogador = self.jogadores[0]  # Apenas o primeiro jogador é usado no modo Solo

        if pergunta.verificar_resposta(resposta):
            tocar_som("correto.wav")  # 🔊 Som ao acertar
            mensagem = (
                MensagemAcerto()
            )  # Usa polimorfismo para gerar a mensagem correta
            messagebox.showinfo("Resultado", mensagem.exibir(jogador))
            jogador.adicionar_pontuacao(1)
        else:
            tocar_som("errado.wav")  # 🔊 Som ao errar
            mensagem = MensagemErro()  # Usa polimorfismo para gerar a mensagem de erro
            messagebox.showinfo("Resultado", mensagem.exibir(jogador))
            jogador.eliminar()
            self.finalizar_jogo_solo()
            return

        self.rodada += 1
        self.mostrar_selecao_categoria_solo()

    def finalizar_jogo_solo(self):
        """
        Exibe a tela final para o modo Solo, mostrando as pontuações e atualizando os recordes.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        ttk.Label(frame, text="Fim de Jogo!", font=("Helvetica", 24, "bold")).pack(
            pady=20
        )
        for jogador in self.jogadores:
            ttk.Label(
                frame,
                text=f"{jogador.nome}: {jogador.pontuacao} pontos",
                font=("Helvetica", 12),
            ).pack(pady=5)
            self.recordes.atualizar_recorde(jogador.nome, jogador.pontuacao)
        ttk.Button(frame, text="Novo Jogo", command=self.mostrar_menu_principal).pack(
            pady=10
        )
        ttk.Button(frame, text="Ver Recordes", command=self.mostrar_recordes).pack(
            pady=10
        )
        ttk.Button(frame, text="Sair", command=self.quit).pack(pady=10)

    # ------------- Modo Normal (GUI) -------------
    def mostrar_selecao_categoria_normal(self):
        """
        Exibe a tela de seleção de categoria para a rodada no modo Normal.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        ttk.Label(
            frame,
            text=f"Rodada {self.rodada} - Selecione a Categoria",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)
        for categoria in self.banco_perguntas.categorias:
            ttk.Button(
                frame,
                text=categoria.capitalize(),
                command=lambda cat=categoria: self.iniciar_rodada_normal(cat),
            ).pack(pady=5)
        ttk.Button(
            frame, text="Voltar ao Menu", command=self.mostrar_menu_principal
        ).pack(pady=10)

    def iniciar_rodada_normal(self, categoria):
        """
        Inicia a rodada no modo Normal definindo a categoria e reiniciando as variáveis de turno.
        """
        self.categoria_rodada = categoria
        self.respostas_rodada = {}  # Reinicia as respostas da rodada
        self.indice_jogador_atual = 0
        self.mostrar_pergunta_normal()

    def mostrar_pergunta_normal(self):
        """
        Exibe a pergunta para o jogador ativo na rodada do modo Normal.
        Se todos os jogadores já responderam, chama o processamento dos resultados.
        """
        self.limpar_tela()
        if self.indice_jogador_atual < len(self.jogadores_ativos):
            jogador = self.jogadores_ativos[self.indice_jogador_atual]
            frame = ttk.Frame(self)
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            ttk.Label(
                frame,
                text=f"Rodada {self.rodada} - Vez de {jogador.nome}",
                font=("Helvetica", 16, "bold"),
            ).pack(pady=10)
            dificuldade = self.definir_dificuldade()
            pergunta = self.banco_perguntas.obter_pergunta_aleatoria(
                self.categoria_rodada, dificuldade
            )
            if not pergunta:
                messagebox.showinfo("Aviso", "Sem mais perguntas nesta categoria!")
                self.mostrar_selecao_categoria_normal()
                return
            ttk.Label(
                frame, text=pergunta.texto, wraplength=600, font=("Helvetica", 12)
            ).pack(pady=10)
            # Se o jogador for BOT, responde automaticamente após um pequeno atraso
            if hasattr(jogador, "responder"):
                self.after(
                    2000,
                    lambda: self.processar_resposta_normal(
                        pergunta, jogador, jogador.responder(pergunta, self.rodada)
                    ),
                )
            else:
                for i, alternativa in enumerate(pergunta.alternativas_embaralhadas):
                    ttk.Button(
                        frame,
                        text=f"{i+1}. {alternativa}",
                        command=lambda idx=i, p=pergunta: self.processar_resposta_normal(
                            p, jogador, idx
                        ),
                    ).pack(pady=5)
        else:
            # Se todos os jogadores já responderam, processa os resultados da rodada
            self.processar_resultados_rodada_normal()

    def processar_resposta_normal(self, pergunta, jogador, resposta):
        """
        Armazena a resposta do jogador, toca o som e passa para o próximo jogador da rodada.
        """
        self.respostas_rodada[jogador.nome] = (pergunta, resposta)

        # 🔊 TOCAR SOM IMEDIATAMENTE APÓS A RESPOSTA
        if pergunta.verificar_resposta(resposta):
            tocar_som("correto.wav")
        else:
            tocar_som("errado.wav")

        # Passa para o próximo jogador
        self.indice_jogador_atual += 1
        self.mostrar_pergunta_normal()

    def processar_resultados_rodada_normal(self):
        """
        Processa as respostas de todos os jogadores na rodada do modo Normal,
        elimina os que erraram e atualiza os pontos.
        Se apenas um jogador acertar, ele é declarado vencedor.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        acertos = []
        eliminados = []

        for jogador in self.jogadores_ativos.copy():
            if jogador.nome in self.respostas_rodada:
                pergunta, resposta = self.respostas_rodada[jogador.nome]
                if pergunta.verificar_resposta(resposta):
                    jogador.adicionar_pontuacao(1)
                    acertos.append(jogador)
                else:
                    jogador.eliminar()
                    eliminados.append(jogador)
                    self.jogadores_ativos.remove(jogador)

        resultado_texto = ""
        if eliminados:
            resultado_texto += (
                "Jogadores eliminados nesta rodada:\n"
                + "\n".join([j.nome for j in eliminados])
                + "\n\n"
            )
        if acertos:
            resultado_texto += "Jogadores que acertaram:\n" + "\n".join(
                [j.nome for j in acertos]
            )
        else:
            resultado_texto += "Nenhum jogador acertou nesta rodada."

        ttk.Label(frame, text=resultado_texto, font=("Helvetica", 12)).pack(pady=10)

        # Critério de término: se apenas um jogador acertou, ele vence.
        if len(acertos) == 1:
            ttk.Label(
                frame,
                text=f"\nVencedor: {acertos[0].nome} com {acertos[0].pontuacao} pontos! 🏆",
                font=("Helvetica", 16, "bold"),
            ).pack(pady=10)
            self.recordes.atualizar_recorde(acertos[0].nome, acertos[0].pontuacao)
            ttk.Button(
                frame, text="Menu Principal", command=self.mostrar_menu_principal
            ).pack(pady=10)
        elif len(acertos) >= 2:
            ttk.Label(
                frame,
                text="\nTodos os jogadores que acertaram continuam para a próxima rodada.",
                font=("Helvetica", 12),
            ).pack(pady=10)
            self.rodada += 1
            ttk.Button(
                frame,
                text="Próxima Rodada",
                command=self.mostrar_selecao_categoria_normal,
            ).pack(pady=10)
        else:
            ttk.Label(
                frame,
                text="\nTodos os jogadores foram eliminados. Fim de jogo! ❌",
                font=("Helvetica", 16, "bold"),
            ).pack(pady=10)
            ttk.Button(
                frame, text="Menu Principal", command=self.mostrar_menu_principal
            ).pack(pady=10)

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

    def mostrar_recordes(self):
        """
        Exibe a tela com os recordes.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        ttk.Label(frame, text="Recordes", font=("Helvetica", 24, "bold")).pack(pady=20)
        recordes_ordenados = sorted(
            self.recordes.recordes.items(), key=lambda x: x[1], reverse=True
        )
        for i, (nome, pontos) in enumerate(recordes_ordenados, 1):
            ttk.Label(
                frame, text=f"{i}. {nome}: {pontos} pontos", font=("Helvetica", 12)
            ).pack(pady=5)
        ttk.Button(frame, text="Voltar", command=self.mostrar_menu_principal).pack(
            pady=20
        )

    def mostrar_regras(self):
        """
        Exibe as regras do jogo lidas do arquivo 'data/regras.txt'.
        """
        self.limpar_tela()
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        ttk.Label(frame, text="Regras do Jogo", font=("Helvetica", 24, "bold")).pack(
            pady=20
        )
        try:
            with open("data/regras.txt", "r", encoding="utf-8") as f:
                regras = f.read()
            text_widget = tk.Text(frame, wrap=tk.WORD, height=20, width=60)
            text_widget.insert(tk.END, regras)
            text_widget.configure(state="disabled")
            text_widget.pack(pady=10)
            scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.config(yscrollcommand=scrollbar.set)
        except FileNotFoundError:
            ttk.Label(
                frame, text="Arquivo de regras não encontrado.", font=("Helvetica", 12)
            ).pack(pady=10)
        ttk.Button(frame, text="Voltar", command=self.mostrar_menu_principal).pack(
            pady=20
        )


if __name__ == "__main__":
    app = JogoInterface()
    app.mainloop()
