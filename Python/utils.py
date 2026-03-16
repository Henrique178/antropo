def dar_dica(palpite, numero_secreto):
    """Gera uma dica baseada no palpite"""
    diferenca = palpite - numero_secreto
    
    if diferenca > 0:
        if diferenca > 20:
            return "📈 Muito alto! Tente um número BEM menor"
        elif diferenca > 10:
            return "📈 Está alto! Diminua um pouco"
        else:
            return "📈 Um pouco alto, tente diminuir"
    else:
        if diferenca < -20:
            return "📉 Muito baixo! Tente um número BEM maior"
        elif diferenca < -10:
            return "📉 Está baixo! Aumente um pouco"
        else:
            return "📉 Um pouco baixo, tente aumentar"

def mostrar_ranking():
    """Mostra o ranking dos jogadores"""
    try:
        with open('pontuacao.txt', 'r') as arquivo:
            pontuacoes = arquivo.readlines()
        
        if pontuacoes:
            print("\n🏆 RANKING DOS JOGADORES:")
            # Ordena por pontuação
            ranking = []
            for linha in pontuacoes:
                nome, pontos = linha.strip().split(':')
                ranking.append((nome, int(pontos)))
            
            ranking.sort(key=lambda x: x[1], reverse=True)
            
            for i, (nome, pontos) in enumerate(ranking, 1):
                print(f"{i}º - {nome}: {pontos} pontos")
        else:
            print("📭 Nenhuma pontuação registrada ainda")
            
    except FileNotFoundError:
        print("📭 Nenhuma pontuação registrada ainda")

def limpar_tela():
    """Limpa a tela do terminal (opcional)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')