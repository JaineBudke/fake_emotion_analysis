from random import randint
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class kmeans:


	sizeData = 134
	data = None

	OldCluster0 = set([1])
	OldOldCluster0 = set([2])



	def __init__( self, sizeDataE, data ):
		self.sizeData = sizeDataE
		self.data = data


	def calculate( self ):

		# gera k numeros aleatorios, de 0 ao tamanho total do conjunto de dados
		ki0 = 0
		#randint(0,self.sizeData)

		ki1 = self.sizeData - 1

		# garante a escolha de centroides iniciais diferentes
		#while( ki0 == ki1 ):
		#	ki1 = randint(0,self.sizeData)

		
		
		k0 = self.data.iloc[ki0, 23:34]
		k1 = self.data.iloc[ki1, 23:34]


		flag = True


		clust0 = set()
		clust1 = set()

		
		# aproximacao dos clusters
		while( self.stopCriteria() ):

			# cria dois clusters
			cluster0 = set()
			cluster1 = set()


			# percorre o dataframe
			#for index, row in self.data.iterrows():
			for index in range( len( self.data ) ):

			
				# computa a distancia euclidiana entre os pontos e o centroide
				d0 = self.manhattanDistance( k0, index )
				d1 = self.manhattanDistance( k1, index )

				
				# atribui cada um dos pontos ao cluster que tem o centroide mais proximo
				if( d0 < d1 ):
					cluster0.add( index )
				else:
					cluster1.add( index )


			# calcula a media de todos os pontos que pertencem a cada cluster e define o novo centroide
			k0 = self.pointsAverage( cluster0 )
			k1 = self.pointsAverage( cluster1 )

			if( flag == True ):
				self.OldCluster0 = cluster0
				flag = False
			else:
				self.OldOldCluster0 = cluster0
				flag = True

			clust0 = cluster0
			clust1 = cluster1
			

		truePositive  = 0
		falsePositive = 0
		trueNegative  = 0
		falseNegative = 0
		total = 0


		# (???) true positives: contrabiliza os que classificaram corretamente (tanto fake ou genuine) 
		# e divide pelo total analisado (???)
		


		#print( "CLASSIFICOU COMO FALSO, MAS É VERDADEIRO" )
		for item in clust0:
			total += 1


			if(self.data.iloc[item, 2] == 1.0):
				truePositive += 1
			elif( self.data.iloc[item, 2] == 0.0 ):
				falsePositive += 1

			#else:
			#	print( self.data.iloc[item, 0] )


		#print( "CLASSIFICOU COMO VERDADEIRO, MAS É FALSO")
		for item in clust1:
			total += 1
			if(self.data.iloc[item, 2] == 0.0):
				trueNegative += 1
			elif(self.data.iloc[item, 2] == 1.0):
				falseNegative += 1 
			#else:
			#	print( self.data.iloc[item, 0] )

		

		print(truePositive)
		print(falsePositive)
		print(trueNegative)
		print(falseNegative)

		print(total)
		
		


		
	def stopCriteria( self ):

		if( len(self.OldCluster0.intersection(self.OldOldCluster0)) == len(self.OldCluster0) ):
			return False
		else:
			return True
		


	def euclideanDistance( self, k, x ):

		result = 0.0


		# recupera cada um dos valores dos FVs da base de dados de x e de k
		count = 0
		for fv in range(23, 33):

			vx = int(self.data.iloc[x, fv])
			vk = int(k[count])

			
			result += ( math.pow( (vx-vk), 2 ) )
			count += 1
		
		return math.sqrt( result )


	def manhattanDistance( self, k, x ):
		
		result = 0.0
		
		# recupera cada um dos valores dos FVs da base de dados de x e de k
		count = 0
		for fv in range(23, 33):

			vx = int(self.data.iloc[x, fv])
			vk = int(k[count])

			xkSum = ( vx - vk )
			if( xkSum < 0 ):
				xkSum *= (-1)

			result += xkSum
			count  += 1

		return result


	def pointsAverage( self, cluster ):
	

		result = [  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
					0.0, 0.0, 0.0, 0.0, 0.0 ]
					
		rIndex = 0
		for fv in range(23, 33):

			valSum = 0
			for index in cluster:

				value = self.data.iloc[index, fv]

				valSum += value 				
			

			result[rIndex] = valSum/len(cluster)

			rIndex += 1

		return result






data = pd.read_csv('facialFeatures.csv') 
dataCohn = pd.read_csv('facialFeatures-cohn.csv') 



data_happy = data[data["emotion"] == "happy"]
cohn_happy = dataCohn[dataCohn["emotion"] == "happy"]

frames = [cohn_happy,data_happy]
happy = pd.concat(frames)


km = kmeans( len(happy), happy )

km.calculate()



# K = 2
# Escolher aleatoriamente K pontos dos dados pra ser os centroides iniciais
# while ( nao ha alteração nos clusters ha uns 10 passos ):
#      computar a distancia euclidiana entre os pontos e o centroide
#      atribuir cada um dos pontos ao cluster que tem o centroide mais proximo
#      calcular a media de todos os pontos que pertencem a cada cluster e definir o novo centroide


# como calcular essa distancia? visto que meus dados tem
# uma serie de parametros e tenho que analisar todos esses
# parametros em conjunto. 
# crio funcao matematica pra modelar isso?

# meus dados tem umas 18 dimensoes
# posso calcular a distancia euclidiana levando em consideracao todas essas
# dimensoes

