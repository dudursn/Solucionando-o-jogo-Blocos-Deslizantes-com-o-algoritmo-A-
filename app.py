# -*- coding: utf-8 -*-
from funcoes_para_fila import *
from heuristica import *
from collections import OrderedDict

#############
# A # B # C #
#############
# D # E # F #
#############
# G # H # I #
#############

#Ambiente e todas aspossiveis movimentações
ambiente = OrderedDict([('A',['B','D']), ('B',['A','C','E']),('C',['B','F']),('D',['A','E','G']),('E',['B','D','F','H']),('F',['C','E','I']),('G',['D','H']),('H',['E','G','I']),('I',['F','H'])])
#objetivo: é o quebra-cabeças de blocos deslizantes objetivo colocados em forma de dicionário
objetivo = OrderedDict([('A',0), ('B',1),('C',2),('D',3),('E',4),('F',5),('G',6),('H',7),('I',8)])

'''
jogo: é o quebra-cabeças de blocos deslizantes criados e colocados em forma de dicionário
passos:  numero de passos
'''
def main():
	print("Informe um numero de 0 a 8 a cada um")
	jogo = criaAmbiente()
	printBloco(jogo)
	pause()
	print("Fazendo a busca...")
	#Faz a busca de melhor escolha A* e retorna o jogo organizado e a quantidade de passos para se chegar nele
	solucao, passos = buscaMelhorEscolha_A_ESTRELA(jogo)	
	if solucao!=None:
		#Imprime a sequencia para se chegar ao jogo e o numero de passos
		for e in solucao:
			printBloco(e)
			print("---------------")
		print("Numero de passos:",passos)
		
	else:
		print("ERRO")
	pause()


##########################################
#Algoritmos para a busca A estrela       #
##########################################

'''
Executa a busca no algoritmo A*
-f: custo de avaliação
-h: heuristica(distância de Manhattan)
-g: custo do que ja foi percorrido(numero de passos dados até o momento) para se chegar ao jogo atual
-no: é uma tupla que contém o jogo atual, custodeAvaliacao, custo Percorrido, jogoAnterior
-borda: fila de prioridades com base no custo de avaliação
-Explorado: fila com nós visitados
-objetivo: é o quebra-cabeças de blocos deslizantes objetivo colocados em forma de dicionário
-jogoCopia: copia do estado do jogo atual, ele será modificado para que possa guardar os estados possiveis na transição, assim não perdemos o jogo atual 
-atual: posição onde o zero está atualmente
-lista: lista de vizinhos a posição atual, ou seja, onde o 0 poderá ser movido

'''
def buscaMelhorEscolha_A_ESTRELA(jogo):
	#Inicializam as filas borda e explorado
	borda = []
	Explorado = []
	#Pega o estado inicial do jogo e coloca-se em um NO
	g = 0
	h = heuristica(jogo)
	f = custoDeAvaliacao(g,h)
	#O jogo está no estado inicial, logo não possui um estado anterior
	no = (jogo, f, g, None)

	# A borda contém um no com o estado inicial do jogo, seu custo de avaliação e o custo percorrido
	borda.append(no)

	#Enquanto a borda não estiver vazia
	while(borda !=[]):
		#NO possui (jogo, custodeAvaliacao, custo Percorrido, jogoAnterior)
		no = borda.pop(0)
		# jogo recebe o jogo no estado atual
		jogo = no[0]
		#g recebe o custo atual que já foi percorrido
		g = no[2]
		#Pega a posição atual que contém o 0
		atual = pegaPosDoZero(jogo)
		# o no é adicionado a fila Explorado
		Explorado.append(no)			
		#Teste de objetivo 
		if jogo == objetivo:
			#Retorna o caminho do jogo resolvido e o numero de passos dados
			return pegaCaminhoFinal(Explorado), g
		#Imprime a profundidade da arvore ou o numero de passos dados
		print(g)
		#Para de executar o programa e dar erro
		if(g==40):
			break
		#Faz uma copia do jogo no estado atual, assim não pega referencia
		jogoCopia = jogo.copy()
		#Pega o custo percorrido para se chegar ao NO atual soma-se mais um, pois será dado um passo
		g = g+1
		#lista de vizinhos a posição atual
		lista = ambiente[atual] 
		for vizinho in lista:
			#Transicão de estados do jogo, onde muda o jogoCopia, mas o estado atual está na variável jogo
			jogoCopia = troca(jogoCopia, atual, vizinho)

			h = heuristica(jogoCopia)
			f = custoDeAvaliacao(g+1,h)

			#cria um no
			no = (jogoCopia, f, g, jogo)

			#Retorna a posição do repetido na Borda ou se não for encontrado, falso
			pos_OR_state = verificaNoBorda(borda, jogoCopia)

			#Verifica se o no já não está nos Explorados ou não esta na borda
			if verificaNoExplorado(Explorado, jogoCopia)==False or pos_OR_state==False:
				#insere na borda
				borda.append(no)
			#Vai entrar nesse caso se o no estiver na borda
			else:
				#O no auxiliar guarda o no repetido da borda naquela posição
				noAux = borda[pos_OR_state]
				#compara custo de avaliação de nós que contém estados de jogo repetido
				if no[1] < noAux[1]:
					#Se o atual tiver menor custo ele substituirá o anterior na fila e o anterior será removido
					borda.pop(pos_OR_state)
					borda.insert(pos_OR_state, no)

			#Organiza a borda(Fila de prioridades) com base no custo de avaliação
			borda = organizaFila(borda)

			#Volta novamente para o jogo, pois jogoCopia foi modificado
			jogoCopia = jogo.copy()

	return None,0

