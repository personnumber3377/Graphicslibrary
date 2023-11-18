
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


def normalizevector(vector):
	return vector/(np.sqrt(np.sum(vector**2)))

def intersectcameraplanewithpoints(camera_object, point_a, point_b, cur_plane):
	if cur_plane == 0:
		# the plane is the right side one aka the right side of the screen:
		# the equation for the plane is z = l*x where l = e
		# the plane normal is normalize([1, 0, l]) X [0,1,0] aka the vector straight up and one vector which points to the direction of the plane from the camera aka origin at this point
		plane_normal = np.cross(normalizevector(np.array([1,0,camera_object.e[2]])), np.array([0,1,0]))
		print(plane_normal)
		# get the normalized vector from point_a to point_b.
		from_point_a_to_b = -1*point_a+point_b
		# let point_a be P_0
		t = -1*((np.dot(point_a, plane_normal)))/(np.dot(normalizevector(from_point_a_to_b), plane_normal))
		print(t)
		finalsolution_point = point_a + t*normalizevector(from_point_a_to_b)
		print(finalsolution_point)
def checkifinview(transformed_point, cameraobj):

	# first check that the point is greater than the plane z = x*l where l = 1/(tan(theta/2)) = camera.e[2]
	if transformed_point[2] < 0:
		return False
	if transformed_point[2] > transformed_point[0]*cameraobj.c[2]:
		return True
	return False


point = np.array([2.0,1.0,6.0])
point2 = np.array([2.0,0.0,1.0])
cameraobj = camera(np.array([0.0,0.0,1.0]), np.array([0.0,0.0,0.0]), np.array([0.0,0.0,0.0]))

print(checkifinview(point,cameraobj))
print(checkifinview(point2,cameraobj))

print(intersectcameraplanewithpoints(cameraobj, point, point2, 0))

exit()



