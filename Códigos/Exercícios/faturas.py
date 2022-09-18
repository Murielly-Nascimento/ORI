# Escreva um programa que receba (entrada de dados através do teclado) o nome 
# do cliente, o dia de vencimento, o mês de vencimento e o valor da fatura  
# e imprima (saída de dados) a mensagem com os dados recebidos, no mesmo formato 
# da mensagem acima. 

nome = input("Digite o nome do cliente:")
dia = input("Digite o dia de vencimento:")
mes = input("Digite o mês de vencimento:")
valor = input("Digite o valor da fatura:")

print("Olá,",nome)
print("A sua fatura com vencimento em",dia,"de",mes,"no valor de R$",valor,"está fechada.")