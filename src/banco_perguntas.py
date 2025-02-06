import os
import json
import random
from pergunta import Pergunta


class BancoDePerguntas:
    def __init__(self, diretorio="perguntas"):
        """
        Inicializa o banco de perguntas, carregando todas as perguntas
        dos ficheiros JSON do diretório informado.
        """
        self.perguntas = []
        self.categorias = []
        self.diretorio = diretorio
        self.carregar_todas_perguntas()

    def carregar_todas_perguntas(self):
        """
        Percorre o diretório de perguntas e carrega cada ficheiro JSON.
        """
        if not os.path.exists(self.diretorio):
            raise FileNotFoundError(f"Diretório não encontrado: {self.diretorio}")
        for ficheiro in os.listdir(self.diretorio):
            if ficheiro.endswith(".json"):
                caminho = os.path.join(self.diretorio, ficheiro)
                self.carregar_perguntas(caminho)

    def carregar_perguntas(self, caminho):
        """
        Carrega as perguntas de um ficheiro JSON, associando a categoria.
        """
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            categoria = dados["categoria"]
            self.categorias.append(categoria)
            for p in dados["perguntas"]:
                pergunta = Pergunta(
                    id=p["id"],
                    texto=p["texto"],
                    alternativas=p["alternativas"],
                    resposta_correta=p["resposta_correta"],
                    dificuldade=p["dificuldade"],
                )
                pergunta.categoria = categoria
                self.perguntas.append(pergunta)

    def obter_pergunta_aleatoria(self, categoria, dificuldade):
        """
        Retorna uma pergunta aleatória da categoria e dificuldade informadas,
        removendo-a do banco para evitar repetições.
        """
        perguntas_filtradas = [
            p
            for p in self.perguntas
            if p.categoria == categoria and p.dificuldade == dificuldade
        ]
        if perguntas_filtradas:
            pergunta_selecionada = random.choice(perguntas_filtradas)
            # Remove a pergunta utilizada para não repetir no mesmo jogo
            self.perguntas.remove(pergunta_selecionada)
            return pergunta_selecionada
        return None
