from funcoes_para_fila import *
from app import *
#####################################################
#Algoritmos para a heurística Distancia de Manhatan #
#####################################################
	
def heuristica(jogo):
	soma = 0
	for i in range(1,9):
		origem = pegaPosdoValor(jogo, i)
		destino = pegaPosdoValor(objetivo, i)
		if origem!=destino:
			soma += buscaCustoUniforme(origem, destino)
	return soma

#Pega a posição que contém o valor atual
def pegaPosdoValor(dicionario, i):
	for e in dicionario:
		if dicionario[e]==i:
			return e

#Busca de custo uniforme para heuristica
def buscaCustoUniforme(origem, destino):
	#Inicia as filas Borda e o Explorado vazios
	Borda = []
	Explorado = []
	no = (origem, 0)
	#Coloca a origem na borda
	Borda.append(no)

	while(Borda!=[]):
		no = Borda.pop(0)
		#Atual[1] é a cidade que será expandida no momento
		atual = no[0]
		custo = no[1]
		#Teste de objetivo com a cidade atual
		if atual == destino:
			return custo
		Explorado.append(atual)
		lista = ambiente[atual]
		for vizinho in lista:
			no = (vizinho,custo+1)
			if verificaNoExplorado(Explorado,vizinho)==False or verificaNoBorda(Borda, vizinho)==False:
				Borda.append(no)
			#Com base no custo
			Borda =organizaFila(Borda)

	return None