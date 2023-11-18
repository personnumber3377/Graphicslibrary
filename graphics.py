
import numpy as np
import math
import turtle
import copy
import keyboard


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



class triangle:
	def __init__(self, point1, point2, point3):
		self.point1 = point1
		self.point2 = point2
		self.point3 = point3
		self.outside = []
	def cameratransform(self,camera):
		
		
		transformed_point1 = self.point1
		transformed_point2 = self.point2
		transformed_point3 = self.point3
		transformed_triangle = [transformed_point1, transformed_point2, transformed_point3]
		for point in transformed_triangle:
			
			# offset aka transformed = original - camera
			point -= camera.c
			# angle z
			zmatrix = np.array([[math.cos(camera.theta[2]), math.sin(camera.theta[2]), 0],[-1*math.sin(camera.theta[2]), math.cos(camera.theta[2]), 0], [0,0,1]])
			point = np.dot(point, zmatrix)
			ymatrix = np.array([[math.cos(camera.theta[1]), 0, -1*math.sin(camera.theta[1])], [0,1,0], [math.sin(camera.theta[1]), 0, math.cos(camera.theta[1])]])
			point = np.dot(point,ymatrix)
			xmatrix = np.array([[1,0,0,],[0,math.cos(camera.theta[0]), math.sin(camera.theta[0])], [0, -1*math.sin(camera.theta[0]), math.cos(camera.theta[0])]])
			point = np.dot(point,xmatrix)
		return transformed_triangle
	def projectto2d(self,camera):
		transformed_point1 = self.point1
		transformed_point2 = self.point2
		transformed_point3 = self.point3
		projected_triangle = [transformed_point1, transformed_point2, transformed_point3]
		for point in projected_triangle:
			# here the z coordinate stays unmodified
			print("§1111111111111")
			print(point)
			print(camera.e)
			print(camera.c)
			print(camera.e[2])
			print(point[2])
			print(point[0])
			print("Shit: ")
			print(camera.e[2])
			print(point[2])
			print(point[0])
			print(camera.e[2]/(point[2])*point[0] + camera.c[0])
			point[0] = camera.e[2]/(point[2])*point[0] + camera.c[0]
			
			point[1] = camera.e[2]/(point[2])*point[1] + camera.c[1]
			print("Final point:")
			print(point)
		return projected_triangle

def drawtriangle(turtleobj, triangle_obj):
	turtle.penup()
	turtle.goto(triangle_obj.point1[0], triangle_obj.point1[1])
	turtle.pendown()
	turtle.goto(triangle_obj.point2[0], triangle_obj.point2[1])
	turtle.goto(triangle_obj.point3[0], triangle_obj.point3[1])
	turtle.goto(triangle_obj.point1[0], triangle_obj.point1[1])
	turtle.penup()
	return




def checkifinview(transformed_point, cameraobj, cur_plane):

	# first check that the point is greater than the plane z = x*l where l = 1/(tan(theta/2)) = camera.e[2]
	if transformed_point[2] < 0: # the point is behind the camera
		return False
	if transformed_point[2] > transformed_point[0]*cameraobj.c[2]:
		return True
	return False

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
		solutionpoint = point_a+t*from_point_a_to_b
		return solutionpoint
	if cur_plane == 1:
		# this is the down plane aka on the down side of the screen

		# the equation for this plane is y = l*z

		# in this case the plane normal will be np.cross(normalizevector(np.array([0,l,1])), np.array([1,0,0]))

		plane_normal = np.cross(normalizevector(np.array([0,camera_object.e[2],1])), np.array([1,0,0]))

		print(plane_normal)

		from_point_a_to_b = -1*point_a+point_b

		t = -1*((np.dot(point_a, plane_normal)))/(np.dot(normalizevector(from_point_a_to_b), plane_normal))

		print(t)
		solutionpoint = point_a+t*from_point_a_to_b
		return solutionpoint





	if cur_plane == 2:
		# the plane is the left side one aka the left side of the screen:
		# the equation for the plane is z = -l*x where l = e
		# the plane normal is normalize([1, 0, -l]) X [0,1,0] aka the vector straight up and one vector which points to the direction of the plane from the camera aka origin at this point
		plane_normal = np.cross(normalizevector(np.array([1,0,-camera_object.e[2]])), np.array([0,1,0]))
		print(plane_normal)
		# get the normalized vector from point_a to point_b.
		from_point_a_to_b = -1*point_a+point_b
		# let point_a be P_0
		t = -1*((np.dot(point_a, plane_normal)))/(np.dot(normalizevector(from_point_a_to_b), plane_normal))
		print(t)
		solutionpoint = point_a+t*from_point_a_to_b
		return solutionpoint
	if cur_plane == 4:
		# this is the up plane aka on the up side of the screen

		# the equation for this plane is y = -l*z

		# in this case the plane normal will be np.cross(normalizevector(np.array([0,-l,1])), np.array([1,0,0]))

		plane_normal = np.cross(normalizevector(np.array([0,-camera_object.e[2],1])), np.array([1,0,0]))

		print(plane_normal)

		from_point_a_to_b = -1*point_a+point_b

		t = -1*((np.dot(point_a, plane_normal)))/(np.dot(normalizevector(from_point_a_to_b), plane_normal))

		print(t)
		solutionpoint = point_a+t*from_point_a_to_b
		return solutionpoint




