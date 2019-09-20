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
		directories = os.listdir("fake")
		for direct in directories:

			
			# items inside directory
			items = os.listdir("fake/"+direct+"/bmp/")
			
			# list ordering
			items = sorted(items)


			neutral_shape = np.empty(68)
			neutral_features = {}

			# for each item (image), start processing
			for item in items:

			
				# row initialize
				row_dict = { "emotion": "", "fake": 0, "1": True, "2": True,
				 "4": True, "5": True, "6": True, "7": True,
				 "9": True, "10": True, "12": True, "15": True,
				 "16": True, "17": True, "20": True, "23": True,
				 "24": True, "25": True, "26": True, "27": True
				}


				# detect emotion labeled 
				if( item == "happy.bmp" ):
					row_dict["emotion"] = "happy"
				elif( item == "sad.bmp" ):
					row_dict["emotion"] = "sad"

				# fake emotion
				row_dict["fake"] = True

				
				# current image path
				path = os.path.join(self.my_path+"/fake/"+direct+"/bmp/"+item)

				# detect facial landmarks
				shape = self.facialLandmarks(path)


				# instance of feature values calculation
				fV = calcFeatureValues(shape)

				# list of feature values
				features = fV.getAllFeatureValues()

				
				# if neutral face image, save shape and features
				if( item == "aneutral.bmp" ):
					neutral_shape = shape
					neutral_features = features
				# otherwise make AU inference
				else:
					
					aI = AUInference(shape, features, neutral_shape, neutral_features)

					AUs = aI.getAllActionUnits()

					for au, value in AUs.items():
						row_dict[au] = value

					self.df = self.df.append(row_dict, ignore_index=True)

				
				
		


	def genuineDirectory(self):
		# Images to process
		emotionDirectories = os.listdir("genuine")

		emotion = 0

		for directories in emotionDirectories:
			
			# row initialize
			row_dict = { "emotion": "", "fake": 0, "1": True, "2": True,
			 "4": True, "5": True, "6": True, "7": True,
			 "9": True, "10": True, "12": True, "15": True,
			 "16": True, "17": True, "20": True, "23": True,
			 "24": True, "25": True, "26": True, "27": True
			}

			# detect emotion labeled 
			if( emotion == 0 ):
				row_dict["emotion"] = "happy"
			elif( emotion == 1 ):
				row_dict["emotion"] = "sad"
			

			emotion += 1 

			# fake emotion
			row_dict["fake"] = False


			# directories inside directory
			directs = os.listdir("genuine/"+directories)

			count = 0

			for direct in directs:

				count+=1

				# items inside directory
				items = os.listdir("genuine/"+directories+"/"+direct)
				
				neutral_shape = np.empty(68)
				neutral_features = {}

				items = sorted(items)


				# for each item (image), start processing
				for item in items:

					# current image path
					path = os.path.join(self.my_path+"/genuine/"+directories+"/"+direct+"/"+item)

					# detect facial landmarks
					shape = self.facialLandmarks(path)

					
					
					# instance of feature values calculation
					fV = calcFeatureValues(shape)

					# list of feature values
					features = fV.getAllFeatureValues()

															
					# if neutral face image, save shape and features
					if( item == "0.jpg" ):
						neutral_shape = shape
						neutral_features = features
					# otherwise make AU inference
					else:
						
						aI = AUInference(shape, features, neutral_shape, neutral_features)

						AUs = aI.getAllActionUnits()

						for au, value in AUs.items():
							row_dict[au] = value

						self.df = self.df.append(row_dict, ignore_index=True)
		


	def main(self):

		# initialize dataframe
		self.df = self.df.reindex(columns = ['emotion', 'fake', '1', '2', '4', '5', '6', 
							   '7', '9', '10', '12', '15', '16', '17', '20', 
							   '23', '24', '25', '26', '27'])

		# relative path
		self.my_path = os.path.abspath(os.path.dirname(__file__))

		# Detect 68 facial landmarks
		self.predictor = dlib.shape_predictor(os.path.join(self.my_path+ "/shape_predictor_68_face_landmarks.dat"))

		# detect the face
		self.detector = dlib.get_frontal_face_detector()
		
		# TROCAR DETECTOR DA FACE PELO DO OPENCV
		#haar_cascade_face = cv2.CascadeClassifier(self.my_path+ '/haarcascade_frontalface_default.xml')
		#faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.8, minNeighbors = 5);


		self.fakeDirectory()
		self.genuineDirectory()

		print(self.df)


		
ip = imageProcess()
ip.main()