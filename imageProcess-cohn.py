import numpy as np
import matplotlib.pyplot as plt
from imutils import face_utils
import dlib
import cv2
import os.path
import pandas as pd
from featureValues import calcFeatureValues
from AUInference import AUInference



class imageProcess:

	# create pandas dataframe to save informations
	# emotion(neutral, happy, sad, fear) / fake(True) or genuine(False) / AUs 
	df = pd.DataFrame()

	# relative path
	my_path = ""

	# predictor and detector
	predictor = ""
	detector = ""

		
	# Converter BGR to RGB
	def convertToRGB(self, image):
	    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


	# Detect facial landmarks
	def facialLandmarks(self, path):

		# get current image
		image = cv2.imread(path)

		# Convert image to grayscale
		grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# face detect with a rectangle
		rects = self.detector(grayImage, 0)


		# initialize shape of current image
		shape = np.empty(68)

		# For each detected face, find the landmark.
		for (i, face) in enumerate(rects):

			# Make the prediction and transfom it to numpy array
			shape = self.predictor(grayImage, face)
			shape = face_utils.shape_to_np(shape)

		return shape


	def fakeDirectory(self):
		# Images to process
		directories = os.listdir("Cohn-Kanade")
		for direct in directories:
			
			# items inside directory
			items = os.listdir("Cohn-Kanade/"+direct+"/")
			
			# list ordering
			items = sorted(items)


			neutral_shape = np.empty(68)
			neutral_features = {}



			
			# for each item (image), start processing
			for item in items:

				if( item != ".DS_Store" ):

					# row initialize
					row_dict = { "emotion": "", "fake": 0, "AU1": True, "AU2": True,
					 "AU4": True, "AU5": True, "AU6": True, "AU7": True,
					 "AU9": True, "AU10": True, "AU12": True, "AU15": True,
					 "AU16": True, "AU17": True, "AU20": True, "AU23": True,
					 "AU24": True, "AU25": True, "AU26": True, "AU27": True,
					 "ieb_height":0.0, "oeb_height":0.0, "eb_frowned":0.0, "eb_slanting":0.0, 
					 "eb_distance":0.0, "eeb_distance":0.0, "e_openness":0.0, "e_slanting":0.0, 
					 "m_openness":0.0, "m_mos":0.0, "m_width":0.0, "mul_height":0.0, "mll_height":0.0, "lc_height":0.0
					}


					# detect emotion labeled 
					if( item == "happy.png" ):
						row_dict["emotion"] = "happy"
					elif( item == "sad.png" ):
						row_dict["emotion"] = "sad"


					# fake emotion
					row_dict["fake"] = True

					
					# current image path
					path = os.path.join(self.my_path+"/Cohn-Kanade/"+direct+"/"+item)

					
					# detect facial landmarks
					shape = self.facialLandmarks(path)


					# instance of feature values calculation
					fV = calcFeatureValues(shape)

					# list of feature values
					features = fV.getAllFeatureValues()

					# if neutral face image, save shape and features
					if( item == "aneutral.png" ):
						neutral_shape = shape
						neutral_features = features
					# otherwise make AU inference
					else:
						
						aI = AUInference(shape, features, neutral_shape, neutral_features)

						AUs = aI.getAllActionUnits()


						for au, value in AUs.items():
							row_dict[au] = value


						for x in features:
	  						row_dict[x] = round( features[x] - neutral_features[x], 6)

						self.df = self.df.append(row_dict, ignore_index=True)
					
				



	def main(self):

		# initialize dataframe
		self.df = self.df.reindex(columns = ['emotion', 'fake', 'AU1', 'AU2', 'AU4', 'AU5', 'AU6', 
							   'AU7', 'AU9', 'AU10', 'AU12', 'AU15', 'AU16', 'AU17', 'AU20', 
							   'AU23', 'AU24', 'AU25', 'AU26', 'AU27', "ieb_height", "oeb_height", 
							   "eb_frowned", "eb_slanting", "eb_distance", "eeb_distance", "e_openness", 
							   "e_slanting", "m_openness", "m_mos", "m_width", "mul_height", "mll_height", "lc_height"
							   ])

		# relative path
		self.my_path = os.path.abspath(os.path.dirname(__file__))

		# Detect 68 facial landmarks
		self.predictor = dlib.shape_predictor(os.path.join(self.my_path+ "/shape_predictor_68_face_landmarks.dat"))

		# detect the face
		self.detector = dlib.get_frontal_face_detector()
		

		self.fakeDirectory()

		self.df.to_csv("facialFeatures-cohn.csv")


		
ip = imageProcess()
ip.main()
