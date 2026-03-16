import random
from jogador import Jogador
from utils import dar_dica, mostrar_ranking

def jogar():
    print("\n" + "="*100)
    print("Jogo de advinhação")
    print("="*100)

    nome = input("\nQual o nome do jogador? ")
    jogador = Jogador(nome)

    while True:
        print(f"\nOlá, {jogador.nome}! Vamos começar?")
        nivel = input("Escolha o nível (1-Fácil, 2-Médio, 3-Difícil): ")

        if nivel == "1":
            max_num = 30
            tentativas_max = 10
        elif nivel == "2":
            max_num = 50
            tentativas_max = 7
        else:
            max_num = 100
            tentativas_max = 5

        numero_secreto = random.randint(1, max_num)
        tentativas = 0

        print(f"\n🎲 Pensei em um número entre 1 e {max_num}")
        print(f"💪 Você tem {tentativas_max} tentativas")
        
        # Loop principal do jogo
        while tentativas < tentativas_max:
            try:
                palpite = int(input(f"\nTentativa {tentativas + 1}: "))
                tentativas += 1
                
                if palpite == numero_secreto:
                    print(f"\n🎉 PARABÉNS! Você acertou em {tentativas} tentativas!")
                    pontos = calcular_pontos(tentativas, tentativas_max)
                    jogador.adicionar_pontuacao(pontos)
                    break
                else:
                    dica = dar_dica(palpite, numero_secreto)
                    print(f"❌ Errou! {dica}")
                    
                    # Dica extra se estiver perto do fim
                    if tentativas >= tentativas_max - 2:
                        if abs(palpite - numero_secreto) <= 5:
                            print("💡 Dica extra: Você está SUPER perto!")
                            
            except ValueError:
                print("⚠️ Digite apenas números!")
        
        # Se acabaram as tentativas
        if tentativas == tentativas_max and palpite != numero_secreto:
            print(f"\n😢 Fim de jogo! O número era {numero_secreto}")
        
        # Pergunta se quer jogar novamente
        print(f"\nSua pontuação total: {jogador.pontuacao}")
        jogar_novamente = input("\nJogar novamente? (s/n): ")
        if jogar_novamente.lower() != 's':
            break
    
    # Mostra ranking ao final
    print("\n📊 RANKING FINAL:")
    jogador.salvar_pontuacao()
    mostrar_ranking()

def calcular_pontos(tentativas_usadas, tentativas_max):
    """Calcula pontos baseado nas tentativas usadas"""
    return (tentativas_max - tentativas_usadas + 1) * 10

# Inicia o jogo
if __name__ == "__main__":
    jogar()