#Função auxiliar que retorna o caminho percorrido para chegar a solução
def pegaCaminhoFinal(Explorado):
	#Lista que contém a sequencia de passos para se chegar a solução
	caminho = []
	#Insere o destino no caminho
	caminho.append(Explorado[-1][0])
	#Pega o estado do jogo anterior ao destino
	atual = Explorado[-1][3]
	#Enquanto não existir o pai, que no caso seria a origem
	while(atual != None):
		#Insere o jogo atual no caminho 
		caminho.append(atual)
		#Procura o jogo anterior(chamado pai) para se chegar no jogo atual
		pai = procuraPai(atual, Explorado)
		#O jogo anterior será o novo atual
		atual = pai
	#Está se inserindo na lista começando pelo último, então eu reorganizo ordenando de forma reversa
	caminho.reverse()

	return caminho

#Função auxiliar que procura o jogo anterior ao atual
def procuraPai(atual, Explorado):
	for i in range(len(Explorado)):
		if(atual==Explorado[i][0]):
			return Explorado[i][3]
	return None



'''
Faz a transição de estados do jogo onde: 
lugar1: é onde o 0 está no momento
lugar2: é um vizinho do lugar1 
'''
def troca(jogo, lugar1, lugar2):
	jogo[lugar1], jogo[lugar2]= jogo[lugar2], jogo[lugar1]
	return jogo

#Cria o jogo de blocos deslizantes
def criaAmbiente():
	jogo = OrderedDict()
	for key in ambiente:
		state = False
		while(not state):
			string = "Informe  um valor na posição "+key+": "
			dado= int(input(string))
			state = verificaDado(jogo,dado)
			if (state):
				jogo[key] = dado
	return jogo

'''Estado inicial, procura onde o 0 está no momento'''
def pegaPosDoZero(jogo):
	for key in jogo:
		if 0 == jogo[key]:
			return key

'''
Imprime o jogo em certo momento
'''
def printBloco(jogo):
	print("#############")
	i =0
	for key in jogo:
		if i!= 0 and i%3==0:
			print("#")
		print("#",jogo[key],end = " ")
		i+=1
	print("#")
	print("#############")

'''
calcula custo de avaliação
'''
def custoDeAvaliacao(g_n, h_n):
	return g_n+h_n

'''
	Verifica se um dado não está repetido ou se está fora do limite estabelecido
'''
def verificaDado(jogo, dado):
	if dado in [1,2,3,4,5,6,7,8,0]:
		for key in jogo:
			if dado == jogo[key]:
				print("Já está no quebra-cabeças! Insira outro")
				return False
		return True
	else:
		print("Informe um numero de 0 a 8!")
		return False

'''
Pausa para verificar as informações na tela
'''
def pause():
	input("Pressione a tecla ENTER para continuar...")



if __name__== "__main__":
	main()