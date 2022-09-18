# Faça um programa em Python que recebe um número inteiro 
# e imprime seu dígito das dezenas. 

numero = int(input("Digite um número inteiro:"))
resto = numero % 10 
numero = ((numero - resto) // 10)%10


print("O dígito das dezenas é",numero)