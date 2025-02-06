import json
import os


class Recordes:
    def __init__(self, caminho="data/recordes.json"):
        """
        Inicializa a classe Recordes, carregando os recordes do arquivo JSON.
        """
        self.caminho = caminho
        self.recordes = self.carregar_recordes()

    def carregar_recordes(self):
        """
        Carrega os recordes do arquivo JSON. Se o arquivo não existir ou estiver corrompido,
        cria um novo.
        """
        if not os.path.exists(self.caminho):
            print(
                f"⚠️ Ficheiro {self.caminho} não encontrado. Criando um novo ficheiro de recordes..."
            )
            os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return {}
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print(
                f"⚠️ Ficheiro {self.caminho} inválido ou corrompido. Criando um novo..."
            )
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump({}, f)
            return {}

    def guardar_recordes(self):
        """
        Salva os recordes no arquivo JSON.
        """
        try:
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump(self.recordes, f, indent=4, ensure_ascii=False)
            print(f"✅ Recordes guardados com sucesso em {self.caminho}")
        except Exception as e:
            print(f"❌ Erro ao guardar os recordes: {e}")

    def atualizar_recorde(self, nome, pontuacao):
        """
        Atualiza o recorde do jogador se a nova pontuação for maior que a registrada.
        """
        if nome not in self.recordes or pontuacao > self.recordes[nome]:
            print(f"🎉 Novo recorde para {nome}: {pontuacao} pontos!")
            self.recordes[nome] = pontuacao
            self.guardar_recordes()

    def exibir_recordes(self):
        """
        Exibe os recordes ordenados por pontuação.
        """
        if not self.recordes:
            print("\nAinda não há recordes registrados.")
        else:
            print("\n=== Quadro de Recordes ===")
            recordes_ordenados = sorted(
                self.recordes.items(), key=lambda x: x[1], reverse=True
            )
            for i, (nome, pontuacao) in enumerate(recordes_ordenados, start=1):
                print(f"{i}. {nome} - {pontuacao} pontos")
