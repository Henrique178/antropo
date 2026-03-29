# for / while

# For: utiliza quando eu sei a quantidade de vezes que preciso repetir a tarefa
# While: quando eu não sei a quantidade de vezes que preciso executar. Vai depender de uma variável ou condição

# for i in range(100, 0, -5):
#     print(i)

# ====================================

# i = int(input('Digite o número: '))

# while i <= 5:
#     print(i)
#     i += 1

# ====================================

senha = ''

while senha != '123':
    senha = input('Qual é a senha do sistema? ')
print('Acesso Liberado!')