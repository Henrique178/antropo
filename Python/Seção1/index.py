# nome = input('Digite o seu nome: ')
# idade = int(input('Digite a sua idade: '))
# idade_futuro = idade + 5

# print(f'Olá {nome}, daqui a 5 anos você terá {idade_futuro} anos de idade')

# numero1 = int(input('Digite o primeiro número: '))
# numero2 = int(input('Digite o segundo número: '))

# print(numero1 + numero2)
# print(numero1 - numero2)
# print(numero1 * numero2)
# print(numero1 / numero2)
# print(numero1 // numero2) # divisão inteira
# print(numero1 % numero2) # resto da divisão
# print(numero1 ** numero2) # potência

preco_original = int(input('Digite o preço do produto: '))
desconto = int(input('Digite o desconto em %: '))

preco_final = preco_original - (preco_original * desconto / 100)

print(f'O preço final do produto é: R$ {preco_final}')