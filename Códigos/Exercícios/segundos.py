# Faça um programa em Python que, dada a quantidade de segundos,
# "quebre" esse valor em dias, horas, minutos e segundos. 

segundos = int(input("Por favor, entre com o número de segundos que deseja converter:"))

dia = segundos//86400
hora = (segundos%86400)//3600
minutos = ((segundos%86400)%3600)//60
segundos = ((segundos%86400)%3600)%60

print(dia,"dias,",hora,"horas,",minutos,"minutos e",segundos,"segundos.")