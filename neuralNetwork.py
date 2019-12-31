from random import randint
import math
import numpy as np
import pandas as pd
import operator
import random
from random import randint

class neuralNetwork:

	learningRate = 0.01

	# wij, wjk
	w = []

	deltaKSum = [100]

	contador = 0


	def train( self, inputLayerNeurons, hiddenLayerNeurons, dataset ):

		self.initializeWeights( inputLayerNeurons, hiddenLayerNeurons )


		# epochs
		while( self.stopCriteria() ):

	

			self.deltaKSum = []

			# percorre os dados de treinamento
			for index, data in dataset.iterrows():
		

				#################################################
				#### PERCORRE NEURONIOS ATÉ CHEGAR NO OUTPUT ####
				#################################################

				inputj = []
				inputk = 0

				# para cada neuronio da camada escondida
				for p in range( hiddenLayerNeurons ):

					xj = 0
					# para cada feature (xi) do dado corrente do dataset
					feature = 21
					for t in range( inputLayer ):
						xi = data[ feature ] # recupera um feature value do dado
						xj += ((xi * self.w[0][p][t]))
						feature += 1

					localyj = self.sigmoidFunction(xj)
					inputj.append(localyj)
				


				# para cada valor de yj
				xk = 0
				count = 0
				for yj in inputj:

					xk += ( (yj * self.w[1][count]) )
					count += 1

				yk = self.sigmoidFunction(xk)
				inputk = yk
					

				
				#########################################
				### CALCULEMOS AGORA O GRADIENT ERROR ###
				#########################################
				
				ek = data[ "fake" ] - inputk

				deltaK = inputk*(1-inputk)*ek
				deltaJ = []

				# para cada nó J da camada escondida, calcula
				count = 0
				for yj in inputj:
					delJ = yj*(1-yj)*(self.w[1][count]*deltaK)
					deltaJ.append(delJ)

					# atualiza os pesos da rede de wjk
					self.w[1][count] = self.w[1][count] + (self.learningRate * yj * deltaK)

					count+=1

				# atualiza pesos da rede de wij
				# para cada peso da rede, calcula
				for p in range( hiddenLayerNeurons ):
					feature = 21
					for t in range( inputLayer ):
						xi = data[ feature ] # recupera um feature value do dado
						# atualiza os pesos da rede de wij
						self.w[0][p][t] = self.w[0][p][t] + self.learningRate * xi * deltaJ[p]
						feature += 1


				self.deltaKSum.append(ek**2)
				#print(inputk)

		

			
	
	def test( self, inputLayerNeurons, hiddenLayerNeurons, dataTest ):

		# deu que é fake e era fake mesmo
		truePositive  = 0
		# deu fake, mas era genuina
		falsePositive = 0
		# deu que é genuina e era genuina mesmo
		trueNegative  = 0
		# deu que é genuina, mas era fake
		falseNegative = 0


		# percorre os dados de treinamento
		for index, data in dataTest.iterrows():


			#################################################
			#### PERCORRE NEURONIOS ATÉ CHEGAR NO OUTPUT ####
			#################################################

			inputj = []
			inputk = 0

			# para cada neuronio da camada escondida
			for p in range( hiddenLayerNeurons ):

				xj = 0
				# para cada feature (xi) do dado corrente do dataset
				feature = 21
				for t in range( inputLayer ):
					xi = data[ feature ] # recupera um feature value do dado
					xj += ((xi * self.w[0][p][t]) )
					feature += 1

				localyj = self.sigmoidFunction(xj)
				inputj.append(localyj)
			


			# para cada valor de yj
			xk = 0
			count = 0
			for yj in inputj:

				xk += ( (yj * self.w[1][count]) )
				count += 1

			yk = self.sigmoidFunction(xk)
			inputk = yk
				

			if( data["fake"] == 1.0 and inputk > 0.5 ):
				truePositive += 1
			elif( data["fake"] == 0.0 and inputk > 0.5 ):
				falsePositive += 1
			elif( data["fake"] == 0.0 and inputk <= 0.5 ):
				trueNegative += 1
			elif( data["fake"] == 1.0 and inputk <= 0.5 ):
				falseNegative += 1
			


		print(truePositive)
		print(falsePositive)
		print(trueNegative)
		print(falseNegative)

	def initializeWeights( self, numberInputLayer, numberHiddenLayer ):

		wij = []
		wjk = []
	
		for i in range( numberHiddenLayer ):

			wtemp = []

			for k in range( numberInputLayer ):
				w = round(random.uniform(0,1),4)
			
				wtemp.append(w)

			wij.append(wtemp)

		for j in range( numberHiddenLayer ):
			w = round(random.uniform(0,1),4)
			wjk.append(w)

		
		self.w.append( wij )
		self.w.append( wjk )




	def sigmoidFunction( self, x ):
		return ( 1/(1+(math.e**(-x)) ) )


	def stopCriteria( self ):

		self.contador += 1 
		print(self.contador)

		media = sum(self.deltaKSum)/len(self.deltaKSum)
		print(media)
		if( media > 0.1 ):
			return True
			
		return False



	###########################################
	#### ESSA É A IDA ATÉ CHEGAR NO OUTPUT ####
	###########################################

	# armazena os yj = []
	# armazena os yk = []

	# para cada neuronio da camada escondida

		# xj = 0
		# para cada dado (xi) do dataset
			# xj += ((xi * wij) - thetaj)
			# yj = sigmoidFunction(xj)


	# para cada valor de yj
		# xk += ( (yj * wjk) - thetak )
		# yk = sigmoidFunction(xk)


	#########################################
	### CALCULEMOS AGORA O ERROR GRADIENT ###
	#########################################
	
	# ek = dk - yk
	# deltaK = yk*(1-yk)*ek

	# para cada nó J da camada escondida, calcula
		# deltaJ = yj*(1-yj)*(wjk*deltaK)

	######### ATUALIZEMOS OS PESOS ##########
	# para cada peso da rede, calcula
		# wij = wij + (learningRate * xi * deltaJ)
		# wjk = wjk + (learningRate * yj * deltaK)



data = pd.read_csv('facialFeatures.csv') 

happy = data[data["emotion"] == "happy"]
sad = data[data["emotion"] == "sad"]



mlp = neuralNetwork( )

inputLayer = 10
hiddenLayer = 2


# pegar uma amostra aleatória dos dados

'''
happy_copy = happy.copy()
train_set = happy_copy.sample(frac=0.7, random_state=42)
test_set = happy_copy.drop(train_set.index)
'''

sad_copy = sad.copy()
train_set = sad_copy.sample(frac=0.7, random_state=42)
test_set = sad_copy.drop(train_set.index)


mlp.train( inputLayer, hiddenLayer, train_set )

mlp.test( inputLayer, hiddenLayer, test_set )
