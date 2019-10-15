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
			return "fake"
		else:
			return "genuine"
		

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


happy = data[data["emotion"] == "happy"]
sad = data[data["emotion"] == "sad"]


# valores dos feature values do novo dado coletado
newData = happy.iloc[0, 21 :]


knnSad = knn( len(happy), happy )
print( knnSad.calculate( newData ) )