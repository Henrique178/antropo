class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.pontuacao = 0
        self.historico = []
    
    def adicionar_pontuacao(self, pontos):
        """Adiciona pontos ao jogador"""
        self.pontuacao += pontos
        self.historico.append(pontos)
        print(f"✨ +{pontos} pontos!")
    
    def salvar_pontuacao(self):
        """Salva pontuação no arquivo"""
        try:
            with open('pontuacao.txt', 'a') as arquivo:
                arquivo.write(f"{self.nome}:{self.pontuacao}\n")
            print("✅ Pontuação salva com sucesso!")
        except:
            print("⚠️ Erro ao salvar pontuação")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do jogador"""
        if self.historico:
            media = sum(self.historico) / len(self.historico)
            print(f"\n📈 Estatísticas de {self.nome}:")
            print(f"Total de pontos: {self.pontuacao}")
            print(f"Média por jogo: {media:.1f}")
            print(f"Melhor pontuação: {max(self.historico)}")