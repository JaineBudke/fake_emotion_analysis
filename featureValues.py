import numpy as np



class calcFeatureValues:

	shape = np.empty(68)

	def __init__(self, shape):
		self.shape = shape


	def ieb_height(self):
		return (( (self.shape[21][1]+self.shape[20][1])/2 + (self.shape[22][1]+self.shape[23][1])/2 )/2)


	def oeb_height(self):
		return (( self.shape[19][1] + self.shape[24][1] )/2)


	def eb_frowned(self):
		return ((((self.shape[21][1] - self.shape[20][1])+(self.shape[19][1] - self.shape[20][1])) + ((self.shape[24][1] - self.shape[23][1])+(self.shape[22][1]-self.shape[23][1])))/2)


	def eb_slanting(self):
		return ((((self.shape[19][1] - self.shape[20][1])+(self.shape[20][1] - self.shape[21][1])) + ((self.shape[24][1] - self.shape[23][1])+(self.shape[23][1] - self.shape[22][1])))/2)


	def eb_distance(self):
		return (self.shape[22][0] - self.shape[21][0])


	def eeb_distance(self):
		return (((self.shape[19][1] - self.shape[37][1]) + (self.shape[24][1] - self.shape[44][1]))/2)


	def e_openness(self):
		return (((self.shape[37][1] - self.shape[41][1]) + (self.shape[44][1] - self.shape[46][1]))/2)


	def e_slanting(self):
		return (((self.shape[36][1] - self.shape[39][1]) + (self.shape[45][1] - self.shape[42][1]))/2)


	def m_openness(self):
		return ((((-(self.shape[57][1]-self.shape[51][1])-(self.shape[58][1]-self.shape[50][1]))/2) + ((-(self.shape[57][1]-self.shape[51][1])-(self.shape[56][1]-self.shape[52][1]))/2))/2)


	def m_mos(self):
		return (((self.shape[48][1] - (self.shape[51][1]+(( self.shape[57][1]-self.shape[51][1] )/2))) + (self.shape[54][1] - (self.shape[51][1]+( (self.shape[57][1] - self.shape[51][1])/2 ))))/2)


	def m_width(self):
		return (self.shape[54][0] - self.shape[48][0])


	def mul_height(self):
		return ((self.shape[50][1] + self.shape[51][1] + self.shape[52][1])/3)


	def mll_height(self):
		return ((self.shape[58][1] + self.shape[57][1] + self.shape[56][1])/3)


	def lc_height(self):
		return ((self.shape[48][1] + self.shape[54][1])/2)


	# get all feature values and add in a dictionary
	def getAllFeatureValues(self):
		features = {
		  "ieb_height": self.ieb_height(),      "oeb_height": self.oeb_height(),
		  "eb_frowned": self.eb_frowned(),      "eb_slanting": self.eb_slanting(),
		  "eb_distance": self.eb_distance(),	"eeb_distance": self.eeb_distance(),
		  "e_openness": self.e_openness(),      "e_slanting": self.e_slanting(),
		  "m_openness": self.m_openness(),	    "m_mos": self.m_mos(),
		  "m_width": self.m_width(), 			"mul_height": self.mul_height(),
		  "mll_height": self.mll_height(),	    "lc_height": self.lc_height()
		}

		return features

