import numpy as np


class AUInference:

	shape = np.empty(68)
	neutral_shape = np.empty(68)

	features = {}
	neutral_features = {}


	def __init__(self, shape, features, neutral_shape, neutral_features):
		self.shape = shape
		self.features = features
		self.neutral_shape = neutral_shape
		self.neutral_features = neutral_features

	
	def AU1(self):
		return ((self.features['ieb_height'] > (self.neutral_features['ieb_height'] + 0.075)) and (self.shape[22][1] >= self.neutral_shape[22][1]) and (self.shape[21][1] >= self.neutral_shape[21][1]))


	def AU2(self):
		return ( (self.features['oeb_height'] > (self.neutral_features['oeb_height'] + 0.08)) and (self.shape[19][1] >= self.neutral_shape[19][1]) and (self.shape[24][1] >= self.neutral_shape[24][1]) )


	def AU4(self):
		return ((self.features['ieb_height'] < (self.neutral_features['ieb_height'] - 0.03)) and (self.features['eb_distance'] < (self.neutral_features['eb_distance'] - 0.03)))

	def AU5(self):
		return ( (self.features['e_slanting'] >= (self.neutral_features['e_slanting'] - 0.05)) and (self.features['e_openness'] > (self.neutral_features['e_openness'] + 0.055)))

	def AU6(self):
		return ((self.features['m_mos'] >= (self.neutral_features['m_mos'] + 0.045)) and (self.features['e_openness'] < (self.neutral_features['e_openness'] - 0.05)))


	def AU7(self):
		return (self.features['e_openness'] < (self.neutral_features['e_openness'] - 0.07))


	def AU9(self):
		return ( (self.features['m_width'] < (self.neutral_features['m_width'] - 0.1)) and (self.features['e_openness'] < (self.neutral_features['e_openness'] - 0.05)) and (self.features['ieb_height'] < (self.neutral_features['ieb_height'] - 0.06)) )


	def AU10(self):
		return ((self.features['mul_height'] > (self.neutral_features['mul_height'] + 0.03)) and (self.features['m_width'] <= self.neutral_features['m_width']) and (self.features['m_openness'] > (self.neutral_features['m_openness'] + 0.15)))


	def AU12(self):
		return ((self.features['m_mos'] >= (self.neutral_features['m_mos'] + 0.05)) and (self.features['m_width'] > (self.neutral_features['m_width'] + 0.12)))


	def AU15(self):
		return (((self.features['m_mos'] + 0.03) <= self.neutral_features['m_mos']) and (self.features['lc_height'] < (self.neutral_features['lc_height'] + 0.055)))


	def AU16(self):
		return ((self.features['mll_height'] <= (self.neutral_features['mll_height'] - 0.01)) and (self.features['m_openness'] > (self.neutral_features['m_openness'] + 0.1)) and (self.features['lc_height'] < self.neutral_features['lc_height']))


	def AU17(self):
		return ( (self.features['m_openness'] < self.neutral_features['m_openness']) and ((abs(self.neutral_features['m_openness']) - abs(self.features['m_openness'])) >= 0.08) and (-self.features['mll_height'] < (-self.neutral_features['mll_height'] - 0.08)) )


	def AU20(self):
		return ((self.features['m_width'] > self.neutral_features['m_width']) and ((abs(self.features['m_width']) - abs(self.neutral_features['m_width'])) >= 0.15) and (self.features['m_mos'] < (self.neutral_features['m_mos'] + 0.075)) and (self.features['lc_height'] < self.neutral_features['lc_height']))

	def AU23(self):
		return (self.features['m_openness'] < (self.neutral_features['m_openness'] - 0.1))

	def AU24(self):
		return ((self.features['mul_height'] < self.neutral_features['mul_height']) and (self.features['mll_height'] > self.neutral_features['mll_height'] + 0.075) and (self.features['m_openness'] < (self.neutral_features['m_openness'] - 0.1)))


	def AU25(self):
		return (self.features['m_openness'] >= (self.neutral_features['m_openness'] + 0.13))


	def AU26(self):
		return ((self.features['m_openness'] >= (self.neutral_features['m_openness'] + 0.55)) and (self.features['m_openness'] <= (self.neutral_features['m_openness'] + 0.63)))


	def AU27(self):
		return (self.features['m_openness'] >= (self.neutral_features['m_openness'] + 0.63))

	# get action units (AUs) and set in a dictionary
	def getAllActionUnits(self):

		AUs = {
		   "AU1": self.AU1(),   "AU2": self.AU2(),   "AU4": self.AU4(),   "AU5": self.AU5(),   "AU6": self.AU6(),   "AU7": self.AU7(),
		   "AU9": self.AU9(),  "AU10": self.AU10(), "AU12": self.AU12(), "AU15": self.AU15(), "AU16": self.AU16(), "AU17": self.AU17(),
		  "AU20": self.AU20(), "AU23": self.AU23(), "AU24": self.AU24(), "AU25": self.AU25(), "AU26": self.AU26(), "AU27": self.AU27()
		}

		return AUs

