
import numpy as np


class camera:
	def __init__(self,e,theta,c):
		'''
		
		Vec c: the place where the camera is in the 3d world
		Vec e: the visual plane relative to the camera
		Vec theta: the angle of the camera in Tait-Bryan angles:


		'''

		self.c = c
		self.e = e
		self.theta = theta



def checkifinview(transformed_point, cameraobj):

	# first check that the point is greater than the plane z = x*l where l = 1/(tan(theta/2)) = camera.e[2]
	if transformed_point[2] < 0:
		return False
	if transformed_point[2] > transformed_point[0]*cameraobj.c[2]:
		return True
	return False


point = np.array([2.0,0.0,6.0])
point2 = np.array([2.0,0.0,-1.0])
cameraobj = camera(np.array([0.0,0.0,1.0]), np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]))

print(checkifinview(point,cameraobj))
print(checkifinview(point2,cameraobj))
exit()



