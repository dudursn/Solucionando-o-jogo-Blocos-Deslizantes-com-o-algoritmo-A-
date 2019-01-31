
##########################################
#      Funções para as Filas             #
##########################################
'''
Organiza a fila com base no custo de avaliação
'''
def organizaFila(borda):
	borda.sort(key=lambda x: x[1])
	return borda

'''
Explorado = Fila formado por nós que já foram espandidos
filho: filho do no que está em expansão
'''
def verificaNoExplorado(Explorado, filho):
	for i in range(len(Explorado)):
		if filho == Explorado[i][0]:
			return True
	return False
'''
borda: prestes a ser expandidos
filho: filho do no em expansão
Retorna falso se não for encontrado, se for encontrado retorna a posição na fila
'''
def verificaNoBorda(borda, filho):
	for i in range(len(borda)):
		if filho == borda[i][0]:
			return i
	return False