point1 = np.array([0.0,0.0,15.0])
point2 = np.array([10.0,0.0,15.0])
point3 = np.array([0.0,10.0,15.0])
theta = np.array([0.0,0.0,0.0])
c = np.array([0.0,0.0,0.0])
e = np.array([0.0,0.0,1.0])
screenheight = 500
screenwidth = 500
turtle.speed(0)

camera_object = camera(e,theta,c)
print("Shitt:")
print(type(triangle))
one_triangle = triangle(point1,point2,point3)

print(one_triangle.cameratransform(camera_object))
result = one_triangle.cameratransform(camera_object)
camera_transformed_triangle = triangle(result[0], result[1], result[2])
print(camera_transformed_triangle.point1)
print(camera_transformed_triangle.point2)
print(camera_transformed_triangle.point3)
print(camera_transformed_triangle.projectto2d(camera_object))

all_triangles = [one_triangle]

turtleobj = turtle.Turtle()
turtleobj.speed(0)
movementspeed = 1.0
while True:
	# for every triangle in triangles: transform triangle
	triangles_thing = copy.deepcopy(all_triangles)
	for triangle_obj in triangles_thing:
		result = triangle_obj.cameratransform(camera_object)
		print("Shitt2:")
		print(type(triangle))
		resultingtriangle = triangle(result[0], result[1], result[2])
		resultingtriangle.projectto2d(camera_object)
		triangle_obj = resultingtriangle

	# sort triangles by z value

	triangles_z_sorted = sorted(triangles_thing, key=lambda x: x.point1[2])

	# if triangle not in view then clip triangle or remove triangle from view:
	
	for triangle_obj in triangles_z_sorted:
		triangle_obj.outside = []
		# check how many points are inside the view cone:
		count = 0
		for point in [triangle_obj.point1, triangle_obj.point2, triangle_obj.point3]:
			result = checkifinview(point, camera_object)
			if result:
				triangle_obj.outside.append(count)


	counter = 0
	for counter in range(len(triangles_z_sorted))
		for plane_counter in range(0,4):


			# the current triangle is triangles_z_sorted[counter]

			triangles_z_sorted[counter].outside = []

			count = 0
			for point in [triangles_z_sorted[counter].point1, triangles_z_sorted[counter].point2, triangles_z_sorted[counter].point3]:
				result = checkifinview(point, camera_object, plane_counter)
				if result:
					triangles_z_sorted[counter].outside.append(count)

			if triangles_z_sorted[counter].outside != []:
				if len(triangles_z_sorted[counter].outside) == 3:
					# every point is outside the view cone:
					triangles_z_sorted.pop(counter)
				if len(triangles_z_sorted[counter].outside) == 2:
					# two points are outside the cone aka the new triangle consists of the one point inside and the two points at the clipping points
					thing = 0
					if 0 not in triangles_z_sorted[counter].outside:
						thing = triangles_z_sorted[counter].point1
						alternative_point1 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point1, triangles_z_sorted[counter].point2)
						alternative_point2 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point1, triangles_z_sorted[counter].point3)
					if 1 not in triangles_z_sorted[counter].outside:
						thing = triangles_z_sorted[counter].point2
						alternative_point1 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point2, triangles_z_sorted[counter].point3)
						alternative_point2 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point2, triangles_z_sorted[counter].point1)
					if 2 not in triangles_z_sorted[counter].outside:
						thing = triangles_z_sorted[counter].point3
						alternative_point1 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point3, triangles_z_sorted[counter].point1)
						alternative_point2 = intersectcameraplanewithpoints(camera_object, triangles_z_sorted[counter].point3, triangles_z_sorted[counter].point2)
					# at this point the new triangle points are alternative_point1, alternative_point2 and triangles_z_sorted[counter]
					newtriangle = triangle()





	# draw every triangle (scaled up to view)


	for triangle_obj in triangles_z_sorted:
		triangle_obj.point1*=screenwidth
		triangle_obj.point2*=screenwidth
		triangle_obj.point3*=screenwidth
		drawtriangle(turtleobj, triangle_obj)

	if keyboard.is_pressed("w"):
		camera_object.c += np.array([0.0,0.0,movementspeed])
	if keyboard.is_pressed("a"):
		camera_object.c += np.array([-1*movementspeed,0.0,0.0])
	turtle.clearscreen()






