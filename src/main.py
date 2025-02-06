import subprocess
import sys
import os


def main():
    print("=========================================")
    print("     Bem-vindo ao Desafio das Mentes     ")
    print("=========================================")
    print("A abrir a interface gráfica...")
    try:
        caminho_interface = os.path.join(os.path.dirname(__file__), "interface.py")
        subprocess.run([sys.executable, caminho_interface])
    except Exception as e:
        print("Erro ao abrir a interface gráfica:", e)


if __name__ == "__main__":
    main()
