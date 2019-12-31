from random import randint
import math
import numpy as np
import pandas as pd
import operator


class knn:

	sizeData = 134
	data = None

	# lista de tuplas [indice do elemento no dataframe,distancia] 
	distList = [[0,1000],[0,1000],[0,1000],[0,1000],[0,1000]]
 


	def __init__( self, sizeDataE, data ):
		self.sizeData = sizeDataE
		self.data = data


	def calculate( self, newData ):

		# Mede a distância do novo dado com todos os outros dados que já estão classificados
		# percorre o dataframe
		for index in range( len( self.data ) ):

			# computa a distancia de manhattan entre os pontos do dataframe e o novo ponto
			dist = self.manhattanDistance( newData, index )


			# obtém as k menores distâncias (vai salvando em um array)	
			# encontra elemento com maior distancia
			maior = self.distList[0][1]
			indexMaior = 0	
			for i in range(len( self.distList ) ):
				if( self.distList[i][1] > maior ):
					maior = self.distList[i][1]
					indexMaior = i


			if( dist < maior ):
				self.distList[indexMaior] = [index, dist]

		
		return self.classifier()
	


	def classifier( self ):

		fake = 0
		genuine = 0

		# percorre a classe dos dados de menor distância e conta a quantidade que aparece de cada classe (fake or genuine)
		for elem in self.distList:
			fakeGenuine = int(self.data.iloc[elem[0], 2])

			if( fakeGenuine == 1 ):
				fake += 1
			elif( fakeGenuine == 0 ):
				genuine += 1

		# Toma como resultado a classe que mais apareceu dentre os dados que tiveram as menores distâncias
		if( fake > genuine ):
			return 1.0
		else:
			return 0.0
		

	def manhattanDistance( self, k, x ):
		
		result = 0.0
		
		# recupera cada um dos valores dos FVs da base de dados de x e de k
		count = 0
		for fv in range(21, 34):

			vx = int(self.data.iloc[x, fv])
			vk = int(k[count])

			xkSum = ( vx - vk )
			if( xkSum < 0 ):
				xkSum *= (-1)

			result += xkSum
			count  += 1

		return result




data = pd.read_csv('facialFeatures.csv') 
dataCohn = pd.read_csv('facialFeatures-cohn.csv') 



data_happy = data[data["emotion"] == "happy"]
cohn_happy = dataCohn[dataCohn["emotion"] == "happy"]

frames = [cohn_happy,data_happy]
happy = pd.concat(frames)


# deu que é fake e era fake mesmo
truePositive  = 0
# deu fake, mas era genuina
falsePositive = 0
# deu que é genuina e era genuina mesmo
trueNegative  = 0
# deu que é genuina, mas era fake
falseNegative = 0

total = 0



# percorre todos os dados do dataset
for count in range(len(happy)):


	# apaga o dado corrente a ser analisado pelo algoritmo
	newHappy = happy.drop( happy.iloc[count, 0] )

	# chama o algoritmo com o dataset sem o dado corrente
	knnHappy = knn( len(newHappy), newHappy )


	result = knnHappy.calculate( happy.iloc[count, 21 :] ) 

	if( result == 1.0 and happy.iloc[count, 2] == 1.0 ):
		truePositive += 1

	elif( result == 0.0 and happy.iloc[count, 2] == 0.0 ):
		trueNegative += 1

	elif( result == 1.0 and happy.iloc[count, 2] == 0.0 ):
		falsePositive += 1

	elif( result == 0.0 and happy.iloc[count, 2] == 1.0 ):
		falseNegative += 1


	total += 1


'''


for count in range(len(sad)):


	newSad = sad.drop( sad.iloc[count, 0] )
	knnSad = knn( len(newSad), newSad )


	result = knnSad.calculate( sad.iloc[count, 21 :] )

	if( result == 1.0 and sad.iloc[count, 2] == 1.0 ):
		truePositive += 1

	elif( result == 0.0 and sad.iloc[count, 2] == 0.0 ):
		trueNegative += 1

	elif( result == 1.0 and sad.iloc[count, 2] == 0.0 ):
		falsePositive += 1

	elif( result == 0.0 and sad.iloc[count, 2] == 1.0 ):
		falseNegative += 1


	total += 1
	
'''


print(truePositive)
print(falsePositive)
print(trueNegative)
print(falseNegative)

print( total )

