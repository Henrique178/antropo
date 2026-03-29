# idade = int(input('Qual é a sua idade: '))
# carteira = False
# verificador = idade >= 18 and carteira

# print(verificador)

usuario = input('Digite o seu usuário: ')
senha = input('Digite a sua senha: ')

login_valido = usuario == 'Admin' and senha == '123admin'

print(f' Login permitido: {login_valido}')