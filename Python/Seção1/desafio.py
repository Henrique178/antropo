# Calcular quantos dias um produto duraria se a pessoa usar X porções por dia

nome = input('Digite o seu nome: ')
produto = input('Digite o nome do produto: ')
estoque = int(input('Qual a quantidade em estoque? '))
porcoes = int(input('Qual a quantidade consumida por dia? '))

dias = estoque // porcoes
print(f'{nome}, você tem {dias} dias para consumir o {produto}')