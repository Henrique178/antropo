/******************************************************************************

Welcome to GDB Online.
  GDB online is an online compiler and debugger tool for C, C++, Python, PHP, Ruby, 
  C#, OCaml, VB, Perl, Swift, Prolog, Javascript, Pascal, COBOL, HTML, CSS, JS
  Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h> // Para suportar acentuação no terminal
#include <ctype.h>  // Para suportar a função tolower()

char nome[100], resposta[10];
int opcao, xp = 0, acertos = 0, categoria, totalQuestoes = 0;
bool continuar = true;
bool estudando = true;

typedef struct {
    char enunciado[300];
    char alternativas[5][200];
    char respostaCorreta;
    int pontuacao;
    char explicacao[300];
} Questao;

void (*categorias[4])();

void perguntasLegislacao();
void perguntasPortugues();
void perguntasAdministracao();
void perguntasRaciocinio();
void exibirProgresso();
void aplicarQuiz(Questao questoes[], int quantidade, const char* tituloCategoria);
void ler_texto(char* buffer, int tamanho); // Prototipação da função de leitura segura

void embaralharQuestoes(Questao questoes[], int quantidade) {
    for (int i = quantidade - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        Questao temp = questoes[i];
        questoes[i] = questoes[j];
        questoes[j] = temp;
    }
}

int main() {
    setlocale(LC_ALL, "Portuguese"); // Ativa o uso de acentos e 'ç'
    srand(time(NULL));
    
    char entrada_temp[10]; // Buffer temporário para os menus
    
    printf("=== Bem-vindo ao AprovaGame ===\n");
    printf("=== Escreva o seu nome: ");
    ler_texto(nome, 100);
    
    categorias[0] = perguntasLegislacao;
    categorias[1] = perguntasPortugues;
    categorias[2] = perguntasAdministracao;
    categorias[3] = perguntasRaciocinio;
    
    while(continuar) {
        printf("\n=== MENU PRINCIPAL ===");
        printf("\n1) Iniciar Estudo");
        printf("\n2) Ver desempenho");
        printf("\n3) Sair");
        printf("\nEscolha uma opção: ");
        
        ler_texto(entrada_temp, 10);
        opcao = atoi(entrada_temp); // Converte o texto digitado para número
        
        switch(opcao) {
            case 1:
                estudando = true;
                while(estudando) {
                    printf("\n=== CATEGORIAS DE ESTUDO ===");
                    printf("\n1) Legislação para Concurso");
                    printf("\n2) Língua Portuguesa para Concurso");
                    printf("\n3) Noções de Administração");
                    printf("\n4) Raciocínio Lógico");
                    printf("\n5) Voltar ao menu principal");
                    printf("\nEscolha uma categoria: ");
                    
                    ler_texto(entrada_temp, 10);
                    categoria = atoi(entrada_temp);
                    
                    if(categoria >= 1 && categoria <= 4) {
                        categorias[categoria-1]();
                        exibirProgresso();
                    } else if(categoria == 5) {
                        estudando = false;
                        printf("\nVoltando ao menu principal...\n");
                    } else {
                        printf("\nOpção Inválida! Tente novamente!\n");
                    }
                }
                break;
                
            case 2:
                printf("\n=== DESEMPENHO DO USUÁRIO ===");
                printf("\nUsuário: %s", nome);
                printf("\nPontuação total: %d XP", xp);
                printf("\nTotal de acertos: %d questões", acertos);
                printf("\nTotal de questões respondidas: %d", totalQuestoes);
                if(totalQuestoes > 0) {
                    printf("\nTaxa de acerto: %.1f%%", (float)acertos/totalQuestoes * 100);
                }
                printf("\n");
                break;
                
            case 3:
                printf("\nEncerrando o AprovaGame. Bons Estudos, %s!\n", nome);
                continuar = false;
                break;
                
            default:
                printf("\nOpção Inválida! Tente novamente.\n");
        }
    }
    return 0;
}

// Função auxiliar para evitar lixo no buffer de memória do teclado
void ler_texto(char* buffer, int tamanho) {
    fgets(buffer, tamanho, stdin);
    if (strchr(buffer, '\n') == NULL) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
    } else {
        buffer[strcspn(buffer, "\n")] = 0;
    }
}

void exibirProgresso() {
    printf("\n=== PROGRESSO ATUAL ===");
    printf("\nXP acumulado: %d", xp);
    printf("\nAcertos: %d", acertos);
    printf("\nTotal questões respondidas: %d", totalQuestoes);
    if(totalQuestoes > 0) {
        printf("\nTaxa de acerto: %.1f%%", (float)acertos/totalQuestoes * 100);
    }
    printf("\n");
}

void aplicarQuiz(Questao questoes[], int quantidade, const char* tituloCategoria) {
    printf("\n=== %s ===\n", tituloCategoria);
    
    for(int i = 0; i < quantidade; i++) {
        printf("\n--- Questão %d de %d ---", i+1, quantidade);
        printf("\n[%d XP] %s\n", questoes[i].pontuacao, questoes[i].enunciado);
        
        for(int j = 0; j < 5; j++) {
            printf("   %c) %s\n", 'a' + j, questoes[i].alternativas[j]);
        }
        
        printf("Sua resposta (a, b, c, d ou e): ");
        ler_texto(resposta, 10);
        
        // tolower transforma 'A' maiúsculo em 'a' minúsculo para evitar erros do usuário
        if(tolower(resposta[0]) == questoes[i].respostaCorreta) {
            printf("✓ CORRETO! +%d XP\n", questoes[i].pontuacao);
            xp += questoes[i].pontuacao;
            acertos++;
        } else {
            printf("✗ INCORRETO!\n");
            printf("Resposta correta: %c\n", questoes[i].respostaCorreta);
            printf("Explicação: %s\n", questoes[i].explicacao);
        }
        totalQuestoes++;
    }
    printf("\n=== Fim das questões de %s ===\n", tituloCategoria);
}

void perguntasLegislacao() {
    Questao questoesLegislacao[15] = {
        {"De acordo com a Lei 8.112/90, sao requisitos basicos para investidura em cargo publico, EXCETO:",
         {"Nacionalidade brasileira", "Idade minima de 21 anos", "Quitacao com as obrigacoes eleitorais", "Aptidao fisica e mental", "Nivel de escolaridade exigido para o cargo"},
         'b', 10, "A idade minima e 18 anos, nao 21."},
        {"O principio da administracao publica que exige transparencia e publicidade dos atos e chamado de:",
         {"Impessoalidade", "Moralidade", "Publicidade", "Eficiencia", "Legalidade"},
         'c', 10, "Publicidade e o principio que exige transparencia dos atos administrativos."},
        {"A Lei de Improbidade Administrativa (Lei 8.429/92) NAO se aplica a:",
         {"Agentes politicos", "Servidores publicos estatutarios", "Empregados de empresas privadas", "Empregados de empresas publicas", "Particulares que recebem recursos publicos"},
         'c', 10, "A lei nao se aplica a empregados de empresas privadas sem vinculo com o poder publico."},
        {"Sao principios expressos da Administracao Publica na Constituicao Federal de 1988, EXCETO:",
         {"Legalidade", "Impessoalidade", "Moralidade", "Eficiencia", "Supremacia do interesse publico"},
         'e', 15, "Supremacia do interesse publico e um principio implicito, nao expresso no art. 37."},
        {"A investidura em cargo publico ocorre apos:",
         {"Nomeacao", "Posse", "Exercicio", "Publicacao no DOU", "Aprovacao no estagio probatorio"},
         'b', 10, "A investidura se da com a posse, conforme art. 7 da Lei 8.112/90."},
        {"O prazo para o servidor publico entrar em exercicio apos a posse e de:",
         {"5 dias", "10 dias", "15 dias", "30 dias", "45 dias"},
         'c', 10, "Art. 13, Lei 8.112/90: 15 dias para entrar em exercicio."},
        {"A estabilidade do servidor publico ocorre apos quantos anos de estagio probatorio?",
         {"1 ano", "2 anos", "3 anos", "4 anos", "5 anos"},
         'c', 15, "Emenda Constitucional 19/98: 3 anos de estagio probatorio."},
        {"O ato administrativo que tornam sem efeito os atos ilegais ou inconvenientes e chamado de:",
         {"Anulacao", "Revogacao", "Convalidacao", "Cassacao", "Caducidade"},
         'a', 15, "Anulacao e para atos ilegais; Revogacao para inconvenientes/ina oportunos."},
        {"O poder disciplinar da Administracao Publica se manifesta mediante:",
         {"Atos normativos", "Atos de organizacao", "Atos de punicao", "Atos de planejamento", "Atos de direcao"},
         'c', 10, "Poder disciplinar e o poder de punir infracoes funcionais dos servidores."},
        {"O servidor publico perde o cargo em decorrencia de sentenca judicial transitada em julgado, EXCETO:",
         {"Condenacao criminal", "Improbus", "Acao civil publica", "Acao popular", "Acao de improbidade"},
         'd', 15, "Acao popular nao e causa de perda do cargo, apenas anulacao de ato lesivo."},
        {"A reversao de servidor publico consiste em:",
         {"Retorno a atividade de servidor apos aposentadoria", "Passagem de cargo para outro", "Promocao funcional", "Transferencia de orgao", "Remocao por interesse da administracao"},
         'a', 15, "Reversao e o retorno a atividade de servidor aposentado."},
        {"A acumulacao de cargos publicos e permitida quando:",
         {"Dois cargos de professor", "Um cargo de professor e outro tecnico-cientifico", "Dois cargos de medico", "Todas as alternativas", "Nenhuma alternativa"},
         'd', 20, "CF/88 permite acumulacao nas hipoteses: dois cargos de professor ou um professor com tecnico."},
        {"O prazo de prescricao para acao disciplinar contra servidor publico e de:",
         {"2 anos", "3 anos", "5 anos", "10 anos", "Nao ha prescricao"},
         'c', 15, "Lei 8.112/90: 5 anos para prescricao da acao disciplinar."},
        {"O servidor publico respondera civil, penal e administrativamente pelos atos que praticar, sendo que a responsabilidade civil:",
         {"E objetiva", "E subjetiva", "Depende de dolo ou culpa", "E sempre solidaria", "Nao existe"},
         'c', 15, "Responsabilidade civil do servidor e subjetiva (depende de dolo ou culpa)."},
        {"A Lei 8.112/90 estabelece como dever do servidor:",
         {"Lealdade as instituicoes", "Manter sigilo sobre assinaturas", "Atender com presteza", "Representar contra ilegalidade", "Todas as alternativas"},
         'e', 10, "Art. 116, Lei 8.112/90: todos sao deveres do servidor publico."}
    };
    embaralharQuestoes(questoesLegislacao, 15);
    aplicarQuiz(questoesLegislacao, 15, "LEGISLAÇÃO PARA CONCURSO");
}

void perguntasPortugues() {
    Questao questoesPortugues[15] = {
        {"Assinale a alternativa em que a palavra esta corretamente acentuada:",
         {"Heroico", "Jiboia", "Assembleia", "Polen", "Idoone"},
         'd', 10, "'Polen' e acentuado (paroxitona terminada em 'n')."},
        {"Qual das frases abaixo apresenta ERRO de regencia verbal?",
         {"Assistimos ao filme ontem.", "Prefiro estudar a trabalhar.", "Obedeço ao regulamento.", "Lembrei do seu aniversario.", "Paguei o boleto hoje."},
         'b', 10, "O correto e 'Prefiro estudar a trabalhar' (sem crase antes de verbo)."},
        {"Em 'O povo elegeu seus representantes', o sujeito e:",
         {"Simples", "Composto", "Oculto", "Indeterminado", "Inexistente"},
         'a', 10, "Sujeito simples: 'O povo' (um unico nucleo)."},
        {"Indique a frase em que a crase foi empregada corretamente:",
         {"Fui a cidade ontem.", "Ele se referiu aquele assunto.", "Vou a festa hoje.", "Ela escreveu a caneta.", "Chegamos as 10 horas."},
         'e', 15, "'as 10 horas' - crase obrigatoria antes de horas determinadas."},
        {"A palavra 'descortinar' significa:",
         {"Ocultar", "Revelar", "Fechar", "Esconder", "Encobrir"},
         'b', 10, "Descortinar significa revelar, tirar a cortina, descobrir."},
        {"Em qual alternativa ocorre hiato?",
         {"Quase", "Passeio", "Saída", "Bicicleta", "Guerra"},
         'c', 15, "Sa-í-da - encontro de vogais em silabas diferentes."},
        {"A frase 'O menino pegou o brinquedo e saiu correndo' apresenta oracao:",
         {"Absoluta", "Coordenada sindetica", "Coordenada assindetica", "Subordinada", "Principal"},
         'b', 10, "Oracao coordenada sindetica aditiva (conectivo 'e')."},
        {"Assinale a alternativa em que a palavra 'como' exerce funcao de conjuncao comparativa:",
         {"Como voce esta?", "Nao sei como fazer isso.", "Ele trabalha como medico.", "Ele e inteligente, como o irmao.", "Como nao estudou, foi reprovado."},
         'd', 15, "'como' comparativo estabelece comparacao entre dois termos."},
        {"A figura de linguagem presente em 'A vida e uma ponte' e:",
         {"Metafora", "Comparacao", "Metonimia", "Catacrese", "Sinestesia"},
         'a', 10, "Metafora - comparacao implicita sem conectivo."},
        {"O vocativo esta presente em:",
         {"Maria foi aprovada!", "Maria, voce foi aprovada!", "A Maria foi aprovada!", "Voce viu a Maria?", "Maria e estudiosa!"},
         'b', 10, "Vocativo 'Maria' - termo que chama/interpela o interlocutor."},
        {"Assinale a alternativa com erro de concordancia verbal:",
         {"Fazem dez anos que nao o vejo.", "Houve muitos problemas.", "Existem solucoes viaveis.", "Deve haver melhorias.", "Tem pessoas esperando."},
         'a', 15, "Correto: 'Faz dez anos' - verbo fazer indicando tempo e impessoal."},
        {"A palavra 'infelizmente' e formada por:",
         {"Derivacao prefixal", "Derivacao sufixal", "Derivacao parassintetica", "Composicao", "Derivacao regressiva"},
         'a', 10, "Prefixo 'in-' + radical 'feliz' + sufixo '-mente'."},
        {"Em 'Ele chegou cedo para a reuniao', o termo 'cedo' classifica-se como:",
         {"Adverbio de tempo", "Adverbio de modo", "Adverbio de lugar", "Adverbio de intensidade", "Adverbio de duvida"},
         'a', 10, "'Cedo' indica circunstancia de tempo."},
        {"A frase 'A menina sorridente acenou para mim' apresenta oracao:",
         {"Absoluta", "Coordenada", "Subordinada adjetiva", "Subordinada adverbial", "Oracao principal"},
         'c', 15, "'que sorria' - oracao subordinada adjetiva restritiva (oculta)."},
        {"Indique a alternativa em que o uso do acento grave (crase) e facultativo:",
         {"Vou a casa dela.", "Refiro-me a aquela pessoa.", "Chegamos a conclusao.", "Vamos a praia.", "A partir de hoje."},
         'c', 15, "Antes de palavra feminina com 'a' - crase facultativa."}
    };
    embaralharQuestoes(questoesPortugues, 15);
    aplicarQuiz(questoesPortugues, 15, "LÍNGUA PORTUGUESA PARA CONCURSO");
}

void perguntasAdministracao() {
    Questao questoesAdministracao[15] = {
        {"Quem e considerado o 'pai da administracao cientifica'?",
         {"Henri Fayol", "Elton Mayo", "Frederick Taylor", "Peter Drucker", "Max Weber"},
         'c', 10, "Frederick Taylor - Administracao Cientifica (foco na tarefa)."},
        {"Na funcao administrativa, o ato de 'comparar resultados com objetivos planejados' corresponde a:",
         {"Planejamento", "Organizacao", "Direcao", "Controle", "Coordenacao"},
         'd', 10, "Controle - funcao que verifica se os resultados estao conforme planejado."},
        {"A estrutura organizacional em forma de piramide, com hierarquia bem definida, e chamada de:",
         {"Estrutura matricial", "Estrutura linear", "Estrutura horizontal", "Estrutura em rede", "Estrutura circular"},
         'b', 10, "Estrutura linear - hierarquica, com unidade de comando."},
        {"O principio da administracao que defende que 'um subordinado deve responder a um unico chefe' e:",
         {"Amplitude de controle", "Unidade de comando", "Hierarquia", "Delegacao", "Centralizacao"},
         'b', 15, "Unidade de comando - cada subordinado se reporta a um unico superior."},
        {"A escola de administracao que enfatiza as relacoes humanas e liderada por:",
         {"Taylor", "Fayol", "Weber", "Elton Mayo", "Maslow"},
         'd', 15, "Elton Mayo - Teoria das Relacoes Humanas (Experiencia de Hawthorne)."},
        {"O processo administrativo, segundo Fayol, e composto por:",
         {"Planejar, dirigir, controlar", "POCCC - Planejar, Organizar, Comandar, Coordenar, Controlar", "Planejar, organizar, liderar", "Planejar, executar, verificar, agir", "Diagnosticar, planejar, executar"},
         'b', 15, "Fayol: Prever, Organizar, Comandar, Coordenar, Controlar."},
        {"A teoria motivacional de Maslow e conhecida como:",
         {"Teoria dos dois fatores", "Teoria X e Y", "Pirâmide das necessidades", "Teoria da expectativa", "Teoria da equidade"},
         'c', 15, "Maslow: Hierarquia das necessidades (fisiologicas, seguranca, social, estima, autorrealizacao)."},
        {"O tipo de lideranca que centraliza as decisoes e impoe determinacoes e chamada de:",
         {"Democratica", "Lideranca situacional", "Autocratica", "Laissez-faire", "Carismatica"},
         'c', 10, "Lideranca autocratica - centralizadora, impositiva."},
        {"A ferramenta de gestao da qualidade que significa '5S' originou-se em:",
         {"EUA", "Alemanha", "Japao", "Franca", "Italia"},
         'c', 10, "5S - programa japones de qualidade total."},
        {"O ciclo PDCA (Plan, Do, Check, Act) foi desenvolvido por:",
         {"Deming", "Juran", "Crosby", "Ishikawa", "Feigenbaum"},
         'a', 15, "William Edwards Deming - criador do ciclo PDCA."},
        {"A matriz SWOT analisa:",
         {"Forcas, fraquezas, oportunidades, ameacas", "Planejamento estrategico", "Custos e beneficios", "Eficiencia e eficacia", "Missao, visao, valores"},
         'a', 15, "SWOT = Strengths, Weaknesses, Opportunities, Threats."},
        {"O principio da 'escala hierarquica' em Weber refere-se a:",
         {"Cadeia de comando", "Divisao do trabalho", "Impessoalidade", "Meritocracia", "Burocracia"},
         'a', 10, "Cadeia de comando - hierarquia de autoridade na burocracia."},
        {"Na administracao, eficacia significa:",
         {"Fazer certo as coisas", "Fazer as coisas certas", "Reduzir custos", "Aumentar produtividade", "Maximizar lucros"},
         'b', 10, "Eficacia = alcance dos objetivos (fazer as coisas certas)."},
        {"O benchmarking consiste em:",
         {"Comparar processos com os melhores", "Reduzir despesas", "Aumentar estoques", "Contratar consultores", "Demitir funcionarios"},
         'a', 15, "Benchmarking - processo de comparacao com as melhores praticas do mercado."},
        {"A teoria que defende que o administrador deve adaptar seu estilo as circunstancias e:",
         {"Teoria contingencial", "Teoria estruturalista", "Teoria sistemica", "Teoria comportamental", "Teoria classica"},
         'a', 15, "Teoria contingencial - nao ha uma unica melhor maneira, depende da situacao."}
    };
    embaralharQuestoes(questoesAdministracao, 15);
    aplicarQuiz(questoesAdministracao, 15, "NOÇÕES DE ADMINISTRAÇÃO");
}

void perguntasRaciocinio() {
    Questao questoesRaciocinio[15] = {
        {"Se Joao e mais alto que Pedro, e Pedro e mais alto que Marcos, entao:",
         {"Marcos e mais alto que Joao", "Joao e mais baixo que Marcos", "Joao e o mais alto dos tres", "Pedro e o mais baixo", "Marcos e mais alto que Pedro"},
         'c', 10, "Joao > Pedro > Marcos, logo Joao e o mais alto."},
        {"Complete a sequencia: 2, 5, 10, 17, __?",
         {"24", "26", "28", "30", "32"},
         'b', 10, "Padrao: +3, +5, +7, +9 -> 17+9=26"},
        {"Se todo concurseiro e dedicado, e alguns dedicados sao ansiosos, pode-se concluir que:",
         {"Todo ansioso e concurseiro", "Nenhum concurseiro e ansioso", "Alguns concurseiros sao ansiosos", "Todo concurseiro e ansioso", "Nenhuma das anteriores"},
         'c', 15, "Alguns concurseiros sao ansiosos (deducao logica valida)."},
        {"Qual e o proximo termo da sequencia: A, D, I, P, __?",
         {"U", "V", "W", "X", "Y"},
         'e', 15, "Diferenca: +3, +5, +7, +9 letras -> P(16)+9=25(Y)."},
        {"Um relogio adianta 3 minutos por hora. Quanto adiantara em 8 horas?",
         {"24 min", "21 min", "18 min", "15 min", "12 min"},
         'a', 10, "3 min/hora x 8 horas = 24 minutos."}, // Erro de compilação corrigido aqui
        {"Se 5 operarios produzem 100 pecas em 4 horas, quantas pecas 8 operarios produzirao em 6 horas?",
         {"200", "240", "280", "300", "320"},
         'b', 15, "Regra de tres composta: (5x4)/(8x6) = 100/x -> x=240"},
        {"Qual a probabilidade de sair um numero par no lancamento de um dado nao viciado?",
         {"1/2", "1/3", "1/6", "2/3", "5/6"},
         'a', 10, "Numeros pares: 2,4,6 -> 3/6 = 1/2"},
        {"Complete: 1, 3, 6, 10, 15, __?",
         {"18", "20", "21", "24", "25"},
         'c', 10, "Numeros triangulares: +2, +3, +4, +5, +6 -> 15+6=21"},
        {"Ana e mais velha que Beatriz. Carla e mais nova que Ana. Beatriz e mais velha que Carla. Quem e a mais nova?",
         {"Ana", "Beatriz", "Carla", "Nao e possivel determinar", "Todas tem mesma idade"},
         'c', 15, "Ana > Beatriz > Carla, logo Carla e a mais nova."},
        {"Se 2x + 5 = 15, entao x e igual a:",
         {"3", "4", "5", "6", "7"},
         'c', 5, "2x = 10 -> x = 5"},
        {"Quantos anagramas tem a palavra 'PROVA'?",
         {"60", "80", "100", "120", "150"},
         'd', 15, "5! = 5x4x3x2x1 = 120 anagramas."},
        {"Qual e o valor logico da proposicao 'Se chove entao faz frio' quando chove e nao faz frio?",
         {"Verdadeiro", "Falso", "Indeterminado", "Contradicao", "Tautologia"},
         'b', 15, "V->F = Falso (condicional so e falsa quando V->F)."},
        {"Complete a matriz: 2 4 6; 8 10 12; 14 16 __",
         {"15", "17", "18", "19", "20"},
         'c', 10, "Progressao de 2 em 2: 14,16,18."},
        {"Se hoje e sabado, que dia sera daqui a 100 dias?",
         {"Sabado", "Domingo", "Segunda", "Terca", "Quarta"},
         'd', 15, "100 dias = 14 semanas (98 dias) + 2 dias = Terca-feira."},
        {"Qual a area de um quadrado cujo perimetro e 20 cm?",
         {"20 cm²", "25 cm²", "30 cm²", "35 cm²", "40 cm²"},
         'b', 10, "Lado = 20/4 = 5, Area = 5x5 = 25 cm²"}
    };
    
    embaralharQuestoes(questoesRaciocinio, 15);
    aplicarQuiz(questoesRaciocinio, 15, "RACIOCÍNIO LÓGICO");
}