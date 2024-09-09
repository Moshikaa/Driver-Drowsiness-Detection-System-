from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2

class Drowsy(object):
		
	def sound_alarm(path):
		playsound.playsound(path)

	def eye_aspect_ratio(eye):
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])
		C = dist.euclidean(eye[0], eye[3])
		ear = (A + B) / (2.0 * C)
		return ear
	
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-p", "--shape-predictor", default = "shape_predictor_68_face_landmarks.dat",
	#	help="path to facial landmark predictor")
	#ap.add_argument("-a", "--alarm", type=str, default="alarm.wav",
	#	help="path alarm .WAV file")
	#ap.add_argument("-w", "--webcam", type=int, default=0,
	#	help="index of webcam on system")
	#args = vars(ap.parse_args())
	EYE_AR_THRESH = 0.3
	EYE_AR_CONSEC_FRAMES = 35
	flag = True
	COUNTER = 0
	ALARM_ON = False
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

	
	def det(frame1):
		while True:
			frame = imutils.resize(frame1, width=450, height=450)
			rects = Drowsy.detector(frame, 0) 
			for rect in rects:
				shape = Drowsy.predictor(frame, rect)
				shape = face_utils.shape_to_np(shape)
				leftEye = shape[Drowsy.lStart:Drowsy.lEnd]
				rightEye = shape[Drowsy.rStart:Drowsy.rEnd]
				leftEAR = Drowsy.eye_aspect_ratio(leftEye)
				rightEAR = Drowsy.eye_aspect_ratio(rightEye)
				ear = (leftEAR + rightEAR) / 2.0
				if ear < Drowsy.EYE_AR_THRESH:
					Drowsy.COUNTER += 1
					if Drowsy.COUNTER >= Drowsy.EYE_AR_CONSEC_FRAMES:
						if not Drowsy.ALARM_ON:
							Drowsy.ALARM_ON = True
							t = Thread(target=Drowsy.sound_alarm,
								args=("alarm.wav",))
							t.deamon = True
							t.start()
						cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
							cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				else:
					Drowsy.COUNTER = 0
					Drowsy.ALARM_ON = False
				cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			
			abc, final = cv2.imencode('.jpeg',frame)
			return final.tobytes()