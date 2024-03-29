import math

def convert(alpha):
	"""Converts a [0,360) angle to a [-180,179) one"""
	return -180*math.floor(alpha/180) + alpha % 180

def compare(beta,alpha):
	"""Returns difference between the two angles, making sure that there are no circle-caused discontinuities"""
	if beta-alpha>180:
		return 360-(beta-alpha)
	elif beta-alpha<-180:
		return -360-(beta-alpha)
	else:
		return beta-alpha
