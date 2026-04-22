programa
{

	cadeia nome, resposta
	inteiro opcao, xp = 0, acertos = 0, categoria
	logico continuar = verdadeiro
	logico estudando = verdadeiro
	
	funcao inicio()
	{
		escreva("=== Bem vindo ao AprovaGame ===\n")
		escreva("=== Escreva o seu nome: ")
		leia(nome)

		enquanto(continuar) {
			escreva("\n=== MENU PRINCIPAL ===")
			escreva("\n1) Iniciar Estudo")
			escreva("\n2) Ver desempenho")
			escreva("\n3) Sair")
			escreva("\nEscolha uma opção: ")
			leia(opcao)

			escolha(opcao) {
				caso 1:
					estudando = verdadeiro
					enquanto(estudando) {
						escreva("\n=== CATEGORIAS DE ESTUDO ===")
						escreva("\n1) Legislação para Concurso")
						escreva("\n2) Língua Portuguesa para Concurso")
						escreva("\n3) Moções de Administração")
						escreva("\n4) Raciocínio Lógico")
						escreva("\n5) Voltar ao menu principal")
						escreva("\nEscolha uma categoria: ")
						leia(categoria)

						escolha(categoria) {
							caso 1:
								perguntasLegislacao()
								pare
							caso 2:
								perguntasPortugues()
								pare
							caso 3:
								perguntasAdministracao()
								pare
							caso 4:
								perguntasRaciocinio()
								pare
							caso 5:
								estudando = falso
								escreva("\nVoltando ao menu principal")
								pare
							caso contrario:
								escreva("\nOpção Inválida! Tente novamente!")
						}
					}
					pare

				caso 2:
					escreva("\n=== DESEMPENHO DO USUÁRIO ===")
					escreva("\nUsuário: ", nome)
					escreva("\nPontuação total: ", xp, " XP")
					escreva("\nTotal de acertos: ", acertos, " questões\n")
					pare

				caso 3:
					escreva("\nEncerrando o AprovaGame. Bons Estudos, ", nome, "!")
					continuar = falso
					pare

				caso contrario:
					escreva("\nOpção Inválida! Tente novamente")
			}
		}
	}

	funcao perguntasLegislacao()
	{
		escreva("\n=== LEGISLAÇÃO PARA CONCURSO ===\n")

		// Questão 1

		escreva("\n1) De acordo com a Lei 8.112/90, são requisitos básicos para investidura em cargo público, EXCETO:")
		escreva("\na) Nacionalidade brasileira")
		escreva("\nb) Idade mínima de 21 anos")
		escreva("\nc) Quitação com as obrigações eleitorais")
		escreva("\nd) Aptidão física e mental")
		escreva("\ne) Nível de escolaridade exigido para o cargo")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)

		se (resposta == "b") {
			escreva("Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("Incorreto! A idade mínima é 18 anos.\n")
		}

		// Questão 2

		escreva("\n2) O princípio da administração pública que exige transparência e publicidade dos atos é chamado de:")
		escreva("\na) Impessoalidade")
		escreva("\nb) Moralidade")
		escreva("\nc) Publicidade")
		escreva("\nd) Eficiência")
		escreva("\ne) Legalidade")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "c") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! Publicidade é o princípio da transparência.\n")
		}

		// Questão 3
		escreva("\n3) A Lei de Improbidade Administrativa (Lei 8.429/92) NÃO se aplica a:")
		escreva("\na) Agentes políticos")
		escreva("\nb) Servidores públicos estatutários")
		escreva("\nc) Empregados de empresas privadas")
		escreva("\nd) Empregados de empresas públicas")
		escreva("\ne) Particulares que recebem recursos públicos")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "c") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! A lei não se aplica a empregados de empresas privadas sem vínculo com o poder público.\n")
		}
		
		escreva("\n=== Fim das questões de Legislação ===\n")
	}
	
	funcao perguntasPortugues()
	{
		escreva("\n=== LÍNGUA PORTUGUESA PARA CONCURSO ===\n")
		
		// Questão 1
		escreva("\n1) Assinale a alternativa em que a palavra está corretamente acentuada:")
		escreva("\na) Heroíco")
		escreva("\nb) Jibóia")
		escreva("\nc) Assembléia")
		escreva("\nd) Pólen")
		escreva("\ne) Idoône")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "d") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! 'Pólen' é acentuado (paroxítona terminada em 'n').\n")
		}
		
		// Questão 2
		escreva("\n2) Qual das frases abaixo apresenta ERRO de regência verbal?")
		escreva("\na) Assistimos ao filme ontem.")
		escreva("\nb) Prefiro estudar a trabalhar.")
		escreva("\nc) Obedeço ao regulamento.")
		escreva("\nd) Lembrei do seu aniversário.")
		escreva("\ne) Paguei o boleto hoje.")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "b") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! O correto é 'Prefiro estudar a trabalhar' (sem o 'a' antes do segundo verbo).\n")
		}
		
		// Questão 3
		escreva("\n3) Em 'O povo elegeu seus representantes', o sujeito é:")
		escreva("\na) Simples")
		escreva("\nb) Composto")
		escreva("\nc) Oculto")
		escreva("\nd) Indeterminado")
		escreva("\ne) Inexistente")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "a") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! O sujeito é simples: 'O povo'.\n")
		}
		
		escreva("\n=== Fim das questões de Língua Portuguesa ===\n")
	}
	
	funcao perguntasAdministracao()
	{
		escreva("\n=== NOÇÕES DE ADMINISTRAÇÃO ===\n")
		
		// Questão 1
		escreva("\n1) Quem é considerado o 'pai da administração científica'?")
		escreva("\na) Henri Fayol")
		escreva("\nb) Elton Mayo")
		escreva("\nc) Frederick Taylor")
		escreva("\nd) Peter Drucker")
		escreva("\ne) Max Weber")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "c") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! Frederick Taylor é o pai da administração científica.\n")
		}
		
		// Questão 2
		escreva("\n2) Na função administrativa, o ato de 'comparar resultados com objetivos planejados' corresponde a:")
		escreva("\na) Planejamento")
		escreva("\nb) Organização")
		escreva("\nc) Direção")
		escreva("\nd) Controle")
		escreva("\ne) Coordenação")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "d") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! Controle é a função que compara resultados com o planejado.\n")
		}
		
		// Questão 3
		escreva("\n3) A estrutura organizacional em forma de pirâmide, com hierarquia bem definida, é chamada de:")
		escreva("\na) Estrutura matricial")
		escreva("\nb) Estrutura linear")
		escreva("\nc) Estrutura horizontal")
		escreva("\nd) Estrutura em rede")
		escreva("\ne) Estrutura circular")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "b") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! Estrutura linear é a hierárquica em pirâmide.\n")
		}
		
		escreva("\n=== Fim das questões de Administração ===\n")
	}
	
	funcao perguntasRaciocinio()
	{
		escreva("\n=== RACIOCÍNIO LÓGICO ===\n")
		
		// Questão 1
		escreva("\n1) Se João é mais alto que Pedro, e Pedro é mais alto que Marcos, então:")
		escreva("\na) Marcos é mais alto que João")
		escreva("\nb) João é mais baixo que Marcos")
		escreva("\nc) João é o mais alto dos três")
		escreva("\nd) Pedro é o mais baixo")
		escreva("\ne) Marcos é mais alto que Pedro")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "c") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! João > Pedro > Marcos, logo João é o mais alto.\n")
		}
		
		// Questão 2
		escreva("\n2) Complete a sequência: 2, 5, 10, 17, __?")
		escreva("\na) 24")
		escreva("\nb) 26")
		escreva("\nc) 28")
		escreva("\nd) 30")
		escreva("\ne) 32")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "b") {
			escreva("✓ Correto! +10 XP (padrão: +3, +5, +7, +9)\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! Padrão: 2+3=5, 5+5=10, 10+7=17, 17+9=26\n")
		}
		
		// Questão 3
		escreva("\n3) Se todo concurseiro é dedicado, e alguns dedicados são ansiosos, pode-se concluir que:")
		escreva("\na) Todo ansioso é concurseiro")
		escreva("\nb) Nenhum concurseiro é ansioso")
		escreva("\nc) Alguns concurseiros são ansiosos")
		escreva("\nd) Todo concurseiro é ansioso")
		escreva("\ne) Nenhuma das anteriores")
		escreva("\nSua resposta (a, b, c, d ou e): ")
		leia(resposta)
		
		se(resposta == "c") {
			escreva("✓ Correto! +10 XP\n")
			xp += 10
			acertos++
		} senao {
			escreva("✗ Incorreto! A conclusão válida é que alguns concurseiros são ansiosos.\n")
		}
		
		escreva("\n=== Fim das questões de Raciocínio Lógico ===\n")
	}
}
	










/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 83; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */